import json
import os

from flask import current_app


def get_json_data():
    filename = "com_list.JSON"
    data_path = os.path.join(current_app.root_path, "com_list/data", filename)

    # デバッグ用にファイルパスを出力
    # print(f"Loading JSON file from: {data_path}")

    with open(data_path) as f:
        data = json.load(f)
    return data


def filter_products_by_int(products, name: str, min: int, max: int):
    filtered_products = []
    for product in products:
        try:
            value = int(product[name])
            if min <= value <= max:
                filtered_products.append(product)
        except (ValueError, TypeError):
            # エラーが発生した場合は例外を発生させる
            raise ValueError(
                f"Product '{product}' has a non-integer value for '{name}'"
            )
    return filtered_products