from imports import *
from keys import *
from run_llava import *
from read_docs import *
import shutil

def cleanup():
    # Delete all PDF files in the pdf_content directory
    pdf_content_dir = "pdf_content"
    if os.path.exists(pdf_content_dir):
        shutil.rmtree(pdf_content_dir)
    
    if os.path.exists("pdf_content.pdf"):
        os.remove("pdf_content.pdf")
    os.makedirs(pdf_content_dir, exist_ok=True)  # Recreate the directory if it doesn't exist

    # Remove the existing vector store directory
    if os.path.exists("storage"):
        shutil.rmtree("storage")

# Perform cleanup tasks before running the application
cleanup()



def build_vector_store(text_vector):
    
    
    client = qdrant_client.QdrantClient(path="qdrant_mixed_img")

    text_store = QdrantVectorStore(
    client=client, collection_name="text_collection"
    )
    image_store = QdrantVectorStore(
        client=client, collection_name="image_collection"
    )
    storage_context = StorageContext.from_defaults(
        vector_store=text_store, image_store=image_store
    )
    
    image_embed_model = ClipEmbedding()

    documents = SimpleDirectoryReader("pdf_content").load_data()

    index = MultiModalVectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        image_embed_model=image_embed_model,
    )
    index.storage_context.persist(persist_dir="./storage")

    return index
