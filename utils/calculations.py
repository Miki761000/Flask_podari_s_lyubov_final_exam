def calculate_quantity_and_price(data, product):
    quantities = product.product_quantity
    quantities_new = data["product_quantity"]
    price = product.product_delivery_price
    price_new = data["product_delivery_price"]
    price_last = round(
        (price * quantities + price_new * quantities_new)
        / (quantities + quantities_new),
        2,
    )
    if quantities + quantities_new < 0:
        return "Not enough quantity"
    data["product_quantity"] = quantities + quantities_new
    data["product_delivery_price"] = price_last
    return data
