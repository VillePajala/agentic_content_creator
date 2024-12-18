from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
import os
from src.agentic_content_creator.config import input_vars, llms

class ResearchParagraph(BaseModel):
	"""Model for a single research paragraph"""
	title: str = Field(..., description="Title or topic of the paragraph")
	content: str = Field(..., description="Content of the research paragraph")
	sources: List[str] = Field(default_factory=list, description="Sources for this research paragraph")

class ResearchOutput(BaseModel):
	"""Model for the complete research output"""
	paragraphs: List[ResearchParagraph] = Field(..., description="List of research paragraphs")
	summary: str = Field(..., description="Brief summary of the research findings")

class LinkedInPostPlan(BaseModel):
	plan: str = Field(..., description="LinkedIn post plan")
	
class ContentPlan(BaseModel):
	plans: List[LinkedInPostPlan]

@CrewBase
class ResearchCrew():
	input_variables = input_vars
	"""ResearchCrew for LinkedIn content creation"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __post_init__(self):
		self.ensure_output_folder_exists()

	def ensure_output_folder_exists(self):
		"""Ensure the output folder exists."""
		output_folder = 'output'
		if not os.path.exists(output_folder):
			os.makedirs(output_folder)

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[SerperDevTool()],
			llm=llms['openai']['gpt-4o'],
			verbose=True
		)

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			llm=llms['openai']['gpt-4o'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='content_research.md',
			output_pydantic=ResearchOutput
		)

	#@task
	#def planning_task(self) -> Task:
	#	return Task(
	#		config=self.tasks_config['planning_task'],
	#		output_pydantic=ContentPlan,
	#		output_file='content_plan.md'
	#	)

	@crew
	def crew(self) -> Crew:
		"""Creates the ResearchCrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			output_pydantic=ContentPlan
		)
