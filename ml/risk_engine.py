def calculate_risk(order):

    risk = 0

    # Previous RTO History
    risk += order.customer_prior_rto * 25

    # New Customer Risk
    if order.customer_prior_orders == 0:
        risk += 20

    # High Value Orders
    if order.order_value > 1000:
        risk += 15

    # Medium Orders
    elif order.order_value > 700:
        risk += 10

    # Source Risk
    risky_sources = [
        "meta_ads",
        "google_ads"
    ]

    if (
        str(order.utm_source)
        .lower()
        in risky_sources
    ):
        risk += 10

    risk = min(risk, 100)

    return risk
