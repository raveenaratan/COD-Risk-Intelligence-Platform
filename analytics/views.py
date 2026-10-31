import pandas as pd
import json

from django.shortcuts import render


def analytics_dashboard(request):

    try:

        df = pd.read_csv(
            "data/orders_sample.csv"
        )

        original_count = len(df)

        df["order_id"] = (
            df["order_id"]
            .astype(str)
            .str.strip()
        )

        df["final_status"] = (
            df["final_status"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        duplicate_count = (
            original_count -
            len(
                df.drop_duplicates(
                    subset=["order_id"]
                )
            )
        )

        df = df.drop_duplicates(
            subset=["order_id"],
            keep="first"
        )

        total_orders = len(df)

        delivered_count = len(
            df[
                df["final_status"] ==
                "DELIVERED"
            ]
        )

        rto_count = len(
            df[
                df["final_status"] ==
                "RTO"
            ]
        )

        transit_count = len(
            df[
                df["final_status"] ==
                "IN_TRANSIT"
            ]
        )

        resolved_count = (
            delivered_count +
            rto_count
        )

        if resolved_count > 0:

            delivered_percentage = round(
                delivered_count /
                resolved_count * 100,
                2
            )

            rto_percentage = round(
                rto_count /
                resolved_count * 100,
                2
            )

        else:

            delivered_percentage = 0
            rto_percentage = 0

        estimated_rto_loss = round(
            rto_count * 169.40,
            2
        )

        status_chart_json = {
            "labels": [
                "Delivered",
                "RTO"
            ],
            "values": [
                delivered_count,
                rto_count
            ]
        }

        context = {

            "total_orders":
            total_orders,

            "delivered_count":
            delivered_count,

            "rto_count":
            rto_count,

            "transit_count":
            transit_count,

            "duplicate_count":
            duplicate_count,

            "delivered_percentage":
            delivered_percentage,

            "rto_percentage":
            rto_percentage,

            "estimated_rto_loss":
            estimated_rto_loss,

            "status_chart_json":
            json.dumps(
                status_chart_json
            ),
        }

        return render(
            request,
            "analytics/dashboard.html",
            context
        )

    except Exception as e:

        return render(
            request,
            "analytics/dashboard.html",
            {
                "error": str(e)
            }
        )

# Create your views here.
