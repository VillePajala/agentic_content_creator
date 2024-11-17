#!/usr/bin/env python
import os
from crewai.flow.flow import Flow, listen, start

from .crews.research_crew.research_crew import ResearchCrew
from .crews.content_crew.content_crew import ContentCrew
from .config import CONTENT_CREATOR_INPUT_VARIABLES

class ContentCreatorFlow(Flow):
    input_variables = CONTENT_CREATOR_INPUT_VARIABLES

    @start()
    def generate_research_content(self):
        print("Starting research")
        return ResearchCrew().crew().kickoff(self.input_variables).pydantic

    @listen(generate_research_content)
    def generate_linkedin_content(self, plan):        
        print("Generating LinkedIn content")
        final_content = []
        for post in plan.posts:
            writer_inputs = self.input_variables.copy()
            writer_inputs['post'] = post.model_dump_json()
            final_content.append(ContentCrew().crew().kickoff(writer_inputs).raw)
        print(final_content)
        return final_content

    @listen(generate_linkedin_content)
    def save_to_markdown(self, content):
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        topic = self.input_variables.get("topic")
        file_name = f"linkedin_posts_{topic}.md".replace(" ", "_")
        output_path = os.path.join(output_dir, file_name)
        
        with open(output_path, "w", encoding='utf-8') as f:
            for post in content:
                f.write(post)
                f.write("\n\n---\n\n")  # Add separator between posts
        
        print(f"LinkedIn posts saved to: {output_path}")
        return content

def kickoff():
    content_flow = ContentCreatorFlow()
    content_flow.kickoff()

if __name__ == "__main__":
    kickoff()
