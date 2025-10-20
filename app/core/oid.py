# app/core/oid.py
from bson import ObjectId
from fastapi import HTTPException, status

def to_object_id(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id")

def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    doc["id"] = str(doc.pop("_id"))
    if "owner_id" in doc:
        doc["owner_id"] = str(doc["owner_id"])
    return doc
