##fastAPI
## first install fastAPI and uvicorn
## pip install fastAPI uvicorn(terminal command)
from fastapi import FastAPI
app = FastAPI()#create FastAPI instance
## add Dynamic input
@app.get("/add")
def add(a: int, b: int):
    return {"result": a + b}

## uvicorn main:app --reload (terminal command to run the FastAPI application, where main is the name of the Python file containing the code and app is the FastAPI instance)

##open browser and go to http://127.0.0.1.8000