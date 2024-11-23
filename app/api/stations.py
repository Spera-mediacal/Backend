from app.database.model import Admins, Stations
from app.model.station import Station, StationU
from fastapi import Depends, HTTPException
from app.core import app, get_session
from sqlmodel import select, Session
from app.model.admin import Admin

@app.get("/api/station", tags=['Stations'])
def get_all_stations(session: Session = Depends(get_session)):
    statement = select(Stations)
    stations = session.exec(statement).all()
    return {'message': stations}

@app.post("/api/station", tags=['Stations'])
def create_new_station(station: Station, session: Session = Depends(get_session)):
    data = session.get(Admins, station.admin_id)
    if not data:
        raise HTTPException(status_code=406, detail="This admin not exists")
    
    new_station = Stations(name=station.name, phone=station.phone, location=station.location, admin=data)
    session.add(new_station)
    session.commit()
    session.refresh(new_station)
    
    return {'message': 'New station created successfully', 'station': new_station}

@app.put("/api/station", tags=["Stations"])
def update_station_by_id(station: StationU, session: Session = Depends(get_session)):
    statement = select(Stations).where(Stations.id == station.id)
    existing_station = session.exec(statement).first()
    
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