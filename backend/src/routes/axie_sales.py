from fastapi import APIRouter, Query
from src.models.axie_sales_search import AxieSalesSearch

router = APIRouter()

@router.get("/graph")
async def get_graph_data(filters: AxieSalesSearch):
    pass

@router.get("/list")
async def get_list_data(filters: AxieSalesSearch):
    pass