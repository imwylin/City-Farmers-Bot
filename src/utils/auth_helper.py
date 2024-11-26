import base64

def get_basic_auth_header(client_id: str, client_secret: str) -> str:
    """Generate Basic Auth header for Twitter API"""
    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}" 