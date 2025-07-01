from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from app.database import engine, get_session
from app.models import User, SQLModel
from app.schemas import UserCreate, UserLogin
from app.auth import get_password_hash, verify_password

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/register")
def register(user: UserCreate, session: Session = Depends(get_session)):
    user_in_db = session.exec(select(User).where(User.username == user.username)).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "User registered successfully", "user_id": new_user.id}

@app.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    user_in_db = session.exec(select(User).where(User.username == user.username)).first()
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful"}
