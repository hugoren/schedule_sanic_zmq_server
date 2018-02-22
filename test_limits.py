from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter
from limits import RateLimitItemPerSecond


def test():
    storage = RedisStorage("redis://127.0.0.1/3")
    strategy = MovingWindowRateLimiter(storage)
    one_per_second = RateLimitItemPerSecond(10, 1)
    r = strategy.hit(one_per_second, "k", "v")
    print(r)

for i in range(100):
    test()


