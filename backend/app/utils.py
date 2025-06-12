import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_embedding(text: str, model: str = "text-embedding-3-small"):
    """
    Call OpenAI to get embedding for a given text.
    """
    response = openai.embeddings.create(
        model=model,
        input=text
    )
    return response.data[0].embedding