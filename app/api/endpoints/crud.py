import os
from typing import Annotated

import aiofile
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi.responses import FileResponse

from app.utils import get_jwt_payload

router = APIRouter(prefix="/files")


@router.get("/download/{file:str}")
async def download(file: str):
    """Эндпоинт отдает файлы"""
    return FileResponse("./files/" + file)


@router.post("/upload")
async def upload_file(file: UploadFile, jwt_access: Annotated[str, Depends(get_jwt_payload)]):
    """Эндпоинт сохраняет файлы"""
    if not file:
        raise HTTPException(400, "В запросе нет файла")
    if any(file.filename in el for el in os.listdir("./files/")):
        existing_indexes = [int(i[1:].split(")")[0]) for i in os.listdir("./files/") if file.filename in i]
        existing_indexes.sort()
        file.filename = "./files/" + f"({max(existing_indexes) + 1}) " + file.filename
    else:
        file.filename = "./files/" + "(0) " + file.filename
    async with aiofile.async_open(file.filename, mode="ab") as f:
        await f.write(file.file.read())
    return file.filename[8:]


@router.post("/upload_list_files")
async def upload_list_files(files: list[UploadFile], jwt_access: Annotated[str, Depends(get_jwt_payload)]):
    """Сохранение спика файлов"""
    if not files:
        raise HTTPException(400, "В запросе нет файлов")
    return_files = list()
    for file in files:
        if any(file.filename in el for el in os.listdir("./files/")):
            existing_indexes = [int(i[1:].split(")")[0]) for i in os.listdir("./files/") if file.filename in i]
            existing_indexes.sort()
            file.filename = "./files/" + f"({max(existing_indexes) + 1}) " + file.filename
        else:
            file.filename = "./files/" + "(0) " + file.filename
        async with aiofile.async_open(file.filename, mode="ab") as f:
            await f.write(file.file.read())
        return_files.append(file.filename[8:])
    return return_files
