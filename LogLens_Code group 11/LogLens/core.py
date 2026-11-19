"""Component 2 - Core logic and functions (Member 2)."""
import datetime as dt

LEVELS = ("INFO", "WARNING", "ERROR")
TS_FORMAT = "%Y-%m-%d %H:%M:%S"

def parse_line(line):
    """Parse 'time | level | module | ip | message'. Return dict, or None if corrupt."""
    parts = [p.strip() for p in line.strip().split("|")]
    if len(parts) != 5:
        return None
    ts, level, module, ip, message = parts
    try:
        when = dt.datetime.strptime(ts, TS_FORMAT)
    except ValueError:
        return None
    level = classify(level)
    if level is None or not module or not message:
        return None
    return {"timestamp": when, "level": level, "module": module, "ip": ip, "message": message}

def classify(level_text):
    """Return a valid level (INFO / WARNING / ERROR) or None."""
    level = level_text.strip().upper()
    return level if level in LEVELS else None

def filter_logs(entries, level=None, date=None, keyword=None):
    """Apply any combination of level, date (YYYY-MM-DD) and keyword filters."""
    result = entries
    if level:
        result = [e for e in result if e["level"] == level.upper()]
    if date:
        result = [e for e in result if e["timestamp"].strftime("%Y-%m-%d") == date]
    if keyword:
        k = keyword.lower()
        result = [e for e in result if k in e["message"].lower()]
    return result

def health_score(entries):
    """100 minus the weighted error (1.0) and warning (0.4) rate, as a percentage."""
    if not entries:
        return 100.0
    errors = sum(1 for e in entries if e["level"] == "ERROR")
    warnings = sum(1 for e in entries if e["level"] == "WARNING")
    return round(100 - (errors + 0.4 * warnings) / len(entries) * 100, 1)

def health_label(score):
    return "Healthy" if score >= 90 else "Needs attention" if score >= 75 else "Critical"
