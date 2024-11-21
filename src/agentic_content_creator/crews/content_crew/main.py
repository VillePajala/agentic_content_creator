#!/usr/bin/env python
import sys
from agentic_content_creator.crews.content_crew.content_crew import ContentCrew
import os
import glob
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

os.environ['OPENAI_MODEL_NAME'] = 'gpt-4o'


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': "Open AI's new model Orion"
    }
    ContentCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "Open AI's new model Orion"
    }
    try:
        ContentCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ContentCrew().crew().replay(task_id=sys.argv[1])

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
        ContentCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

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
