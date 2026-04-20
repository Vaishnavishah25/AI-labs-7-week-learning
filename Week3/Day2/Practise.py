from fastapi import Body ,FastAPI
app = FastAPI()
BOOKS = [
    {'title': 'Title One', 'author': 'Author One','category':'Science'},
    {'title': 'Title Two', 'author': 'Author Two','category':'Fiction'},
    {'title': 'Title Three', 'author': 'Author Three','category':'History'},
    {'title': 'Title Four', 'author': 'Author Four','category':'Science'},
    {'title': 'Title Five', 'author': 'Author Five','category':'Fiction'}
]

@app.get("/books/book_author")
async def read_books_by_author(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

###  http://127.0.0.1:8000/docs gives Swagger UI