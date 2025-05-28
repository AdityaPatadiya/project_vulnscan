# plugins/xss.py
import requests
import urllib.parse
import json

def load_payloads():
    with open("data/payloads.json", "r") as f:
        payloads = json.load(f)
    return payloads.get("xss", [])

def is_vulnerable(response_text, payload):
    return payload in response_text

def scan(url):
    payloads = load_payloads()
    parsed_url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed_url.query)

    if not query:
        return  # No parameters to inject

    for payload in payloads:
        new_query = {param: payload for param in query}
        encoded_query = urllib.parse.urlencode(new_query, doseq=True)
        test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{encoded_query}"

        try:
            response = requests.get(test_url, timeout=5)
            if is_vulnerable(response.text, payload):
                print(f"[!] Possible XSS vulnerability: {test_url}")
        except requests.RequestException:
            continue
