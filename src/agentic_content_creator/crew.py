from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from agentic_content_creator.types import Report
import os

# Uncomment the following line to use an example of a custom tool
# from agentic_content_creator.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

search_tool = SerperDevTool()
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

@CrewBase
class AgenticContentCreatorCrew():
	"""AgenticContentCreator crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[search_tool], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def blog_designer(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_designer'],
			tools=[search_tool],
			verbose=True
		)
	
	@agent
	def blog_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['blog_writer'],
			tools=[search_tool],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			#output_pydantic=Report,
			output_file='research.md'
		)

	@task
	def design_task(self) -> Task:
		return Task(
			config=self.tasks_config['design_task'],
			input_file='research.md',
			context=[self.research_task()],
			#output_pydantic=Report,
			output_file='blog_outline.md'
		)
	
	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
			context=[self.research_task(), self.design_task()],
			#output_pydantic=Report,
			output_file='blog.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AgenticContentCreator crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
