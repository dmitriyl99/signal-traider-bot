from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(prefix='/webapp', tags=['Webapp'])


@router.get('/')
def launch_web_app():
    return FileResponse('app/public/webapp.html')
