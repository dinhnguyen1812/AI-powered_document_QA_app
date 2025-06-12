from openai import OpenAI
from .search import search_chunks_any_doc, search_chunks_same_doc
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Build a prompt in Japanese using the retrieved document chunks and user question
def build_prompt(chunks, question):
    context = "\n\n".join(chunk.content for chunk in chunks)
    prompt = f"""
        あなたは有能なAIアシスタントです。以下の文書抜粋を参考にして、質問に日本語で簡潔かつ正確に答えてください。

        【文書抜粋】
        {context}

        【質問】
        {question}

        【回答】
        """
    return prompt

# Search related document chunks and generate an answer using OpenAI's chat model
def get_answer(question: str):
    chunks = search_chunks_same_doc(question)  # Retrieve document chunks relevant to the question
    prompt = build_prompt(chunks, question)    # Create a prompt with the retrieved chunks

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは有能なAIアシスタントです。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=512,
    )

    answer = response.choices[0].message.content.strip()  # Extract and clean the model's answer
    return answer, chunks  # Return both the answer and the document chunks used
