import os
import openai
import chainlit as cl

from imports import *  # Ensure this includes OpenAIMultiModal and other necessary imports
from build_vector_store import *  # Ensure this includes build_vector_store and other necessary imports

# Initialize the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of OpenAIMultiModal with appropriate parameters
openai_mm_llm = OpenAIMultiModal(
    model="gpt-4",  # Use the correct model identifier
    api_key=os.getenv("OPENAI_API_KEY"),
    max_new_tokens=300
)

@cl.on_chat_start
async def start():
    await cl.Message(
        author="Assistant", content="Hello! I'm an AI assistant. How may I help you?"
    ).send()
    try:
        index = MultiModalVectorStoreIndex.load(persist_dir="./storage")
    except Exception as e:
        print(f"Failed to load index from storage: {e}")
        documents = SimpleDirectoryReader("/").load_data()
        nodes = split(documents)
        index = build_vector_store(nodes)

    query_engine = index.as_query_engine(llm=openai_mm_llm)
    cl.user_session.set("query_engine", query_engine)

@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")
    
    if not query_engine:
        await cl.Message(content="Query engine is not initialized.", author="Assistant").send()
        return

    # Call the ask method of openai_mm_llm instance
    response = query_engine.query(message.content, top_k=1)

    # Access the response content correctly
    reply = response['answers'][0]['answer']  # Adjust according to the actual structure of the response
    await cl.Message(content=reply, author="Assistant").send()

# Run the app (if required to be run as a script, include this)
if __name__ == "__main__":
    cl.run("app.py")
