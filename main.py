from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

responses = {
    "hello": "Hello! How can I assist you with farming today?",
    "weather": "You can check the weather forecast on our Weather Prediction page.",
    "crop": "I can suggest suitable crops based on soil and climate conditions.",
    "irrigation": "Smart irrigation optimizes water usage for better yield.",
    "market": "You can check predicted market prices for better planning.",
    "bye": "Goodbye! Happy farming!",
    "i want basic details of paddy irrigation":"To cultivate paddy, prepare well-leveled, clayey soil with proper irrigation, then sow high-quality seeds using direct seeding or transplanting methods. Maintain adequate water, fertilization, and pest control for a healthy yield.",
    "how to overcome flood risks from wheat cultivation":"To overcome flood risks in wheat cultivation, choose flood-tolerant wheat varieties and ensure proper field drainage through raised beds or furrow irrigation. Additionally, implement soil conservation techniques like mulching and crop rotation to improve water absorption and reduce waterlogging.",
    "what is today market price of cotton in india":"As of February 22, 2025, the most recent available data indicates that cotton prices in India vary by region and quality. For instance, on February 17, 2025, prices ranged from ₹6,500 to ₹7,600 per quintal across different markets",
    "ok":"The best high-yielding crops include maize, rice, and wheat for grains, soybean and groundnut for pulses, and potato and tomato for vegetables. Among fruits, banana and papaya provide high yields, while sugarcane and cotton are profitable cash crops. Proper irrigation, high-quality seeds, and good pest management help maximize production.",
}

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

# Weather Prediction Route (Mock API Call)
@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('location')
    mock_weather = {"temperature": random.randint(20, 40), "condition": "Sunny"}
    return jsonify(mock_weather)

# Crop Recommendation Route (Mock Recommendation)
@app.route('/crop', methods=['POST'])
def crop():
    soil = request.form.get('soil')
    climate = request.form.get('climate')
    
    # Mock Crop Recommendations (Replace with ML model later)
    recommendations = {
        "loamy-warm": ["Wheat", "Maize"],
        "clayey-humid": ["Rice", "Sugarcane"],
        "sandy-dry": ["Millets", "Groundnut"]
    }
    
    key = f"{soil}-{climate}"
    recommended_crops = recommendations.get(key, ["No recommendation available"])
    
    return jsonify({"recommended_crops": recommended_crops})

# Disease Detection Route (Mock Detection)
@app.route('/disease', methods=['POST'])
def disease():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"})
    
    image = request.files['image']
    
    # Mock Disease Detection (Replace with ML model later)
    diseases = ["Healthy", "Leaf Rust", "Blight", "Mosaic Virus"]
    detected_disease = random.choice(diseases)
    
    return jsonify({"disease": detected_disease})

# Market Price Prediction Route (Mock Price Prediction)
@app.route('/market', methods=['POST'])
def market():
    crop = request.form.get('crop')
    mock_price = random.randint(1000, 5000)
    return jsonify({"predicted_price": mock_price})

# Smart Irrigation Route (Mock Optimization)
@app.route('/irrigation', methods=['POST'])
def irrigation():
    soil_moisture = float(request.form.get('soil_moisture'))
    temperature = float(request.form.get('temperature'))
    humidity = float(request.form.get('humidity'))
    
    # Mock Irrigation Decision (Replace with AI Model later)
    if soil_moisture < 30 and temperature > 25 and humidity < 50:
        irrigation_needed = "Yes, irrigation is required."
    else:
        irrigation_needed = "No, irrigation is not required."
    
    return jsonify({"soil_moisture": soil_moisture, "temperature": temperature, "humidity": humidity, "irrigation_needed": irrigation_needed})

# AI Chatbot Route (Mock Chatbot Response)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.form.get('message').lower()
    response = responses.get(user_message, "I'm not sure about that. Can you ask something else?")
    
    return jsonify({"user_message": user_message, "bot_response": response})

if __name__ == '__main__':
    app.run(debug=True)