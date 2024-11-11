from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from agentic_content_creator.types import Report
import os

search_tool = SerperDevTool()
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

@CrewBase
class AgenticContentCreatorCrew():
	"""AgenticContentCreator crew"""

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools=[search_tool],
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

	@agent
	def social_media_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['social_media_strategist'],
			tools=[search_tool],
			verbose=True
		)

	@agent
	def content_reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_reviewer'],
			tools=[search_tool],
			verbose=True
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			output_file='research.md'
		)

	@task
	def design_task(self) -> Task:
		return Task(
			config=self.tasks_config['design_task'],
			input_file='research.md',
			context=[self.research_task()],
			output_file='blog_outline.md'
		)
	
	@task
	def writing_task(self) -> Task:
		return Task(
			config=self.tasks_config['writing_task'],
			context=[self.research_task(), self.design_task()],
			output_file='blog.md'
		)

	@task
	def social_media_task(self) -> Task:
		return Task(
			config=self.tasks_config['social_media_task'],
			context=[
				self.writing_task(),
				self.research_task()
			],
			output_file='social_media_content.md'
		)

	@task
	def review_task(self) -> Task:
		return Task(
			config=self.tasks_config['review_task'],
			context=[
				self.social_media_task(),
				self.writing_task(),
				self.research_task()
			],
			output_file='final_social_media_content.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AgenticContentCreator crew"""
		return Crew(
				agents=self.agents,
				tasks=self.tasks,
				process=Process.sequential,
				verbose=True,
		)
