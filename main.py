from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import random
import os

app = Flask(__name__)

# ── Load ML Model (Crop Recommendation) ──────────────────────────────────────
MODEL_PATH = "model/crop_model.pkl"
SCALER_PATH = "model/scaler.pkl"
ENCODER_PATH = "model/label_encoder.pkl"

if os.path.exists(MODEL_PATH):
    crop_model   = joblib.load(MODEL_PATH)
    scaler       = joblib.load(SCALER_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    ML_READY = True
    print("✅ Crop recommendation model loaded successfully.")
else:
    ML_READY = False
    print("⚠️  Model not found. Run train_model.py first.")

# ── Chatbot Responses ─────────────────────────────────────────────────────────
responses = {
    "hello": "Hello! How can I assist you with farming today?",
    "weather": "You can check the weather forecast on our Weather Prediction page.",
    "crop": "I can suggest suitable crops based on soil and climate conditions.",
    "irrigation": "Smart irrigation optimizes water usage for better yield.",
    "market": "You can check predicted market prices for better planning.",
    "bye": "Goodbye! Happy farming!",
    "i want basic details of paddy irrigation": (
        "To cultivate paddy, prepare well-leveled, clayey soil with proper irrigation, "
        "then sow high-quality seeds using direct seeding or transplanting methods. "
        "Maintain adequate water, fertilization, and pest control for a healthy yield."
    ),
    "how to overcome flood risks from wheat cultivation": (
        "Choose flood-tolerant wheat varieties and ensure proper field drainage through "
        "raised beds or furrow irrigation. Implement soil conservation techniques like "
        "mulching and crop rotation to improve water absorption and reduce waterlogging."
    ),
    "what is today market price of cotton in india": (
        "Cotton prices in India vary by region and quality, typically ranging from "
        "₹6,500 to ₹7,600 per quintal. Check agmarknet.gov.in for live mandi prices."
    ),
    "ok": (
        "High-yielding crops include maize, rice, and wheat for grains; soybean and "
        "groundnut for pulses; potato and tomato for vegetables. Among fruits, banana "
        "and papaya provide high yields. Proper irrigation and pest management help "
        "maximize production."
    ),
}

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/weather')
def page2_1():
    return render_template('weather.html')

@app.route('/crop')
def page2_2():
    return render_template('crop.html')

@app.route('/disease')
def page2_3():
    return render_template('disease.html')

@app.route('/market')
def page2_4():
    return render_template('market.html')

@app.route('/irrigation')
def page2_5():
    return render_template('irrigation.html')

@app.route('/chatbot')
def page2_6():
    return render_template('chatbot.html')


# ── Crop Recommendation (REAL ML MODEL) ──────────────────────────────────────
@app.route('/crop', methods=['POST'])
def crop():
    if not ML_READY:
        return jsonify({"error": "Model not loaded. Please run train_model.py first."})

    try:
        # Parse inputs from form
        N           = float(request.form.get('N', 0))
        P           = float(request.form.get('P', 0))
        K           = float(request.form.get('K', 0))
        temperature = float(request.form.get('temperature', 0))
        humidity    = float(request.form.get('humidity', 0))
        ph          = float(request.form.get('ph', 0))
        rainfall    = float(request.form.get('rainfall', 0))

        # Scale and predict
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        features_scaled = scaler.transform(features)

        # Top 3 crop predictions with probabilities
        probabilities = crop_model.predict_proba(features_scaled)[0]
        top3_indices  = probabilities.argsort()[-3:][::-1]
        top3_crops    = [
            {
                "crop": label_encoder.classes_[i],
                "confidence": f"{probabilities[i]*100:.1f}%"
            }
            for i in top3_indices
        ]

        return jsonify({
            "recommended_crop": top3_crops[0]["crop"],
            "confidence": top3_crops[0]["confidence"],
            "top_3": top3_crops,
            "inputs": {
                "N": N, "P": P, "K": K,
                "temperature": temperature,
                "humidity": humidity,
                "ph": ph,
                "rainfall": rainfall
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ── Weather (Mock — replace with real weather API) ────────────────────────────
@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location', 'Unknown')
    # TODO: Replace with OpenWeatherMap API call
    mock_weather = {
        "location": location,
        "temperature": random.randint(20, 40),
        "humidity": random.randint(40, 90),
        "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
        "note": "Mock data — integrate OpenWeatherMap API for real values."
    }
    return jsonify(mock_weather)


# ── Disease Detection (Mock — replace with CNN model) ─────────────────────────
@app.route('/disease', methods=['POST'])
def disease():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"})
    # TODO: Replace with trained CNN/image classification model
    diseases = ["Healthy", "Leaf Rust", "Blight", "Mosaic Virus"]
    return jsonify({
        "disease": random.choice(diseases),
        "note": "Mock data — integrate a trained plant disease CNN for real detection."
    })


# ── Market Price (Mock — replace with price prediction model) ─────────────────
@app.route('/market', methods=['POST'])
def market():
    crop_name = request.form.get('crop', 'Unknown')
    # TODO: Replace with time-series price prediction model
    return jsonify({
        "crop": crop_name,
        "predicted_price": random.randint(1000, 5000),
        "unit": "INR per quintal",
        "note": "Mock data — integrate a price forecasting model for real values."
    })


# ── Irrigation (Rule-based logic) ─────────────────────────────────────────────
@app.route('/irrigation', methods=['POST'])
def irrigation():
    try:
        soil_moisture = float(request.form.get('soil_moisture', 0))
        temperature   = float(request.form.get('temperature', 0))
        humidity      = float(request.form.get('humidity', 0))

        if soil_moisture < 30 and temperature > 25 and humidity < 50:
            decision = "Yes, irrigation is required."
            reason   = "Low soil moisture + high temperature + low humidity detected."
        elif soil_moisture < 30:
            decision = "Yes, irrigation is recommended."
            reason   = "Soil moisture is below the 30% threshold."
        else:
            decision = "No, irrigation is not required."
            reason   = "Soil moisture levels are sufficient."

        return jsonify({
            "soil_moisture": soil_moisture,
            "temperature": temperature,
            "humidity": humidity,
            "irrigation_needed": decision,
            "reason": reason
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ── Chatbot ───────────────────────────────────────────────────────────────────
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form.get('message', '').lower().strip()
    response = responses.get(
        user_message,
        "I'm not sure about that. Try asking about crops, irrigation, weather, or market prices."
    )
    return jsonify({"user_message": user_message, "bot_response": response})


if __name__ == '__main__':
    app.run(debug=True)
