from app.database.model import UserTB, DonationHistory
from sqlmodel import select, Session, delete
from fastapi import Depends, HTTPException
from app.model.donate import Donate
from app.core import app, get_session
from app.model.user import User

@app.get("/api/user/donate/{user_id}", tags=["Donations"])
def get_user_donation_history(id: str, session: Session = Depends(get_session)):
    user = select(UserTB).where(UserTB.id == id)
    result = session.exec(user).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    statement = select(DonationHistory).where(DonationHistory.user_id == id)
    donates = session.exec(statement).all()
    
    if not donates:
        raise HTTPException(status_code=404, detail="This user doesn't donate yet")
    
    return {'message': 'found', 'donate_history': donates}

@app.post("/api/user/donate", tags=["Donations"])
def user_new_donate(donate: Donate, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == donate.id)
    user = session.exec(statement).first()
    if user:
        user.lastdonate = donate.date
        session.add(user)
        session.commit()
    elif not user:
        raise HTTPException(status_code=404, detail="This user not found")

    data = session.get(UserTB, donate.id)
    new_donate = DonationHistory(quantity=donate.quantity, date=donate.date, user=data)
    session.add(new_donate)
    session.commit()
    return {'message': 'Donation created successfully', 'donation': new_donate}