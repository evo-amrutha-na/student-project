from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from project.component.loggings import set_up_logging
from project.controller.v1.student import student, auth
from fastapi.requests import Request


from fastapi.exceptions import RequestValidationError


# Set up logging at application startup
logger = set_up_logging()
logger.info("Application starting up")

app = FastAPI()

app.include_router(student.router, tags=['manage student'])
app.include_router(auth.router, tags=['student auth'])



# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):  
    logger.error(str(exc.errors))
    error_body = exc.errors()[0]['msg']
    res_status = 'error'
    res_message = error_body
    logger.error(res_message)
    status_code = 422
    return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code= status_code)

