from .redis_client import redis_client
import uuid

CONFIRMATION_TTL = 300  

def set_confirmation_code(user_id: int) -> str:
    code = str(uuid.uuid4())[:6]  
    key = f"confirmation_code:{user_id}"
    redis_client.setex(key, CONFIRMATION_TTL, code)
    return code

def get_confirmation_code(user_id: int) -> str | None:
    key = f"confirmation_code:{user_id}"
    return redis_client.get(key)

def delete_confirmation_code(user_id: int) -> None:
    key = f"confirmation_code:{user_id}"
    redis_client.delete(key)
