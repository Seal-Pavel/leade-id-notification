import redis
from config import config

redis = redis.Redis(host='redis', port=6379, db=0, password=config.REDIS_PASSWORD)
