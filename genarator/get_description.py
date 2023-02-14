import openai

from config import Config 

OPEN_AI_API_KEY = Config.OPEN_AI_API_KEY

def get_description(query):
    model_engine = "text-davinci-002"
    openai.api_key = OPEN_AI_API_KEY

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=f"brief description of {query}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message