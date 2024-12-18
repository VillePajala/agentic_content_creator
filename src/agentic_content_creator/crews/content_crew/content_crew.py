from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from src.agentic_content_creator.config import input_vars, llms
from typing import List

@CrewBase
class ContentCrew():
	input_variables = input_vars
	"""ContentCrew for LinkedIn content creation"""

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
	def content_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_writer'],
			#tools=[SerperDevTool()],
			llm=llms['openai']['gpt-4o'],
			verbose=True
		)

	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			tools=[SerperDevTool()],
			llm=llms['openai']['gpt-4o'],
			verbose=True
		)
	

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	#@task
	#def writing_task(self) -> Task:
	#	return Task(
	#		config=self.tasks_config['writing_task'],
	#	)

	#@task
	#def editing_task(self) -> Task:
	#	return Task(
	#		config=self.tasks_config['editing_task'],
	#	)

	@crew
	def crew(self) -> Crew:
		"""Creates the EduContentWriter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
