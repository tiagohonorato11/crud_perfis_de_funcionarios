from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import uuid

router = APIRouter(tags=["Upload"])

UPLOAD_DIR = "app/static/uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
async def upload_arquivo(file: UploadFile = File(...)):
    try:
        # Gera nome único para o arquivo
        extensao = file.filename.split(".")[-1]
        nome_arquivo = f"{uuid.uuid4()}.{extensao}"
        caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)
        
        with open(caminho_arquivo, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        url_arquivo = f"/static/uploads/{nome_arquivo}"
        return {"url": url_arquivo}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")
