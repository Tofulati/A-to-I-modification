import json
import pickle
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "database")

def handler(request):
    query = request.get("queryStringParameters") or {}
    gene = query.get("gene_name")
    sample = query.get("sample")

    if not gene or not sample:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "gene_name and sample required"})
        }

    pkl_path = os.path.join(
        BASE_DIR,
        f"{sample}_per_read_pkls",
        f"{gene}_per_read.pkl"
    )

    if not os.path.exists(pkl_path):
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Gene not found"})
        }

    with open(pkl_path, "rb") as f:
        df = pickle.load(f)

    records = df.to_dict(orient="records")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(records)
    }
