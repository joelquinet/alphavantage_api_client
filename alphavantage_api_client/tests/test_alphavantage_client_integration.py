import pytest
import json
import os
import time
from alphavantage_api_client import AlphavantageClient


def setup_function(function):
    pass


def teardown_function(function):
    pass


def setup_module(module):
    pass


def teardown_module(module):
    pass


def quoteLatestPrice(success_criteria=True, event=None):
    assert event != None
    client = AlphavantageClient()

    results = client.get_global_quote(event)
    assert results.success == success_criteria, f"success was found to be {results.success}: {results.error_message}"
    assert results.symbol == event.get("symbol"), "Response symbol doesn't matched requested symbol"
    assert not results.limit_reached, f"{results.error_message}"

    # free api key is only allow 5 calls per min, so need to make sure i don't have a dependency on function order AND
    # I can have as many functions with the same key.
    time.sleep(20)
    return results


@pytest.mark.integration
def test_canQuoteStockSymbolJson():
    event = {
        "symbol": "tsla"
    }
    results = quoteLatestPrice(True, event)
    assert len(results.data) > 0, "Response should have data but contains zero"
    print(f"Can quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_canQuoteStockSymbolCsv():
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    latest_stock_price = quoteLatestPrice(True, event)
    assert latest_stock_price.csv, "CSV field was not found "
    assert len(latest_stock_price.csv), "Csv return value has no data"
    print(f"Can quote stock symbol in CSV {event.get('symbol', None)}")


@pytest.mark.integration
def test_canNotQuoteWrongSymbolJson():
    event = {
        "symbol": "tsla2323"
    }
    results = quoteLatestPrice(False, event)
    print(results)
    assert len(results.data) == 0, "Response should not have data but contains zero"
    print(f"Can NOT quote stock symbol in JSON {event.get('symbol', None)}")


@pytest.mark.integration
def test_canNotQuoteWrongSymbolCsv():
    event = {
        "symbol": "tsla2233",
        "datatype": "csv"
    }
    results = quoteLatestPrice(False, event)
    print(f"Can NOT quote stock symbol in csv {event.get('symbol', None)} : {results.error_message}")


@pytest.mark.integration
def test_canReachLimitJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }
    limit_reached = False
    results = None
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    for i in range(7):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
    print(f"Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")
    time.sleep(60)


@pytest.mark.integration
def test_canReachLimitCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }
    limit_reached = False
    # force limit reached
    # my api key is free, so 5 calls per min and total of 500 per day
    results = None
    for i in range(7):
        results = client.get_global_quote(event)
        if results.limit_reached:
            limit_reached = True
            break

    assert limit_reached, "Failed to reach limit"
    assert results.symbol == event['symbol'], f" Expected symbol doesn't match given: {event.get('symbol', None)}"
    print(f"Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")
    time.sleep(60)

    print(f"Can Reach Limit while quoting for symbol {event.get('symbol', None)} in JSON")
    time.sleep(60)


@pytest.mark.integration
def test_canQuoteEthJson():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min"
    }
    client = AlphavantageClient()
    results = client.get_crypto_intraday(event)
    print(results)
    assert not results.limit_reached, f"limit_reached should not be true {results.error_message}"
    assert results.success, f"success is false {results.error_message}"
    print(f"Successfully quoted cryptocurrency symbol {event['symbol']} in JSON")
    time.sleep(20)


