import requests
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def scan(url):
    try:
        with open("data/payloads.json", "r") as f:
            payloads = json.load(f)["XSS_payloads"]
    except Exception as e:
        print(f"[!] Error loading XSS payloads: {e}")
        return

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        return  # No parameters to inject

    for param in query_params:
        original_value = query_params[param][0]
        for payload in payloads:
            query_params[param] = payload
            new_query = urlencode(query_params, doseq=True)
            test_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment
            ))

            try:
                response = requests.get(test_url, timeout=5)
                if payload.lower() in response.text.lower():
                    print(f"[!] Possible XSS vulnerability found at: {test_url}")
            except requests.RequestException as e:
                print(f"[!] Request error on: {test_url} -> {e}")
