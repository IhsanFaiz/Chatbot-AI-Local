import socket
import urllib.request

OFFLINE_WARNING_MESSAGE = (
    "⚠️ Internet connection is unavailable.\n"
    "Please enable your internet connection to use Web Search."
)

def check_internet_connection(host="8.8.8.8", port=53, timeout=2.0) -> bool:
    """
    Check if the local machine has an active internet connection.
    Attempts a rapid TCP socket connection to a public DNS server,
    with a fallback HTTP HEAD request if needed.
    Never throws an unhandled exception; returns True or False.
    """
    # 1. Quick socket test to 8.8.8.8 or 1.1.1.1 (DNS port 53)
    dns_targets = [(host, port), ("1.1.1.1", 53)]
    for target_host, target_port in dns_targets:
        try:
            with socket.create_connection((target_host, target_port), timeout=timeout):
                return True
        except (socket.timeout, OSError):
            continue

    # 2. Secondary fallback via lightweight HTTP request
    try:
        req = urllib.request.Request(
            "https://www.cloudflare.com",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status in (200, 301, 302):
                return True
    except Exception:
        pass

    return False
