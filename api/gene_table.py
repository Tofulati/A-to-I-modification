import json
import os
import pickle
import numpy as np
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = "database"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        gene = query.get("gene_name", [None])[0]
        sample = query.get("sample", [None])[0]

        if not gene or not sample:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "gene_name and sample required"}).encode()
            )
            return

        pkl_path = os.path.join(
            BASE_DIR,
            f"{sample}_per_read_pkls",
            f"{gene}_per_read.pkl"
        )

        if not os.path.exists(pkl_path):
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "Gene not found"}).encode()
            )
            return

        try:
            with open(pkl_path, "rb") as f:
                df = pickle.load(f)

            # Convert numpy types to native Python
            records = df.to_dict(orient="records")
            for rec in records:
                for k, v in rec.items():
                    if isinstance(v, (np.integer, np.floating)):
                        rec[k] = v.item()
                    elif isinstance(v, np.ndarray):
                        rec[k] = v.tolist()  # Convert arrays to lists

            # Stream JSON to avoid huge memory usage
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(b"[")
            for i, rec in enumerate(records):
                if i > 0:
                    self.wfile.write(b",")
                self.wfile.write(json.dumps(rec, ensure_ascii=False).encode("utf-8"))
            self.wfile.write(b"]")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "error": str(e),
                    "type": type(e).__name__
                }).encode()
            )
