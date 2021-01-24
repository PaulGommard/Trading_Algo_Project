import socket
import time
import pandas as pd
import data_stocks

host, port = "192.168.0.41", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
# url_TEL = 'https://fr.finance.yahoo.com/quote/TEL?p=TEL'
# price = data.GetActualPrice(url_TEL)

# df = pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])
# df = data_stocks.GetPastData("AAPL")
# # df = df.iloc[2]
# # df = df.astype(str)
# print(df)

# def get_row():
#     for row in df['Close']:
#         time.sleep(0.1)
#         sock.send(str(row).encode("UTF-8"))

# get_row()

while True:
    
    time.sleep(0.5) #sleep 0.5 sec
    receivedData = sock.recv(1024).decode("UTF-8") #receiveing data in Byte fron C#, and converting it to String
    print("DATE RECU")
    print(receivedData)

    if(receivedData == 'test'):
        print("tamere")
    

# startPos = [0, 0, 0] #Vector3   x = 0, y = 0, z = 0
# while True:
#     time.sleep(0.5) #sleep 0.5 sec
#     startPos[0] +=1 #increase x by one
#     posString = ','.join(map(str, startPos)) #Converting Vector3 to a string, example "0,0,0"
#     print(posString)

#     sock.sendall(posString.encode("UTF-8")) #Converting string to Byte, and sending it to C#
#     receivedData = sock.recv(1024).decode("UTF-8") #receiveing data in Byte fron C#, and converting it to String
#     print(receivedData)
