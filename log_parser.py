"""
Parses Combined Log Format access log lines into structured records.
"""
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Named groups format
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
)

TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"


@dataclass
class LogEntry:
    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int
    size: int


def parse_line(line: str) -> Optional[LogEntry]:
    """
    Returns a LogEntry, or None if the line doesn't match the expected format.
    None lets the script continue once a malformed log line is found.
    """
    match = LOG_PATTERN.match(line)
    if not match:
        return None

    try:
        return LogEntry(
            ip=match.group("ip"),
            timestamp=datetime.strptime(match.group("timestamp"), TIMESTAMP_FORMAT),
            method=match.group("method"),
            path=match.group("path"),
            status=int(match.group("status")),
            size=int(match.group("size")) if match.group("size") != "-" else 0,
        )
    except ValueError:
        return None


def parse_log_file(path: str) -> tuple[list[LogEntry], int]:
    """
    Returns (entries, skipped_count).
    Skipping is counted to prevent malinformed log lines missing from final log output.
    """
    entries = []
    skipped = 0
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = parse_line(line)
            if entry:
                entries.append(entry)
            else:
                skipped += 1
    return entries, skipped