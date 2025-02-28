import time
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.routers import users, tasks, auth
from app.middleware import confirm_deletion


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
app.include_router(auth.router)


app.middleware("http")(confirm_deletion)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(type(response))
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response

