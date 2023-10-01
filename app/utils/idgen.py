import uuid

def idgen() -> str:
    # Generate a random uuid string
    return str(uuid.uuid4().hex)