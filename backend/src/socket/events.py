from src.socket.socket_manager import sio
import logging

logger = logging.getLogger(__name__)


@sio.event
async def connect(sid, environ, auth=None):
    logger.info("socket connected: %s", sid)


@sio.event
async def disconnect(sid):
    logger.info("socket disconnected: %s", sid)


async def emit_attendance_marked(room: str, payload: dict):
    await sio.emit("attendance:marked", payload, room=room)


async def emit_notice_published(room: str, payload: dict):
    await sio.emit("notice:published", payload, room=room)


async def emit_fees_updated(room: str, payload: dict):
    await sio.emit("fees:updated", payload, room=room)