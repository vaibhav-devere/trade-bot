import os
import threading

from flask import Flask, render_template

from ai_updater import AIModelUpdater
from helpers.analysis import StockAnalyzer
from helpers.charting import generate_chart

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize AI Updater
ai_updater = AIModelUpdater()
ai_thread = threading.Thread(target=ai_updater.run)
ai_thread.daemon = True
ai_thread.start()


@app.route('/swing/<symbol>')
def swing_analysis(symbol):
    analyzer = StockAnalyzer(symbol, 'swing')
    return handle_analysis(analyzer, 'Swing Trading Analysis')


@app.route('/intraday/<symbol>')
def intraday_analysis(symbol):
    analyzer = StockAnalyzer(symbol, 'intraday')
    return handle_analysis(analyzer, 'Intraday Analysis')


@app.route('/holding/<symbol>')
def holding_analysis(symbol):
    analyzer = StockAnalyzer(symbol, 'holding')
    return handle_analysis(analyzer, 'Long-term Holding Analysis')


@app.route('/scan/<strategy>')
def scan_stocks(strategy):
    analyzer = StockAnalyzer(None, strategy)
    top_stocks = analyzer.get_top_stocks()
    return render_template('scan.html',
                           strategy=strategy.capitalize(),
                           stocks=top_stocks)


def handle_analysis(analyzer, title):
    if not analyzer.data_valid:
        return render_template('error.html',
                               error="Invalid stock symbol or data unavailable")

    analysis = analyzer.full_analysis()
    chart = generate_chart(analyzer.data)

    return render_template('analysis.html',
                           title=title,
                           symbol=analyzer.symbol,
                           analysis=analysis,
                           chart=chart,
                           strategy=analyzer.strategy)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
