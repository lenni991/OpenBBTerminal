import datetime
import requests
import pandas as pd


class PolygonProvider:
    def __init__(self):
        self.api_key = None

    def load_stock_data(
        self,
        api_key: str,
        symbol: str,
        start_date: str,
        end_date: str,
        weekly: bool,
        monthly: bool,
    ) -> pd.DataFrame:
        self.api_key = api_key
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Polygon allows: day, minute, hour, day, week, month, quarter, year
        timespan = "day"
        if weekly or monthly:
            timespan = "week" if weekly else "month"

        request_url = (
            f"https://api.polygon.io/v2/aggs/ticker/"
            f"{symbol.upper()}/range/1/{timespan}/"
            f"{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?adjusted=true"
            f"&sort=desc&limit=49999&apiKey={self.api_key}"
        )
        r = requests.get(request_url)
        if r.status_code != 200:
            print("[red]Error in polygon request[/red]")
            return pd.DataFrame()

        r_json = r.json()
        if "results" not in r_json.keys():
            print("[red]No results found in polygon reply.[/red]")
            return pd.DataFrame()

        df_stock_candidate = pd.DataFrame(r_json["results"])

        df_stock_candidate = df_stock_candidate.rename(
            columns={
                "o": "Open",
                "c": "Adj Close",
                "h": "High",
                "l": "Low",
                "t": "date",
                "v": "Volume",
                "n": "Transactions",
                "vw": "VolWeight Avg",
            }
        )
        df_stock_candidate["date"] = pd.to_datetime(df_stock_candidate["date"])
        df_stock_candidate["date"] = df_stock_candidate["date"].dt.date
        df_stock_candidate["Close"] = df_stock_candidate["Adj Close"]
        df_stock_candidate = df_stock_candidate.sort_values("date")
        df_stock_candidate = df_stock_candidate.reset_index(drop=True)

        return df_stock_candidate

    def load_fundamental_data(
        self, api_key: str, symbol: str, date: str
    ) -> pd.DataFrame:
        self.api_key = api_key
        request_url = f"https://api.polygon.io/v3/reference/tickers/{symbol}?date={date}&apiKey={api_key}"
        r = requests.get(request_url)
        if r.status_code != 200:
            print("[red]Error in polygon request[/red]")
            return pd.DataFrame()

        r_json = r.json()
        if "results" not in r_json.keys():
            print("[red]No results found in polygon reply.[/red]")
            return pd.DataFrame()

        # Remove the "address" field from the response object
        r_json.pop("address", None)

        response_obj = r_json["results"]
        if "branding" in response_obj:
            del response_obj["branding"]

        df_fundamental_candidate = pd.DataFrame([response_obj])

        return df_fundamental_candidate
