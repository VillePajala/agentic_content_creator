#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
import os

from .crews.research_crew.research_crew import ResearchCrew
from .crews.content_crew.content_crew import ContentCrew

class ContentCreatorFlow(Flow):
    # Define required input variables
    input_variables = {
        "topic": "AI and Machine Learning",  # Default value
        "audience_level": "beginner",        # Default value
        # Add any other required variables
    }

    @start()
    def start_research(self):
        print("Starting research")
        # Pass input variables to ResearchCrew
        result = ResearchCrew().crew().kickoff(self.input_variables)
        print("Research completed")
        return result.raw

    @listen(start_research)
    def create_content(self, research):
        print("Creating content")
        # Combine research results with input variables
        inputs = {
            **self.input_variables,  # Include all input variables
            "research": research     # Add research results
        }
        result = ContentCrew().crew().kickoff(inputs)
        print("Content created")
        return result.raw

    @listen(create_content)
    def save_content(self, content):
        print("Saving content")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Use topic from input variables for the filename
        file_name = f"{self.input_variables['topic'].replace(' ', '_')}.txt"
        output_path = os.path.join(output_dir, file_name)
        
        with open(output_path, "w") as f:
            f.write(content)

def kickoff():
    content_flow = ContentCreatorFlow()
    # You can override default input variables here if needed
    # content_flow.input_variables["topic"] = "Different Topic"
    content_flow.kickoff()

def plot():
    content_flow = ContentCreatorFlow()
    content_flow.plot()
