from website.models.user import User
from typing import List

def user_filter(kriteria: dict) -> List[User]:
    print(kriteria)
    users = User.query.all()
    return users