import redis
from loguru import logger
from config import settings


class _NullRedis:
    """
    بديل آمن عند غياب Redis — يمنع السيرفر من التوقف.
    جميع عمليات OTP ستُعيد قيماً افتراضية آمنة (False / None / 0).
    """
    def exists(self, *args, **kwargs): return 0
    def get(self, *args, **kwargs): return None
    def setex(self, *args, **kwargs): return True
    def delete(self, *args, **kwargs): return 0
    def incr(self, *args, **kwargs): return 1
    def ttl(self, *args, **kwargs): return 0
    def ping(self): return False


def get_redis_client():
    """إنشاء اتصال Redis مع معالجة الأخطاء بشكل آمن."""
    try:
        client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=3,
        )
        client.ping()  # اختبار الاتصال فعلياً
        logger.success(f"✅ Redis متصل بنجاح على {settings.REDIS_HOST}:{settings.REDIS_PORT}")
        return client
    except Exception as e:
        logger.warning(
            f"⚠️ تعذّر الاتصال بـ Redis ({e}). "
            "سيعمل النظام بوضع محدود — OTP لن يُحفظ."
        )
        return _NullRedis()


redis_client = get_redis_client()
