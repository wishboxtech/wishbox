"""Redis-like cache operations for isolated Django tests, never production."""

import math
import time

from django.core.cache.backends.locmem import LocMemCache


class MemoryTTLCache(LocMemCache):
    def validate_key(self, key):
        # Redis/LocMem accept long JWT keys; the base warning targets Memcached.
        pass

    def set(self, key, value, timeout=None, version=None, nx=False):
        if nx:
            return self.add(key, value, timeout=timeout, version=version)
        super().set(key, value, timeout=timeout, version=version)
        return True

    def ttl(self, key):
        encoded = self.make_and_validate_key(key)
        with self._lock:
            if self._has_expired(encoded):
                return 0
            deadline = self._expire_info.get(encoded)
            return (
                None if deadline is None else max(0, math.ceil(deadline - time.time()))
            )

    def expire(self, key, timeout):
        if timeout == 0:
            return self.delete(key)
        return self.touch(key, timeout=timeout)
