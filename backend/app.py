from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from classes.BOT2 import BOT2
from classes.service import Service
import uuid             #Nos permite crear un identificador único a nivel global


#activar entorno virtual .\venv\Scripts\activate
#ejecutar con fastapi dev app.py


#app es una instancia de FastAPI
app = FastAPI()
#bot es una instancia de BOT2
bot2 = BOT2()
#dbm es una instancia de Service2
dbm = Service()

#  Crear abla Sesiones si no existe
dbm.create_table_sessions()
dbm.create_table_historial()


# *METODOS*

@app.get("/test")
async def rootGet():
    return {"status": bot2.test()}
    

@app.post("/test")
async def rootPost(num: int):
    return {"numero": 2 * num}


@app.post("/session")
async def register_session(request: Request) -> dict[str, str]:

    #Crear UUID y obtener IP del cliente
    session_id = str(uuid.uuid4())
    ip_cliente = request.client.host
    
    # Insertamos los datos a la bd
    dbm.insert_session(session_id, ip_cliente)
    
    return {"id": session_id} 


@app.post("/message")
async def manage_query(query: str, request: Request) -> str:

    # Recuperar id de sesión
    session_id = request.headers.get("id")
    if session_id is None:
        raise HTTPException(status_code=400, detail="No existe la sesión")

    # Buscar datos sesión
    sesion = dbm.fetch_data_session(session_id)

    # Comprobar que la sesión sea de menos de 15 minutos
    dbm.check_expiry(sesion)

    dateTimeQuery = datetime.now()

    # Hace la query al modelo
    response = bot2.message(query, session_id)
    dateTimeResponse = datetime.now()

    # Insertar en historial
    dbm.insert_historial(session_id, query, response, dateTimeQuery, dateTimeResponse)

    return response


