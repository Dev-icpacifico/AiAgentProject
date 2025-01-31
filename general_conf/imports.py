# 🔹 Importaciones estándar de Python
import os
import sys
import shutil
import datetime
import wikipedia
from tempfile import NamedTemporaryFile
from os.path import exists
from click import prompt
from tabnanny import verbose

# 🔹 Carga de variables de entorno
from dotenv import load_dotenv, find_dotenv
from config import key  # Configuración personalizada

# 🔹 Streamlit (para interfaces interactivas)
import streamlit as st

# 🔹 LangChain - Carga y procesamiento de documentos
from langchain import hub
from langchain.document_loaders import PyPDFLoader  # Carga de documentos PDF
from langchain.text_splitter import RecursiveCharacterTextSplitter  # División de texto en fragmentos
from langchain_text_splitters import CharacterTextSplitter  # Alternativa para dividir textos

# 🔹 LangChain - Embeddings y Bases Vectoriales
from langchain.embeddings import OpenAIEmbeddings  # Embeddings de OpenAI
from langchain.vectorstores import Chroma  # Base de datos vectorial Chroma

# 🔹 LangChain OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # Embeddings y Chat Model de OpenAI

# 🔹 LangChain Chroma
from langchain_chroma import Chroma  # Alternativa para Chroma

# 🔹 LangChain Community
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# 🔹 LangChain - Agentes y Cadenas de Consulta
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chains import RetrievalQA
from langchain.chains.constitutional_ai.principles import PRINCIPLES

# 🔹 LangChain - Prompts y Herramientas
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate  # Plantillas para modelos de chat
from langchain.tools import Tool  # Herramientas de LangChain

# 🔹 OpenAI API
from openai import models
