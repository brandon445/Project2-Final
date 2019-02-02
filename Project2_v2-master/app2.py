import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib
import dash
import plotly
plotly.tools.set_credentials_file(username='Brybtb', api_key='50jVIE7Kj5EttwIAtSyJ')
from plotly.offline import init_notebook_mode, iplot, plot
from IPython.display import display, HTML

market_cap_stg = pd.read_csv('market_cap_stg.csv', index_col=False)
sector_stg = pd.read_csv('sector_stg.csv', index_col=False)
pe_stg = pd.read_csv('pe_stg.csv', index_col=False).fillna(0)

starting_year = 1980

def clean_df(df, value_name):
    period_colums = [x for x in df.columns if x not in ['Ticker','Company Name']]
    result = pd.melt(df, 
                     id_vars=['Ticker','Company Name'], 
                     value_vars=period_colums, 
                     var_name='Period',
                     value_name=value_name)
    result['Date'] = pd.to_datetime(result['Period'], format='%Y-%m-%d')
    result['Year'] = result['Date'].dt.year
    result['Period'] = result['Date'].dt.to_period('Q')
    del result['Date']
    return result[result.Year >= starting_year]

market_cap = clean_df(market_cap_stg, 'MarketCap')
sector = clean_df(sector_stg, 'Sector')
pe = clean_df(pe_stg, 'PE')

# remove sectors not present in 1979
valid_sectors = sector[sector.Year==starting_year].Sector.unique()
sector = sector[sector.Sector.isin(valid_sectors)]

result = market_cap.merge(sector,how='inner',on=['Ticker','Period','Year'])
result = result.merge(pe,how='inner',on=['Ticker','Period','Year'])

# number of entities per sector
company_by_sectoryear = result[result.MarketCap.notnull()][['Sector','Year','Ticker']].drop_duplicates()
company_by_sectoryear = company_by_sectoryear.groupby(['Sector','Year']).count().reset_index()
company_by_sectoryear.columns = ['Sector','Year','Count']

# remove negative PE 
result = result[(result.PE > 0) & (result.MarketCap.notnull())]

# normalize values over year range
mktcap_by_sectoryear = result[['Sector','MarketCap','Year']]
mktcap_by_sectoryear = mktcap_by_sectoryear.groupby(['Sector','Year']).mean().reset_index()
mktcap_by_sectoryear.columns = ['Sector','Year','MarketCap']

# pe wtd by marketcap
pe_avg = result[['Sector','Period','Year','PE','MarketCap']].groupby(['Sector','Period','Year'])
pe_by_pd = pe_avg.apply(lambda x: ((x['MarketCap'] * x['PE']).sum()) / x['MarketCap'].sum()).reset_index()
pe_by_pd.columns = ['Sector','Period','Year','PE']
pe_by_sectoryear = pe_by_pd[['Sector','Year','PE']].groupby(['Sector','Year']).mean().reset_index()
pe_by_sectoryear.columns = ['Sector','Year','PE']

max_mktcap = mktcap_by_sectoryear.MarketCap.max()
years = mktcap_by_sectoryear.Year.unique()[0::2]

sectors = company_by_sectoryear.Sector.unique().tolist()
company_range = [company_by_sectoryear.Count.min(), company_by_sectoryear.Count.max()]

pe_min = pe_by_sectoryear.PE.min() - 5
pe_max = pe_by_sectoryear.PE.max() + 5

# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': company_range, 'title': 'Number of Companies'}
figure['layout']['yaxis'] = {'range': [pe_min, pe_max], 'title': 'PE Ratio'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 400,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': starting_year,
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}

figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

# filter for given sector/year
def filter_sector_year(df, sector, year):
    return df[(df.Sector == sector) & (df.Year == year)]
    
# make data
year = starting_year
for sector in sectors:
    cap_x = filter_sector_year(mktcap_by_sectoryear, sector, year)
    co_x = filter_sector_year(company_by_sectoryear, sector, year)
    pe_x = filter_sector_year(pe_by_sectoryear, sector, year)
        
    data_dict = {
            'y': list(pe_x['PE']),
            'x': list(co_x['Count']),
            'mode': 'markers',
            'text': list(co_x['Sector']),
            'marker': dict(
                size=cap_x['MarketCap'],
                #sizeref=2.*max_mktcap/(40.**2)
                sizeref=max_mktcap/(15.**2)
            ),
            'name': sector
    }
    figure['data'].append(data_dict)
    
# make frames
for year in years:
    frame = {'data': [], 'name': str(year)}
    for sector in sectors:
        cap_x = filter_sector_year(mktcap_by_sectoryear, sector, year)
        co_x = filter_sector_year(company_by_sectoryear, sector, year)
        pe_x = filter_sector_year(pe_by_sectoryear, sector, year)
        
        data_dict = {
            'y': list(pe_x['PE']),
            'x': list(co_x['Count']),
            'mode': 'markers',
            'text': list(co_x['Sector']),
            'marker': dict(
                size=cap_x['MarketCap'],
                #sizeref=2.*max_mktcap/(40.**2)
                sizeref=max_mktcap/(15.**2)
            ),
            'name': sector
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': str(year),
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

    
figure['layout']['sliders'] = [sliders_dict]

plot(figure)