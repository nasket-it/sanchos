import pandas as pd
from Config import InfoTiker, Config
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


async def kjhjhgjf(di_ct):
    while True:
        await asyncio.sleep(1)
        print(di_ct)
async def main():
    data_dict = {}  # Словарь для хранения данных по акциям

    # with Client(TOKEN) as client:
    #     instruments: InstrumentsService = client.instruments
    #     for item in instruments.shares().instruments:  # Перебираем только акции
    #         ticker_data = {
    #             "name": item.name,
    #             "ticker": item.ticker,
    #             "class_code": item.class_code,
    #             "figi": item.figi,
    #             "uid": item.uid,
    #             "min_price_increment": quotation_to_decimal(item.min_price_increment),
    #             "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
    #             "lot": item.lot,
    #             "trading_status": str(SecurityTradingStatus(item.trading_status).name),
    #             "api_trade_available_flag": item.api_trade_available_flag,
    #             "currency": item.currency,
    #             "exchange": item.exchange,
    #             "buy_available_flag": item.buy_available_flag,
    #             "sell_available_flag": item.sell_available_flag,
    #             "short_enabled_flag": item.short_enabled_flag,
    #             "klong": quotation_to_decimal(item.klong),
    #             "kshort": quotation_to_decimal(item.kshort),
    #         }
    #         if ticker_data["ticker"] in  Config.tickers_moex:
    #             data_dict[item.ticker] = ticker_data["figi"]
    # print(data_dict)
    orderbook = {}
    # subscript = [OrderBookInstrument(figi=i ,depth=10,) for i in InfoTiker.figi_reverse]
    # async def request_iterator():
    #     yield MarketDataRequest(
    #         subscribe_order_book_request=SubscribeOrderBookRequest(
    #             subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
    #             instruments= subscript,
    #         )
    #     )
    #     while True:
    #         await asyncio.sleep(1)
    #
    # async with AsyncClient(TOKEN) as client:
    #     async for marketdata in client.market_data_stream.market_data_stream(
    #         request_iterator()
    #     ):
    #         if marketdata.orderbook:
    #
    #
    #                 # print(marketdata.orderbook.bids)
    #                 h =  (marketdata.orderbook.asks[i].price.units + marketdata.orderbook.asks[i].price.nano / 1e9 for i in range(3))
    #                 h2 =  (marketdata.orderbook.bids[i].price.units + marketdata.orderbook.bids[i].price.nano / 1e9 for i in range(3))
    #                 tiker = InfoTiker.figi_reverse[marketdata.orderbook.figi]
    #                 df = pd.DataFrame({(tiker ,'bids' ,  *h , 'asks' , *h2)})
    #                 print(df)
                    # print(h , InfoTiker.figi_reverse[marketdata.orderbook.figi])
                    # print(f"{InfoTiker.figi_reverse[marketdata.orderbook.figi]} "
                    #       f"Ask - {marketdata.orderbook.asks[0].price.units + marketdata.orderbook.asks[0].price.nano / 1e9} "
                    #       f"Bid - {marketdata.orderbook.bids[0].price.units + marketdata.orderbook.bids[0].price.nano / 1e9}"  )

                # await kjhjhgjf(ordeerbook)



if __name__ == "__main__":
    asyncio.run(main())
