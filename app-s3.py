from flask import Flask, render_template
from flask import Flask, request, send_from_directory, jsonify, abort
import os
import logging
import json
import requests
from flask import Response
from urllib.parse import urlparse, parse_qs
from pathlib import Path

app = Flask(__name__)
# Constants and globals
GRAPH_DATA_REQ = {}
BASE_DIR = ''
page_id = ''
BASE_DIR_ORG = 'https://bucket-name.s3.amazonaws.com/downloads/'
BASE_MATTERPORTDL_DIR = Path(os.getcwd()).resolve()  # Use current working directory
app = Flask(__name__)

def stream_remote_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        return Response(response.iter_content(chunk_size=8192),
                        content_type=response.headers['Content-Type'])
    else:
        return Response("Error fetching file", status=response.status_code)

def get_modified_name(filename):
    basename, _, query = filename.partition("?")
    pos = basename.rfind(".")
    ext = basename[pos + 1:] if pos != -1 else ""
    basename = basename[:pos] if pos != -1 else basename
    if query:
        ext += f"?{query}"
    return f"{basename}.modified.{ext}"

def open_dir_read_graph_reqs(path, page_id):
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().startswith("get") and file.lower().endswith(".json"):
                with open(os.path.join(root, file), "r", encoding="UTF-8") as f:
                    GRAPH_DATA_REQ[file.replace(".json", "")] = f.read().replace("[MATTERPORT_MODEL_ID]", page_id)

@app.after_request
def add_custom_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


def separate_page_id(path):
    if page_id+'/' in path:
        return path.replace(page_id+'/','', 1) #remove the page_id
    else:
        return path.replace(page_id,'', 1)

@app.route("/<path:path>", methods=["GET"])
def serve_file(path):
    global page_id
    if len(path.split("/")[0]) == 11:
        if page_id != path.split("/")[0]:
            page_id = path.split("/")[0]
            open_dir_read_graph_reqs(os.path.join(BASE_MATTERPORTDL_DIR, "graph_posts"), page_id)
    elif page_id == '':
        abort(404)
    path = separate_page_id(path)
    path = path.replace('~', '_')
    print('path',path)
    BASE_DIR = f"{BASE_DIR_ORG}{page_id}"
    if not path or path == '' or path == '/':
        path = "index.html"
    modified_name = get_modified_name(path)
    modified_url = f"{BASE_DIR}/{modified_name}"
    original_url = f"{BASE_DIR}/{path}"
    # Check if the modified file exists
    response = requests.head(modified_url)
    response2 = requests.head(original_url)
    print(modified_url, original_url)
    if response.status_code == 200:
        return stream_remote_file(modified_url)
    # Check if the original file exists
    elif response2.status_code == 200:
        return stream_remote_file(original_url)
    else:
        print('Cant serve', path)
        abort(404)


@app.route("/api/mp/models/graph", methods=["POST"])
def handle_graph_post():
    try:
        data = request.json
        operation_name = data.get("operationName", "")
        if operation_name in GRAPH_DATA_REQ:
            file_path = os.path.join(BASE_DIR, f"api/mp/models/graph_{operation_name}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="UTF-8") as file:
                    return jsonify(json.loads(file.read()))
            logging.warning(f"Unknown graph operation: {operation_name}")
            return jsonify({"data": "empty"})
        return jsonify({"data": "empty"})
    except Exception as e:
        logging.error(f"Error handling POST request: {e}")
        abort(500)

@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0",port=port, debug=False)