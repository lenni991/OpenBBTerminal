from stockdataobject import StockDataObject
from fundamentalDataObject import FundamentalDataObject

API_POLYGON_KEY = "INSERT"


print("Testing stock data object")
# create a stock object
stockObject = StockDataObject()
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
fundamentalObject = FundamentalDataObject()
fundamentalObject.load_from_api(
    api_key=API_POLYGON_KEY,
    api_name="polygon",
    symbol="AAPL",
)
