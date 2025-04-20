import MetaTrader5 as mt5
import pandas as pd
import time

# Connect to MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MT5")
    quit()

# Define trading parameters
SYMBOL = "BTCUSD"  # Updated to BTCUSD
TIMEFRAME = mt5.TIMEFRAME_M5  # Changed to 5-minute timeframe
LOT_SIZE = 0.01
MA_PERIOD = 14  # Moving average period
SL_PIPS = 10  # Stop loss in pips
TP_PIPS = 20  # Take profit in pips

def get_data(symbol, timeframe, n):
    """Retrieve historical data for the symbol."""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    if rates is None:
        print(f"Failed to get rates for {symbol}")
        return None
    return pd.DataFrame(rates)

def calculate_moving_average(data, period):
    """Calculate simple moving average."""
    return data['close'].rolling(window=period).mean()

def place_order(symbol, action, lot, sl_pips, tp_pips):
    """Place a market order."""
    deviation = 20
    magic = 4289
    sl = mt5.symbol_info_tick(symbol).ask + sl_pips
    tp = mt5.symbol_info_tick(symbol).bid- tp_pips
    order_type_dict = {
        'buy': mt5.ORDER_TYPE_BUY,
        'sell': mt5.ORDER_TYPE_SELL
    }
    price_dict = {
        'buy': mt5.symbol_info_tick(symbol).ask,
        'sell': mt5.symbol_info_tick(symbol).bid
    }
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type_dict[action],
        "price": price_dict[action],
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": "Scalping",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,  # mt.ORDER_FILLING_FOK if IOC does not work
    }
    order_result = mt5.order_send(request)
    print(f"Order failed: {order_result}")
    return (order_result)

    # result = mt5.order_send(request)
    # if result.retcode != mt5.TRADE_RETCODE_DONE:
    #     print(f"Order failed: {result.comment} {result.retcode}")
    # else:
    #     print(f"Order placed: {action} {lot} lots of {symbol}")

# Main trading loop
try:
    while True:
        place_order(SYMBOL, 'buy', LOT_SIZE, SL_PIPS, TP_PIPS)


        # data = get_data(SYMBOL, TIMEFRAME, MA_PERIOD + 1)
        # if data is None or len(data) < MA_PERIOD + 1:
        #     time.sleep(1)
        #     continue

        # data['ma'] = calculate_moving_average(data, MA_PERIOD)
        # last_close = data['close'].iloc[-1]
        # last_ma = data['ma'].iloc[-1]

        # # Simple strategy: Buy if price > MA, Sell if price < MA
        # if last_close > last_ma:
        #     place_order(SYMBOL, "buy", LOT_SIZE, SL_PIPS, TP_PIPS)
        # elif last_close < last_ma:
        #     place_order(SYMBOL, "sell", LOT_SIZE, SL_PIPS, TP_PIPS)

        # time.sleep(60)  # Wait for the next minute
except KeyboardInterrupt:
    print("Trading stopped by user.")
finally:
    mt5.shutdown()