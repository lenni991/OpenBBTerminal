import pandas as pd
import numpy as np
from polygonProvider import PolygonProvider


API_POLYGON_KEY = "INSERT"


class StockDataObject:
    """OpenBB stock object"""

    def __init__(self):
        self.stock_schema = {  # base schema
            "Volume": float,
            "VolWeight Avg": float,
            "Open": float,
            "Adj Close": float,
            "High": float,
            "Low": float,
            "Transactions": int,
            "Close": float,
            "date": "datetime64[ns]",
        }

        # metadata
        self.api_name = None
        self.symbol = None
        self.start_date = None
        self.end_date = None
        self.weekly = None
        self.monthly = None
        self.stock_data = None
        self.verified = False

    def load_from_api(
        self,
        api_key: str,
        api_name: str,
        symbol: str,
        start_date: str,
        end_date: str,
        weekly: bool,
        monthly: bool,
    ) -> pd.DataFrame:
        """Load stock data from API

        Args:
            api (str): api to use
            symbol (str): stock symbol
            start_date (str: start date
            end_date (str): end date
            weekly (bool): weekly data
            monthly (bool): monthly data

        Returns:
            pd.DataFrame: stock data from API
        """
        self.api_name = api_name
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.weekly = weekly
        self.monthly = monthly

        if self.api_name == "polygon":
            self.stock_data = PolygonProvider().load_stock_data(
                api_key=api_key,
                symbol=self.symbol,
                start_date=self.start_date,
                end_date=self.end_date,
                weekly=self.weekly,
                monthly=self.monthly,
            )

        # check data
        result, msg = self._check_df()
        if result is False:
            self.verified = False
            self.stock_data = None
            print(msg)
        else:
            self.verified = True
            print(msg)

    def load_from_file(self, file_path: str) -> pd.DataFrame:
        pass

    def load_from_sql(self, sql_query: str) -> pd.DataFrame:
        pass

    def _check_df(self):
        # Check if all columns are present in the schema
        missing_cols = (
            set(self.stock_schema.keys())
            - set(self.stock_data.columns)
            - set([self.stock_data.index.name])
        )
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"

        # Check data types
        for col, dtype in self.stock_schema.items():
            if col in self.stock_data.columns:
                if not np.issubdtype(self.stock_data[col].dtype, dtype):
                    self.verified = False
                    return (
                        False,
                        f"Column {col} has incorrect data type. Expected {dtype}, but got {self.stock_data[col].dtype}",
                    )
            elif col == self.stock_data.index.name:
                if not np.issubdtype(self.stock_data.index.dtype, dtype):
                    self.verified = False
                    return (
                        False,
                        f"Index {col} has incorrect data type. Expected {dtype}, but got {self.stock_data.index.dtype}",
                    )

        # Check for any null values
        if self.stock_data.isnull().sum().sum() > 0:
            self.verified = False
            return False, "Dataframe contains null values"

        self.verified = True
        return True, "Verification successful"
