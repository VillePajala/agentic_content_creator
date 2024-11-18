import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# Define pydantic models in the same file
class LinkedInPost(BaseModel):
	hook: str = Field(..., description="Attention-grabbing opening line")
	main_insight_1: str = Field(..., description="Core message or insight")
	main_insight_2: str = Field(..., description="Another Core message or insight")
	sources: List[str] = Field(..., description="Reference links")

class ContentPlan(BaseModel):
	posts: List[LinkedInPost]

@CrewBase
class ResearchCrew():
	"""ResearchCrew for LinkedIn content creation"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SerperDevTool()],
			verbose=True
		)

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			tools=[SerperDevTool()],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['planning_task'],
			output_pydantic=ContentPlan,
			output_file='content_plan.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ResearchCrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)
