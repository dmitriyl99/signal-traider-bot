import random
from typing import Optional

import redis

import app.services.sms as sms
from app.config import config


class OTPService:
    _phone: str

    def __init__(self, phone: str):
        self._phone = phone

    def send_otp(self):
        rand_otp = random.randint(1000, 9999)
        text = f"MassPay. Vash kod: {rand_otp}"
        sms.send_sms('+' + self._phone, text)
        self._write_otp_to_cache(rand_otp)

    def verify_otp(self, otp: int) -> bool:
        cached_otp = int(self._get_otp_from_cache())
        if cached_otp is None:
            return False
        result = cached_otp == otp
        if result:
            self._clear_otp_from_cache()
            return True
        return False

    def _create_redis_client(self) -> redis.Redis:
        return redis.Redis(host=config.REDIS_HOST)

    def _write_otp_to_cache(self, otp: int):
        r = self._create_redis_client()
        r.set(name=f'user_{self._phone}_verification_code', value=otp, ex=600)

    def _get_otp_from_cache(self) -> Optional[int]:
        r = self._create_redis_client()
        value = r.get(f'user_{self._phone}_verification_code')
        return value

    def _clear_otp_from_cache(self):
        r = self._create_redis_client()
        r.delete(f'user_{self._phone}_verification_code')
