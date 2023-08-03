
import json
import asyncio
from secrete import Token
from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
SubscribeOrderBookRequest,
OrderBookInstrument,

)
from tinkoff.invest import Client, SecurityTradingStatus
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal

TOKEN = Token.tinkov_token


# async def main():
#     async def request_iterator():
#         yield MarketDataRequest(
#             subscribe_candles_request=SubscribeCandlesRequest(
#                 subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
#                 instruments=[
#                     CandleInstrument(
#                         figi="BBG004730N88",
#                         interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
#                     )
#                 ],
#             )
#         )
#         while True:
#             await asyncio.sleep(1)
#
#     async with AsyncClient(TOKEN) as client:
#         async for marketdata in client.market_data_stream.market_data_stream(
#             request_iterator()
#         ):
#             print(marketdata.candle)
#
figi = ['BBG004730ZJ9', "BBG004730N88"]

async def main():
#     data_dict = {}  # Словарь для хранения данных по акциям
#
#     with Client(TOKEN) as client:
#         instruments: InstrumentsService = client.instruments
#         for item in instruments.shares().instruments:  # Перебираем только акции
#             ticker_data = {
#                 "name": item.name,
#                 "ticker": item.ticker,
#                 "class_code": item.class_code,
#                 "figi": item.figi,
#                 "uid": item.uid,
#                 "min_price_increment": quotation_to_decimal(item.min_price_increment),
#                 "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
#                 "lot": item.lot,
#                 "trading_status": str(SecurityTradingStatus(item.trading_status).name),
#                 "api_trade_available_flag": item.api_trade_available_flag,
#                 "currency": item.currency,
#                 "exchange": item.exchange,
#                 "buy_available_flag": item.buy_available_flag,
#                 "sell_available_flag": item.sell_available_flag,
#                 "short_enabled_flag": item.short_enabled_flag,
#                 "klong": quotation_to_decimal(item.klong),
#                 "kshort": quotation_to_decimal(item.kshort),
#             }
#             if ticker_data["exchange"] == 'MOEX':
#                 data_dict[item.ticker] = ticker_data["figi"]
#     print(data_dict)
    async def request_iterator():
        yield MarketDataRequest(
            subscribe_order_book_request=SubscribeOrderBookRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    OrderBookInstrument(
                        figi="BBG004730N88",
                        depth=1,
                    ), OrderBookInstrument(
                        figi='BBG004730ZJ9',
                        depth=1,
                    )
                ],
            )
        )
        while True:
            await asyncio.sleep(1)

    async with AsyncClient(TOKEN) as client:
        async for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            if 'orderbook' in  marketdata.orderbook:
                bids_data = marketdata.orderbook.bids

                print(bids_data)






if __name__ == "__main__":
    asyncio.run(main())
