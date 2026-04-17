from fastapi import FastAPI
app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One','category':'Science'},
    {'title': 'Title Two', 'author': 'Author Two','category':'Fiction'},
    {'title': 'Title Three', 'author': 'Author Three','category':'History'},
    {'title': 'Title Four', 'author': 'Author Four','category':'Science'},
    {'title': 'Title Five', 'author': 'Author Five','category':'Fiction'},
    {'title': 'Title Six', 'author': 'Author Six','category':'History'},
]

@app.get("/api-endpoint")
async def read_all_books():
    return BOOKS

