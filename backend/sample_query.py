import sys
#Agrego estas dos lienas para tomar el archivo .env
from dotenv import load_dotenv
load_dotenv() 

# fix problema en liux de sqlite
if sys.platform.startswith("linux"):
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.


current_dir = os.getcwd()
CHROMA_PATH = os.path.join(current_dir,"db") #Crea una ruta al directorio llamado db dentro del directorio actual. Este será el lugar donde se almacenan los datos de la base de datos vectorial.


# ejemplo de query
#Define la pregunta o consulta que el usuario quiere hacer. 
query = 'Que es Pyplan?'
embeddings = OpenAIEmbeddings() #Crea un objeto OpenAIEmbeddings, que se utiliza para generar representaciones vectoriales (embeddings) de texto.

# referencia a la base de datos vectorial creada previamente
db_chroma = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings) #Crea una instancia de la base de datos vectorial Chroma.


# retrieve context - obtiene 5 partes mas relevantes de la base de datos vectorial
docs_chroma = db_chroma.similarity_search_with_score(query, k=5)

# generar una respuesta basada en la consulta del usuario y la información contextual recuperada
context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])

# Aqui se define lo mas importante, el "PROMPT". Estas son las instrucciones que tiene el BOT para responder la pregunta
PROMPT_TEMPLATE = """
Answer the question based only on the following context:
{context}
Answer the question based on the above context: {question}.
Provide a detailed answer.
Answers using the language in which the question was asked.
Don't justify your answers.
Don't give information not mentioned in the CONTEXT INFORMATION.
Do not say "according to the context" or "mentioned in the context" or similar.
"""

# Cargar el contexto recuperado y la consulta del usuario en la plantilla de consulta
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context_text, question=query)

# llamar al modelo LLM para que genere la respuesta en función del contexto y la consulta del usuario dado
model = ChatOpenAI(model="gpt-4o")
response = model.invoke(prompt)

print (f"\nPregunta: {query}")
print (f"\nRespuesta:\n {response.content}")
