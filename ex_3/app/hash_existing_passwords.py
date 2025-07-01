from app.database import engine
from sqlmodel import Session, select
from app.models import User
from app.auth import get_password_hash

with Session(engine) as session:
    users = session.exec(select(User)).all()
    for user in users:
        if not user.hashed_password.startswith("$2b$"):  # проверка: уже хеш?
            user.hashed_password = get_password_hash(user.hashed_password)
    session.commit()

print("Все открытые пароли были захешированы.")
