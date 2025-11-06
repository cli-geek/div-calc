import os
from dotenv import load_dotenv

load_dotenv()

def get_req_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Required environment variable {var_name} is not set")
    return value

class Config:
    SECRET_KEY = get_req_env_var('SECRET_KEY')
    DATABASE = 'info.db'
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'csv'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
