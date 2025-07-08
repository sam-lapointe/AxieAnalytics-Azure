from fastapi import APIRouter
from src.models.axie_sales_search import AxieSalesSearch, CollectionWrapper, CollectionDetail
from src.services.axie_sales import get_all_data, get_data_by_breed_count
from src.utils import format_data_line_graph, format_data_line_graph_by_collection
import copy
import asyncio

router = APIRouter()

@router.get("/graph/overview")
async def get_graph():
    """
    Query all axies sales for the last 30 days and format the data into 3 timeframes: 24H, 7D and 30D.
    """
    query_select = "SELECT price_eth, sale_date FROM axies_full_info"
    filter = AxieSalesSearch()
    raw_data = await get_all_data(query_select, filter)

    d1_data = format_data_line_graph(raw_data, "days", 1)
    d7_data = format_data_line_graph(raw_data, "days", 7)
    d30_data = format_data_line_graph(raw_data, "days", 30)

    data = {
        "1d": d1_data,
        "7d": d7_data,
        "30d": d30_data,
    }
    return data

@router.post("/graph/overview")
async def get_graph_custom(filters: AxieSalesSearch):
    """
    Query all axies sales for the last 30 days and format the data into 3 timeframes: 24H, 7D and 30D.
    This endpoint is used to get custom filters from the frontend.
    """
    query_select = "SELECT price_eth, sale_date FROM axies_full_info"
    raw_data = await get_all_data(query_select, filters)

    data = format_data_line_graph(raw_data, filters.time_unit, filters.time_num)

    return data

@router.get("/graph/collection")
async def get_graph_collection():
    query_select = """
        SELECT
            price_eth,
            sale_date,
            eyes_special_genes,
            ears_special_genes,
            mouth_special_genes,
            horn_special_genes,
            back_special_genes,
            tail_special_genes,
            collection_title
        FROM axies_full_info
    """
    filter = AxieSalesSearch()
    raw_data = await get_all_data(query_select, filter)

    d1_data = format_data_line_graph_by_collection(raw_data, "days", 1)
    d7_data = format_data_line_graph_by_collection(raw_data, "days", 7)
    d30_data = format_data_line_graph_by_collection(raw_data, "days", 30)

    data = {
        "1d": d1_data,
        "7d": d7_data,
        "30d": d30_data,
    }
    return data

@router.get("/graph/breed_count")
async def get_graph_breed_count():
    d1_data = await get_data_by_breed_count("days", 1)
    d7_data = await get_data_by_breed_count("days", 7)
    d30_data = await get_data_by_breed_count("days", 30)

    data = {
        "1d": d1_data,
        "7d": d7_data,
        "30d": d30_data,
    }

    # Convert to dict and round values
    for key in data:
        new_list = []
        for item in data[key]:
            d = dict(item)
            d["volume_eth"] = round(d["volume_eth"], 5)
            d["avg_price_eth"] = round(d["avg_price_eth"], 5)
            new_list.append(d)
        data[key] = new_list
    return data

@router.post("/list")
async def get_list_data(filters: AxieSalesSearch):
    query_select = "SELECT * from axies_full_info"
    raw_data =  await get_all_data(query_select, filters)
    data = []
    for axie in raw_data:
        data.append(
            {
                "axie_id": axie["axie_id"],
                "price_eth": axie["price_eth"],
                "transaction_hash": axie["transaction_hash"],
                "sale_date": axie["sale_date"],
                "level": axie["level"],
                "xp": axie["xp"],
                "breed_count": axie["breed_count"],
                "image_url": axie["image_url"],
                "class": axie["class"],
                "parts": {
                    "eyes": {
                        "id": axie["eyes_id"],
                        "name": axie["eyes_name"],
                        "stage": axie["eyes_stage"],
                        "class": axie["eyes_class"],
                        "special_genes": axie["eyes_special_genes"]
                    },
                    "ears": {
                        "id": axie["ears_id"],
                        "name": axie["ears_name"],
                        "stage": axie["ears_stage"],
                        "class": axie["ears_class"],
                        "special_genes": axie["ears_special_genes"]
                    },
                    "mouth": {
                        "id": axie["mouth_id"],
                        "name": axie["mouth_name"],
                        "stage": axie["mouth_stage"],
                        "class": axie["mouth_class"],
                        "special_genes": axie["mouth_special_genes"]
                    },
                    "horn": {
                        "id": axie["horn_id"],
                        "name": axie["horn_name"],
                        "stage": axie["horn_stage"],
                        "class": axie["horn_class"],
                        "special_genes": axie["horn_special_genes"]
                    },
                    "back": {
                        "id": axie["back_id"],
                        "name": axie["back_name"],
                        "stage": axie["back_stage"],
                        "class": axie["back_class"],
                        "special_genes": axie["back_special_genes"]
                    },
                    "tail": {
                        "id": axie["tail_id"],
                        "name": axie["tail_name"],
                        "stage": axie["tail_stage"],
                        "class": axie["tail_class"],
                        "special_genes": axie["tail_special_genes"]
                    }
                },
                "body_shape": axie["body_shape_id"],
                "collection_title": axie["collection_title"]
            }
        )
    
    return data
