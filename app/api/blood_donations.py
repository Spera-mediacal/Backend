from app.database.model import UserTB, DonationHistory
from sqlmodel import select, Session, delete
from fastapi import Depends, HTTPException
from app.model.donate import Donate
from app.core import app, get_session
from app.model.user import User

@app.get("/api/donate", tags=["Donations"])
def get_all_donations(session: Session = Depends(get_session)):
    statement = (select(DonationHistory.id, DonationHistory.quantity, DonationHistory.date, UserTB.bloodType, UserTB.id, UserTB.name).join(UserTB, UserTB.id == DonationHistory.user_id))
    donates = session.exec(statement).all()
    return [
        {
            "donate_id": row[0],
            "donate_quantity": row[1],
            "donate_date": row[2],
            "blood_type": row[3],
            "user_id": row[4],
            "name": row[5]
        }
        for row in donates
    ]

@app.get("/api/donate/{user_id}", tags=["Donations"])
def get_user_donation_history(id: str, session: Session = Depends(get_session)):
    user = select(UserTB).where(UserTB.id == id)
    result = session.exec(user).first()
    
    if not result:
        raise HTTPException(status_code=406, detail="User not found")
    
    statement = select(DonationHistory).where(DonationHistory.user_id == id)
    donates = session.exec(statement).all()
    
    if not donates:
        raise HTTPException(status_code=404, detail="0")
    
    return {'message': 'found', 'donate_history': donates}

@app.post("/api/donate", tags=["Donations"])
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