import pandas as pd
from pykrakenapi import KrakenAPI
import krakenex
from forex_python.converter import CurrencyRates


cost_treshold = 0.1
just_default = 14
round_default = 4

df = pd.read_csv(r'trades.csv')
keep_cols = ['time', 'pair', 'type', 'cost', 'fee', 'vol']
df = df[keep_cols]
euro_to_czk = CurrencyRates().get_rate('EUR', 'CZK')


def notation(col: pd.Series) -> list:
    return [float('%f' % x) for x in col.tolist()]


def f(x, just=just_default, decimal_places=round_default):
    if not isinstance(x, str):
        x = str(round(x, decimal_places))
    return x.ljust(just)


def get_price(token):
    ohlc, _ = KrakenAPI(krakenex.API()).get_ohlc_data(token)
    price = float(ohlc.head(1)['open'])
    return price


vol = notation(df['vol'])
df = df.drop([x[0] for x in enumerate(vol) if x[1] < cost_treshold])
df.reset_index(drop=True, inplace=True)

coins = list(set(df['pair'].to_list()))
coin_dfs = {coin: [] for coin in coins}

for index, row in df.iterrows():
    coin_dfs[row['pair']].append(row)

for k, v in coin_dfs.items():
    coin_dfs[k] = pd.DataFrame(v)
    coin_dfs[k].reset_index(drop=True, inplace=True)


def coin_analysis(coin):
    print()
    print(coin)
    df = coin_dfs[coin]
    header_items = 'typ', 'avg', 'tokens', 'eur', 'tot_tokens', 'tot_eur', 'fee', 'tot_fees', 'time'
    header = '+'.join([f"f('{x}')" for x in header_items])
    _eval = header.replace("'", '')
    print(eval(header))

    tot_tokens, tot_eur, tot_fees = 0, 0, 0
    for index, row in df.iterrows():
        time = row['time']
        fee = row['fee']
        tot_fees += fee
        typ = row['type']
        sell = -1 if typ == 'sell' else 1
        eur = row['cost'] * -sell
        tokens = row['vol'] * sell
        avg = -eur / tokens
        tot_eur += eur
        tot_tokens += tokens
        if tot_tokens <= cost_treshold:  # stake
            tot_tokens = 0
            tot_avg = 0
        else:
            tot_avg = abs(tot_eur / tot_tokens)

        print(eval(_eval))

    if tot_avg <= cost_treshold:
        profit = round(tot_eur, round_default)
        print('You exited with:', profit, ' Euro')
    else:
        print('Your average is:', round(tot_avg, round_default), ' Euro/token')
        current_price = get_price(coin)
        current_net = tot_tokens * current_price
        profit = current_net + tot_eur
        print('Your profit is: ', profit, ' Euro')
    return profit


total_profit = 0
for coin in coin_dfs.keys():
    total_profit += coin_analysis(coin)

print('\nYour total profit is:  ', total_profit, 'Euro', ' or ', total_profit * euro_to_czk, ' CZK')
