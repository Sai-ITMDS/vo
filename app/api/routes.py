from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi import Request
from fastapi import BackgroundTasks
import os

from app.services.obfuscator import VoiceObfuscator
from app.utils.file_handler import save_temp_file, delete_file
from app.core.security import create_access_token
from app.core.limiter import limiter


router = APIRouter()

obfuscator = VoiceObfuscator()


@router.get("/token")

def token():

    return {

        "access_token":

        create_access_token(
            {"user": "enterprise"}
        )
    }



@router.post("/obfuscate")
@limiter.limit("5/minute")
async def obfuscate(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):



    if not file.filename.endswith((".wav", ".mp3")):

        raise HTTPException(400, "Invalid format")


    content = await file.read()


    input_path = save_temp_file(
        content,
        ".wav"
    )


    output_path = obfuscator.obfuscate(
        input_path
    )


    background_tasks.add_task(
        delete_file,
        input_path
    )


    return FileResponse(

        output_path,

        filename="secure_obfuscated.wav"
    )
