from fastapi import APIRouter
from src.models.axie_sales_search import AxieSalesSearch
from src.services.axie_sales import get_all_data
import time

router = APIRouter()

@router.post("/graph")
async def get_graph(filters: AxieSalesSearch):
    query_select = "SELECT price_eth, sale_date from axies_full_info"
    raw_data = await get_all_data(query_select, filters)
    data = {
        "total_sales": 0,
        "total_volume_eth": 0,
        "avg_price_eth": 0,
        "chart": []
    }

    def update_data_chart(idx: int) -> None:
        data["total_sales"] += data["chart"][idx]["sales"]
        data["total_volume_eth"] += data["chart"][idx]["volume_eth"]
        data["chart"][idx]["avg_price_eth"] = round(data["chart"][idx]["volume_eth"] / data["chart"][idx]["sales"], 5)

    current_time = time.time()
    if filters.time_unit == "hours":
            timeframe_seconds = 3600 * filters.time_num
    elif filters.time_unit == "days":
        timeframe_seconds = 86400 * filters.time_num
    start_time = current_time - timeframe_seconds

    chart_timestamps = (current_time - start_time) // 30
    chart_idx = 0
    for i in range(len(raw_data) - 1, 0, -1):
        while raw_data[i]["sale_date"] >= start_time + (chart_timestamps * (chart_idx + 1)):
            if chart_idx  == len(data["chart"]) - 1:
                update_data_chart(chart_idx)
            else:
                data["chart"].append({"sales": 0, "volume_eth": 0, "avg_price_eth": 0})

            chart_idx += 1

        if chart_idx == len(data["chart"]) - 1:
            data["chart"][chart_idx]["sales"] += 1
            data["chart"][chart_idx]["volume_eth"] += raw_data[i]["price_eth"]
        else:
            data["chart"].append({})
            data["chart"][chart_idx]["sales"] = 1
            data["chart"][chart_idx]["volume_eth"] = raw_data[i]["price_eth"]

    update_data_chart(29)  # Update the last data chart index.
    data["avg_price_eth"] = round(data["total_volume_eth"] / data["total_sales"], 5)
    data["total_volume_eth"] = round(data["total_volume_eth"], 5)

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

@router.get("/")
async def test(filter: AxieSalesSearch):
    data = await get_all_data(filter)
    print(len(data))