import os
from crewai.flow.flow import Flow, listen, start
#from langtrace_python_sdk import langtrace
from .crews.research_crew.research_crew import ResearchCrew
from .crews.content_crew.content_crew import ContentCrew
from .config import input_vars

#api_key = os.getenv('LANGTRACE_API_KEY')
#langtrace.init(api_key=api_key)

class ContentCreatorFlow(Flow):
    input_variables = input_vars

    @start()
    def generate_research_content(self):
        print("Starting research")
        return ResearchCrew().crew().kickoff(self.input_variables).pydantic

    @listen(generate_research_content)
    def generate_linkedin_content(self, planset):        
        print("Generating LinkedIn content")
        final_content = []
        for post in planset.plans:
            writer_inputs = self.input_variables.copy()
            writer_inputs['content_plan'] = post.model_dump_json()
            self.ensure_content_plan(writer_inputs)
            final_content.append(ContentCrew().crew().kickoff(writer_inputs).raw)
        print(final_content)
        return final_content

    @listen(generate_linkedin_content)
    def save_to_markdown(self, content):
        print("Saving LinkedIn posts")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        topic = self.input_variables.get("topic")
        saved_files = []

        # Create separate file for each post
        for index, post in enumerate(content, 1):
            file_name = f"linkedin_post_{topic}_{index}.md".replace(" ", "_").lower()
            output_path = os.path.join(output_dir, file_name)
            
            # Use UTF-8 encoding to handle emojis
            with open(output_path, "w", encoding='utf-8') as f:
                f.write(post)
            
            saved_files.append(output_path)
            print(f"LinkedIn post {index} saved to: {output_path}")
        
        # Create a summary file with all posts (optional)
        summary_file = os.path.join(output_dir, f"linkedin_posts_{topic}_all.md".replace(" ", "_").lower())
        with open(summary_file, "w", encoding='utf-8') as f:
            for index, post in enumerate(content, 1):
                f.write(f"# Post {index}\n\n")
                f.write(post)
                f.write("\n\n---\n\n")
            
        print(f"All posts also saved to: {summary_file}")
        return content

    def ensure_content_plan(self, writer_inputs):
        if 'content_plan' not in writer_inputs:
            writer_inputs['content_plan'] = self.get_default_content_plan()

    def get_default_content_plan(self):
        # Implement logic to obtain a default content plan
        pass

def kickoff():
    content_flow = ContentCreatorFlow()
    content_flow.kickoff()

def delete_md_files():
    # Get all files in current directory
    files = os.listdir('.')
    
    # Filter for .md files excluding readme.md
    md_files = [f for f in files if f.endswith('.md') and f.lower() != 'readme.md']
    
    # Delete each file
    for file in md_files:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except OSError as e:
            print(f"Error deleting {file}: {e}")

        

if __name__ == "__main__":
    delete_md_files()
    kickoff()
    
