from django.shortcuts import render, get_object_or_404
from orders.models import Order
import plotly.express as px
import pandas as pd
from ml.risk_engine import calculate_risk


def home(request):

    total_orders = Order.objects.count()

    delivered = Order.objects.filter(
        final_status__iexact="DELIVERED"
    ).count()

    rto = Order.objects.filter(
        final_status__iexact="RTO"
    ).count()

    rto_rate = round((rto / total_orders) * 100, 2)

    estimated_loss = rto * 170

    recent_orders = Order.objects.all()[:20]

    context = {
        "total_orders": total_orders,
        "delivered": delivered,
        "rto": rto,
        "rto_rate": rto_rate,
        "estimated_loss": estimated_loss,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/home.html",
        context,
    )


def orders_list(request):

    query = request.GET.get("q", "")

    status = request.GET.get(
        "status",
        ""
    )

    source = request.GET.get(
        "source",
        ""
    )

    orders = Order.objects.all()

    if query:

        orders = orders.filter(
            order_id__icontains=query
        )

    if status:

        orders = orders.filter(
            final_status__iexact=status
        )

    if source:

        orders = orders.filter(
            utm_source__icontains=source
        )

    context = {
        "orders": orders,
        "query": query,
        "status": status,
        "source": source,
    }

    return render(
        request,
        "dashboard/orders.html",
        context,
    )


def order_detail(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        order_id=order_id
    )

    risk = calculate_risk(order)

    if risk < 30:

        action = "Ship As Is"

    elif risk < 55:

        action = (
            "Confirm via WhatsApp"
        )

    elif risk < 75:

        action = (
            "Nudge To Prepaid"
        )

    else:

        action = (
            "Hold / Cancel"
        )

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order,
            "risk": risk,
            "action": action
        }
    )


