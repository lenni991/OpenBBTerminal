from stockModel import StockDataModel
from fundamentalModel import FundamentalDataModel

API_POLYGON_KEY = "INSERT"

stock_source = "polygon"

print("Testing stock data object")
# create a stock object
stockObject = StockDataModel()
if stock_source == "polygon":
    stockObject.load_from_api(
        api_key=API_POLYGON_KEY,
        source="polygon",
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2023-01-09",
        weekly=False,
        monthly=False,
    )
elif stock_source == "yahoo":
    stockObject.load_from_api(
        api_key=API_POLYGON_KEY,
        source="yahoo",
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
    api_key=API_POLYGON_KEY,
    source="polygon",
    symbol="AAPL",
)
