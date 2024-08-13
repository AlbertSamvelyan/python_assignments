from flask import jsonify, request, Flask
import redis
import os
import requests
from cachetools import TTLCache
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

#Some kind of defult home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"message": "INVOKER SERVICE HOME PAGE"})

# Initialize local cache with TTL of 10 seconds and limit of 3 keys
local_cache = TTLCache(maxsize=3, ttl=10)

# Initialize Redis client
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_client = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)

# URL for the GENERATOR service
GENERATOR_URL = 'http://generator:5000/generate_recommendation'

def runcascade(user_id):
    def fetch_recommendation(model_name):
        response = requests.post(GENERATOR_URL, json={"model_name": model_name, "viewerid": user_id})
        return response.json()

    # Models for demonstration
    model_names = [f"Model{i}" for i in range(1, 6)]
    
    with ThreadPoolExecutor() as executor:
        # Fetch recommendations in parallel
        results = list(executor.map(fetch_recommendation, model_names))
    
    # Merge results (simple example: just concatenating results)
    merged_result = {"results": results}
    return merged_result

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id')
    
    # Check local cache
    if user_id in local_cache:
        return jsonify(local_cache[user_id])
    
    # Check Redis cache
    redis_result = redis_client.get(user_id)
    if redis_result:
        return jsonify(eval(redis_result))
    
    # Fetch recommendations if not in cache
    recommendations = runcascade(user_id)
    
    # Store in local cache and Redis cache
    local_cache[user_id] = recommendations
    redis_client.setex(user_id, 60, str(recommendations))  # TTL for Redis cache is 60 seconds
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
