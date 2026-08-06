import re
import pandas as pd

def tokenize_url(url):
    return re.split(r'[\/\.\-\_\?\=\&]', url.lower())

def extract_features(url):
    return pd.Series({
        "url_length": len(url),
        "digit_count": sum(c.isdigit() for c in url),
        "has_https": 1 if url.startswith("https") else 0,
        "has_ip": 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        "num_dots": url.count('.'),
        "num_hyphens": url.count('-'),
    })