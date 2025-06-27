from rest_framework.throttling import SimpleRateThrottle
import re 
import hashlib
class SendOneTimePasswordThrottleByDateHour(SimpleRateThrottle):
    scope = 'otp_hour'

    def get_cache_key(self, request, view):
        phone_number = self.extract_phone_number(request)
        if not phone_number or not self._is_valid_phone_number(phone_number):
            return None
        phone_hash = self._hash_phone_number(phone_number)
        return f"otp_{phone_hash}"

    def _extract_phone_number(self, request):
        return request.data.get('phone_number')
    
    def _is_valid_phone_number(self, phone_number):
        return re.match(r'^\+?\d{10,12}$', phone_number) is not None
    
    def _hash_phone_number(self, phone_number):
        return hashlib.sha256(phone_number.encode()).hexdigest()

class SendOneTimePasswordThrottleByDataDay(SendOneTimePasswordThrottleByDateHour):
    scope = 'otp_day'