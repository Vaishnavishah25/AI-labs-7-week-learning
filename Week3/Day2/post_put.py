from fastapi import Body ,FastAPI
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

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

@app.get("/books/")        
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_anchor}/")
async def read_author_category_by_query(book_author: str, book_category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == book_category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)
     ####put

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return BOOKS[i]
        