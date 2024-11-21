import os
from crewai import LLM

input_vars = {
    "topic": "Timeline of AGI"
} 

LLM_CONFIGS = {
    "openai": {
        "api_key": os.getenv('OPENAI_API_KEY'),
        "models": {
            "gpt-4o-mini": "gpt-4o-mini",
            "gpt-4o": "gpt-4o",
            "o1-mini": "o1-mini",
            "o1-preview": "o1-preview",
        }
    },
    "groq": {
        "api_key": os.getenv('GROQ_API_KEY'),
        "models": {
            "llama3-groq-70b": "groq/llama3-groq-70b-8192-tool-use-preview",
            "llama3-groq-8b": "groq/llama3-groq-8b-8192-tool-use-preview",
            "llama3-groq-405b": "groq/llama3-groq-405b-8192-tool-use-preview",
        }
    },
    "anthropic": {
        "api_key": os.getenv('CLAUDE_API_KEY'),
        "models": {
            "claude-3-5-sonnet": "anthropic/claude-3-5-sonnet-20240620",
            "claude-3-sonnet": "anthropic/claude-3-sonnet-20240229",
            "claude-3-opus": "anthropic/claude-3-opus-20240229",
            "claude-3-haiku": "anthropic/claude-3-haiku-20240307",
        }
    }
}

def initialize_llms():
    llms = {}
    for provider, config in LLM_CONFIGS.items():
        llms[provider] = {}
        api_key = config['api_key']
        for model_name, model_id in config['models'].items():
            llms[provider][model_name] = LLM(
                model=model_id,
                api_key=api_key
            )
    return llms

llms = initialize_llms()

