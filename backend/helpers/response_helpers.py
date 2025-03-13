from datetime import datetime

def success_response(data=None, message="Success", status=200):
    if data is not None and not isinstance(data, dict):
        raise ValueError("The 'data' parameter must be a dictionary or None.")

    return {
        "status": "success",
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }, status

def error_response(message="An error occurred", status=400, error_code=None, error_details=None):
    if error_details is not None and not isinstance(error_details, dict):
        raise ValueError("The 'error_details' parameter must be a dictionary or None.")

    response = {
        "status": "error",
        "message": message,
        "error_code": error_code,
        "error_details": error_details,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Remove keys with None values
    response = {key: value for key, value in response.items() if value is not None}

    return response, status
