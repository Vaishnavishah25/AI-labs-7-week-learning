from fastapi import FastAPI
app = FastAPI()

@app.get("/items")
def list_items():
    return {"items": []}

@app.post("/items")
def create_item(item:dict):
    return {"created": item}

@app.put("/items/{id}")
def update_item(id: str, item: dict):
    return {"updated": {"id": id, "data": item}}

@app.patch("/items/{id}")
def patch_item(id:int , item:dict):
    return {"pathed" :item}

@app.delete("/items/{id}")
def delete_item(id: int):
    return {"deleted": id}