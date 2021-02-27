from tkinter import *
from tkinter import messagebox, Menu
import json
import requests
import sqlite3

pycrpto = Tk()
pycrpto.title("My Crypto Portfolio")
pycrpto.iconbitmap("favicon.ico")

con = sqlite3.connect("coin.db")
cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY,symbol TEXT,amount INTEGER,price REAL)")
con.commit()

def reset():
    for cell in pycrpto.winfo_children():
        cell.destroy()

    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        cObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notification","Portfolio cleared-add new coins")
        reset()

    def close_app():
        pycrpto.destroy()

    menu = Menu(pycrpto)
    file_item = Menu(menu)
    file_item.add_command(label="Clear portfolio",command=clear_all)
    file_item.add_command(label="Close App",command=close_app)
    menu.add_cascade(label="file",menu=file_item)
    pycrpto.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=4&convert=USD&CMC_PRO_API_KEY=4acb15d7-44c8-43f2-8bd8-fffce0f9832d")
    api = json.loads(api_request.content)

    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()

    def font_color(amount):
        if amount>0:
            return "green"
        if amount<0:
            return "red"

    def insert_coin():
        cObj.execute("INSERT INTO coin(symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(),price_txt.get(),amount_txt.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification","Coin added to portfolio successfully")
        reset()

    def update_coin():
        cObj.execute("UPDATE coin SET symbol=?,price=?,amount=? WHERE id=?",(symbol_update.get(),price_update.get(),amount_update.get(),portid_update.get()))
        con.commit()

        messagebox.showinfo("Portfolio Notification","Coin updated to portfolio successfully")
        reset()

    def delete_coin():
        cObj.execute("DELETE FROM coin WHERE id=?",(portid_delete.get(),))
        con.commit()

        messagebox.showinfo("Portfolio Notification","Coin deleted successfully")
        reset()

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,4):
        for coin in coins:
            if (api["data"][i]["symbol"])==coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid


                portfolio_id = Label(pycrpto,text=coin[0], bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrpto,text=api["data"][i]["symbol"], bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrpto,text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=coin_row, column=2, sticky=N+S+E+W)

                no_coins = Label(pycrpto,text=coin[2], bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrpto,text="${0:.2f}".format(total_paid),  bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

                current_value = Label(pycrpto,text="${0:.2f}".format(current_value),bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                current_value.grid(row=coin_row, column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrpto,text="${0:.2f}".format(pl_percoin), bg="#C0C0C0", fg=font_color(float("{0:.2f}".format(pl_percoin))),font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                totalpl = Label(pycrpto,text="${0:.2f}".format(total_pl_coin), bg="#C0C0C0", fg=font_color(float("{0:.2f}".format(total_pl_coin))),font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
                totalpl.grid(row=coin_row, column=7, sticky=N+S+E+W)

                coin_row += 1

    #insert data
    symbol_txt = Entry(pycrpto,borderwidth=2,relief="groove")
    symbol_txt.grid(row=coin_row+1,column=1)

    price_txt = Entry(pycrpto,borderwidth=2,relief="groove")
    price_txt.grid(row=coin_row+1,column=2)

    amount_txt = Entry(pycrpto,borderwidth=2,relief="groove")
    amount_txt.grid(row=coin_row+1,column=3)

    add_coin = Button(pycrpto,text="add coin", bg="#000066", fg="white",command=insert_coin,font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row+1, column=4, sticky=N+S+E+W)

    #update data
    portid_update = Entry(pycrpto,borderwidth=2,relief="groove")
    portid_update.grid(row=coin_row+2,column=0)

    symbol_update = Entry(pycrpto,borderwidth=2,relief="groove")
    symbol_update.grid(row=coin_row+2,column=1)

    price_update = Entry(pycrpto,borderwidth=2,relief="groove")
    price_update.grid(row=coin_row+2,column=2)

    amount_update = Entry(pycrpto,borderwidth=2,relief="groove")
    amount_update.grid(row=coin_row+2,column=3)

    update_coin_txt = Button(pycrpto,text="update coin", bg="#000066", fg="white",command=update_coin,font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    update_coin_txt.grid(row=coin_row+2, column=4, sticky=N+S+E+W)

    #delete coin
    portid_delete = Entry(pycrpto,borderwidth=2,relief="groove")
    portid_delete.grid(row=coin_row+3,column=0)

    delete_coin_txt = Button(pycrpto,text="delete coin", bg="#000066", fg="white",command=delete_coin,font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    delete_coin_txt.grid(row=coin_row+3, column=4, sticky=N+S+E+W)

    totalap = Label(pycrpto,text="${0:.2f}".format(total_amount_paid), bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    totalap.grid(row=coin_row, column=4, sticky=N+S+E+W)

    totalcv = Label(pycrpto,text="${0:.2f}".format(total_current_value), bg="#C0C0C0", fg="black",font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    totalcv.grid(row=coin_row, column=5, sticky=N+S+E+W)

    total_plpotfolio = Label(pycrpto,text="${0:.2f}".format(total_pl), bg="#C0C0C0", fg=font_color(float("{0:.2f}".format(total_pl))),font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    total_plpotfolio.grid(row=coin_row, column=7, sticky=N+S+E+W)

    api = ""

    refresh = Button(pycrpto,text="refresh", bg="#000066", fg="white",command=reset,font="Lato 12 ", padx="5", pady="5", borderwidth=2, relief="groove")
    refresh.grid(row=coin_row+1, column=7, sticky=N+S+E+W)

def app_header():
    portfolio_id = Label(pycrpto,text="portfolio_id", bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    name = Label(pycrpto,text="Coin Name", bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+S+E+W)

    price = Label(pycrpto,text="Price", bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    price.grid(row=0, column=2, sticky=N+S+E+W)

    no_coins = Label(pycrpto,text="Coin Owned", bg="#000066", fg="white", font="Lato 12 bold", pady="5", padx="5", borderwidth=2, relief="groove")
    no_coins.grid(row=0, column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrpto,text="Total Amount Paid",  bg="#000066", fg="white", font="Lato 12 bold", pady="5", padx="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

    current_value = Label(pycrpto,text="Current Value",bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    current_value.grid(row=0, column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrpto,text="P/L per coin", bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

    totalpl = Label(pycrpto,text="Total P/L with coin", bg="#000066", fg="white", font="Lato 12 bold", padx="5", pady="5", borderwidth=2, relief="groove")
    totalpl.grid(row=0, column=7, sticky=N+S+E+W)

app_nav()
app_header()
my_portfolio()

pycrpto.mainloop()

cObj.close()
con.close()
print("program completed")
