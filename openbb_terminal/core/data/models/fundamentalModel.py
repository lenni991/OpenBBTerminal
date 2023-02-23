import pandas as pd
import numpy as np
from providerFactory import ApiFactory
from schemas.fundamentals_schema import schema


class FundamentalDataModel:
    """OpenBB stock object"""

    def __init__(self):
        self.schema = schema

        # metadata
        self.source = None
        self.symbol = None
        self.date = None
        self.data_frame = None
        self.verified = False

    def load_from_api(
        self,
        api_key: str,
        source: str,
        symbol: str,
        date: str,
    ) -> pd.DataFrame:
        """Load stock data from API

        Args:
            api (str): api to use
            symbol (str): stock symbol

        Returns:
            pd.DataFrame: stock data from API
        """
        self.source = source
        self.symbol = symbol
        self.date = date
        self.data_frame = pd.DataFrame()

        api_provider = ApiFactory.create(self.source)
        self.data_frame = api_provider.load_fundamental_data(
            api_key=api_key,
            symbol=self.symbol,
            date=self.date,
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

        return self.data_frame

    def _check_df(self):
        # Check if all columns are present in the schema
        print("------------------------------------------------------------")
        print("Validating Fundamental Dataframe")
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
                # Check if column is of correct type in case its of type 'object'
                if self.data_frame[col].dtype == object:
                    if isinstance(self.data_frame[col].iat[0], dtype):
                        continue  # allow objects to be stored as 'object' type
                    else:
                        self.verified = False
                        return (
                            False,
                            f"Column '{col}' has incorrect data type. Expected {dtype}, but got {self.data_frame[col].dtype}",
                        )
            elif col == self.data_frame.index.name:
                if self.data_frame.index.dtype != dtype:
                    self.verified = False
                    return (
                        False,
                        f"Index '{col}' has incorrect data type. Expected {dtype}, but got {self.data_frame.index.dtype}",
                    )

        # Check for any null values
        if self.data_frame.isnull().sum().sum() > 0:
            self.verified = False
            return False, "Dataframe contains null values"

        self.verified = True
        return True, "Verification successful"
