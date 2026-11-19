"""Component 6 - Visualisation and report (Member 6)."""
import matplotlib
matplotlib.use("Agg")                      # save to file; works without a display
import matplotlib.pyplot as plt
import analysis as an

BLUE, GREEN, AMBER, RED = "#0B5CA8", "#1FB36B", "#F2A33A", "#D64550"

def _hourly(ax, df):
    eh = an.errors_by_hour(df)
    ax.plot(eh.index, eh.values, color=RED, marker="o", lw=2, ms=4)
    ax.fill_between(eh.index, eh.values, color=RED, alpha=.12)
    pk = eh.idxmax()
    ax.annotate(f"peak {pk}:00 ({eh.max()})", (pk, eh.max()), (pk + 2, eh.max() * .8), arrowprops=dict(arrowstyle="->"), fontsize=8)
    ax.set_title("Errors per hour of day", fontweight="bold"); ax.set_xlabel("Hour (0-23)"); ax.set_ylabel("ERROR count"); ax.set_xticks(range(0, 24, 4))

def _levels(ax, df):
    c = df.level.value_counts().reindex(["INFO", "WARNING", "ERROR"])
    bars = ax.bar(c.index, c.values, color=[GREEN, AMBER, RED]); ax.bar_label(bars, fontsize=8, padding=2)
    ax.set_ylim(0, c.max() * 1.15); ax.set_title("Entries by log level", fontweight="bold"); ax.set_ylabel("Count")

def _modules(ax, df):
    m = an.errors_by_module(df).sort_values()
    bars = ax.barh(m.index, m.values, color=BLUE); ax.bar_label(bars, fontsize=8, padding=2)
    ax.set_xlim(0, m.max() * 1.15); ax.set_title("Errors per module", fontweight="bold"); ax.set_xlabel("ERROR count")

def _daily(ax, df):
    d = an.daily_levels(df); d.index = [x.strftime("%d %b") for x in d.index]
    d.plot(ax=ax, color=[GREEN, AMBER, RED], lw=2); ax.legend(fontsize=7, frameon=False, ncol=3, loc="upper center")
    ax.set_ylim(0, d.values.max() * 1.25); ax.set_title("Daily volume", fontweight="bold"); ax.set_xlabel("")

def make_charts(df, folder="."):
    plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False})
    files = []
    for name, fn in [("chart1_hourly_errors.png", _hourly), ("chart2_level_counts.png", _levels)]:
        fig, ax = plt.subplots(figsize=(6, 4.2)); fn(ax, df); fig.tight_layout()
        fig.savefig(f"{folder}/{name}", dpi=200); plt.close(fig); files.append(name)
    fig, axs = plt.subplots(2, 2, figsize=(6.4, 4.6))
    for ax, fn in zip(axs.flat, (_hourly, _levels, _modules, _daily)):
        fn(ax, df); ax.title.set_fontsize(10); ax.tick_params(labelsize=8)
        ax.xaxis.label.set_size(8); ax.yaxis.label.set_size(8)
    fig.suptitle("LogLens health dashboard", fontweight="bold", fontsize=12); fig.tight_layout()
    fig.savefig(f"{folder}/chart3_dashboard.png", dpi=200); plt.close(fig); files.append("chart3_dashboard.png")
    return files
