import fastapi
from sklearn.dummy import DummyClassifier
import numpy as np

# Create a dummy model for demonstration
# In a real scenario, you would load a trained model
model = DummyClassifier(strategy="constant", constant=1)
model.fit([0], [1])  # Dummy fit

app = fastapi.FastAPI()
@app.post("/predict")
def predict(text: str):
    result = model.predict([text])
    return {"prediction": int(result[0])}

## flow - user - API - ML model - prediction - API - User
## uvicorn apidemo3:app --reload (terminal command to run the FastAPI application, where apidemo3 is the name of the Python file containing the code and app is the FastAPI instance)

## status code
## 200 - success
## 404 - not found
## 500 - server error



#### incomplete