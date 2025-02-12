from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import ArmTracking
import openai
import os
import base64
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class Config:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.mongodb_uri = os.getenv("MONGODB_CONNECTION_STRING")

class OpenAIClient:
    def __init__(self, api_key):
        self.client = openai.Client(api_key=api_key)

    def query_llm(self, prompt):
        try:
            response = self.client.chat.completions.create(
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

class MongoDBClient:
    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["rehab_data"]
        self.collection = self.db["rom_data"]
        self.ensure_connection()

    def ensure_connection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        print("Collections in rehab_data:", self.db.list_collection_names())

    def save_to_mongodb(self, day, rom, description, image_path):
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        document = {
            "day": day,
            "rom": rom,
            "description": description,
            "image": encoded_image
        }
        result = self.collection.insert_one(document)
        return result.inserted_id

    def get_all_documents(self):
        documents = list(self.collection.find({}))
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return documents

class ROMService:
    def __init__(self, openai_client, mongodb_client):
        self.openai_client = openai_client
        self.mongodb_client = mongodb_client

    def generate_prompt(self, rom):
        return f"My arm's range of motion is {rom} degrees. Suggest some exercises or advice to improve my shoulder flexibility and mobility based on my current range of motion."

    def get_rom_data(self):
        try:
            rom, image_path = ArmTracking.track_arm_rom()
            if rom is not None:
                prompt = self.generate_prompt(rom)
                llm_response = self.openai_client.query_llm(prompt)
                day = f"{len(list(self.mongodb_client.collection.find({}))) + 1}"
                image_id = self.mongodb_client.save_to_mongodb(day, rom, llm_response, image_path)
                document = {
                    "_id": str(image_id),
                    "day": day,
                    "rom": rom,
                    "description": llm_response,
                    "image": image_path
                }
                return document
            else:
                return {"error": "No ROM detected."}
        except Exception as e:
            return {"error": str(e)}

app = Flask(__name__)
CORS(app)
config = Config()
openai_client = OpenAIClient(config.openai_api_key)
mongodb_client = MongoDBClient(config.mongodb_uri)
rom_service = ROMService(openai_client, mongodb_client)

@app.route('/get_rom', methods=['GET', 'POST'])
def get_rom():
    result = rom_service.get_rom_data()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

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
        documents = mongodb_client.get_all_documents()
        return jsonify(documents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
