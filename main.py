# import requests
# from bs4 import BeautifulSoup
# import time
# import pandas as pd
# import matplotlib
# from datetime import datetime
# from datetime import timedelta
# import bs4 as bs
# import data_stocks
# import tkinter
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
# from tkinter import *
# import tkinter.ttk as tkk
# import numpy as np
# import matplotlib.pyplot as plt

# # Initialisation liste pandas
# df =  pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])

# # Creer premiere fenetre
# window = Tk()

# # Personnalisation
# window.title("Trading Bot")
# window.geometry("1920x1080")
# window.minsize(1920, 1080)
# window.maxsize(1920, 1080)
# window.config(background='#3CF1E9')

# # Ajouter texte
# label_title = Label(window, text="Trading Algorithmique", font=("Courrier", 20), bg = '#3CF1E9')
# label_title.pack(pady=5)

# # # Canvas for graph
# # canvasGraph = Canvas(window, height = 500, width = 1500)
# # canvasGraph.pack(pady=30)

# # Figure for stock graph
# fig = Figure(figsize=(22,5), dpi=80, facecolor='white')
# axes = fig.add_subplot(111)
# axes.plot(0)

# # Insert the matplotlib graph into the canvasGraph
# canvas = FigureCanvasTkAgg(fig, master=window)
# canvas.draw()
# canvas.get_tk_widget().pack(pady=20)

# # Figure for stock graph
# figMACD = Figure(figsize=(22,2), dpi=80, facecolor='white')
# axes = fig.add_subplot(111)
# axes.plot(0)

# canvasMACD = FigureCanvasTkAgg(figMACD, master=window)
# canvasMACD.draw()
# canvasMACD.get_tk_widget().pack(pady=5)

# # # Toolbar og the graph
# # toolbar = NavigationToolbar2Tk(canvas, window)
# # toolbar.update()
# # canvas.get_tk_widget().pack()

# # Table of buy and sell
# table = LabelFrame(window, text="Buy and sell",  height = 200, width = 1400)
# table.pack(pady = 20)

# colonne = tkk.Treeview(table, columns=(1,2,3,4), show="headings", height="6")
# colonne.pack()

# colonne.heading(1, text="Date")
# colonne.heading(2, text="Close")
# colonne.heading(3, text="MACD")
# colonne.heading(4, text='e9')

# # Put the value og the stock in the table
# def PutValueOnTable(stk):
#     df = data_stocks.GetPastData(stk)
#     for index, row in df.iterrows():
#         colonne.insert('', 'end',value=("Date", row['Close'], row['MACD'],row['e9']))

# # Affichage graph
# def graph():
#     # Clear the table
#     ClearTable()
#     # Clear the graph
#     fig.clf()
#     # Get the date of the stock
#     df = data_stocks.GetPastData(entree.get())
#     fig.add_subplot(111).plot(df['Close'])
#     # Zoom on the stock
#     axes.set_ylim(df['Close'].min(), df['Close'].max())
#     canvas.draw()
#     # Put all the value on the table
#     PutValueOnTable(entree.get())

# # Clear the table
# def ClearTable():
#     for i in colonne.get_children():
#         colonne.delete(i)

# # Button pour afficher le graph
# my_button = Button(window, text="Graph", command=graph)
# my_button.pack()

# # Saisir le stock
# entree = Entry(window)
# entree.pack()

# # Afficher
# window.mainloop()

# # df =  pd.DataFrame(columns=['Close', 'e9', 'MACD', 'e26', 'lastClose', 'e12', 'Position'])
# # url_TEL = 'https://fr.finance.yahoo.com/quote/TEL?p=TEL'

# # df = data_stocks.GetPastData("AAPL")

# # for row in df['Close']:
# #     print(str(row))

from fastapi import FastAPI, Request
import sqlite3, config
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    # Get the app data already created
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    # Get symbol and company from the database
    cursor.execute("""SELECT symbol, name FROM stock ORDER by symbol""")
    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    # Get the app data already created
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    # Get symbol and company from the database
    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""", (symbol,))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
    """, (row['id'],))
    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "prices": prices})






