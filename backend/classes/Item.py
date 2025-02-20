from pydantic import BaseModel
#Cuerpo de la solicitud: son los datos que envía el cliente a tu API. El cuerpo de una respuesta son los datos que tu API envía al cliente. 
#Para declarar el cuerpo de una solicitud , utilice Pidántico.
#Declara tu modelo de datos como una clase que hereda de BaseModel

class Item(BaseModel):
    numero: float

class QueryRequest(BaseModel):
    query: str


