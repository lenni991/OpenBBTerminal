from stockdataobject import StockDataObject

API_POLYGON_KEY = "7bLS_SJL3phqLxk9sOMve7FewcLwyNDd"

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


# stockObject
if stockObject.verified:
    print(stockObject)
    print(stockObject.stock_schema)
    print(stockObject.stock_data.head())
