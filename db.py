from orator import DatabaseManager, Schema, Model
import os
from dotenv import load_dotenv

load_dotenv()


DATABASES = {
    "postgres": {
        "driver": "postgres",
        "host": os.environ['HOST'],
        "database": os.environ['DATABASE'],
        "user": os.environ['DB_USER'],
        "password": os.environ['PASSWORD'],
        "prefix": "",
        "port": os.environ['PORT']
    }
}

db = DatabaseManager(DATABASES)
schema = Schema(db)
Model.set_connection_resolver(db)
