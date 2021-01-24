# import UnityEngine as ue
import pandas as pd
import data_stocks

df = pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])
df = data_stocks.GetPastData("AAPL")

# pastData = ue.GameObject.Find("PastData")
# ue.Debug.Log(pastData.name)

# def get_row():
#     for row in df['Close']:
#         time.sleep(0.1)
#         sock.send(str(row).encode("UTF-8"))

# get_row()