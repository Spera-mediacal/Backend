from sqlmodel import select, Session
from fastapi import Depends, HTTPException
from app.database.model import Doctors
from app.model.doctor import Doctor
from app.core import app, get_session

@app.get('/api/doctor', tags=["Doctors"])
def get_all_doctors(session: Session = Depends(get_session)):
    statement = select(Doctors)
    doctors = session.exec(statement).all()
    return {'message': doctors}

@app.post('/api/doctor', tags=["Doctors"])
def create_doctor(doctor: Doctor, session: Session = Depends(get_session)):
    statement = select(Doctors).where(Doctors.id == doctor.id)
    result = session.exec(statement).first()
    
    if result:
        raise HTTPException(status_code=406, detail='This doctor already exists')
    
    new_doctor = Doctors(id=doctor.id, name=doctor.name, specialization=doctor.specialization, workDays=doctor.workDays, address=doctor.address, joinDate=doctor.joinDate, phone=doctor.phone, start=doctor.start, end=doctor.end, rate=doctor.rate, image=doctor.image)
    session.add(new_doctor)
    session.commit()
    return {'message': 'Doctor created successfully', 'doctor': new_doctor}

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
    if doctor.workDays[0]:
        existing_doctor.workDays = doctor.workDays
    if doctor.phone:
        existing_doctor.phone = doctor.phone
    if doctor.address:
        existing_doctor.address = doctor.address
    if doctor.joinDate:
        existing_doctor.joinDate = doctor.joinDate
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