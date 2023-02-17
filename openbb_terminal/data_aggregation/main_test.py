from models.stockModel import StockDataModel
from models.fundamentalModel import FundamentalDataModel

requested_source = "polygon"

if requested_source == "polygon":
    API_KEY = "INSERT"
elif requested_source == "yahoo":
    API_KEY = None

print("Testing stock data object")
# create a stock object
stockObject = StockDataModel()
stockObject.load_from_api(
    api_key=API_KEY,
    source=requested_source,
    symbol="AAPL",
    start_date="2023-01-01",
    end_date="2023-01-09",
    weekly=False,
    monthly=False,
)

# Check data within object using its members
if stockObject.verified:
    print(stockObject.stock_schema)
    print(stockObject.stock_data.head())

# --------------------------------------------
print("Testing fundamental data object")
fundamentalObject = FundamentalDataModel()
fundamentalObject.load_from_api(
    api_key=API_KEY,
    source=requested_source,
    symbol="AAPL",
)
