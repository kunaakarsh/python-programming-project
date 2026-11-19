# LogLens - Server Log File Analyzer and Error Monitor
Group 11 | B.Tech CSE (Data Science) | Python Programming Group Project

## Run
    pip install pandas matplotlib
    python main.py          # option 8 generates server.log if you do not have one

## Files (one component per member)
| File | Component |
|---|---|
| menu.py | Menu, input and validation |
| core.py | Core logic: parse_line, classify, filter_logs, health_score |
| structures.py | Counter, unique-IP set, corrupt-line tuples, nested module/level table |
| file_handler.py | Read log line by line, write JSON/CSV, corrupt-line handling, sample data generator |
| analysis.py | pandas: errors per hour/module, top messages, busiest hours |
| visuals.py | 3 charts incl. a 2x2 subplot dashboard |
| main.py | Integrates everything into one menu-driven program |

Log format: `YYYY-MM-DD HH:MM:SS | LEVEL | module | ip | message`
