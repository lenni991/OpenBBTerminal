""" Alpha Vantage View """
__docformat__ = "numpy"

import logging
import os
from typing import Union

# from openbb_terminal import config_plot as cfp
from openbb_terminal.config_terminal import theme
from openbb_terminal.core.plots.plotly_helper import OpenBBFigure
from openbb_terminal.decorators import check_api_key, log_start_end
from openbb_terminal.economy import alphavantage_model
from openbb_terminal.helper_funcs import (
    export_data,
    print_rich_table,
)

# is_valid_axes_count,; plot_autoscale,
from openbb_terminal.rich_config import console

# import matplotlib


logger = logging.getLogger(__name__)

# pylint: disable=C0302,unused-argument


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def realtime_performance_sector(
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display Real-Time Performance sector. [Source: AlphaVantage]

    Parameters
    ----------
    raw : bool
        Output only raw data
    export : str
        Export dataframe data to csv,json,xlsx file
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    df_rtp = alphavantage_model.get_sector_data()

    # pylint: disable=E1101
    if df_rtp.empty:
        return

    if raw:
        print_rich_table(
            df_rtp,
            show_index=False,
            headers=df_rtp.columns,
            title="Real-Time Performance",
        )

    else:
        df_rtp.set_index("Sector", inplace=True)
        df_rtp = df_rtp.squeeze(axis=1)
        colors = [theme.up_color if x > 0 else theme.down_color for x in df_rtp.values]

        fig = OpenBBFigure(
            title="Real Time Performance (%) per Sector",
            yaxis=dict(side="right", dtick=1, title="Sector"),
        )
        fig.add_bar(
            orientation="h",
            x=df_rtp.values,
            y=df_rtp.index,
            name="Performance (%)",
            marker_color=colors,
            showlegend=False,
        )
        fig.update_layout(xaxis=dict(nticks=10))

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "rtps",
        df_rtp,
        sheet_name,
    )

    return fig.show(external=external_axes) if not raw else None


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_real_gdp(
    interval: str = "q",
    start_year: int = 2010,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display US GDP from AlphaVantage

    Parameters
    ----------
    interval : str
        Interval for GDP.  Either "a" or "q", by default "q"
    start_year : int, optional
        Start year for plot, by default 2010
    raw : bool, optional
        Flag to show raw data, by default False
    export : str, optional
        Format to export data, by default ""
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    gdp = alphavantage_model.get_real_gdp(interval, start_year)

    if gdp.empty:
        return

    int_string = "Annual" if interval == "a" else "Quarterly"
    year_str = str(start_year) if interval == "a" else str(list(gdp["date"])[-1].year)

    fig = OpenBBFigure(
        title=f"{int_string} US GDP ($B) from {year_str}",
        yaxis=dict(side="right", title="US GDP ($B) "),
    )

    fig.add_scatter(
        x=gdp["date"],
        y=gdp["GDP"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "gdp",
        gdp,
        sheet_name,
    )
    if raw:
        print_rich_table(
            gdp.head(20), headers=["Date", "GDP"], show_index=False, title="US GDP"
        )

    return fig.show(external=external_axes)


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_gdp_capita(
    start_year: int = 2010,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display US GDP per Capita from AlphaVantage

    Parameters
    ----------
    start_year : int, optional
        Start year for plot, by default 2010
    raw : bool, optional
        Flag to show raw data, by default False
    export : str, optional
        Format to export data, by default
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    gdp = alphavantage_model.get_gdp_capita(start_year)
    if gdp.empty:
        console.print("Error getting data.  Check API Key")
        return

    fig = OpenBBFigure(
        title=f"US GDP per Capita (Chained 2012 USD) from {start_year}",
        yaxis=dict(side="right", title="US GDP (Chained 2012 USD) "),
    )

    fig.add_scatter(
        x=gdp["date"],
        y=gdp["GDP"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "gdpc",
        gdp,
        sheet_name,
    )
    if raw:
        print_rich_table(
            gdp.head(20),
            headers=["Date", "GDP"],
            show_index=False,
            title="US GDP Per Capita",
        )

    return fig.show(external=external_axes)


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_inflation(
    start_year: int = 2010,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display US Inflation from AlphaVantage

    Parameters
    ----------
    start_year : int, optional
        Start year for plot, by default 2010
    raw : bool, optional
        Flag to show raw data, by default False
    export : str, optional
        Format to export data, by default ""
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    inf = alphavantage_model.get_inflation(start_year)
    if inf.empty:
        console.print("Error getting data.  Check API Key")
        return

    fig = OpenBBFigure(
        title=f"US Inflation from {list(inf['date'])[-1].year}",
        yaxis=dict(side="right", title="Inflation (%)"),
    )

    fig.add_scatter(
        x=inf["date"],
        y=inf["Inflation"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "inf",
        inf,
        sheet_name,
    )
    if raw:
        print_rich_table(
            inf.head(20),
            headers=["Date", "Inflation"],
            show_index=False,
            title="US Inflation",
        )

    return fig.show(external=external_axes)


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_cpi(
    interval: str = "m",
    start_year: int = 2010,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display US consumer price index (CPI) from AlphaVantage

    Parameters
    ----------
    interval : str
        Interval for GDP.  Either "m" or "s"
    start_year : int, optional
        Start year for plot, by default 2010
    raw : bool, optional
        Flag to show raw data, by default False
    export : str, optional
        Format to export data, by default ""
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    cpi = alphavantage_model.get_cpi(interval, start_year)
    if cpi.empty:
        console.print("Error getting data.  Check API Key")
        return

    int_string = "Semi-Annual" if interval == "s" else "Monthly"
    year_str = str(list(cpi["date"])[-1].year)

    fig = OpenBBFigure(
        title=f"{int_string} Consumer Price Index from {year_str}",
        yaxis=dict(side="right", title="CPI"),
    )

    fig.add_scatter(
        x=cpi["date"],
        y=cpi["CPI"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "cpi",
        cpi,
        sheet_name,
    )
    if raw:
        print_rich_table(
            cpi.head(20), headers=["Date", "CPI"], show_index=False, title="US CPI"
        )

    return fig.show(external=external_axes)


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_treasury_yield(
    interval: str = "m",
    maturity: str = "10y",
    start_date: str = "2010-01-01",
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display historical treasury yield for given maturity

    Parameters
    ----------
    interval : str
        Interval for data.  Can be "d","w","m" for daily, weekly or monthly, by default "m"
    maturity : str
        Maturity timeline.  Can be "3mo","5y","10y" or "30y", by default "10y"
    start_date: str
        Start date for data.  Should be in YYYY-MM-DD format, by default "2010-01-01"
    raw : bool, optional
        Flag to display raw data, by default False
    export : str, optional
        Format to export data, by default ""
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """
    d_maturity = {"3m": "3month", "5y": "5year", "10y": "10year", "30y": "30year"}
    yld = alphavantage_model.get_treasury_yield(interval, maturity, start_date)
    if yld.empty:
        console.print("Error getting data.  Check API Key")
        return

    fig = OpenBBFigure(
        title=f"{d_maturity[maturity]} Treasury Yield",
        yaxis=dict(side="right", title="Yield (%)"),
    )

    fig.add_scatter(
        x=yld["date"],
        y=yld["Yield"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "tyld",
        yld,
        sheet_name,
    )
    if raw:
        print_rich_table(
            yld.head(20),
            headers=["Date", "Yield"],
            title="Historical Treasury Yield",
            show_index=False,
        )

    return fig.show(external=external_axes)


@log_start_end(log=logger)
@check_api_key(["API_KEY_ALPHAVANTAGE"])
def display_unemployment(
    start_year: int = 2010,
    raw: bool = False,
    export: str = "",
    sheet_name: str = None,
    external_axes: bool = False,
) -> Union[OpenBBFigure, None]:
    """Display US unemployment AlphaVantage

    Parameters
    ----------
    start_year : int, optional
        Start year for plot, by default 2010
    raw : bool, optional
        Flag to show raw data, by default False
    export : str, optional
        Format to export data, by default ""
    external_axes : bool, optional
        Whether to return the figure object or not, by default False
    """

    un = alphavantage_model.get_unemployment(start_year)

    if un.empty:
        console.print("Error getting data. Check API Key")
        return

    fig = OpenBBFigure(
        title=f"US Unemployment from {start_year}",
        yaxis=dict(side="right", title="US Unemployment (%)"),
    )

    fig.add_scatter(
        x=un["date"],
        y=un["unemp"],
    )

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        "unemp",
        un,
        sheet_name,
    )

    if raw:
        print_rich_table(
            un.head(20),
            headers=["Date", "GDP"],
            title="US Unemployment",
            show_index=False,
        )

    return fig.show(external=external_axes)
