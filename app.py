from flask import Flask, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 15; V2437 Build/AP3A.240905.015.A2_V000L1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/150.0.7871.181 Mobile Safari/537.36",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'sec-ch-ua-platform': '"Android"',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Android WebView";v="150"',
    'sec-ch-ua-mobile': "?1",
    'X-Requested-With': "consumerapp.bsmart.bcits.JVVNLcis",
    'Sec-Fetch-Site': "cross-site",
    'Sec-Fetch-Mode': "cors",
    'Sec-Fetch-Dest': "empty",
    'Accept-Language': "en-US,en;q=0.9"
}

@app.route('/get-bill/<string:k_number>', methods=['GET'])
def get_bill_details(k_number):
    target_url = f"https://api-jvvnl.bijliprabandh.com/accountdetailsByKno/{k_number}"
    
    try:
        response = requests.get(target_url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "status": "success",
                "data": response.json()
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Upstream API error code {response.status_code}"
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch data from server",
            "error_details": str(e)
        }), 500

# Root endpoint testing ke liye
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "JVVNL Bill API is live!",
        "usage": "/get-bill/<k_number>"
    })

# Vercel Serverless entry point
app = app
