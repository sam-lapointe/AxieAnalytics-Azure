from src.app import app

# Entrypoint for the FastAPI development server
# This allows you to run the server with `uvicorn src.server:app --reload`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "__main__:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )