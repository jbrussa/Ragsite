from fastapi import HTTPException
import sqlite3
import os
from datetime import datetime,timedelta



class Service:
    
    def create_table_sessions(self) -> None:
        # Ruta completa a la base de datos dentro de 'db'
        db_path = os.path.join("db", "base.db")

       # Usamos with para manejar la conexión automáticamente, se cierra sola
        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()
            # Crear la tabla para almacenar sesiones
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sesiones (
                id TEXT NOT NULL,
                ip TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
             # Guardar cambios
            conn.commit()

        return


    def create_table_historial(self) -> None:
        # Ruta completa a la base de datos dentro de 'db'
        db_path = os.path.join("db", "base.db")

       # Usamos with para manejar la conexión automáticamente, se cierra sola
        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()
            # Crear la tabla para almacenar historial
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idsession TEXT NOT NULL,
                rol TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP)
            """)
             # Guardar cambios
            conn.commit()

        return


    def insert_session(self, session_id: str, ip_cliente: str) -> None:
        
        # Fecha y hora actual en formato para la bd
        dateTime = datetime.now().isoformat()   

        db_path = os.path.join("db", "base.db")

        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()
            # Insertamos datos en tabla sesiones
            cursor.execute("INSERT INTO sesiones (id, ip, fecha) VALUES (?, ?, ?)", (session_id, ip_cliente, dateTime))   
            conn.commit()

        return


    def fetch_data_session(self, session_id: str) -> list[str]:

        db_path = os.path.join("db", "base.db")

        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()

            # Busco en bd los datos de la session_id, y me trae solo uno. Si no existe error 400
            sesion = cursor.execute("SELECT * from sesiones where id = ?", (session_id,)).fetchone()
            if not sesion:
                raise HTTPException(status_code=400, detail="No existe la sesión")
        
        return sesion


    def check_expiry(self, sesion: list[str]) -> None:
        
         # Compruebo que no hayan pasado 15 minutos desde que se inició la sesión
        dateTime = sesion[2]
        dateTimeFormateado = datetime.fromisoformat(dateTime)
        if  datetime.now() - dateTimeFormateado > timedelta(minutes = 15):
            raise HTTPException(status_code=400, detail="La sesión ha caducado")
        
        return
    

    def insert_historial(self, session_id: str, query: str, response:str, dateTimeQuery: datetime, dateTimeResponse: datetime) -> None:
            
            # Fecha y hora en formato para la bd
            dateTimeQueryFormatted = dateTimeQuery.isoformat()   
            dateTimeResponseFormatted = dateTimeResponse.isoformat()   

            db_path = os.path.join("db", "base.db")

            with sqlite3.connect(db_path) as conn:

                cursor = conn.cursor()

                # Insertamos datos en tabla historial
                cursor.execute("INSERT INTO historial (idsession, rol, mensaje, fecha_hora) VALUES (?, ?, ?, ?)", (session_id, "user", query, dateTimeQueryFormatted)) 
                cursor.execute("INSERT INTO historial (idsession, rol, mensaje, fecha_hora) VALUES (?, ?, ?, ?)", (session_id, "assistant", response, dateTimeResponseFormatted))   
                conn.commit()


    def search_history(self, session_id: str) -> list[str]:
         
        db_path = os.path.join("db", "base.db")

        with sqlite3.connect(db_path) as conn:

            cursor = conn.cursor()

            # buscar en bd los datos y los traigo como una lista de string
            history = cursor.execute("""
        SELECT rol, mensaje 
        FROM historial 
        WHERE idsession = ? 
        ORDER BY fecha_hora ASC ;
        """, (session_id,)).fetchall()
            
            # formatear en par rol mensaje
            history_format = [f"{rol}: {mensaje}" for rol, mensaje in history]

        return history_format