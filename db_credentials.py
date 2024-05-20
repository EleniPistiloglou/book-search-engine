import os


host = os.getenv('db_host', '')
port = os.getenv('db_port', '5432')
user = os.getenv('db_user', '')
password = os.getenv('db_password', '')
name = os.getenv('db_name', '')