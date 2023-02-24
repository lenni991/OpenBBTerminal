import pandas as pd
import numpy as np
from provider_factory import ApiFactory
from schemas.stocks_schemas import schema


class StockDataModel:
    """OpenBB stock object"""

    def __init__(self):
        self.schema = schema

        # metadata
        self.source = None
        self.symbol = None
        self.start_date = None
        self.end_date = None
        self.weekly = None
        self.monthly = None
        self.data_frame = None
        self.verified = False

    def load_from_api(
        self,
        api_key: str,
        source: str,
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
        self.source = source
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.weekly = weekly
        self.monthly = monthly

        api_provider = ApiFactory.create(self.source)

        self.data_frame = api_provider.load_stock_data(
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
            self.data_frame = None
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
        print("------------------------------------------------------------")
        print("Validating Dataframe")
        print("------------------------------------------------------------")
        missing_cols = (
            set(self.schema.keys())
            - set(self.data_frame.columns)
            - set([self.data_frame.index.name])
        )
        if missing_cols:
            return False, f"Missing columns: {missing_cols}"

        # Check data types
        for col, dtype in self.schema.items():
            if col in self.data_frame.columns:
                if not np.issubdtype(self.data_frame[col].dtype, dtype):
                    self.verified = False
                    return (
                        False,
                        f"Column {col} has incorrect data type. Expected {dtype}, but got {self.data_frame[col].dtype}",
                    )
            elif col == self.data_frame.index.name:
                if not np.issubdtype(self.data_frame.index.dtype, dtype):
                    self.verified = False
                    return (
                        False,
                        f"Index {col} has incorrect data type. Expected {dtype}, but got {self.data_frame.index.dtype}",
                    )

        # Check for any null values
        if self.data_frame.isnull().sum().sum() > 0:
            self.verified = False
            return False, "Dataframe contains null values"

        self.verified = True
        return True, "Verification successful"
