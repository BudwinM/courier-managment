import re
import os

files = [
    "api-gateway/app.py",
    "billing-service/app.py",
    "branch-service/app.py",
    "orders-service/app.py",
    "tracking-service/app.py",
    "delivery-service/app.py",
    "customer-service/app.py",
]

for f in files:
    with open(f, "r", encoding="utf-8") as r:
        c = r.read()
    
    if '"hide_top_bar"' not in c:
        if f == "api-gateway/app.py":
            c = re.sub(r'(config={)', r'\1\n    "hide_top_bar": True,\n    "footer_text": "<style>.swagger-ui .wrapper .clear { display: none !important; }</style>",', c)
        else:
            c = re.sub(r'(swagger_config = {)', r'\1\n    "hide_top_bar": True,\n    "footer_text": "<style>.swagger-ui .wrapper .clear { display: none !important; }</style>",', c)
        
        with open(f, "w", encoding="utf-8") as w:
            w.write(c)
