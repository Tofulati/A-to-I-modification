import json
import os
import pickle
import numpy as np
import pandas as pd
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = "database"

def extract_mean(val):
    match = re.match(r"([0-9.]+)", str(val))
    return float(match.group(1)) if match else None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        gene = query.get("gene_name", [None])[0]
        
        if not gene:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "gene_name required"}).encode()
            )
            return
        
        # Load from processed_gene directory
        pkl_path = os.path.join(BASE_DIR, "processed_gene", f"{gene}.pkl")
        
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
            
            # Extract means from the data
            df["MR01_1_mean"] = df["MR01_1"].apply(extract_mean)
            df["MR01_2_mean"] = df["MR01_2"].apply(extract_mean)
            
            # Convert to records
            records = df.to_dict(orient="records")
            
            # Convert numpy types to native Python
            for rec in records:
                for k, v in rec.items():
                    if isinstance(v, (np.integer, np.floating)):
                        rec[k] = v.item()
                    elif isinstance(v, np.ndarray):
                        rec[k] = v.tolist()
                    elif pd.isna(v):
                        rec[k] = None
            
            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "public, max-age=3600")
            self.end_headers()
            self.wfile.write(json.dumps(records, ensure_ascii=False).encode("utf-8"))
            
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