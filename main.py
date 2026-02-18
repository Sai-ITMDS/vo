from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(

    title="Enterprise Voice Obfuscator"

)


app.include_router(router)
