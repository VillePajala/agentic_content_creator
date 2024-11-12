#!/usr/bin/env python
import sys
from agentic_content_creator.crew import AgenticContentCreatorCrew
import os
import glob
from dotenv import load_dotenv
from langtrace_python_sdk import langtrace

load_dotenv()  # Load environment variables from .env file
langtrace.init(api_key=os.getenv('LANGTRACE_API_KEY'))

os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o'


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': "Open AI's new model Orion"
    }
    AgenticContentCreatorCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Open AI's new model Orion"
    }
    try:
        AgenticContentCreatorCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgenticContentCreatorCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "Open AI's new model Orion"
    }
    try:
        AgenticContentCreatorCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def cleanup_output_files():
    # Define the pattern for markdown files
    pattern = os.path.join(os.path.dirname(__file__), '*.md')
    # Find and delete all markdown files except README.md
    for file_path in glob.glob(pattern):
        if os.path.basename(file_path).lower() != 'readme.md':
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
