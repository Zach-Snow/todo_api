import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CLUSTER = os.getenv("DB_CLUSTER")


class Database(pymongo.database.Database):

    def __init__(self, username=DB_USERNAME, password=DB_PASSWORD, database="TODO_DB", cluster=DB_CLUSTER):
        self.username = username
        self.password = password
        self.database = database
        self.cluster = cluster
        mongo = pymongo.MongoClient(
            f"mongodb+srv://{self.username}:{self.password}@{self.cluster}.4fryz.mongodb.net/{self.database}?retryWrites=true&w=majority",
            connect=False,
            tlsAllowInvalidCertificates=True
        )
        super().__init__(mongo, self.database)


db = Database()

