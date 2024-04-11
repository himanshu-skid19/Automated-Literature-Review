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
from llama_index.core import PromptTemplate
from llama_index.core.query_engine import SimpleMultiModalQueryEngine
from llama_index.core.schema import ImageNode
from llama_index.core.indices import MultiModalVectorStoreIndex