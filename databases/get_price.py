from datetime import datetime
import sqlite3
import requests
import click

CREATE_INVESTMENT_SQL = """PRAGMA database_list"""

def get_coin_price(coin_id, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price


@click.group()
def cli():
    pass


@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="inr")
def show_coin_price(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")


@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="inr")
@click.option("--sell", is_flag=True)
@click.option("--amount", type=float)
def add_investment(coin_id, currency, amount, sell):
    sql = "INSERT INTO investments VALUES(?,?,?,?,?)"
    values = (coin_id, currency, amount, sell, datetime.now())
    cur.execute(sql, values)
    db.commit()

    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")


cli.add_command(show_coin_price)
cli.add_command(add_investment)

if __name__ == "__main__":
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    cur.execute(CREATE_INVESTMENT_SQL)
    cli()
