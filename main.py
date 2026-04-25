# Building the API's

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Hii, I am here for your help."}

