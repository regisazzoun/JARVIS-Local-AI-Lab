def group_entries(rows):
    result = {}
    for row in rows:
        label = row.pop('label')
        result.setdefault(label, []).append(row)
    return result
