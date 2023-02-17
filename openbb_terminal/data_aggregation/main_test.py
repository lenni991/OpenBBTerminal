import joblib
import os
import shutil
import glob
import time

from models.stockModel import StockDataModel
from models.fundamentalModel import FundamentalDataModel


# -----------------------------------------------
# Set up caching
# -----------------------------------------------
# total memory of 100 mb
total_allowable_cache_size = 1e8  # 100
remove_cache = False
cachedir = os.path.join(os.getcwd(), "cache")
memory = joblib.Memory(
    location=cachedir, verbose=0
)  # create a memory object to cache the data objects


def check_cache_size():
    cache_files = glob.glob(os.path.join(cachedir, "*.joblib"))
    total_size = sum(os.path.getsize(f) for f in cache_files)
    return total_size


def remove_oldest_cache():
    cache_files = glob.glob(os.path.join(cachedir, "*.joblib"))
    oldest_file = min(cache_files, key=os.path.getctime)
    os.remove(oldest_file)
    print("--------------------")
    print(f"Removed oldest file: {oldest_file}")
    print("--------------------")


# Remove cached objects
if remove_cache:
    print("--------------------")
    print("Removing cached objects")
    print("--------------------")
    memory.clear(warn=False)

# -----------------------------------------------
# Define cache creation functions
# -----------------------------------------------
@memory.cache
def create_stock_object(api_key, source, symbol, start_date, end_date, weekly, monthly):
    temp_cache_name = f"stock_{source}_{symbol}_{start_date}_{end_date}.joblib"
    cache_path = os.path.join(cachedir, temp_cache_name)
    if os.path.exists(cache_path):
        print("--------------------")
        print(f"Object with parameters {temp_cache_name} already exists in cache.")
        print("--------------------")
        return None
    else:
        print("--------------------")
        print(f"Object with parameters {temp_cache_name} does not exist in cache.")
        print("Creating object...")
        print("--------------------")
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
            print(data_object.stock_data.head())
            # Cache object if verified
            current_cache_size = check_cache_size()
            if current_cache_size > total_allowable_cache_size:
                remove_oldest_cache()
            joblib.dump(data_object, cache_path)
        else:
            print("--------------------")
            print("Data object not verified. Not caching object.")
            print("--------------------")

        return data_object


@memory.cache
def create_fundamental_object(api_key, source, symbol):
    temp_cache_name = f"fundamental_{source}_{symbol}.joblib"
    cache_path = os.path.join(cachedir, temp_cache_name)
    if os.path.exists(cache_path):
        print("--------------------")
        print(f"Object with parameters {temp_cache_name} already exists in cache.")
        print("--------------------")
        return None
    else:
        print("--------------------")
        print(f"Object with parameters {temp_cache_name} does not exist in cache.")
        print("Creating object...")
        print("--------------------")
        data_object = FundamentalDataModel()
        data_object.load_from_api(
            api_key=api_key,
            source=source,
            symbol=symbol,
        )

        if data_object.verified:
            print(data_object.fundamental_data)
            # Cache object if verified
            current_cache_size = check_cache_size()
            if current_cache_size > total_allowable_cache_size:
                remove_oldest_cache()
            joblib.dump(data_object, cache_path)
        else:
            print("--------------------")
            print("Data object not verified. Not caching object.")
            print("--------------------")

        return data_object


if __name__ == "__main__":

    # -----------------------------------------------
    # Set up API keys
    # -----------------------------------------------
    requested_source = "polygon"
    if requested_source == "polygon":
        API_KEY = "insert"
    elif requested_source == "yahoo":
        API_KEY = None

    # user input
    ticker = "AAPL"
    s_d = "2023-01-01"
    e_d = "2023-01-09"
    w = False
    m = False

    # Cache the objects
    print("--------------------")
    print("Creating and caching stock data object")
    print("--------------------")
    stockObject = create_stock_object(
        api_key=API_KEY,
        source=requested_source,
        symbol=ticker,
        start_date=s_d,
        end_date=e_d,
        weekly=w,
        monthly=m,
    )
    print("--------------------")
    print("Creating and caching fundamental data object")
    print("--------------------")
    fundamentalObject = create_fundamental_object(
        api_key=API_KEY,
        source=requested_source,
        symbol="AAPL",
    )

    # Load cached objects with specific names
    cache_name = f"stock_{requested_source}_{ticker}_{s_d}_{e_d}.joblib"
    cached_stock = joblib.load(os.path.join(cachedir, cache_name))

    # Use cached objects
    print("--------------------")
    print("Using cached objects")
    print("--------------------")
    print(cached_stock.stock_data.head())

    # Remove cached objects
    if remove_cache:
        print("--------------------")
        print("Removing cached objects")
        print("--------------------")
        memory.clear(warn=False)
