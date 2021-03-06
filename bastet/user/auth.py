import jwt
from datetime import timezone
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from bastet.conf import settings

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = settings.SECRET_KEY

    def get_password_hash(self, password):
        """takes plain text password and return the hashed password
        using CryptContext
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    # For getting the current time in UTC, use an aware datetime object with the timezone explicitly set to UTC.
    # REF: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    # EXAMPLE: https://docs.sourcery.ai/suggestions/aware-datetime-for-utc/
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=0, minutes=5), 
            'iat': datetime.now(timezone.utc), 
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail='Signature has expired') from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token') from e

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)