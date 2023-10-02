# Import the FastAPI class from the FastAPI framework
from fastapi import FastAPI

# Import the add_pagination
from fastapi_pagination import add_pagination

# Import the 'router' from the 'app.api.v1.api' module
from app.api.v1.api import router

# Import the 'settings' object from the 'app.core.settings' module
from app.core.settings import settings

# Create an instance of the FastAPI application
# - 'title' is set to the project name from 'settings'
# - 'openapi_url' specifies the URL for the OpenAPI documentation
app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add the necessary pagination parameters to all routes that use paginate
add_pagination(app)

# Include the 'router' (which contains your API routes) in the FastAPI application
app.include_router(router)
