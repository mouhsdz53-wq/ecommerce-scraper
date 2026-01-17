from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from models import get_db, Alert, Product
from pydantic import BaseModel
from decimal import Decimal

router = APIRouter()


class AlertCreate(BaseModel):
    product_id: int
    type_alerte: str  # price_drop, new_viral, low_saturation
    seuil: Optional[Decimal] = None


class AlertResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    type_alerte: str
    seuil: Optional[Decimal]
    actif: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    actif_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des alertes
    """
    query = db.query(Alert).join(Product)
    
    if actif_only:
        query = query.filter(Alert.actif == True)
    
    alerts = query.all()
    
    result = []
    for alert in alerts:
        result.append(AlertResponse(
            id=alert.id,
            product_id=alert.product_id,
            product_name=alert.product.nom,
            type_alerte=alert.type_alerte,
            seuil=alert.seuil,
            actif=alert.actif,
            created_at=alert.created_at
        ))
    
    return result


@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle alerte
    """
    # Vérifier que le produit existe
    product = db.query(Product).filter(Product.id == alert.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Créer l'alerte
    new_alert = Alert(
        product_id=alert.product_id,
        type_alerte=alert.type_alerte,
        seuil=alert.seuil,
        actif=True
    )
    
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)
    
    return AlertResponse(
        id=new_alert.id,
        product_id=new_alert.product_id,
        product_name=product.nom,
        type_alerte=new_alert.type_alerte,
        seuil=new_alert.seuil,
        actif=new_alert.actif,
        created_at=new_alert.created_at
    )


@router.put("/{alert_id}")
async def update_alert(
    alert_id: int,
    actif: Optional[bool] = None,
    seuil: Optional[Decimal] = None,
    db: Session = Depends(get_db)
):
    """
    Modifier une alerte
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if actif is not None:
        alert.actif = actif
    if seuil is not None:
        alert.seuil = seuil
    
    db.commit()
    db.refresh(alert)
    
    return {"message": "Alert updated successfully", "alert_id": alert_id}


@router.delete("/{alert_id}")
async def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une alerte
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alert deleted successfully", "alert_id": alert_id}
