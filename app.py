from flask import Flask, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 15; V2437 Build/AP3A.240905.015.A2_V000L1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/150.0.7871.181 Mobile Safari/537.36",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Language': "en-US,en;q=0.9",
    'X-Requested-With': "consumerapp.bsmart.bcits.JVVNLcis",
    'Connection': "keep-alive"
}

@app.route('/get-bill/<string:k_number>', methods=['GET'])
def get_bill_details(k_number):
    target_url = f"https://api-jvvnl.bijliprabandh.com/accountdetailsByKno/{k_number}"
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    try:
        # Timeout 20 seconds set kiya gaya hai
        response = session.get(target_url, timeout=20)
        
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

    except requests.exceptions.Timeout:
        return jsonify({
            "status": "error",
            "message": "JVVNL Server Response Timeout (Server is slow or blocking Vercel IP)"
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Failed to fetch data from server",
            "error_details": str(e)
        }), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "JVVNL Bill API is live!",
        "usage": "/get-bill/<k_number>"
    })

app = app