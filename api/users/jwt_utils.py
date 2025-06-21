import jwt
print(jwt.__file__)  # It should point to site-packages/pyjwt/
<<<<<<< HEAD
=======
print(jwt.encode)
>>>>>>> 307bd68 (Adding Docs and Labs in admin panel done)
import datetime
from django.conf import settings

def generate_jwt(username):
    try:
        print('Generating JWT for user:', username)
        # Convert datetime to Unix timestamp (seconds)
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # 1 day expiry
        iat_time = datetime.datetime.utcnow()  # Issued at time

        # Convert datetime to Unix timestamps
        # exp_timestamp = int(exp_time.timestamp())
        # iat_timestamp = int(iat_time.timestamp())

        payload = {
            'username': username,
            'exp': exp_time,  # 1 day expiry
            'iat': iat_time  # Issued at time
        }
        
        print('Payload:', payload)
        print('JWT Secret:', settings.JWT_SECRET)  # Print the secret key for debugging purposes
        # Generate the JWT token    
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')
        print('Generated token:', token)
        return token
    except Exception as e:
        print('Error generating JWT:', str(e))
        return None
    
def decode_jwt(token):
    try:
        print('Decoding JWT token:', token)
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        print('Decoded payload:', payload)
        # Return the username from the payload  
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
