from app.database.model import DonationHistory
from app.core import app, get_session
from sqlmodel import Session
from fastapi import Depends, HTTPException
from sqlalchemy import func

def get_donation_counts(session: Session):
    date_conversion = func.date(func.concat(func.substr(DonationHistory.date, 7, 4), '-', func.substr(DonationHistory.date, 4, 2), '-', func.substr(DonationHistory.date, 1, 2)))
    
    def format_results(results, labels):
        return [dict(zip(labels, row)) for row in results]

    daily_results = (session.query(date_conversion.label("day"),func.count(DonationHistory.id).label("donation_count")).group_by(date_conversion).all())
    daily = format_results(daily_results, ["dalily", "donation_count"])

    weekly_results = (session.query(func.date_format(date_conversion, '%Y-%u').label("week"),func.count(DonationHistory.id).label("donation_count")).group_by(func.date_format(date_conversion, '%Y-%u')).all())
    weekly = format_results(weekly_results, ["weekly","donation_count"])

    monthly_results = (session.query(func.date_format(date_conversion, '%Y-%m').label("month"),func.count(DonationHistory.id).label("donation_count")).group_by(func.date_format(date_conversion, '%Y-%m')).all())
    monthly = format_results(monthly_results, ["monthly", "donation_count"])

    yearly_results = (session.query(func.date_format(date_conversion, '%Y').label("year"),func.count(DonationHistory.id).label("donation_count")).group_by(func.date_format(date_conversion, '%Y')).all())
    yearly = format_results(yearly_results, ["yearly", "donation_count"])

    return {"daily": daily, "weekly": weekly, "monthly": monthly, "yearly": yearly}


@app.get('/api/admin/daily', tags=['Admin'])
def get_daily_donations(session: Session = Depends(get_session)):
    daily_donation = get_donation_counts(session)['daily']
    return daily_donation

@app.get('/api/admin/weekly', tags=['Admin'])
def get_weekly_donations(session: Session = Depends(get_session)):
    weekly_donation = get_donation_counts(session)['weekly']
    return weekly_donation

@app.get('/api/admin/monthly', tags=['Admin'])
def get_monthly_donations(session: Session = Depends(get_session)):
    monthly_donation = get_donation_counts(session)['monthly']
    return monthly_donation

@app.get('/api/admin/yearly', tags=['Admin'])
def get_yearly_donations(session: Session = Depends(get_session)):
    yearly_donation = get_donation_counts(session)['yearly']
    return yearly_donation