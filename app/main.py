import streamlit as st
from services import utils
from services.config import read_config
import yfinance as yf


def get_data(symbol):
    """Get data from config.toml
    """
    config = read_config()
    for stock in config['stocks']:
        if stock['symbol'] == symbol:
            return stock


@st.cache_data(ttl=3600)
def get_matrics():
    """Get matrics from yfinance and build a list of matrics
    """
    config = read_config()
    symbols = [symbol['symbol'] for symbol in config['stocks']]
    tickers = yf.Tickers(' '.join(symbols))
    matrics = []
    for k, v in tickers.tickers.items():
        gain = (v.info['currentPrice']/get_data(v.info['symbol'])['cost'] - 1) * 100
        matrics.append({
            'metric': {
                'label': k,
                'value': v.info['currentPrice'],
                'delta': f'{gain:.2f}%',
            },
            'meta': {
                'cost': get_data(v.info['symbol'])['cost'],
                'targetMeanPrice': v.info.get('targetMeanPrice', 0),
                'recommendationKey': v.info.get('recommendationKey', 'N/A'),
                'percent_to_target': -1 * ((v.info['currentPrice'] - v.info.get('targetMeanPrice', 0)) / v.info.get('targetMeanPrice', 0)) * 100
            }
        })
    return sorted(matrics, key=lambda x: x['meta']['percent_to_target'])


def render_metrics(matrics, num_cols=4):
    chunks = utils.chunkify(matrics, num_cols)
    cols = st.columns(num_cols)
    for i in range(num_cols):
        with cols[i]:
            for matric in chunks[i]:
                recommedationKey = matric['meta']['recommendationKey']
                st.metric(**matric['metric'])
                st.write(f"💰 {matric['meta']['cost']}")
                st.write(f"🎯 {matric['meta']['targetMeanPrice']} ({matric['meta']['percent_to_target']:.0f}%)")
                if recommedationKey == 'buy':
                    st.write(f"📊 :blue[{matric['meta']['recommendationKey']}]")
                else:
                    st.write(f"📊 :red[{matric['meta']['recommendationKey']}]")
                st.divider()


def main():
    st.title("Stockdash")
    render_metrics(get_matrics(), num_cols=4)


if __name__ == "__main__":
    main()