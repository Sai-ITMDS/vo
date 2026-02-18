import os
import pytest
from fastapi.testclient import TestClient

from main import app
from app.services.obfuscator import VoiceObfuscator


client = TestClient(app)


# ---------- TEST HEALTH ENDPOINT ----------

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


# ---------- TEST AUDIO OBFUSCATION API ----------

def test_obfuscate_endpoint():

    test_file = "test.wav"


    # create dummy audio file

    with open(test_file, "wb") as f:

        f.write(os.urandom(1000))


    with open(test_file, "rb") as f:

        response = client.post(

            "/obfuscate",

            files={"file": ("test.wav", f, "audio/wav")}

        )


    os.remove(test_file)


    assert response.status_code == 200

    assert response.headers["content-type"] == "audio/wav"


# ---------- TEST OBFUSCATOR SERVICE ----------

def test_obfuscator_service():

    obfuscator = VoiceObfuscator()


    test_file = "test.wav"


    with open(test_file, "wb") as f:

        f.write(os.urandom(1000))


    output = obfuscator.obfuscate(test_file)


    assert os.path.exists(output)


    os.remove(test_file)

    os.remove(output)
