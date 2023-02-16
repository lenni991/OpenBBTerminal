from stockDataModel import StockDataModel
from fundamentalDataModel import FundamentalDataModel

API_POLYGON_KEY = "replace"


print("Testing stock data object")
# create a stock object
stockObject = StockDataModel()
stockObject.load_from_api(
    api_key=API_POLYGON_KEY,
    api_name="polygon",
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2023-01-09",
    weekly=False,
    monthly=False,
)

# Check data within object
if stockObject.verified:
    print(stockObject)
    print(stockObject.stock_schema)
    print(stockObject.stock_data.head())

# --------------------------------------------
print("Testing fundamental data object")
fundamentalObject = FundamentalDataModel()
fundamentalObject.load_from_api(
    api_key=API_POLYGON_KEY,
    api_name="polygon",
    symbol="AAPL",
)
