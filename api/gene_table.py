import json
import os
import pickle
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
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "Gene not found"}).encode()
            )
            return

        try:
            with open(pkl_path, "rb") as f:
                df = pickle.load(f)

            records = df.to_dict(orient="records")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(records).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "error": str(e),
                    "type": type(e).__name__
                }).encode()
            )

        records = df.to_dict(orient="records")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(records).encode())
