import os
from fastapi import status, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import json


async def confirm_deletion(request: Request, call_next):
    if request.method == "DELETE":
        deletion_confirmed = input("Sure to delete? [yes/no]") == "yes"

        if not deletion_confirmed:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Deletion cancelled"})

    return await call_next(request)


async def log_operations(request: Request, call_next):
    data = {
        "endpoint_URL": str(request.url),
        "method": request.method,
        "timestamp": str(datetime.now()),
    }

    response = await call_next(request)
    data["response_code"] = response.status_code

    if os.path.exists("log.json"):
        with open("log.json", "r") as f:
            file_data = json.load(f)

        file_data.append(data)
        with open("log.json", "w") as f:
            json.dump(file_data, f, indent=2)
    else:
        with open("log.json", "w") as f:
            json.dump([data], f, indent=2)

    return response
