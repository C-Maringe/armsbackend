import datetime
import base64
import hashlib
import hmac

SECRET_KEY = b'Doctorcm@1'
DECODE_KEY = b'Doctorcm@1'


def generate_expiration_token(data):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=data)
    print("Current Time:", datetime.datetime.utcnow())
    expiration_timestamp = int(expiration_time.timestamp())
    encoded_timestamp = base64.urlsafe_b64encode(str(expiration_timestamp).encode()).decode()
    hash_value = hmac.new(SECRET_KEY, encoded_timestamp.encode(), hashlib.sha256).hexdigest()
    expiration_token = encoded_timestamp + hash_value[:6]
    return expiration_token


token = generate_expiration_token(24)
print("Generated Token:", token)


def decode_expiration_token(expiration_token):
    encoded_timestamp = expiration_token[:-6]
    hash_value = expiration_token[-6:]
    calculated_hash = hmac.new(DECODE_KEY, encoded_timestamp.encode(), hashlib.sha256).hexdigest()[:6]

    if calculated_hash != hash_value:
        raise ValueError(
            f"Token integrity check failed. The token may be tampered. Decode key does not match the key used for "
            f"generation.")

    decoded_timestamp_bytes = base64.urlsafe_b64decode(encoded_timestamp)
    decoded_timestamp = int(decoded_timestamp_bytes.decode())
    expiration_time = datetime.datetime.utcfromtimestamp(decoded_timestamp)

    return expiration_time


try:
    decoded_time = decode_expiration_token(token)
    print("Decoded Expiration Time:", decoded_time)
except ValueError as e:
    print(str(e))
