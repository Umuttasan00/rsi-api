from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

# RSI hesaplama fonksiyonu
def calculate_rsi(close_prices, period=14):
    delta = close_prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# API rotası
@app.route('/rsi', methods=['GET'])
def get_rsi():
    # URL parametresi olarak hisseyi al
    hisse = request.args.get('hisse')

    if not hisse:
        return jsonify({"error": "Lütfen hisse parametresi verin. Örnek: /rsi?hisse=AAPL"}), 400

    try:
        # Canlı veriyi çek
        data = yf.download(hisse, period="1d", interval="5m")
        if data.empty:
            return jsonify({"error": "Veri alınamadı. Hisse kodu yanlış olabilir."}), 404

        # RSI hesapla
        data["RSI"] = calculate_rsi(data["Close"])
        rsi_value = data["RSI"].iloc[-1]

        return jsonify({
            "hisse": hisse,
            "rsi": round(rsi_value, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Uygulamayı çalıştır
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=10000)

