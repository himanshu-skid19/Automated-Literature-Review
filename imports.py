import requests
import PyPDF2
import fitz
from PIL import Image
import matplotlib.pyplot as plt
import io
import os
import glob
import pandas as pd
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from torchvision import transforms
import torch
import qdrant_client
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from langchain_core.prompts.prompt import PromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)
# set Logging to DEBUG for more detailed outputs
from llama_index.core.query_engine import MultiStepQueryEngine




import warnings
warnings.filterwarnings('ignore')