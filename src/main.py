import uvicorn

from .bootstrap import app

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        reload=True,
        http="httptools",
    )
