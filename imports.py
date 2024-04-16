import os
import requests
import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
import fitz
import io
from PIL import Image
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from llama_index.core import PromptTemplate, VectorStoreIndex, StorageContext
from llama_index.core.query_engine import SimpleMultiModalQueryEngine
from llama_index.core.schema import ImageNode
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import TextNode
from pathlib import Path
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.clip import ClipEmbedding
from llama_index.embeddings.cohere import CohereEmbedding
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

