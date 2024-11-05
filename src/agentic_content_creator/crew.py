from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from agentic_content_creator.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AgenticContentCreatorCrew():
	"""AgenticContentCreator crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['analyst'],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='research.md'
		)

	@task
	def analyzing_task(self) -> Task:
		return Task(
			config=self.tasks_config['analyzing_task'],
			input_file='research.md',
			output_file='marketanalysis.md'
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
