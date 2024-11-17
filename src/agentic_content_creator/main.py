#!/usr/bin/env python
from random import randint
import os
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start

from .crews.research_crew.research_crew import ResearchCrew
from .crews.content_crew.content_crew import ContentCrew
from .config import CONTENT_CREATOR_INPUT_VARIABLES

class ContentCreatorFlow(Flow):
    # Use config variables instead of hardcoding
    input_variables = CONTENT_CREATOR_INPUT_VARIABLES

    @start()
    def start_research(self):
        print("Starting research")
        research_result = ResearchCrew().crew().kickoff(self.input_variables).pydantic
        print(f"Research result type: {type(research_result)}")
        print(f"Research result content: {research_result}")
        return research_result

    @listen(start_research)
    def create_content(self, research):
        print("Creating content")
        print(f"Received research type: {type(research)}")
        print(f"Received research content: {research}")
        
        # Temporary fix to avoid the error while we debug
        if not hasattr(research, 'sections'):
            # Convert the research into the format we need
            content = research.content if hasattr(research, 'content') else str(research)
            return [content]
            
        final_content = []
        for section in research.sections:
            content_inputs = self.input_variables.copy()
            content_inputs['section'] = section.model_dump_json()
            final_content.append(ContentCrew().crew().kickoff(content_inputs).raw)
        
        print("Content created")
        return final_content

    @listen(create_content)
    def save_content(self, content):
        print("Saving content")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Use both topic and audience_level for filename
        topic = self.input_variables.get("topic")
        audience_level = self.input_variables.get("audience_level")
        file_name = f"{topic}_{audience_level}.md".replace(" ", "_")
        
        output_path = os.path.join(output_dir, file_name)
        
        with open(output_path, "w") as f:
            for section in content:
                f.write(section)
                f.write("\n\n")  # Add spacing between sections

def kickoff():
    content_flow = ContentCreatorFlow()
    # You can override default input variables here if needed
    # content_flow.input_variables["topic"] = "Different Topic"
    content_flow.kickoff()

def plot():
    content_flow = ContentCreatorFlow()
    content_flow.plot()
