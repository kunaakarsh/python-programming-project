"""Component 4 - Files and error handling (Member 4)."""
import csv, json, random, datetime as dt
from core import parse_line
from structures import corrupt_record

def load_log(path):
    """Read a log line by line. Return (entries, corrupt_lines). Never crashes on bad input."""
    entries, corrupt = [], []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    corrupt.append(corrupt_record(n, "(blank line)"))
                    continue
                rec = parse_line(line)
                if rec:
                    entries.append(rec)
                else:
                    corrupt.append(corrupt_record(n, line.strip()))
    except FileNotFoundError:
        print(f"  File not found: {path}")
    except PermissionError:
        print(f"  No permission to read: {path}")
    return entries, corrupt

def save_json(summary, path="summary.json"):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, default=str)
        return True
    except OSError as e:
        print(f"  Could not write {path}: {e}")
        return False

def save_csv(entries, path="parsed_logs.csv"):
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "level", "module", "ip", "message"])
            for e in entries:
                w.writerow([e["timestamp"].strftime("%Y-%m-%d %H:%M:%S"), e["level"], e["module"], e["ip"], e["message"]])
        return True
    except OSError as e:
        print(f"  Could not write {path}: {e}")
        return False

def save_corrupt(corrupt, path="corrupt_lines.csv"):
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["line_number", "raw_text"]); w.writerows(corrupt)
        return True
    except OSError as e:
        print(f"  Could not write {path}: {e}")
        return False

# ---- realistic sample data generator (random module) ----
_MODULES = {"auth": (3, ["Login failed: invalid token", "Session expired for user", "Password retry limit reached"]),
            "database": (4, ["Connection timeout to db-primary", "Deadlock detected on orders table", "Slow query exceeded 2000 ms"]),
            "api": (5, ["Upstream service returned 503", "Request payload validation failed", "Rate limit exceeded for client"]),
            "payment": (2, ["Gateway timeout while charging card", "Payment callback signature mismatch"]),
            "cache": (1, ["Redis eviction rate high", "Cache miss ratio above threshold"])}
_INFO = ["Request completed in {} ms", "Health check passed", "User session started", "Cache refreshed", "Scheduled job finished"]
_WARN = ["High memory usage 85%", "Retrying request", "Disk usage above 80%", "Response time degraded"]
_HOUR_W = [1,1,1,1,1,2,3,5,8,10,9,8,7,8,9,10,9,8,6,5,4,3,2,1]

def generate_sample_log(path="server.log", n=1200, seed=11, corrupt=14):
    random.seed(seed)
    names = list(_MODULES); weights = [_MODULES[m][0] for m in names]
    ips = [f"10.0.{random.randint(1,6)}.{random.randint(2,60)}" for _ in range(25)]
    base = dt.date(2026, 11, 10); lines = []
    for _ in range(n):
        d = base + dt.timedelta(days=random.randint(0, 6))
        h = random.choices(range(24), _HOUR_W)[0]
        if d.day == 13 and h in (14, 15) and random.random() < .5:
            lvl = "ERROR"                      # simulated incident window
        else:
            lvl = random.choices(["INFO", "WARNING", "ERROR"], [72, 15, 13])[0]
        m = random.choices(names, weights)[0]
        msg = (random.choice(_INFO).format(random.randint(20, 900)) if lvl == "INFO"
               else random.choice(_WARN) if lvl == "WARNING" else random.choice(_MODULES[m][1]))
        t = dt.datetime(d.year, d.month, d.day, h, random.randint(0, 59), random.randint(0, 59))
        lines.append(f"{t:%Y-%m-%d %H:%M:%S} | {lvl} | {m} | {random.choice(ips)} | {msg}")
    lines.sort()
    for i in random.sample(range(len(lines)), corrupt):
        lines[i] = random.choice(["@@##corrupt###", "2026-11-1x 99:99:99 | ??? | broken", "", "----- truncated entry ----"])
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path
