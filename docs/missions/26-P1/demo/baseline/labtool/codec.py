def normalize(payload):
    result = payload.copy()
    result['count'] = int(payload.get('count', 0))
    return result
