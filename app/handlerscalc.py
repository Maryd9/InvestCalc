from fastapi import APIRouter, Request, Form
from app.calculation import calculation
from starlette.responses import HTMLResponse
from app.handlers import templates

router = APIRouter(tags=['Calculation'])


@router.post('/', response_class=HTMLResponse)
async def home(request: Request, indexes: str = Form(...), initialInvestment: int = Form(...),
               discountRate: int = Form(...), cashflows: int = Form(...), cf1: int = Form(...)):
    result = calculation(indexes, initialInvestment, discountRate, cashflows, cf1)
    return templates.TemplateResponse('html/home.html', {'request': request, 'result': result})