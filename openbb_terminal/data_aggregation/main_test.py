import joblib  # to cache the objects
import os

from models.stockModel import StockDataModel
from models.fundamentalModel import FundamentalDataModel

# -----------------------------------------------"
# Set up caching
# -----------------------------------------------"
remove_cache = True
cachedir = os.path.join(os.getcwd(), "cache")
memory = joblib.Memory(
    location=cachedir, verbose=0
)  # create a memory object to cache the data objects


# Remove cached objects
if remove_cache:
    print("Removing cached objects")
    memory.clear(warn=False)
# -----------------------------------------------"


# -----------------------------------------------"
# Set up API keys
# -----------------------------------------------"
requested_source = "polygon"
if requested_source == "polygon":
    API_KEY = "INSERT API KEY HERE"
elif requested_source == "yahoo":
    API_KEY = None
# -----------------------------------------------"


@memory.cache
def create_stock_object(name):
    data_object = StockDataModel()
    data_object.load_from_api(
        api_key=API_KEY,
        source=requested_source,
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-01-09",
        weekly=False,
        monthly=False,
    )

    # Check data within object using its members
    if data_object.verified:
        print(data_object.stock_schema)
        print(data_object.stock_data.head())
        # cache object if verified
        joblib.dump(data_object, os.path.join(cachedir, f"{name}.joblib"))
    return data_object


@memory.cache
def create_fundamental_object(name):
    data_object = FundamentalDataModel()
    data_object.load_from_api(
        api_key=API_KEY,
        source=requested_source,
        symbol="AAPL",
    )

    if data_object.verified:
        print(data_object.fundamental_data)
        # cache object is verified
        joblib.dump(data_object, os.path.join(cachedir, f"{name}.joblib"))
    return data_object


if __name__ == "__main__":

    # Cache the objects
    print("Creating and caching stock data object")
    stockObject = create_stock_object(name="my_cached_stock")

    print("Creating and caching fundamental data object")
    fundamentalObject = create_fundamental_object(name="my_cached_fundamental")

    # Load cached objects with specific names
    cached_stock = joblib.load(os.path.join(cachedir, "my_cached_stock.joblib"))

    # use cached objects
    print("Using cached objects")
    print(cached_stock.stock_data.head())

    # Remove cached objects
    if remove_cache:
        print("Removing cached objects")
        memory.clear(warn=False)
