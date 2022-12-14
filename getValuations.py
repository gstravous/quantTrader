import pandas as pd
import numpy as np
import math
import getFundamentalData as fun
from getVolatility import load_daily_volatility


def get_earnings_estimates_valuations():
    fun.update_earnings_estimates()
    estimates = fun.get_earnings_estimates()

    symbols = list(estimates['ticker'].unique())
    blended_estimates = pd.DataFrame({'symbol': [], 'future_blended_eps': [], 'unfac_estimate_list': []})
    for symbol in symbols:
        estimate = estimates[estimates['ticker'] == symbol]
        years = sorted(estimate['per_cal_year'])
        first_year = min(years)
        years.remove(first_year)
        year_count = len(years)
        total_factor = (year_count * (year_count + 1)) / 2

        estimate_list = []
        unfac_estimate_list = []
        for year in years:
            factored_estimate = estimate[estimate['per_cal_year'] == year].reset_index()['eps_mean_est'][0] * year_count
            unfactored_estimate = estimate[estimate['per_cal_year'] == year].reset_index()['eps_mean_est'][0]
            estimate_list.append(factored_estimate)
            unfac_estimate_list.append(unfactored_estimate)
            year_count = year_count - 1

        yr1_eps = estimate[estimate['per_cal_year'] == first_year].reset_index()['eps_mean_est'][0]
        unfac_estimate_list.append(yr1_eps)

        try: blended = ((sum(estimate_list) / total_factor) + yr1_eps) / 2
        except: blended = 0

        if blended > 0: blended_estimates = blended_estimates.append(pd.DataFrame([[symbol, blended, unfac_estimate_list]], columns=blended_estimates.columns))  # must be positive valuation

    blended_estimates['future_valuation'] = 15 * blended_estimates['future_blended_eps']

    return blended_estimates


def get_financials_valuations():
    fun.update_financials()
    financials = fun.get_financials()
    symbols = list(financials['ticker'].unique())

    financials['net_debt_to_ebitda'] = (financials['debtusd'] - financials['cashnequsd']) / financials['ebitdausd']
    financials['profit_margin'] = financials['netmargin']
    financials['diluted_eps'] = financials['epsdil']
    financials['diluted_fcfps'] = financials['fcf'] / (financials['shareswadil'] * financials['sharefactor'])
    financials['year'] = financials['calendardate'].astype(str).str[0:4].astype(float)

    financials = financials[financials['year'] >= 2016]  # don't go further back than 2016
    financials = financials.filter(['ticker', 'year', 'net_debt_to_ebitda', 'profit_margin', 'diluted_eps', 'diluted_fcfps', 'bvps'])
    blended_financials = pd.DataFrame(
         {'symbol': [], 'net_debt_to_ebitda': [], 'profit_margin': [], 'diluted_eps': [], 'diluted_fcfps': [],
          'bvps': [], 'unfac_eps_list': []})

    for symbol in symbols:
        financial = financials[financials['ticker'] == symbol]

        if not financial.empty:  # if data since 2016
            years = sorted(financial['year'])
            num_of_years = len(years)

            if num_of_years >= 5:  # min 5 yr history
                total_factor = (num_of_years * (num_of_years + 1)) / 2

                year_count = 1

                ebitda_list = []
                margin_list = []
                fac_eps_list = []
                unfac_eps_list = []
                fcfps_list = []
                bvps_list = []
                for year in years:
                    factored_ebitda = financial[financial['year'] == year].reset_index()['net_debt_to_ebitda'][0] * year_count
                    factored_margin = financial[financial['year'] == year].reset_index()['profit_margin'][0] * year_count
                    factored_eps = financial[financial['year'] == year].reset_index()['diluted_eps'][0] * year_count
                    unfactored_eps = financial[financial['year'] == year].reset_index()['diluted_eps'][0]
                    factored_fcfps = financial[financial['year'] == year].reset_index()['diluted_fcfps'][0] * year_count
                    factored_bvps = financial[financial['year'] == year].reset_index()['bvps'][0] * year_count

                    ebitda_list.append(factored_ebitda)
                    margin_list.append(factored_margin)
                    fac_eps_list.append(factored_eps)
                    unfac_eps_list.append(unfactored_eps)
                    fcfps_list.append(factored_fcfps)
                    bvps_list.append(factored_bvps)

                    year_count = year_count + 1

                blended_ebitda = (sum(ebitda_list) / total_factor)
                blended_margin = (sum(margin_list) / total_factor)
                blended_eps = (sum(fac_eps_list) / total_factor)
                blended_fcfps = (sum(fcfps_list) / total_factor)
                blended_bvps = (sum(bvps_list) / total_factor)

                if blended_eps > 0:  # must be positive valuation
                    blended_financials = blended_financials.append(
                        pd.DataFrame([[symbol, blended_ebitda, blended_margin, blended_eps, blended_fcfps, blended_bvps, unfac_eps_list]],
                                     columns=blended_financials.columns))

    blended_financials['historic_valuation'] = 15 * blended_financials['diluted_eps']

    return blended_financials


def get_valuations():
    blended_estimates = get_earnings_estimates_valuations()
    blended_financials = get_financials_valuations()
    company_info = fun.get_company_info()
    volatility = load_daily_volatility()

    company_info['symbol'] = company_info['ticker']
    company_info = company_info[company_info['currency'] == 'USD']

    valuations = pd.merge(pd.merge(pd.merge(blended_estimates, blended_financials, on='symbol'), company_info, on='symbol'), volatility, on='symbol')

    valuations['averaged_valuation'] = (2 * valuations['future_valuation'] + valuations['historic_valuation']) / 3
    valuations['eps_list'] = valuations['unfac_estimate_list'] + valuations['unfac_eps_list']
    valuations['stddev'] = valuations['eps_list'].apply(np.std)
    valuations['stdev_fact'] = 1 - ((-1 / (1 + math.e ** (valuations['stddev'] - 7))) + 1)
    valuations['ndte_factor'] = np.where(valuations['net_debt_to_ebitda'] <= 0, 1.15, np.where(valuations['net_debt_to_ebitda'] >= 8, .55, np.where((valuations['net_debt_to_ebitda'] > 0) & (valuations['net_debt_to_ebitda'] < 8), (-.075 * valuations['net_debt_to_ebitda']) + 1.15, 1)))
    valuations['factored_valuation'] = valuations['averaged_valuation'] * valuations['ndte_factor'] * valuations['stdev_fact']
    valuations['price'] = '=RTD("tos.rtd",,"MARK","' + valuations['symbol'] + '")'
    valuations['3_yr_daily_growth_rate'] = '=((AU2-AV2)/AV2)/756'
    # valuations['sharpe_ratio'] = '=((AU2-AV2)/AV2)/756'

    return valuations


get_valuations().to_csv('valuations.csv')
