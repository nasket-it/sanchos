import pandas as pd
from Config import InfoTiker, Config
import asyncio
from secrete import Token
from tinkoff import invest
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

figi = ['BBG004730ZJ9', "BBG004730N88"]
data_dict = {}

async def kjhjhgjf(di_ct):
    while True:
        await asyncio.sleep(1)
        print(di_ct)


TICKER_LIMIT = 5  # количество акций, которое обрабатывается за один запрос
SLEEP_TIME = 12  # задержка между группами запросов

# async def main1():
#     tickers = [i for i in InfoTiker.figi_reverse]  # предполагаю, что это список ваших тикеров
#     async with invest.AsyncClient(TOKEN) as client:
#         for i in range(0, len(tickers), TICKER_LIMIT):
#             subscript = [OrderBookInstrument(figi=ticker, depth=10,) for ticker in tickers[i:i+TICKER_LIMIT]]
#             async def request_iterator():
#                 yield MarketDataRequest(
#                     subscribe_order_book_request=SubscribeOrderBookRequest(
#                         subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
#                         instruments=subscript,
#                     )
#                 )
#
#                 while True:
#                     await asyncio.sleep(1)
#
#             try:
#                 async for marketdata in client.market_data_stream.market_data_stream(request_iterator()):
#                     if marketdata.orderbook:
#                         figi = marketdata.orderbook.figi
#                         bids = f'{figi} - {tuple(marketdata.orderbook.bids[i].price.units + marketdata.orderbook.bids[i].price.nano / 1e9 for i in range(10))}'
#
#                         # Проверка, есть ли уже figi в словаре
#                         if figi in data_dict:
#                             # Если figi уже есть в словаре, обновляем значения
#                             data_dict[figi] = bids
#                         else:
#                             # Если figi нет в словаре, добавляем новую записьзне
#                             data_dict[figi] = bids
#                     #pass  # сюда добавьте обработку данных стаканов, например сортировку данных
#                         # Вывод значений bids для каждого figi
#                         # print(f"{figi} - {bids}")
#                         values = data_dict.values()
#                         print(len(data_dict))

                            # print(f"{marketdata.orderbook.figi} - {marketdata.orderbook.bids}")
                        #                 h =  (marketdata.orderbook.asks[i].price.units + marketdata.orderbook.asks[i].price.nano / 1e9 for i in range(3))
                        #                 h2 =  (marketdata.orderbook.bids[i].price.units + marketdata.orderbook.bids[i].price.nano / 1e9 for i in range(3))
                        #                 tiker = InfoTiker.figi_reverse[marketdata.orderbook.figi]
                        #                 df = pd.DataFrame({(tiker ,'bids' ,  *h , 'asks' , *h2)})
                        #                 print(df)
                        #                 print(h , InfoTiker.figi_reverse[marketdata.orderbook.figi])
                        #                 print(f"{InfoTiker.figi_reverse[marketdata.orderbook.figi]} "
                        #                       f"Ask - {marketdata.orderbook.asks[0].price.units + marketdata.orderbook.asks[0].price.nano / 1e9} "
                        #                       f"Bid - {marketdata.orderbook.bids[0].price.units + marketdata.orderbook.bids[0].price.nano / 1e9}"



            # except Exception as e:
            #     print(f"Произошла ошибка при подписке на тикер: {e}")
            #
            # await asyncio.sleep(SLEEP_TIME)  # задержка между группами запросов, чтобы не превышать лимит

async def main1():
#
    subscript = [OrderBookInstrument(figi=i ,depth=10,) for i in InfoTiker.figi_reverse]
    async def request_iterator():
        yield MarketDataRequest(
            subscribe_order_book_request=SubscribeOrderBookRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments= subscript,
            )
        )
        while True:
            await asyncio.sleep(10)


    # data_dict = {}
    async with AsyncClient(TOKEN) as client:
        async for marketdata in client.market_data_stream.market_data_stream(
            request_iterator()
        ):
            if marketdata.orderbook:
                figi = marketdata.orderbook.figi
                figi_bids = f'{InfoTiker.figi_reverse[figi]}_bids'
                figi_asks = f'{InfoTiker.figi_reverse[figi]}_asks'

                bids =tuple(marketdata.orderbook.bids[i].price.units + marketdata.orderbook.bids[i].price.nano / 1e9 for i in range(10))
                asks =tuple(marketdata.orderbook.asks[i].price.units + marketdata.orderbook.asks[i].price.nano / 1e9 for i in range(10))
                print(f'{figi_bids} - {bids}')
                # Проверка, есть ли уже figi в словаре
                if figi_bids in data_dict:
                    # Если figi уже есть в словаре, обновляем значения
                    data_dict[figi_bids] = bids
                else:
                    # Если figi нет в словаре, добавляем новую записьзне
                    data_dict[figi_bids] = bids
                if figi_asks in data_dict:
                    # Если figi уже есть в словаре, обновляем значения
                    data_dict[figi_asks] = asks
                else:
                    # Если figi нет в словаре, добавляем новую записьзне
                    data_dict[figi_asks] = asks

                # Вывод значений bids для каждого figi
                # print(f"{figi} - {bids}")
                # values = f "{data_dict.keys()}  {data_dict.values()}"
            # if 'TATN_asks' in  data_dict:
            #     print(data_dict['TATN_asks'])
            #     await asyncio.sleep(1)

                    # print(f"{marketdata.orderbook.figi} - {marketdata.orderbook.bids}")
    #                 h =  (marketdata.orderbook.asks[i].price.units + marketdata.orderbook.asks[i].price.nano / 1e9 for i in range(3))
    #                 h2 =  (marketdata.orderbook.bids[i].price.units + marketdata.orderbook.bids[i].price.nano / 1e9 for i in range(3))
    #                 tiker = InfoTiker.figi_reverse[marketdata.orderbook.figi]
    #                 df = pd.DataFrame({(tiker ,'bids' ,  *h , 'asks' , *h2)})
    #                 print(df)
    #                 print(h , InfoTiker.figi_reverse[marketdata.orderbook.figi])
    #                 print(f"{InfoTiker.figi_reverse[marketdata.orderbook.figi]} "
    #                       f"Ask - {marketdata.orderbook.asks[0].price.units + marketdata.orderbook.asks[0].price.nano / 1e9} "
    #                       f"Bid - {marketdata.orderbook.bids[0].price.units + marketdata.orderbook.bids[0].price.nano / 1e9}"  )
    # #
    #             # await kjhjhgjf(ordeerbook)

            # if 'TATNP_bids' in data_dict:
            #     print(data_dict['TATNP_bids'])
            #     await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main1())
