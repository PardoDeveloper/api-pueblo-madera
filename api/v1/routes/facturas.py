from fastapi import APIRouter, Depends, status, HTTPException, Body
from typing import List, Dict, Any
from sqlmodel import Session
from session import get_session
from schemas.factura import FacturaCreate, FacturaRead, DetalleFacturaCreate
from repositories.factura_repository import FacturaRepository

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post("/", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def create_factura(payload: Dict[str, Any] = Body(...), session: Session = Depends(get_session)):
    """Recibe un objeto con las claves 'data' (FacturaCreate) y 'detalles' (lista de DetalleFacturaCreate).
    Ejemplo:
    {
        "data": { proyecto_id: 1, subtotal: 100, impuestos: 19, total: 119, estado: "pendiente" },
        "detalles": [ { concepto: "Mueble A", cantidad: 1, precio_unitario: 100, total: 100 } ]
    }
    """
    try:
        data = payload.get('data')
        detalles = payload.get('detalles', [])

        if not data:
            raise HTTPException(status_code=400, detail="Falta la clave 'data' en el payload de la factura.")

        factura_obj = FacturaCreate(**data)
        detalles_obj = [DetalleFacturaCreate(**d) for d in detalles]

        return FacturaRepository.create(session, factura_obj, detalles_obj)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
