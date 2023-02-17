import datetime
import pandas as pd
import yfinance as yf
import os


class YahooProvider:
    def __init__(self):
        pass

    def load_stock_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        weekly: bool,
        monthly: bool,
    ) -> pd.DataFrame:
        int_ = "1d"
        int_string = "Daily"
        if weekly:
            int_ = "1wk"
            int_string = "Weekly"
        if monthly:
            int_ = "1mo"
            int_string = "Monthly"

        # Win10 version of mktime cannot cope with dates before 1970
        if os.name == "nt" and start_date < datetime.datetime(1970, 1, 1):
            start_date = datetime.datetime(
                1970, 1, 2
            )  # 1 day buffer in case of timezone adjustments

        # Adding a dropna for weekly and monthly because these include weird NaN columns.
        df_stock_candidate = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True,
            actions=True,
            interval=int_,
            ignore_tz=True,
        ).dropna(axis=0)

        # Check that loading a stock was not successful
        if df_stock_candidate.empty:
            return pd.DataFrame()
        df_stock_candidate_cols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
            "Dividends",
            "Stock Splits",
        ]
        df_stock_candidate.index.name = "date", int_string
        df_stock_candidate["Adj Close"] = df_stock_candidate["Close"].copy()
        df_stock_candidate = pd.DataFrame(
            data=df_stock_candidate, columns=df_stock_candidate_cols
        )
        return df_stock_candidate
