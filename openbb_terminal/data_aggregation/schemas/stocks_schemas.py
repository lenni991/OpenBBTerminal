from datetime import datetime
import numpy as np

schema = {
    "Volume": float,
    "VolWeight Avg": float,
    "Open": float,
    "Adj Close": float,
    "High": float,
    "Low": float,
    "Transactions": np.int64,
    "Close": float,
    "date": datetime,
}
