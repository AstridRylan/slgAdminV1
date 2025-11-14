
def format_response(data, status_code=200):
    response = {
        'status': status_code,
        'data': data
    }
    return response