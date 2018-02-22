def cache(func):
    cache_dict = {}

    def inner(*args, **kwargs):
        try:
            key = repr(args, kwargs)
            print(key)
        except Exception as e:
            print(e)
        try:
            return cache_dict[key]
        except KeyError:
            cache_dict[key] = func(*args, **kwargs)
            return cache_dict[key]
    inner.csrf_exempt = True
    return inner


@cache
def query_limit(sql=None):
    print(sql)


import better_exceptions
request = "test test test"
a, b, c, d = request.split()  # 处理数据