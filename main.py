from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

from app.api.routes import router


app = FastAPI(

    title="Enterprise Voice Obfuscator"

)


app.include_router(router)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total requests"
)


@app.middleware("http")
async def count_requests(request, call_next):

    REQUEST_COUNT.inc()

    response = await call_next(request)

    return response


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )

