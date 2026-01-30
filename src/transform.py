from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])


class QueryEnum(Enum):
    DELIVERY_DATE_DIFFERENCE = "delivery_date_difference"  
    GLOBAL_AMOUNT_ORDER_STATUS = "global_amount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"
    


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_name (str): The name of the file.

    Returns:
        str: The query.
    """
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
        sql = text(sql_file)
    return sql


def query_delivery_date_difference(database: Engine) -> QueryResult:
    """Get the query for delivery date difference.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for delivery date difference.
    """
    query_name = QueryEnum.DELIVERY_DATE_DIFFERENCE.value
    query = read_query(QueryEnum.DELIVERY_DATE_DIFFERENCE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_global_amount_order_status(database: Engine) -> QueryResult:  
    """Get the query for global amount of order status.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for global percentage of order status.
    """
    query_name = QueryEnum.GLOBAL_AMOUNT_ORDER_STATUS.value  
    query = read_query(QueryEnum.GLOBAL_AMOUNT_ORDER_STATUS.value)  
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    """Get the query for revenue by month year.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for revenue by month year.
    """
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(QueryEnum.REVENUE_BY_MONTH_YEAR.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_per_state(database: Engine) -> QueryResult:
    """Get the query for revenue per state.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for revenue per state.
    """
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(QueryEnum.REVENUE_PER_STATE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 least revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for top 10 least revenue categories.
    """
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    """Get the query for top 10 revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for top 10 revenue categories.
    """
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(QueryEnum.TOP_10_REVENUE_CATEGORIES.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    """Get the query for real vs estimated delivered time.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for real vs estimated delivered time.
    """
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value)
    return QueryResult(query=query_name, result=read_sql(query, database))

def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    """Get the freight_value weight relation for delivered orders."""
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value

    orders = pd.read_sql_table("olist_orders", database)
    items = pd.read_sql_table("olist_order_items", database)
    products = pd.read_sql_table("olist_products", database)

    df = orders.merge(items, on="order_id", how="inner")
    df = df.merge(products, on="product_id", how="inner")

    df = df[df["order_status"] == "delivered"]

    result_df = (
        df.groupby("order_id")
          .agg({
              "freight_value": "sum",
              "product_weight_g": "sum"
          })
          .reset_index()
    )

    return QueryResult(query=query_name, result=result_df)

    
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value

    # Get orders from olist_orders table
    orders = read_sql("SELECT * FROM olist_orders", database)

    # Get items from olist_order_items table
    items = read_sql("SELECT * FROM olist_order_items", database)

    # Get products from olist_products table
    products = read_sql("SELECT * FROM olist_products", database)

    # TODO: Merge items, orders and products tables on 'order_id'/'product_id'.
    # We suggest to use pandas.merge() function.
    # Assign the result to the `data` variable.
    data = ...

    # TODO: Get only delivered orders.
    # Using the previous results from the merge (stored in `data` variable),
    # apply a boolean mask to keep only the 'delivered' orders.
    # Assign the result to the variable `delivered`.
    delivered = ...

    # TODO: Get the sum of freight_value and product_weight_g for each order_id.
    # The same order (identified by 'order_id') can have multiple products inside,
    # then we decided to sum all the products 'freight_value' and 'product_weight_g'
    # inside that order.
    # Use the pandas DataFrame stored in `delivered` variable. We suggest you to
    # look at pandas.DataFrame.groupby() and pandas.DataFrame.agg() for the data
    # transformation.
    # Store the result in the `aggregations` variable.
    aggregations = ...

    # Keep the code below as it is, this will return the result from
    # `aggregations` variable with the corresponding name and format.
    return QueryResult(query=query_name, result=aggregations)


def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    """Get orders per day and holidays in 2017.
    
    Returns:
        QueryResult: With query name and DataFrame containing:
            - date: order date in milliseconds (timestamp)
            - order_count: number of orders that day
            - holiday: boolean indicating if date was a holiday
    """
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value

    orders_query = """
    SELECT 
        order_id, 
        order_purchase_timestamp
    FROM olist_orders
    WHERE strftime('%Y', order_purchase_timestamp) = '2017'
    """
    orders_df = pd.read_sql(orders_query, database)
    
    holidays_df = pd.read_sql("SELECT date FROM public_holidays", database)

    orders_df['date'] = pd.to_datetime(orders_df['order_purchase_timestamp']).dt.floor('D')
    orders_per_day = orders_df.groupby('date').size().reset_index(name='order_count')
    
    holidays_df['date'] = pd.to_datetime(holidays_df['date']).dt.floor('D')
    holiday_dates = set(holidays_df['date'])
    
    orders_per_day['holiday'] = orders_per_day['date'].isin(holiday_dates)
    orders_per_day['date'] = (orders_per_day['date'].astype('int64') // 10**6).astype('int64')
    
    result_df = orders_per_day.sort_values('date')[['date', 'order_count', 'holiday']]
    
    return QueryResult(query=query_name, result=result_df)


def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Get all queries.

    Returns:
        List[Callable[[Engine], QueryResult]]: A list of all queries.
    """
    return [
        query_delivery_date_difference,
        query_global_amount_order_status,  
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Transform data based on the queries. For each query, the query is executed and
    the result is stored in the dataframe.

    Args:
        database (Engine): Database connection.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the query file names and
        values the result of the query as a dataframe.
    """
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results