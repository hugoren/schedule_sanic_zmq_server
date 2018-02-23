from limits.storage import RedisStorage
from limits.strategies import MovingWindowRateLimiter, FixedWindowElasticExpiryRateLimiter
from limits import RateLimitItemPerSecond, RateLimitItemPerMinute


def test():
    storage = RedisStorage("redis://127.0.0.1/3")
    strategy = FixedWindowElasticExpiryRateLimiter(storage)
    # one_per_second = RateLimitItemPerSecond(20, 1)
    one_per_min = RateLimitItemPerMinute(100, 1)
    r = strategy.hit(one_per_min, "k", "v")
    if r == True :
        print(True)
    else:
        print("请求满了")

for i in range(100):
    test()


