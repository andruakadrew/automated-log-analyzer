"""
Example of a Combined Log Format access log for testing the analyzer.
Includes normal traffic baseline, single injected spike, and a cluster of errors.
"""
import random
from datetime import datetime, timedelta

IPS = [f"192.168.1.{i}" for i in range(1, 20)]
PATHS = ["/index.html", "/login", "/api/users", "/api/orders", "/static/style.css", "/favicon.ico"]
METHODS = ["GET", "GET", "GET", "POST"]  # weighted towards GET
STATUSES = [200, 200, 200, 200, 200, 301, 404, 500]  # mostly consistent, with some slight disruptions

def make_line(ts: datetime, ip: str, method: str, path: str, status: int) -> str:
    size = random.randint(200, 5000)
    return (f'{ip} - - [{ts.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
            f'"{method} {path} HTTP/1.1" {status} {size} "-" "Mozilla/5.0"')

def main():
    start = datetime(2026, 10, 10, 13, 0, 0)
    lines = []
    # 3 requests per minute for 30 minutes.
    for minute in range(30):
        for _ in range(random.randint(2, 4)):
            ts = start + timedelta(minutes=minute, seconds=random.randint(0, 59))
            lines.append(make_line(ts, random.choice(IPS), random.choice(METHODS),
                                    random.choice(PATHS), random.choice(STATUSES)))

    # Injection spike at minute 15 for API request.
    spike_minute = start + timedelta(minutes=15)
    for _ in range(60):
        ts = spike_minute + timedelta(seconds=random.randint(0, 59))
        lines.append(make_line(ts, random.choice(IPS), "GET", "/api/orders", 200))

    # Injected error cluster from a single IP.
    error_minute = start + timedelta(minutes=22)
    for _ in range(8):
        ts = error_minute + timedelta(seconds=random.randint(0, 59))
        lines.append(make_line(ts, "192.168.1.99", "POST", "/login", 401))

    lines.sort()
    with open("sample_access.log", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} lines to sample_access.log")


if __name__ == "__main__":
    main()