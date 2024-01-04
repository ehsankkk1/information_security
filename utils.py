import base64
import hashlib
import random
import uuid
import secrets
import os


def convert_string_to_key(input_string):
  # Create a SHA-256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    hash_object.update(input_string.encode())

    # Get the digest of the hash object
    digest = hash_object.digest()

    # Base64 encode the digest and make it URL-safe
    key = base64.urlsafe_b64encode(digest)

    return key

def generate_mathematical_equation():
    # Replace this with your logic to generate a suitable mathematical equation
    # for the professor to solve, ensuring appropriate difficulty levels.
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*'])
    equation = f"{num1} {operator} {num2} = ?"
    return equation, num1 + num2 if operator == '+' else num1 - num2 if operator == '-' else num1 * num2
