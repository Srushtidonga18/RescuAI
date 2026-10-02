import os

path = 'backend/app/api/v1/responder.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

delete_route = '''@router.delete("/sos/{sos_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sos(
    sos_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sos_record = db.query(SOSRequest).filter(SOSRequest.id == sos_id).first()
    if sos_record:
        # Also delete associated dispatch card
        dispatch_card = db.query(DispatchCard).filter(DispatchCard.sos_id == sos_id).first()
        if dispatch_card:
            db.delete(dispatch_card)
        db.delete(sos_record)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

'''

content = content.replace('@router.post("/inventory"', delete_route + '@router.post("/inventory"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
