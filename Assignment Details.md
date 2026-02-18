Intern Evaluation Exercise
Project: Voice Obfuscation API for Customer Call Recordings
**Objective**

1.Build a production-ready API service that:

2.Accepts customer call audio recordings

3.Applies voice obfuscation so:

    Speech remains intelligible

    Speaker identity cannot be cloned or used for deepfake training

    Returns the transformed audio securely

🔐 Requirements
**Functional Requirements**

    1.Upload audio file (WAV, MP3)

    2. Output processed WAV

    3. Preserve speech clarity

**Prevent**

    1.Voiceprint extraction

    2.Speaker embedding reuse

    3.Training for TTS/deepfake cloning

    4.Non-Functional Requirements

**Production-grade structure**

    1.Proper logging

    2.Input validation

    3.Error handling

    4.Streaming support (optional bonus)

    5.Container-ready (Dockerfile)

