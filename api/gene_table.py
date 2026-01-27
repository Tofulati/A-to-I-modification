import json
import pickle
import os

BASE_DIR = "database"

def handler(request):
    q = request.get("query", {})
    gene = q.get("gene_name")
    sample = q.get("sample")

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
            "statusCode": 400,
            "body": json.dumps({"error": "Gene not found"})  
        }

    with open(pkl_path, "rb") as f:
        df = pickle.load(f)

    records = df.to_dict(orient="records")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(records)
    }
