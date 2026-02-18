Voice Obfuscation API – Enterprise Version

Live Demo:
https://vo-xd2y.onrender.com

Features:

• Prevents voice cloning
• Production-ready FastAPI
• Dockerized
• Cloud deployed
• Secure processing
• Anti-deepfake protection


Tech Stack:

FastAPI
Docker
AWS-ready
Librosa
Python


Architecture:

Client → API → Obfuscation Engine → Secure Output


Run locally:

docker build -t obfuscator .
docker run -p 8000:8000 obfuscator
