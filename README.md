**Voice Obfuscation API** | Sairam Ramakrishnan
<br/>
**IITM ID:** 24f2006201@ds.study.iitm.ac.in


**Live Demo**:
https://vo-xd2y.onrender.com/docs - select obsfuscate, upload audio file
*Note: First time the server may boot and could take couple of mins. Subsequent requests will be served in <5 seconds*

**Metrics**:
https://vo-xd2y.onrender.com/metrics

*Grafana - not configured as Prometheus server could not be configured on time.*

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
github - CI/CD - Render
Librosa
Python

Architecture:
Client → API → Obfuscation Engine → Secure Output

Run locally:

docker build -t obfuscator .
docker run -p 8000:8000 obfuscator
