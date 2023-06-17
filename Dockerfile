FROM python:3

WORKDIR /app

RUN pip install telethon
RUN pip install aiogram
RUN pip install requests
RUN pip install datetime
RUN pip install pytz
RUN pip install uuid
RUN pip install websockets
RUN pip install asyncio



COPY . .

CMD [ "python", "./main.py" ]