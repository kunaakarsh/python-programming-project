"""LogLens - Server Log File Analyzer and Error Monitor.
Run:  python main.py        (put server.log next to it, or use option 8 to generate one)
"""
import menu, core, structures, file_handler, analysis, visuals

def main():
    entries, corrupt = [], []
    while True:
        menu.show_menu()
        ch = menu.get_choice()
        try:
            if ch == "0":
                print("Goodbye!"); break
            if ch == "8":
                n = file_handler.generate_sample_log(menu.get_path("server.log"))
                print(f"  Sample log written to {n}"); continue
            if ch == "1":
                new_e, new_c = file_handler.load_log(menu.get_path())
                if new_e:                      # keep old data if the new load failed
                    entries, corrupt = new_e, new_c
                    print(f"  Parsed {len(entries)} entries, skipped {len(corrupt)} corrupt lines")
                else:
                    print("  No valid entries loaded; previous data (if any) kept.")
                continue
            if not entries:
                print("  Load a log file first (option 1)."); continue

            if ch == "2":
                res = core.filter_logs(entries, level=menu.get_level(), date=menu.get_date())
                menu.show_entries(res)
            elif ch == "3":
                kw = menu.get_keyword()
                menu.show_entries(core.filter_logs(entries, keyword=kw)) if kw else print("  Nothing to search.")
            elif ch == "4":
                score = core.health_score(entries)
                print("\n  Levels      :", dict(structures.level_counts(entries)))
                print("  Unique IPs  :", len(structures.unique_ips(entries)))
                print("  Corrupt     :", len(corrupt), "lines skipped")
                print(f"  Health score: {score}/100 ({core.health_label(score)})")
            elif ch == "5":
                df = analysis.to_dataframe(entries)
                print("\n  Top error messages:"); print(analysis.top_error_messages(df).to_string())
                print("\n  Errors per module:"); print(analysis.errors_by_module(df).to_string())
                print("\n  Busiest hours (entries):"); print(analysis.busiest_hours(df).to_string())
            elif ch == "6":
                df = analysis.to_dataframe(entries)
                ok = file_handler.save_json(analysis.build_summary(df, core.health_score(entries)))
                ok &= file_handler.save_csv(entries)
                ok &= file_handler.save_corrupt(corrupt)
                print("  Saved summary.json, parsed_logs.csv, corrupt_lines.csv" if ok else "  Some files could not be saved.")
            elif ch == "7":
                print("  Charts saved:", ", ".join(visuals.make_charts(analysis.to_dataframe(entries))))
        except (ValueError, KeyError) as e:
            print("  Input error:", e)

if __name__ == "__main__":
    main()
