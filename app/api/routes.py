from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends, Request
from fastapi.responses import FileResponse
import os
import logging

from app.services.obfuscator import obfuscator
from app.utils.file_handler import save_temp_file, delete_file
from app.core.security import create_access_token, verify_token
from app.core.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

OUTPUT_DIR = "outputs"


# =========================
# TOKEN ENDPOINT
# =========================

@router.get("/token")

def token():

    return {

        "access_token":

        create_access_token(

            {"user": "enterprise"}

        )

    }


# =========================
# OBFUSCATION ENDPOINT
# =========================

@router.post("/obfuscate")

@limiter.limit("5/minute")

async def obfuscate(

    request: Request,

    background_tasks: BackgroundTasks,

    file: UploadFile = File(...),

    user=Depends(verify_token)

):

    try:

        logger.info(f"Upload received: {file.filename}")


        if not file.filename.endswith(

            (".wav", ".mp3")

        ):

            raise HTTPException(

                400,

                "Invalid file format"

            )


        content = await file.read()


        if len(content) > 20 * 1024 * 1024:

            raise HTTPException(

                400,

                "File too large"

            )


        input_path = save_temp_file(

            content,

            ".wav"

        )


        output_path = obfuscator.obfuscate(

            input_path,

            OUTPUT_DIR

        )


        background_tasks.add_task(

            delete_file,

            input_path

        )


        background_tasks.add_task(

            delete_file,

            output_path

        )


        return FileResponse(

            output_path,

            filename="secure_obfuscated.wav"

        )


    except Exception as e:

        logger.error(str(e))

        raise HTTPException(

            500,

            "Processing failed"

        )
