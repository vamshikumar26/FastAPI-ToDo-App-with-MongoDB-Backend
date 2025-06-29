
# FastAPI Auth API with JWT, OAuth2 & Docker

This project is a **production-ready FastAPI backend** with user authentication (OAuth2 + JWT), password hashing, and containerization using Docker. It follows a modular structure for scalability and easy maintenance.

---

##  Features

- **User Authentication** using OAuth2 + JWT
- **JWT Token Generation and Verification**
- **Secure Password Hashing** (bcrypt)
- **Modular Structure** with `models`, `schemas`, `routes`
- **Dockerized** for easy deployment
- Auto-generated API docs with **Swagger UI**
- Configuration management with `config.py`

---

## Tech Stack

- **FastAPI** – Web framework
- **OAuth2** – Authentication protocol
- **JWT (PyJWT)** – Token-based auth
- **Passlib (bcrypt)** – Password hashing
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server
- **Docker** – Containerization

---

## 🗂 Project Structure
├── main.py # Entry point for the FastAPI app
├── config.py # Environment/config settings
├── requirements.txt # Project dependencies
├── docker-compose.yml # Docker Compose setup
├── Dockerfile # Docker build file
├── Oauth2.py # OAuth2 password flow & token handling
├── jwt_token_module.py # JWT encoding/decoding utilities
├── hasing.py # Password hashing logic
├── models/ # SQLAlchemy models
├── routes/ # API route definitions
├── schema/ # Pydantic schemas for validation


Install dependencies:
-->pip install -r requirementst.txt

Run the app:
-->uvicorn main:app --reload

Open your browser and go to:
-->http://127.0.0.1:8000/docs


docker-compose up --build(Your app will be accessible at: http://localhost:8000)

########
Security Notes
1> JWT tokens should be stored securely (HTTP-only cookies or secure storage)

2> Use HTTPS in production

3> Rotate secret keys periodically
