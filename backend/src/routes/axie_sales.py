from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.models.axie_sales_search import AxieSalesSearch
from src.services.axie_sales import get_all_data

router = APIRouter()

@router.post("/graph")
async def get_graph(filters: AxieSalesSearch):
    pass

@router.get("/list")
async def get_list_data(filters: AxieSalesSearch):
    pass

@router.get("/")
async def test(filter: AxieSalesSearch):
    data = await get_all_data(filter)
    print(len(data))