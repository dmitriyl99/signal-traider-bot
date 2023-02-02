from fastapi import APIRouter, Depends, Request
from fastapi_csrf_protect import CsrfProtect
from fastapi.templating import Jinja2Templates

from app.config import CsrfSettings


router = APIRouter(prefix='/webapp', tags=['Webapp'])
templates = Jinja2Templates(directory='templates')


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@router.get('/')
def launch_web_app(request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    return templates.TemplateResponse('cloud-payments.html', {
        'request': request, 'csrf_token': csrf_token
    })
