import time


def binary_search(data: list[dict], field: str, target: int) -> int:
    left = 0
    right = len(data)

    while left < right:
        mid = (left + right) // 2
        if data[mid][field] >= target:
            left = mid + 1
        else:
            right = mid
    return left - 1 if left > 0 else left

def format_data_line_graph(raw_data: list[dict], time_unit: str, time_num:int):
    data = {
        "total_sales": 0,
        "total_volume_eth": 0,
        "avg_price_eth": 0,
        "chart": []
    }

    current_time = time.time()
    if time_unit == "hours":
            timeframe_seconds = 3600 * time_num
    elif time_unit == "days":
        timeframe_seconds = 86400 * time_num

    start_time = current_time - timeframe_seconds
    num_buckets = 30
    bucket_size = (current_time - start_time) // 30
    bucket_idx = 0

    # Pre-allocate chart buckets
    for _ in range(num_buckets):
        data["chart"].append({"sales": 0, "volume_eth": 0, "avg_price_eth": 0})

    # Binary search to find the first relevant index
    idx = binary_search(raw_data, "sale_date", start_time)
    if idx <= 0:
        return data

    # Assign each sale to the correct bucket.
    for i in range(idx, -1, -1):
        sale = raw_data[i]
        if sale["sale_date"] < start_time:
            break
        bucket_idx = int((sale["sale_date"] - start_time) // bucket_size)
        if bucket_idx >= num_buckets:
            bucket_idx = num_buckets - 1
        data["chart"][bucket_idx]["sales"] += 1
        data["chart"][bucket_idx]["volume_eth"] += sale["price_eth"]

    # Calculate average and totals
    for bucket in data["chart"]:
        if bucket["sales"] > 0:
            bucket["avg_price_eth"] = round(bucket["volume_eth"] / bucket["sales"], 5)
            data["total_sales"] += bucket["sales"]
            data["total_volume_eth"] += bucket["volume_eth"]

    if data["total_sales"] > 0:
        data["avg_price_eth"] = round(data["total_volume_eth"] / data["total_sales"], 5)
    data["total_volume_eth"] = round(data["total_volume_eth"], 5)
    return data

def format_data_bar_graph(raw_data: list[dict], field: str, field_range: list, time_unit: str, time_num: int):
    current_time = time.time()
    if time_unit == "hours":
            timeframe_seconds = 3600 * time_num
    elif time_unit == "days":
        timeframe_seconds = 86400 * time_num

    data = []

    start_time = current_time - timeframe_seconds
    num_buckets = len(field_range)

    # Binary search to find the first relevant index
    idx = binary_search(raw_data, "sale_date", start_time)
    if idx <= 0:
        return data
    
    # Pre-allocate chart buckets
    for _ in range(num_buckets):
        data.append({field: field_range[_], "sales": 0, "volume_eth": 0, "avg_price_eth": 0})

    hashmap = {}

    # Populate the hashmap
    for i in range(0, idx + 1):
        sale = raw_data[i]
        if sale["sale_date"] < start_time:
            break

        if sale[field] in hashmap:
            hashmap[sale[field]]["sales"] += 1
            hashmap[sale[field]]["volume_eth"] += sale["price_eth"]
        else:
            hashmap[sale[field]] = {"sales": 0, "volume_eth": 0}

    for bucket in data:
        if isinstance(bucket[field], list):
            for f in range(bucket[field][0], bucket[field][1] + 1):
                bucket["sales"] += hashmap[f]["sales"]
                bucket["volume_eth"] += hashmap[f]["volume_eth"]
        else:
            bucket["sales"] += hashmap[bucket[field]]["sales"]
            bucket["volume_eth"] += hashmap[bucket[field]]["volume_eth"]
        bucket["avg_price_eth"] = round(bucket["volume_eth"] / bucket["sales"], 5)
        bucket["volume_eth"] = round(bucket["volume_eth"], 5)

    return data