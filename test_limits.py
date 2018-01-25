from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter

redis_storage = RedisStorage("redis://127.0.0.1/3")
moving_window = MovingWindowRateLimiter(redis_storage)
a = moving_window
print(moving_window)
