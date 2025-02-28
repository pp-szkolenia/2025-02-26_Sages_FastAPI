from fastapi import status, Request
from fastapi.responses import JSONResponse


async def confirm_deletion(request: Request, call_next):
    if request.method == "DELETE":
        deletion_confirmed = input("Sure to delete? [yes/no]") == "yes"

        if not deletion_confirmed:
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Deletion cancelled"})

        return await call_next(request)