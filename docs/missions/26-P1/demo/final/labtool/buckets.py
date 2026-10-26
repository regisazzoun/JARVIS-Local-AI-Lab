def group_entries(rows):
    result = {}
    for row in rows:
        label = row.copy().pop('label')
        result.setdefault(label, []).append(row)
    return result
