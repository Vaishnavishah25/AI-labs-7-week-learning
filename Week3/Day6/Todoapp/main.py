from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI , Depends , HTTPException
import models
from models import Todos
from database import engine , sessionlocal

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy =Annotated[Session , Depends(get_db)]

@app.get("/")
async def read_all(db: db_dependancy):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(db:db_dependancy,todo_id:int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code = 404 , details = 'Todo not found.')

