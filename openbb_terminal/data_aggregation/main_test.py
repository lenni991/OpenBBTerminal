import joblib  # to cache the objects
import os

from models.stockModel import StockDataModel
from models.fundamentalModel import FundamentalDataModel

# -----------------------------------------------
# Set up caching
# -----------------------------------------------
remove_cache = True
cachedir = os.path.join(os.getcwd(), "cache")
memory = joblib.Memory(
    location=cachedir, verbose=0
)  # create a memory object to cache the data objects

# Remove cached objects
if remove_cache:
    print("Removing cached objects")
    memory.clear(warn=False)

# -----------------------------------------------
# Set up API keys
# -----------------------------------------------
requested_source = "polygon"
if requested_source == "polygon":
    API_KEY = "insert"
elif requested_source == "yahoo":
    API_KEY = None

# -----------------------------------------------
# Define cache creation functions
# -----------------------------------------------
@memory.cache
def create_stock_object(api_key, source, symbol, start_date, end_date, weekly, monthly):
    data_object = StockDataModel()
    data_object.load_from_api(
        api_key=api_key,
        source=source,
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
        weekly=weekly,
        monthly=monthly,
    )

    # Check data within object using its members
    if data_object.verified:
        print(data_object.stock_schema)
        print(data_object.stock_data.head())
        # Cache object if verified
        cache_name = f"{source}_{symbol}_{start_date}_{end_date}"
        joblib.dump(data_object, os.path.join(cachedir, f"{cache_name}.joblib"))

    return data_object


@memory.cache
def create_fundamental_object(api_key, source, symbol):
    data_object = FundamentalDataModel()
    data_object.load_from_api(
        api_key=api_key,
        source=source,
        symbol=symbol,
    )

    if data_object.verified:
        print(data_object.fundamental_data)
        # Cache object if verified
        cache_name = f"{source}_{symbol}"
        joblib.dump(data_object, os.path.join(cachedir, f"{cache_name}.joblib"))

    return data_object


if __name__ == "__main__":
    # Cache the objects
    print("Creating and caching stock data object")
    stockObject = create_stock_object(
        api_key=API_KEY,
        source=requested_source,
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-01-09",
        weekly=False,
        monthly=False,
    )

    print("Creating and caching fundamental data object")
    fundamentalObject = create_fundamental_object(
        api_key=API_KEY,
        source=requested_source,
        symbol="AAPL",
    )

    # Load cached objects with specific names
    cache = f"{requested_source}_AAPL_2023-01-01_2023-01-09.joblib"
    cached_stock = joblib.load(os.path.join(cachedir, cache))

    # Use cached objects
    print("Using cached objects")
    print(cached_stock.stock_data.head())

    # Remove cached objects
    if remove_cache:
        print("Removing cached objects")
        memory.clear(warn=False)
