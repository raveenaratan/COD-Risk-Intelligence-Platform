import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("data/orders_sample.csv")

df["target"] = (
    df["final_status"]
    .astype(str)
    .str.upper()
    .eq("RTO")
    .astype(int)
)

features = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto",
    "utm_source",
    "courier",
    "state"
]

data = df[features].copy()

for col in ["utm_source", "courier", "state"]:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])

X_train, X_test, y_train, y_test = train_test_split(
    data,
    df["target"],
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("Accuracy:", accuracy)

joblib.dump(model, "ml/model.pkl")

print("Model Saved Successfully")
