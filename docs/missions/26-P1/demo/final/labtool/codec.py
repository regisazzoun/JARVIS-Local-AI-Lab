def normalize(payload):
    if 'count' not in payload:
        raise ValueError("count is required")
    value = payload['count']
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("count must be a strict integer")
    if value < 0:
        raise ValueError("count must be >= 0")
    result = payload.copy()
    result['count'] = value
    return result
