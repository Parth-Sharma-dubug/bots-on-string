from fastapi import APIRouter, UploadFile, File, HTTPException
import os

router = APIRouter(prefix="/upload", tags=["File Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{company_id}")
async def upload_company_file(company_id: str, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, f"{company_id}_{file.filename}")

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {e}")

    return {"message": "File uploaded successfully", "filename": file.filename}
