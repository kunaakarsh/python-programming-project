"""Component 5 - Data analysis with pandas (Member 5)."""
import pandas as pd

def to_dataframe(entries):
    df = pd.DataFrame(entries)
    df["hour"] = df["timestamp"].dt.hour
    df["date"] = df["timestamp"].dt.date
    return df

def errors_by_hour(df):
    err = df[df.level == "ERROR"]
    return err.groupby("hour").size().reindex(range(24), fill_value=0)

def errors_by_module(df):
    return df[df.level == "ERROR"].groupby("module").size().sort_values(ascending=False)

def top_error_messages(df, n=5):
    return df[df.level == "ERROR"]["message"].value_counts().head(n)

def busiest_hours(df, n=3):
    """Hours with the most log traffic (all levels)."""
    return df.groupby("hour").size().sort_values(ascending=False).head(n)

def daily_levels(df):
    return df.groupby(["date", "level"]).size().unstack(fill_value=0).reindex(columns=["INFO", "WARNING", "ERROR"], fill_value=0)

def build_summary(df, health):
    return {
        "total_entries": int(len(df)),
        "health_score": health,
        "levels": {k: int(v) for k, v in df.level.value_counts().items()},
        "errors_by_module": {k: int(v) for k, v in errors_by_module(df).items()},
        "top_error_messages": {k: int(v) for k, v in top_error_messages(df).items()},
        "errors_by_hour": {int(k): int(v) for k, v in errors_by_hour(df).items()},
        "busiest_hours": {int(k): int(v) for k, v in busiest_hours(df).items()},
    }
