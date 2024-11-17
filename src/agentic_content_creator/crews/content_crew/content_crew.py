from ...config import LLM_CONFIG
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from src.agentic_content_creator.config import CONTENT_CREATOR_INPUT_VARIABLES

@CrewBase
class ContentCrew():
	input_variables = CONTENT_CREATOR_INPUT_VARIABLES
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
	def content_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_writer'],
			verbose=True
		)

	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True
		)

	@task
	def writing_task(self) -> Task:
		topic = self.input_variables.get("topic")
		file_name = f"linkedin_post_{topic}_draft.md".replace(" ", "_")
		output_file_path = os.path.join('output', file_name)
		
		return Task(
			config=self.tasks_config['writing_task'],
			output_file=output_file_path
		)

	@task
	def editing_task(self) -> Task:
		topic = self.input_variables.get("topic")
		file_name = f"linkedin_post_{topic}_final.md".replace(" ", "_")
		output_file_path = os.path.join('output', file_name)
		
		return Task(
			config=self.tasks_config['editing_task'],
			output_file=output_file_path
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LinkedIn Content Creation crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)
