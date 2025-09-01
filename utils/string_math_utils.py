def change_data_format(data: list):
    new_list = []
    for coin in data:
        coin_info = (coin['id'], coin['symbol'], coin['name'])
        new_list.append(coin_info)
    return new_list
