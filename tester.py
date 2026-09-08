from log_parser import parse_log_file
entries, skipped = parse_log_file("sample_access.log")
print(f"Parsed {len(entries)} entries")
print(f"Skipped {skipped} entries")

# Analyze the entire log file
for entry in entries:
    if entry.status >= 500:
        print(f"Server error at {entry.timestamp}: {entry.path}")

# Find all request from suspicious IPs
for entry in entries:
    if entry.ip == "192.168.1.99":
        print(f"Anomalous: {entry.method} {entry.path} - {entry.status}")