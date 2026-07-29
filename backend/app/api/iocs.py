from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.ioc import IOC
from app.schemas.ioc import IOCOut

router = APIRouter()


@router.get("/iocs/{ioc_id}/enrichment", response_model=IOCOut)
def get_ioc_enrichment(ioc_id: str, db: Session = Depends(get_db)):
    ioc = db.query(IOC).filter(IOC.id == ioc_id).first()
    if not ioc:
        raise HTTPException(status_code=404, detail="IoC not found")
    return IOCOut.model_validate(ioc)


@router.get("/iocs/search", response_model=list[IOCOut])
def search_iocs(
    value: Optional[str] = Query(None, description="Partial or full IoC value to search for"),
    ioc_type: Optional[str] = Query(None),
    min_risk: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(IOC)
    if value:
        query = query.filter(IOC.value.ilike(f"%{value}%"))
    if ioc_type:
        query = query.filter(IOC.ioc_type == ioc_type)
    if min_risk is not None:
        query = query.filter(IOC.risk_score >= min_risk)

    results = query.order_by(IOC.created_at.desc()).limit(50).all()
    return [IOCOut.model_validate(r) for r in results]