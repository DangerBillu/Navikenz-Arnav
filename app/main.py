from fastapi import FastAPI
app = FastAPI()

@app.get("/test-connection")
def test_connection():
    from app.database import test_connection
    return test_connection()


@app.get("/")
def home():
    return {
        "message": "home page for the fastapi application"
    }
