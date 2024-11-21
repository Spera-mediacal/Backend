from app.database.model import DonationHistory, UserTB
from fastapi import Depends, HTTPException
from app.core import get_session, app
from sqlmodel import Session, select
from app.model.user import User
from sqlalchemy import delete

@app.get("/api/user", tags=['User'])
def get_all_users_info(session: Session = Depends(get_session)):
    statement = select(UserTB)
    result = session.exec(statement).all()
    return {'message': result}

@app.get("/api/user/{user_id}", tags=["User"])
def get_user_info_by_id(user_id: str, session: Session = Depends(get_session)):
    statemnet = select(UserTB).where(UserTB.id == user_id)
    user = session.exec(statemnet).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {'message': 'User is exist', 'user': user}

@app.put("/api/user", tags=["User"])
def update_user_by_id(user: User, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == user.id)
    existing_user = session.exec(statement).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.name:
        existing_user.name = user.name
    if user.phone:
        existing_user.phone = user.phone
    if user.bloodType:
        existing_user.bloodType = user.bloodType
    if user.weight is not 0:
        existing_user.weight = user.weight
    if user.hight is not 0:
        existing_user.hight = user.hight
    if user.age is not 0:
        existing_user.age = user.age
    
    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)
    
    return {"message": "User updated successfully", "user": existing_user}

@app.post("/api/user", tags=["User"])
def create_user(user: User, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == user.id)
    result = session.exec(statement).first()
    if result:
        raise HTTPException(status_code=406, detail="This user already exists")
    new_user = UserTB(id=user.id, name=user.name, phone=user.phone, bloodType=user.bloodType, weight=user.weight, hight=user.hight, age=user.age, lastdonate="")
    session.add(new_user)
    session.commit()
    return {'message': 'User created successfully', 'user': new_user}

@app.delete('/api/user/{id}', tags=['User'])
def delete_user_by_id(id: str, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.exec(delete(DonationHistory).where(DonationHistory.user_id == id))
    
    session.delete(user)
    session.commit()
    
    return {'message': 'User deleted successfully', 'user': user}