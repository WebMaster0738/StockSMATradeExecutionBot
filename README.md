# StockSMATradeExecutionBot

from tda.auth import easy_client
from tda.client import Client
from tda.streaming import StreamClient
import pandas as pd
import asyncio
import json
import requests
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session

client = easy_client(
    api_key='AARYPZGHY9QGXQ3RBIEHFRG6XL5LETH4',
    redirect_uri='http://localhost/test',
    token_path='C:/Users/admin/PycharmProjects/pythonProject/token.pickle')
stream_client = StreamClient(client, account_id=498688834)
list1 = []
SMA5 = []
close_price = 0
count1 = 0


async def read_stream():
    await stream_client.login()
    await stream_client.quality_of_service(StreamClient.QOSLevel.EXPRESS)
    dictionary1 = {}

    def print_message(message):

        quote1 = json.dumps(message, indent=4)

        dictionary1 = message
        #print(dictionary1['content'][0]['CLOSE_PRICE'])
        df2 = pd.DataFrame(dictionary1['content'])

        close_price = float(dictionary1['content'][0]['CLOSE_PRICE'])
        list1.append(close_price)
        df2['column_number'] = close_price

        avg_5 = 0
        # with open('output.txt', 'a') as f:
        #   f.writelines(df2['column_number'].to_string() + "\n")
#change to 4 v
        if len(list1) > 4:
            avg_5 = ( list1[(len(list1) - 1)] + list1[(len(list1) - 2)] + list1[(len(list1) - 3)] + list1[
                (len(list1) - 4)] + list1[(len(list1) - 5)]) / 5

            SMA5.append(avg_5)
            df2['5sma'] = avg_5
            #print(list1)
            if (list1[len(list1) - 2] < SMA5[len(SMA5) - 2]) & (list1[len(list1) - 1] > SMA5[len(SMA5) - 1]):
                print("buy")
                print(close_price)
            elif (list1[len(list1) - 2] > SMA5[len(SMA5) - 2]) & (list1[len(list1) - 1] < SMA5[len(SMA5) - 1]):
                print("sell")
                print(close_price)
            else:
                print("Do nothing")
                print(close_price)

        else:
            SMA5.append(close_price)

            avg_5 = close_price

            print(close_price)
            client.place_order(
                498688834,  # account_id
                equity_buy_limit('LCID', 1, (close_price - 1.0))
                    .set_duration(Duration.GOOD_TILL_CANCEL)
                    .set_session(Session.SEAMLESS)
                    .build())

    # print(df2)
    #    print(list1)
    # Always add handlers before subscribing because many streams start sending
    # data immediately after success, and messages with no handlers are dropped.
    stream_client.add_chart_equity_handler(print_message)
    await stream_client.chart_equity_subs(['AAPL'])

    while True:
        await stream_client.handle_message()


asyncio.run(read_stream())