def analytics(request):

    df = pd.read_csv("data/orders_sample.csv")

    status_counts = (
        df["final_status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    pie = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Delivered vs RTO Orders"
    )

    pie_html = pie.to_html(
        full_html=False
    )

    return render(
        request,
        "dashboard/analytics.html",
        {
            "pie_chart": pie_html
        }
    )


def predict(request):

    risk = None
    action = None

    if request.method == "POST":

        order_value = float(
            request.POST.get(
                "order_value",
                0
            )
        )

        prior_orders = int(
            request.POST.get(
                "prior_orders",
                0
            )
        )

        prior_rto = int(
            request.POST.get(
                "prior_rto",
                0
            )
        )

        source = request.POST.get(
            "source",
            ""
        )

        risk = 0

        risk += prior_rto * 25

        if prior_orders == 0:
            risk += 20

        if order_value > 1000:
            risk += 15

        elif order_value > 700:
            risk += 10

        if source in [
            "meta_ads",
            "google_ads"
        ]:
            risk += 10

        risk = min(
            risk,
            100
        )

        if risk < 30:

            action = (
                "Ship As Is"
            )

        elif risk < 55:

            action = (
                "WhatsApp Confirmation"
            )

        elif risk < 75:

            action = (
                "Nudge To Prepaid"
            )

        else:

            action = (
                "Hold / Cancel"
            )

    return render(
        request,
        "dashboard/predict.html",
        {
            "risk": risk,
            "action": action
        }
    )


def founder(request):

    return render(
        request,
        "dashboard/founder.html"
    )


def whatsapp(request):

    return render(
        request,
        "dashboard/whatsapp.html"
    )

def customer_history(
    request,
    name
):

    orders = Order.objects.filter(
        customer_name=name
    )

    total_orders = orders.count()

    delivered = (
        orders.filter(
            final_status__iexact="DELIVERED"
        ).count()
    )

    rto = (
        orders.filter(
            final_status__iexact="RTO"
        ).count()
    )

    total_value = sum(
        [
            x.order_value
            for x in orders
        ]
    )

    avg_value = 0

    if total_orders > 0:

        avg_value = round(
            total_value / total_orders,
            2
        )

    rto_rate = 0

    if total_orders > 0:

        rto_rate = round(
            (rto / total_orders) * 100,
            2
        )

    if rto_rate < 10:

        customer_grade = "Trusted Customer"

        recommendation = (
            "Ship Immediately"
        )

    elif rto_rate < 30:

        customer_grade = "Medium Risk"

        recommendation = (
            "WhatsApp Confirmation Recommended"
        )

    else:

        customer_grade = "High Risk"

        recommendation = (
            "Prepaid or Hold Order"
        )

    context = {

        "name": name,

        "orders": orders,

        "total_orders": total_orders,

        "delivered": delivered,

        "rto": rto,

        "rto_rate": rto_rate,

        "total_value": total_value,

        "avg_value": avg_value,

        "customer_grade": customer_grade,

        "recommendation": recommendation

    }

    return render(
        request,
        "dashboard/customer.html",
        context
    )


def pincode_detail(
    request,
    pincode
):

    orders = Order.objects.filter(
        pincode=pincode
    )

    total_orders = orders.count()

    delivered = (
        orders.filter(
            final_status__iexact="DELIVERED"
        ).count()
    )

    rto = (
        orders.filter(
            final_status__iexact="RTO"
        ).count()
    )

    rto_rate = 0

    if total_orders > 0:

        rto_rate = round(
            (rto / total_orders) * 100,
            2
        )

    if rto_rate < 10:

        risk_level = "Low"

        recommendation = (
            "Safe Area - Ship Normally"
        )

    elif rto_rate < 25:

        risk_level = "Medium"

        recommendation = (
            "Confirmation Recommended"
        )

    else:

        risk_level = "High"

        recommendation = (
            "Prepaid or Hold Order"
        )

    context = {

        "pincode": pincode,

        "orders": orders,

        "total_orders": total_orders,

        "delivered": delivered,

        "rto": rto,

        "rto_rate": rto_rate,

        "risk_level": risk_level,

        "recommendation": recommendation,

    }

    return render(
        request,
        "dashboard/pincode.html",
        context
    )


def courier_detail(
    request,
    courier
):

    orders = Order.objects.filter(
        courier=courier
    )

    total_orders = orders.count()

    delivered = (
        orders.filter(
            final_status__iexact="DELIVERED"
        ).count()
    )

    rto = (
        orders.filter(
            final_status__iexact="RTO"
        ).count()
    )

    rto_rate = 0

    if total_orders > 0:

        rto_rate = round(
            (rto / total_orders) * 100,
            2
        )

    total_revenue = sum(
        [
            o.order_value
            for o in orders
        ]
    )

    if rto_rate < 10:

        recommendation = (
            "Excellent Courier Performance"
        )

    elif rto_rate < 25:

        recommendation = (
            "Monitor Courier Performance"
        )

    else:

        recommendation = (
            "High RTO Courier Risk"
        )

    return render(
        request,
        "dashboard/courier.html",
        {
            "courier": courier,
            "orders": orders,
            "total_orders": total_orders,
            "delivered": delivered,
            "rto": rto,
            "rto_rate": rto_rate,
            "total_revenue": total_revenue,
            "recommendation": recommendation
        }
    )

def whatsapp_simulator(request):

    message = None
    outcome = None
    color = None

    if request.method == "POST":

        response = request.POST.get(
            "response"
        )

        if response == "yes":

            outcome = (
                "Order Confirmed"
            )

            message = (
                "Customer confirmed the order. Ship normally."
            )

            color = "#22c55e"

        elif response == "no":

            outcome = (
                "Order Cancelled"
            )

            message = (
                "Customer rejected the order."
            )

            color = "#ef4444"

        else:

            outcome = (
                "No Response"
            )

            message = (
                "Send reminder or prepaid incentive."
            )

            color = "#f59e0b"

    return render(
        request,
        "dashboard/whatsapp.html",
        {
            "message": message,
            "outcome": outcome,
            "color": color
        }
    )
