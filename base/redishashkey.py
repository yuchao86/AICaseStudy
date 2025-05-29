
import redis

# 创建 Redis 连接对象
redis_connections = [redis.Redis(db=db,host="redis-**.redis.ivolces.com",password="**8") for db in range(16)]

# 将 key 分配到不同的数据库
def set_key(key, value):
    a = hash(key)
    db_number = a % 16
    # 构造带前缀的 key
    full_key = f"db{db_number}:{key}"
    print(full_key)
    # 选择对应的数据库，并设置值
    redis_connections[db_number].set(full_key, value)


# 从不同的数据库获取 key
def get_key(key):
    a = hash(key)
    db_number = a % 16
    full_key = f"db{db_number}:{key}"
    return redis_connections[db_number].get(full_key)


# 示例使用
set_key("mykey", "myvalue11")
set_key("yourkey", "yourvalue11")

value = get_key("mykey")
print(value)  # 输出: myvalue

value = get_key("yourkey")
print(value)  # 输出: yourvalue
