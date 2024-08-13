from flask import jsonify, request, Flask
import random

app = Flask(__name__)

#Some kind of defult home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"message": "GENERATOR SERVICE HOME PAGE:)"})

# Generator: The service that generates recommendations.
@app.route('/generate_recommendation', methods=['POST', 'GET'])
def generate_recommendation():
    if request.content_type != 'application/json':
        return jsonify({"error": f"Content-Type must be application/json: {request.content_type}"}), 400

    data = request.get_json()

    if data is None:
        return jsonify({"error": "No data was provided"}), 400

    model_name = data.get('model_name')
    viewerid = data.get('viewerid')

    if not model_name or not isinstance(model_name, str):
        return jsonify({"error": "model_name is invalid or missing"}), 400
    
    if viewerid is None or not isinstance(viewerid, int):
        return jsonify({"error": "viewer id is invalid or missing"})

    # Generate a pseudo-random number influenced by 'viewerid'
    random.seed(viewerid)  # Seed the random number generator with 'viewerid'
    random_number = random.randint(1, 100)

    response = {
        "reason" : model_name,
        "result" : random_number
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)