import os
from common.aws.secretsmanager import get_secret

class Config:
    def __init__(self):
        self._secrets = get_secret("sleepnumber", "us-east-1")

    @property
    def aws_region(self):
        return os.getenv('AWS_REGION', 'us-east-1')

    @property
    def skill_id(self):
        return self._secrets["skill_id"]

    @property
    def log_level(self):
        return os.getenv('LOG_LEVEL', 'DEBUG').upper()
    
    @property
    def username(self):
        return self._secrets["username"]
    
    @property
    def password(self):
        return self._secrets["password"]

config = Config()
