from imports import *
from keys import *
from run_llava import *
from read_docs import *

# def build_vector_store():
#     openai_mm_llm = OpenAIMultiModal(
#         model="gpt-4-vision-preview", api_key=OPENAI_API_KEY, max_new_tokens=300
#     )

#     client = qdrant_client.QdrantClient(path="qdrant_mm_db")

#     text_store = QdrantVectorStore(
#         client=client, collection_name="text_collection"
#     )
#     image_store = QdrantVectorStore(
#         client=client, collection_name="image_collection"
#     )
#     storage_context = StorageContext.from_defaults(
#         vector_store=text_store, image_store=image_store
#     )

#     # Create the MultiModal index
#     documents = SimpleDirectoryReader("pdf_content").load_data()
#     index = MultiModalVectorStoreIndex.from_documents(
#         documents,
#         api_key=OPENAI_API_KEY,
#         storage_context=storage_context,
#     )

#     # Save it
#     index.storage_context.persist(persist_dir="./storage")

#     return index

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
