##API works as waiter who takes order from customer and gives it to chef, then delivers the food back to customer
## means receives request from client, processes it and returns response
## Client - API - Server -API - Client

##API stands for Application Programming Interface
##TYPES OF API
# GET - Fetch data from server
# POST - Send data to server
# PUT - Update existing data on server
# DELETE - Remove data from server

## API (Using requests) : Fetch data
import requests
response = requests.get("https://jsonplaceholder.typicode.com/posts/1", verify=False)#send GET request to API endpoint
print("Status Code:", response.status_code)  # Verify if the request was successful (200 means OK)
if response.status_code == 200:
    print("API is working! Response received.")
    print(response.json())#print response in JSON format
else:
    print("API request failed.")

##JSON (JavaScript Object Notation) - lightweight data interchange format that is easy for humans to read and write, and easy for machines to parse and generate
{
    "name": "Alice",
    "age": 30
}

