import asyncio
import websockets
import json
from secrete import Token


async def orderBookSubscribe():
    async with websockets.connect('wss://api.alor.ru/ws') as websocket:
        tickers = ['CARM', 'ENPG', 'ETLN', 'FIXP', 'GLTR', 'SFTL', 'OKEY', 'OZON', 'PEP-RM', 'POLY'] # Ваши выбранные тикеры

        for ticker in tickers:
            request = {
                "opcode": "OrderBookGetAndSubscribe",
                "code": ticker,
                "depth": 10,
                "exchange": "MOEX",
                "format": "Simple",
                "frequency": 0,
                "guid": "f35a2373-612c-4518-54af-72025384f59b",
                "token": Token.alol_token # Ваш токен доступа
            }
            await websocket.send(json.dumps(request))

        async for message in websocket:
            response = json.loads(message)
            print(response)

# Запуск асинхронного цикла для подписки на биржевой стакан
asyncio.get_event_loop().run_until_complete(orderBookSubscribe())
