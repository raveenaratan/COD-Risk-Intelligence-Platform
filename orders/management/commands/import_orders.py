from django.core.management.base import BaseCommand
from orders.models import Order
import pandas as pd


class Command(BaseCommand):
    help = "Import Orders CSV"

    def handle(self, *args, **kwargs):

        df = pd.read_csv("data/orders_sample.csv")

        for _, row in df.iterrows():

            Order.objects.create(
                order_id=str(row['order_id']),
                order_datetime=str(row['order_datetime']),
                customer_name=str(row['customer_name']),
                phone=str(row['phone']),
                address=str(row['address']),
                city=str(row['city']),
                state=str(row['state']),
                pincode=str(row['pincode']),
                order_value=float(row['order_value']),
                items=str(row['items']),
                num_items=int(row['num_items']),
                customer_prior_orders=int(row['customer_prior_orders']),
                customer_prior_rto=int(row['customer_prior_rto']),
                utm_source=str(row['utm_source']),
                courier=str(row['courier']),
                payment_method=str(row['payment_method']),
                final_status=str(row['final_status'])
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(df)} orders successfully"
            )
        )
