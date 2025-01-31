from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import ArmTracking
import openai
import os
import base64
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from environment variables or replace with your API key
openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)
uri = os.getenv("MONGODB_CONNECTION_STRING")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["rehab_data"]
collection = db["rom_data"]

# Ensure MongoDB connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
print("Collections in rehab_data:", db.list_collection_names())  # Check collections

def generate_prompt(rom):
    return f"My arm's range of motion is {rom} degrees. Suggest some exercises or advice to improve my shoulder flexibility and mobility based on my current range of motion."

def query_llm(prompt):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a physiotherapy assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error querying LLM: {e}"

def save_to_mongodb(day, rom, description, image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    document = {
        "day": day,
        "rom": rom,
        "description": description,
        "image": encoded_image
    }
    result = collection.insert_one(document)
    return result.inserted_id

@app.route('/get_rom', methods=['GET', 'POST'])
def get_rom():
    try:
        # Track arm ROM and image capture
        rom, image_path = ArmTracking.track_arm_rom()
        
        if rom is not None:
            # Generate prompt for LLM based on ROM
            prompt = generate_prompt(rom)
            
            # Query LLM for response
            llm_response = query_llm(prompt)
            
            # Get the next day value
            day = f"{len(list(collection.find({}))) + 1}"
            
            # Save data to MongoDB
            image_id = save_to_mongodb(day, rom, llm_response, image_path)
            
            # Prepare the document format to match /get_data structure
            document = {
                "_id": str(image_id),
                "day": day,
                "rom": rom,
                "description": llm_response,
                "image": image_path  # Return the image path (Base64 or URL can be handled separately in frontend)
            }

            # Return the data in the same format as /get_data
            return jsonify(document)
        else:
            return jsonify({"error": "No ROM detected."})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_images/<filename>', methods=['GET'])
def get_images(filename):
    IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "ROM_Captures")
    try:
        return send_from_directory(IMAGE_FOLDER, filename)
    except Exception as e:
        return {"error": f"File not found: {e}"}, 404
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Fetch all documents in the collection
        documents = list(collection.find({}))
        
        # Convert MongoDB ObjectId to string (needed for JSON serialization)
        for doc in documents:
            doc['_id'] = str(doc['_id'])

        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
