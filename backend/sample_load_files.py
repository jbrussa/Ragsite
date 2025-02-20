import sys

#Agrego estas dos lienas para tomar el archivo .env
from dotenv import load_dotenv
load_dotenv() 
# Fix problema en Linux de sqlite
if sys.platform.startswith("linux"):
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document


#Cargar archivos Markdown desde una carpeta (docs), procesarlos en partes más pequeñas (chunks) y luego crear una base de datos vectorial 
# utilizando embeddings de OpenAI con la ayuda de LangChain y Chroma

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


# Crea paths independientes del s.o. parametros: directorio inicial, directorios intermedios, directorio final
current_dir = os.getcwd()
DOC_PATH = os.path.join(current_dir, "docs")  
CHROMA_PATH = os.path.join(current_dir, "db") 

# Crea carpetas si no existen
os.makedirs(DOC_PATH, exist_ok=True)
os.makedirs(CHROMA_PATH, exist_ok=True)

# Recorre todos los archivos de la carpeta 'docs'
md_files = [f for f in os.listdir(DOC_PATH) if f.endswith(".md")]  #os.listdir(DOC_PATH) devuelve una lista de todos los archivos en la carpeta docs. Luego, f.endswith(".md") filtra para que solo se incluyan los archivos con extensión .md
# Recorre todos los archivos de la carpeta 'docs', usa solo los de tipo markdown
md_files = [f for f in os.listdir(DOC_PATH) if f.endswith(".md")]
if not md_files:
    print("No se encontraron archivos Markdown en la carpeta 'docs'")
else:
    # Lista para almacenar los documentos cargados
    all_texts = []

    # Cargar todos los archivos Markdown de la carpeta
    for filename in md_files:
        file_path = os.path.join(DOC_PATH, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            markdown_content = file.read()
            document = Document(page_content=markdown_content, metadata={"source": filename})
            all_texts.append(document)
            

    # Divide los documentos en partes más pequeñas (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(all_texts)

    # Usa OpenAI Embedding model para generar base de datos vectorial con la información de los documentos
    embeddings = OpenAIEmbeddings()  # openai_api_key=OPENAI_API_KEY)

    # Crea la base de datos vectorial conteniendo los chunks
    db_chroma = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    print("La base de datos se actualizó correctamente")