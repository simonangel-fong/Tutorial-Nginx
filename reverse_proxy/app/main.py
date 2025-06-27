import os
from fastapi import FastAPI

app = FastAPI(title="FastAPI App", version="1.0.0")


@app.get("/")
async def read_root():
    app_name = os.getenv("APP_NAME")
    return {"message": f"This is {app_name}."}      # show env var

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
