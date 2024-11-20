from app.database.model import UserTB, DonationHistory, Doctors
from sqlmodel import create_engine, select, Session, SQLModel
from fastapi import FastAPI, Depends
from app.model.doctor import Doctor
from app.model.donate import Donate
from app.model.user import User
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DB_URL")

app = FastAPI()

engine = create_engine(DB_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event(event_type="startup")
def on_event():
    SQLModel.metadata.create_all(engine)

@app.get("/api/user/{user_id}", tags=["Blood Donations"])
def get_user_info(user_id: str, session: Session = Depends(get_session)):
    data = session.get(UserTB, user_id)
    return data

@app.post("/api/user", tags=["Blood Donations"])
def create_user(user: User, session: Session = Depends(get_session)):
    new_user = UserTB(id=user.id, name=user.name, phone=user.phone, bloodType=user.bloodType, weight=user.weight, hight=user.hight, age=user.age, lastdonate="")
    session.add(new_user)
    session.commit()
    return {'message': 'Done'}

@app.post("/api/user/donate", tags=["Blood Donations"])
def user_new_donate(donate: Donate, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == donate.id)
    user = session.exec(statement).first()
    if user:
        user.lastdonate = donate.date
        session.add(user)
        session.commit()
    data = session.get(UserTB, donate.id)
    new_donate = DonationHistory(quantity=donate.quantity, date=donate.date, user=data)
    session.add(new_donate)
    session.commit()
    return {'message': 'Done'}

@app.get("/api/user/donate/{user_id}", tags=["Blood Donations"])
def get_user_donation_history(id: str, session: Session = Depends(get_session)):
    statement = select(DonationHistory).where(DonationHistory.user_id == id)
    donates = session.exec(statement).all()
    return donates

@app.get('/api/doctor', tags=["Doctors"])
def get_all_doctors(session: Session = Depends(get_session)):
    statement = select(Doctors)
    doctors = session.exec(statement).all()
    return doctors

@app.post('/api/doctor', tags=["Doctors"])
def create_doctor(doctor: Doctor, session: Session = Depends(get_session)):
    new_doctor = Doctors(id=doctor.id, name=doctor.name, specialization=doctor.specialization, workDays=doctor.workDays, phone=doctor.phone, start=doctor.start, end=doctor.end, rate=doctor.rate, image=doctor.image)
    session.add(new_doctor)
    session.commit()
    return {'message': 'Done'}