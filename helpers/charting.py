import base64
from io import BytesIO

import mplfinance as mpf


def generate_chart(data):
    buf = BytesIO()
    mpf.plot(data[-50:], type='candle', style='charles',
             volume=True, savefig=dict(fname=buf, dpi=100))
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
