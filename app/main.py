from fastapi import FastAPI

app = FastAPI()

@app.get("/data")
async def get_data():
    return {"message": "Hello", "value": 123}
