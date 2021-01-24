import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib
from datetime import datetime
from datetime import timedelta
import bs4 as bs
import data_stocks
import Tkinter 
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Tkinter import *
import numpy as np
import matplotlib.pyplot as plt

# Initialisation liste pandas
df =  pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])

# Creer premiere fenetre
window = Tk()

# Personnalisation
window.title("Trading Bot")
window.geometry("1400x920")
window.minsize(1400, 920)
window.maxsize(1400, 920)
window.config(background='#3CF1E9')

# Ajouter texte
label_title = Label(window, text="Trading Algorithmique", font=("Courrier", 20), bg = '#3CF1E9')
label_title.pack()

fig = Figure(figsize=(5, 5), dpi=100)
axes = fig.add_subplot(111)
axes.plot(0)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)


# toolbar = NavigationToolbar2TkAgg(canvas, window)
# toolbar.update()
# canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)

# Affichage graph
def graph():
    df = data_stocks.GetPastData(entree.get())
    fig.add_subplot(111).plot(df['Close'])
    axes.set_ylim(df['Close'].min(), df['Close'].max())
    canvas.show()

   

# Button pour afficher le graph
my_button = Button(window, text="Graph", command=graph)
my_button.pack()

# Saisir le stock
entree = Entry(window)
entree.pack()

# Afficher
window.mainloop()

print(type(df['Close']))



# df =  pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])
# url_TEL = 'https://fr.finance.yahoo.com/quote/TEL?p=TEL'

# df = data_stocks.GetPastData("AAPL")

# for row in df['Close']:
#     print(str(row))










