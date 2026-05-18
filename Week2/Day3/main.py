import fastapi

app = fastapi.FastAPI(
    title="My First API",
    description="A simple API to learn FastAPI",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to my API!"}

@app.get("/greet/{name}")
def greet_user(name: str):
    """
    Greet a specific user by name.

    Args:
        name : The name of the person to greet.

    Returns:
        A greeting message.
    """
    return {"Greeting": f"Hello, {name}!"}
