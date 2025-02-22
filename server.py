import os

import uvicorn

from app import create_app
from app.core.config import settings

if not os.path.exists("./files"):
    os.mkdir("./files")
app = create_app()

if __name__ == "__main__":
    uvicorn.run("server:app", host=settings.API_HOST, port=settings.API_PORT)
