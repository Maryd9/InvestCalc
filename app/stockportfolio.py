# pip install PyPortfolioOpt
# pip install yfinance --upgrade --no-cache-dir
import pandas as pd
import pypfopt.plotting as pplt
import yfinance as yf
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models, get_latest_prices, DiscreteAllocation, expected_returns
from pypfopt.cla import CLA
from matplotlib.ticker import FuncFormatter

# Получаем цены закрытия акций с фондового рынка
tickers = ['LKOH.ME', 'GAZP.ME', 'DSKY.ME', 'NKNC.ME', 'MTSS.ME', 'YNDX.ME', 'SBER.ME', 'AFLT.ME']
df_stocks = yf.download(tickers, start='2021-01-01', end='2022-12-31')['Adj Close']

# Получаем цену закрытия акций с фондового рынка
print(df_stocks.head())

# Проверяем есть ли пустые значения
nullin_df = pd.DataFrame(df_stocks, columns=tickers)
print(nullin_df.isnull().sum())

# Строим портфель с максимальным коэффициентом Шарпа и минимальной дисперсией
# Годовая доходность
mu = expected_returns.mean_historical_return(df_stocks)
# Дисперсия портфеля
Sigma = risk_models.sample_cov(df_stocks)
# Максимальный коэффициент Шарпа
ef = EfficientFrontier(mu, Sigma, weight_bounds=(0, 1))

weights = ef.max_sharpe()
# Усекаем крошечные веса до нуля и округляем остальные, приводим к красивому виду веса
sharpe_pfolio = ef.clean_weights()
print(sharpe_pfolio)
ef.portfolio_performance(verbose=True)

# Строим портфель с минимальной волатильностью

ef1 = EfficientFrontier(mu, Sigma, weight_bounds=(0, 1))
minvol = ef1.min_volatility()
minvol_pwt = ef1.clean_weights()
print(minvol_pwt)
ef1.portfolio_performance(verbose=True, risk_free_rate=0.27)

# Строим график эффективных границ
cl_obj = CLA(mu, Sigma)
ax = pplt.plot_efficient_frontier(cl_obj, showfig=False)
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))

# Считаем первый портфель
latest_prices = get_latest_prices(df_stocks)
allocation_minv, rem_minv = DiscreteAllocation(minvol_pwt, latest_prices, total_portfolio_value=100000).lp_portfolio()
print(allocation_minv)
print("Осталось денежных средств после построения портфеля с минимальной волатильностью - {:.2f} рублей".format(rem_minv))
print()

# Считаем второй портфель
latest_prices1 = get_latest_prices(df_stocks)
allocation_shp, rem_shp = DiscreteAllocation(sharpe_pfolio, latest_prices1, total_portfolio_value=100000).lp_portfolio()
print(allocation_shp)
print("Осталось денежных средств после построения портфеля с максимальным коэффициентом Шарпа {:.2f} рублей".format(rem_shp))
