import jwt
print(jwt.__file__)
print(jwt.encode({'user': 'test'}, 'secret', algorithm='HS256'))
