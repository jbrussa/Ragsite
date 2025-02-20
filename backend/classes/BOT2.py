import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from classes.service import Service

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

#dbm es una instancia de Service2
dbm = Service()

class BOT2:
    def test(self):
        return "ok"        
    

    def message(self, query: str, session_id: str) -> str:
        
        # dirección actual y de la base de datos
        current_dir = os.getcwd()
        CHROMA_PATH = os.path.join(current_dir,"db")
        
        embeddings = OpenAIEmbeddings()

        # referencia a la base de datos vectorial creada previamente
        db_chroma = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

        # obtiene 5 partes mas relevantes de la base de datos vectorial
        docs_chroma = db_chroma.similarity_search_with_score(query, k=5)

        # generar una respuesta basada en la consulta del usuario y la información contextual recuperada
        context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])

        # traer el historial del chat desde la bd
        history_text = "\n\n".join(dbm.search_history(session_id))

        # Aqui se define el "PROMPT". Estas son las instrucciones que tiene el BOT para responder la pregunta
        PROMPT_TEMPLATE = """
        Answer the question based only on the following context:
        {context}
        Chat history:
        {history}
        Answer the question based on the above context and chat history: {question}.
        Provide a detailed answer.
        Answers using the language in which the question was asked.
        Don't justify your answers.
        Don't give information not mentioned in the CONTEXT INFORMATION.
        Do not say "according to the context" or "mentioned in the context" or similar.
        """

        # Cargar el contexto recuperado y la consulta del usuario en la plantilla de consulta
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, history=history_text, question=query)

        # llamar al modelo LLM para que genere la respuesta en función del contexto y la consulta del usuario dado
        model = ChatOpenAI(model="gpt-4o")
        response = model.invoke(prompt)

        return response.content