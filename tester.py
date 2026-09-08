from log_parser import parse_log_file
entries, skipped = parse_log_file("sample_access.log")
print(f"Parsed {len(entries)} entries, skipped {skipped}")
print(entries[0])