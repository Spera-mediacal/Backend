from app.database.model import UserTB, DonationHistory, Doctors, Stations
from sqlmodel import create_engine, select, Session, SQLModel
from fastapi import FastAPI, Depends, HTTPException
from app.model.station import Station
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

@app.get("/api/user/donate/{user_id}", tags=["Blood Donations"])
def get_user_donation_history(id: str, session: Session = Depends(get_session)):
    statement = select(DonationHistory).where(DonationHistory.user_id == id)
    donates = session.exec(statement).all()
    return donates

@app.put("/api/user", tags=["Blood Donations"])
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

@app.delete('/api/user/{id}', tags=['Blood Donations'])
def delete_user_by_id(id: str, session: Session = Depends(get_session)):
    statement = select(UserTB).where(UserTB.id == id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    
    return {'message': 'User deleted successfully', 'user': user}

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

@app.put("/api/doctor", tags=["Doctors"])
def update_doctor_by_id(doctor: Doctor, session: Session = Depends(get_session)):
    statement = select(Doctors).where(Doctors.id == doctor.id)
    existing_doctor = session.exec(statement).first()
    
    if not existing_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    if doctor.name:
        existing_doctor.name = doctor.name
    if doctor.specialization:
        existing_doctor.specialization = doctor.specialization
    if doctor.workDays is not None:
        existing_doctor.workDays = doctor.workDays
    if doctor.phone:
        existing_doctor.phone = doctor.phone
    if doctor.start:
        existing_doctor.start = doctor.start
    if doctor.end:
        existing_doctor.end = doctor.end
    if doctor.rate is not 0:
        existing_doctor.rate = doctor.rate
    if doctor.image:
        existing_doctor.image = doctor.image
    
    session.add(existing_doctor)
    session.commit()
    session.refresh(existing_doctor)
    
    return {"message": "Doctor updated successfully", "doctor": existing_doctor}

@app.delete('/api/doctor/{id}', tags=['Doctors'])
def delete_doctor_by_id(id: str, session: Session = Depends(get_session)):
    statement = select(Doctors).where(Doctors.id == id)
    doctor = session.exec(statement).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="doctor not found")
    
    session.delete(doctor)
    session.commit()
    
    return {'message': 'doctor deleted successfully', 'doctor': doctor}

@app.get("/api/station", tags=['Stations'])
def get_all_stations(session: Session = Depends(get_session)):
    statement = select(Stations)
    stations = session.exec(statement).all()
    return stations

@app.post("/api/station", tags=['Stations'])
def create_new_station(station: Station, session: Session = Depends(get_session)):
    new_station = Stations(name=station.name, manager=station.manager, phone=station.phone, location=station.location)
    session.add(new_station)
    session.commit()
    session.refresh(new_station)
    
    return {'message': 'New station created successfully', 'station': new_station}

@app.put("/api/station", tags=["Stations"])
def update_station_by_id(station: Station, session: Session = Depends(get_session)):
    statement = select(Stations).where(Stations.id == station.id)
    existing_station = session.exec(statement).first()
    
    if not existing_station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    if station.name:
        existing_station.name = station.name
    if station.manager:
        existing_station.manager = station.manager
    if station.phone:
        existing_station.phone = station.phone
    if station.location:
        existing_station.location = station.location
    
    # Commit the changes
    session.add(existing_station)
    session.commit()
    session.refresh(existing_station)
    
    return {"message": "Station updated successfully", "station": existing_station}

@app.delete("/api/station/{id}", tags=['Stations'])
def delete_station_by_id(id: int, session: Session = Depends(get_session)):
    statement = select(Stations).where(Stations.id == id)
    station = session.exec(statement).first()
    
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    session.delete(station)
    session.commit()
    
    return {'message': 'station deleted successfully', 'station': station}