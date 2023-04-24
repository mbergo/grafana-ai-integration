from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap
import psutil
import openai
import json

# Replace with your OpenAI API key
OPENAI_API_KEY = "your_openai_api_key"

# Initialize OpenAI API client
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_system_data', methods=['GET'])
def get_system_data():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_io = psutil.disk_io_counters()
    load_avg = psutil.getloadavg()

    data = {
        "cpu_percent": cpu_percent,
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used,
            "free": memory.free,
        },
        "disk_io": {
            "read_count": disk_io.read_count,
            "write_count": disk_io.write_count,
            "read_bytes": disk_io.read_bytes,
            "write_bytes": disk_io.write_bytes,
            "read_time": disk_io.read_time,
            "write_time": disk_io.write_time,
        },
        "load_avg": load_avg,
    }

    return jsonify(data)

@app.route('/query_gpt4', methods=['GET'])
def query_gpt4():
    system_data = get_system_data()
    system_data_json = json.dumps(system_data, indent=2)

    # Create a prompt for GPT-4 based on system monitoring data
    prompt = f"Analyze the following Linux system monitoring data and suggest tuning parameters: {system_data_json}"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    gpt4_response = response.choices[0].text.strip()
    return jsonify({"suggestions": gpt4_response})

if __name__ == "__main__":
    app.run(debug=True)
