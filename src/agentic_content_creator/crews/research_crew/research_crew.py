import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel
from typing import List

# Import LLM configuration

class LinkedInPost(BaseModel):
	hook: str
	why_matters: str
	main_insight: str
	supporting_points: List[str]
	formatting_suggestions: str
	sources: List[str]

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