@pytest.mark.integration
def test_canQuoteEthCsv():
    event = {
        "function": "CRYPTO_INTRADAY",
        "symbol": "ETH",
        "market": "USD",
        "interval": "5min",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert "success" in results and results.get("success",
                                                None) is True, f"Failed to receive a quote for {event.get('symbol', None)}"
    assert results.get("csv"), "Csv field is not present"
    assert len(results.get("csv")), "Csv return value has no data"
    print(f"Successfully quoted cryptocurrency symbol {event['symbol']} in CSV")
    time.sleep(20)


@pytest.mark.integration
def test_canQuoteRealGDPJson():
    event = {
        "function": "REAL_GDP",
        "interval": "annual"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) is False, f'{results.get("Error Message", None)}'
    assert results.get('success', False) == True, \
        "Success flag not present or equal to false when quoting real GDP"
    print("Can quote Real GDP")
    time.sleep(20)


@pytest.mark.integration
def test_canQuoteRealGDPCsv():
    event = {
        "function": "REAL_GDP",
        "interval": "annual",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert "success" in results and results.get(
        'success', None) == True, "Success flag not present or equal to false when quoting real GDP"
    assert results.get("csv"), "Csv field is not present"
    assert len(results.get("csv")), "Csv return value has no data"
    print("Can quote Real GDP")
    time.sleep(20)


@pytest.mark.integration
def test_canQuoteTechnicalIndicatorJson():
    event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) is False, f'{results.get("Error Message", None)}'
    assert "success" in results and results.get(
        'success', None) == True, "Success flag not present or equal to false when quoting IBM EMA technical indicator"
    print("Can quote IBM EMA technical indicator")
    time.sleep(20)


@pytest.mark.integration
def test_canQuoteTechnicalIndicatorCsv():
    event = {
        "function": "EMA",
        "symbol": "IBM",
        "interval": "weekly",
        "time_period": "10",
        "series_type": "open",
        "datatype": "csv"
    }
    client = AlphavantageClient()
    results = client.get_data_from_alpha_vantage(event)
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) is False, f'{results.get("Error Message", None)}'
    assert "success" in results and results.get(
        'success', None) == True, "Success flag not present or equal to false when quoting IBM EMA technical indicator"
    assert results.get("csv"), "Csv field is not present"
    assert len(results.get("csv")), "Csv return value has no data"

    print("Can quote IBM EMA technical indicator")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryCompanyOverviewJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_company_overview(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) is False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query company overview {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryCompanyOverviewCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_company_overview(event)
        assert True == False, "Expected an error because company overview doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because company overview doesn't support csv"

    print(f"Querying Company Overview as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryLatestIncomeStatementJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_latest_income_statement_for_symbol(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query latest income statement {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryLatestIncomeStatementCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_latest_income_statement_for_symbol(event)
        assert True == False, "Expected an error because latest income statement doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because latest income statement doesn't support csv"

    print(f"Querying latest income statement as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryLatestEarningsJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_latest_earnings(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query latest earnings {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryLatestEarningsCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_latest_earnings(event)
        assert True == False, "Expected an error because test_canQueryIncomeStatementJson doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because earnings doesn't support csv"

    print(f"Querying latest earnings as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryIncomeStatementJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_income_statement_for_symbol(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query income statement {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryIncomeStatementCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_income_statement_for_symbol(event)
        assert True == False, "Expected an error because income statement doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because income statement doesn't support csv"

    print(f"Querying income statement as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryEarningsJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_earnings(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query earnings {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryEarningsCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_earnings(event)
        assert True == False, "Expected an error because earnings doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because earnings doesn't support csv"

    print(f"Querying earnings as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryLatestCashFlowJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_latest_cash_flow(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query latest cash flow {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryLatestCashFlowCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_latest_cash_flow(event)
        assert True == False, "Expected an error because latest cash flow doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because latest cash flow doesn't support csv"

    print(f"Querying latest cash flow as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canQueryCashFlowJson():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla"
    }

    try:
        results = client.get_cash_flow(event)
    except ValueError as error:
        assert error == None, error
    assert len(results) > 0, "Response should have fields but contains zero"
    assert results.get(
        'success',
        None) == True, f"success was found to be false: {results.get('Error Message', None)}"
    assert "symbol" in results, "Symbol field not present in response"
    assert "limit_reached" in results, "limit_reached is not present in results"
    assert results.get("limit_reached", None) == False, f'{results.get("Error Message", None)}'
    assert results.get("symbol", None) == event.get("symbol",
                                                    None), f"Symbol {results.get('symbol', None)} is not equal to {event.get('symbol', None)}"
    print(f"Can query cash flow {event.get('symbol', None)}")
    time.sleep(20)


@pytest.mark.integration
def test_canNotQueryCashFlowCsv():
    client = AlphavantageClient()
    event = {
        "symbol": "tsla",
        "datatype": "csv"
    }

    try:
        results = client.get_cash_flow(event)
        assert True == False, "Expected an error because cash flow doesn't support csv"
    except ValueError as error:
        assert True == True, "Expected an error because cash flow doesn't support csv"

    print(f"Querying cash flow as CSV threw error as expected {event.get('symbol', None)}")
    time.sleep(20)
