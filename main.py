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

from fastapi import FastAPI, Request, Form
import sqlite3, config
from fastapi.templating import Jinja2Templates
from datetime import date
from fastapi.responses import RedirectResponse
import pandas as pd
from pychartjs import BaseChart, ChartType, Color 
from flask import Flask, render_template, jsonify
import json, random
from django.shortcuts import render
from random import sample
import backtesting_macd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    stock_filter = request.query_params.get('filter', False)

    # Get the app data already created
    connection = sqlite3.connect(config.DATA_BASE)
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
        cursor.execute("""
            select * from (
                select symbol, name, stock_id, max(close), date
                from stock_price join stock on stock.id = stock_price.stock_id
                group by stock_id
                order by symbol
            ) where date =  ?
            """, (date.today().isoformat(),))
    else:
        # Get symbol and company from the database
        cursor.execute("""SELECT symbol, name FROM stock ORDER by symbol""")

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    # Get the app data already created
    connection = sqlite3.connect(config.DATA_BASE)
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM strategy
        """)

    strategies = cursor.fetchall()

    # Get symbol and company from the database
    cursor.execute("""SELECT id, symbol, name FROM stock WHERE symbol = ?""", (symbol,))
    row = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC
    """, (row['id'],))
    prices = cursor.fetchall()


    # Get symbol and company from the database
    cursor.execute("""SELECT * FROM twitter_analysis where stock_id = (?)""", (row['id'],))

    #df = pd.read_sql_query(f"""SELECT close FROM stock_price_minutes where stock_id = 9074""" ,connection)

    sentiments = cursor.fetchall()
    polaritys = []
    dates = []
    volumes = []

    for sentiment in sentiments:
        polarity = sentiment['polarity']
        polaritys.append(polarity)
        date = sentiment['date']
        dates.append(date)
        volume = sentiment['volume']
        volumes.append(volume)

    polaritys = [float(i) for i in polaritys]
    volumes= [float(i) for i in volumes]

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices, "strategies": strategies,"polaritys": polaritys, "dates": dates, "volumes": volumes})


@app.post("/apply_strategy")
def apply_strategy(strategy_id: int = Form(...), stock_id: int = Form(...)):
    connection = sqlite3.connect(config.DATA_BASE)
    cursor = connection.cursor()
    
    cursor.execute("""
        INSERT INTO stock_strategy (stock_id, strategy_id) VALUES (?, ?)
        """, (stock_id, strategy_id))

    connection.commit()

    return RedirectResponse(url=f"/strategy/{strategy_id}", status_code=303)


@app.get("/strategy/{strategy_id}")
def strategy(request: Request, strategy_id):
    # Get the app data already created
    connection = sqlite3.connect(config.DATA_BASE)
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name
        FROM strategy
        WHERE id = ?
        """, (strategy_id,))

    strategy = cursor.fetchone()

    cursor.execute("""
        SELECT symbol, name
        FROM stock JOIN stock_strategy on stock_strategy.stock_id = stock.id
        WHERE strategy_id = ?
        """, (strategy_id,))
    
    stocks = cursor.fetchall()

    return templates.TemplateResponse("strategy.html", {"request": request, "stocks": stocks, "strategy": strategy})

@app.post("/backtesting")
def backtesting(strategy_id: int = Form(...), stock_id: int = Form(...)):

    return RedirectResponse(url=f"/backtesting/{strategy_id}/{stock_id}", status_code=303)

@app.get("/backtesting/{startegy_id}/{stock_id}")
def apply_backtesting(request: Request, stock_id):
    # Get the app data already created
    connection = sqlite3.connect(config.DATA_BASE)
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    # Get symbol and company from the database
    cursor.execute("""SELECT id, symbol, name FROM stock WHERE id = ?""", (stock_id,))
    stock = cursor.fetchone()
    print(stock['symbol'])
    df = backtesting_macd.BackTestingMACD(backtesting_macd.GetPastData(stock['symbol']))

    MACD = [float(i) for i in df['MACD']]
    e9 = [float(i) for i in df['e9']]
    closes = [float(i) for i in df['Close']]
    dates = [str(i) for i in df['Date']]

    df_filtred = df[(df.Order == 'buy') | (df.Order == 'sell')]
    closes_order = [float(i) for i in df_filtred['Close']]
    
    benefice = backtesting_macd.CalculateBenef(df)
    print(benefice)
    
    return templates.TemplateResponse("backtesting_macd.html", {"request": request, "stock": stock, "MACD": MACD, 'e9': e9, "closes": closes, "dates": dates,"closes_order": closes_order , "df_order": df_filtred.to_dict(orient='records'), "benefice": benefice})

@app.get("/test")
def test(request: Request):

    # Get the app data already created
    connection = sqlite3.connect(config.DATA_BASE)
    connection.row_factory = sqlite3.Row

    # Create connection
    cursor = connection.cursor()

    # Get symbol and company from the database
    cursor.execute("""SELECT * FROM stock_price_minutes where stock_id = 9074""")

    #df = pd.read_sql_query(f"""SELECT close FROM stock_price_minutes where stock_id = 9074""" ,connection)

    rows = cursor.fetchall()
    closes = []
    dates = []

    for row in rows:
        close = row['close']
        closes.append(close)
        date = row['date']
        dates.append(date)

    closes = [float(i) for i in closes]
    data = json.dumps(closes)
    labels = json.dumps(dates)
    
    return templates.TemplateResponse("test.html", {"request": request, "stocks": closes, "dates": dates})
    
