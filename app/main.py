from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router


app = FastAPI(
    title="Attendance Management System using Face Recognition",
    description="This is a simple Attendance Management System using Face Recognition, which is a final year project for the department of Electrical and Electronics Engineering, University of Lagos.",
    version="0.1.0",

    # OpenAPI tags metadata
    openapi_tags=[
        {
            "name": "admin",
            "description": "Operations related to the admin of the system.",
        },
        {
            "name": "student",
            "description": "Operations related to the student of the system.",
        },
        {
            "name": "lecturer",
            "description": "Operations related to the lecturer of the system.",
        }
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api_router)
