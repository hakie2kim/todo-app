from fastapi import FastAPI
from api.routers import task, done, user_security

app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
app.include_router(user_security.router)

# @app.get("/hello")
# async def hello():
#     return {"message": "hello world!"}

