from sqlalchemy.orm import Session
from app.models.user import User
from app.models.post import Post

class InMemoryDatabase:
    def __init__(self):
        self.users = []
        self.posts = []

in_memory_db = InMemoryDatabase()

def get_db():
    return in_memory_db
