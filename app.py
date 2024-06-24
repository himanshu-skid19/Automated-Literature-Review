import os
import openai
import chainlit as cl
import shutil
from imports import *  # Ensure this includes OpenAIMultiModal and other necessary imports
from build_vector_store import *  # Ensure this includes build_vector_store and other necessary imports
from query import *

# Initialize the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of OpenAIMultiModal with appropriate parameters
# Ensure you have initialized openai_mm_llm correctly here

@cl.on_chat_start
async def start():
    await cl.Message(
        author="Assistant", content="Hello! I'm an AI assistant. How may I help you?"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    files = message.elements
    if files:
        for file in files:
            if file.path is not None and "pdf" in file.mime:
                # Ensure the 'files' directory exists
                os.makedirs('files', exist_ok=True)
                
                # Save the PDF file
                pdf_save_path = os.path.join('files', os.path.basename(file.path))
                shutil.copy(file.path, pdf_save_path)
                
                # Load documents and build the vector store
                documents = SimpleDirectoryReader("files/").load_data()
                nodes = split(documents)
                index = build_vector_store(nodes, documents)

                # Create a query engine
                query_engine = index.as_query_engine(llm=openai_mm_llm)
                
                # Store the query engine and index in the user session
                cl.user_session.set("query_engine", query_engine)
                cl.user_session.set("index", index)
    
    # Retrieve query engine and index from user session
    try:
        query_engine = cl.user_session.get("query_engine")
        index = cl.user_session.get("index")
    except Exception as e:
        query_engine = None
        index = None
        print(f"Error retrieving from session: {e}")
    
    if not query_engine:
        await cl.Message(content="Query engine is not initialized.", author="Assistant").send()
        return

    # Query the index
    response = query(message.content, index)
    if response == "Empty Response":
        query_engine2 = index.as_query_engine(llm=openai_mm_llm)
        response = query_engine2.query(message.content)

    # Send the response back to the user
    reply = response  # Adjust according to the actual structure of the response
    print(reply)
    await cl.Message(content=reply, author="Assistant").send()

# Run the app (if required to be run as a script, include this)
if __name__ == "__main__":
    cl.run("app.py")
