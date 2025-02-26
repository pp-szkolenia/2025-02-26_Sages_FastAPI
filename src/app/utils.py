def get_item_by_id(items_list, item_id):
    for item in items_list:
        if item["id"] == item_id:
            return item
    return None

def get_item_index_by_id(items_list, item_id):
    for i, item in enumerate(items_list):
        if item["id"] == item_id:
            return i
    return None
