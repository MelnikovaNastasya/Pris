from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def dashboard():
    """
    Simple HTML dashboard shell. Frontend JS calls analytics APIs.
    """
    index_path = TEMPLATES_DIR / "index.html"
    html = index_path.read_text(encoding="utf-8")
    return HTMLResponse(content=html)

