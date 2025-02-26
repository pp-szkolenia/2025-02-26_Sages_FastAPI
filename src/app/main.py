from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.routers import users, tasks


app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Task mananger API",
    description="Description of my API....",
    version="1.0.0",
)


@app.get("/", description="Test endpoint for demonstration purposes")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Hello World!"})


app.include_router(users.router)
app.include_router(tasks.router)
