import os
import socketio
from dotenv import load_dotenv

load_dotenv()

allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_URI", "").split(",")
    if origin.strip()
]

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=allowed_origins if allowed_origins else "*"
)