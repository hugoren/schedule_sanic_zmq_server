a = b"{'retcode': None, 'stderr': '127.0.0.1 client disconnects.'}"
import json

# b = json.loads(str(a, encoding="utf-8"))
b = eval(a)
print(b)
