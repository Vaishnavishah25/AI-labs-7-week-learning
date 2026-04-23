from fastapi import FastAPI,Body
from pydantic import BaseModel ,Field
app = FastAPI()

class Book :
    id : int
    title : str
    author : str
    description : str
    rating : int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class Bookrequest(BaseModel):
    id: int = Field(description="ID is not needed on create", default=None)
    ### if want id optional then write like this "Optional[int] = None"
    title: str = Field(min_length=3) ## validation with pydantic
    author : str = Field(min_length=1) ## validation with pydantic
    description :str = Field(min_length=1 , max_length=100) ## validation with pydantic
    rating: int = Field(gt = 0,lt = 6)

    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title" : "A new book",
                "author" : "codingwithroby",
                "description" : "Book Description of new book",
                "rating" : 5
            }
        }
    } 

    ## its visible as a example shcema in the docs and we can use it to test the api in the docs.
BOOKS = [
    Book(1,'Computer Science Pro','codingwithroby','A very nice book !',5),
    Book(2,'Be Fast with FastAPI','codingwithroby','A great book !',5),
    Book(3,'Master Endpoints','codingwithroby','A awesome book !',5),
    Book(4 ,'HP1','Author 1' ,'Book Description',5),
    Book(5,'HP2','Author 2' , 'Book Description',5),
    Book(6,'HP3','Author 3','Book Description',5)

]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}") ## fetch by bookid
async def read_book(book_id : int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
@app.get("/books/{rating}") ## fetch by rating
async def read_book_by_rating(rating : int):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            books_by_rating.append(book)
    return books_by_rating


@app.put("/update_book")
async def update_book(book: Bookrequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.dict())
            return BOOKS[i]
        
@app.post("/create-book")
async def create_book(book_request : Bookrequest):
    new_book = Book(**book_request.dict())
    BOOKS.append(find_book_id(new_book))


@app.delete("/books/{book_id}")
async def delete_book(book_id : int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            del BOOKS[i]
            return {"message" : "Book deleted successfully"}
        
def find_book_id(book:Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
   # if len(BOOKS) > 0:
  #      book.id = BOOKS[-1].id + 1
 #   else:
   #     book.id = 1

    return book
### this block gives unique id to each book when we create a new book and append it to the list of books.