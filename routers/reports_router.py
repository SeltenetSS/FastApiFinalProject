from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from io import BytesIO
import pandas as pd
from fastapi.responses import StreamingResponse


router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/orders")
def orders_report(db: Session = Depends(get_db)):

    orders = crud.list_orders(db)

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")


    data = []
    for order in orders:
        for item in order.items:
            data.append({
                "Order ID": order.id,
                "Customer ID": order.customer_id,
                "Status": order.status.value if hasattr(order.status, 'value') else order.status,
                "Product ID": item.product_id,
                "Product Name": item.product.name,
                "Qty": item.qty,
                "Unit Price": item.unit_price,
                "Line Total": item.line_total,
                "Order Total": order.total,
                "Created At": order.created_at
            })

    df = pd.DataFrame(data)


    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Orders")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=orders_report.xlsx"}
    )
