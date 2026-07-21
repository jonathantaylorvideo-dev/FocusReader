import json

REQUIRED_KEYS = ("id", "content_type", "payload")


def validate_payload(payload_str):
    try:
        data = json.loads(payload_str)
    except json.JSONDecodeError:
        return {"status": "invalid_json_format"}

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        return {"status": "missing_keys", "missing_keys": missing}

    return {"status": "success", "data": data}
