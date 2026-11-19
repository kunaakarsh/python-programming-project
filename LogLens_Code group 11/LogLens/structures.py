"""Component 3 - Data structures (Member 3)."""
from collections import Counter

def level_counts(entries):
    """Counter (dict subclass): level -> number of entries."""
    return Counter(e["level"] for e in entries)

def unique_ips(entries):
    """Set of distinct client IP addresses."""
    return {e["ip"] for e in entries}

def module_level_table(entries):
    """Nested dict: module -> level -> count."""
    table = {}
    for e in entries:
        table.setdefault(e["module"], {"INFO": 0, "WARNING": 0, "ERROR": 0})[e["level"]] += 1
    return table

def corrupt_record(line_number, raw_text):
    """Tuple (immutable) describing one corrupt line."""
    return (line_number, raw_text)

def top_n(counter, n=5):
    return counter.most_common(n)

def error_messages(entries):
    return Counter(e["message"] for e in entries if e["level"] == "ERROR")

def errors_per_hour(entries):
    """dict: hour (0-23) -> ERROR count, using a dict comprehension."""
    c = Counter(e["timestamp"].hour for e in entries if e["level"] == "ERROR")
    return {h: c.get(h, 0) for h in range(24)}
