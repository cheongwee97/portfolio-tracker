import os
import redis
from dotenv import load_dotenv
load_dotenv()

REDIS_HOST=os.getenv("REDIS_HOSTNAME", "redis")
REDIS_PORT=os.getenv("REDIS_PORT", 6379)

def get_redis_client(redis_host, redis_port, decode_response=True):
    return redis.Redis(
        host=redis_host,
        port=int(redis_port),
        decode_responses=True
    )

redis_client = get_redis_client(REDIS_HOST, REDIS_PORT)