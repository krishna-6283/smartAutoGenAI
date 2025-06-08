from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

stored_xpaths = {}

def generate_xpath(element):
    path = []
    while element.name != '[document]':
        siblings = element.find_previous_siblings(element.name)
        idx = len(siblings) + 1
        path.insert(0, f"{element.name}[{idx}]")
        element = element.parent
    return '/' + '/'.join(path)

@app.route('/extract-xpaths', methods=['GET'])
def extract_xpaths():
    try:
        # Accept both 'url' and 'normalizedUrl' for compatibility
        url = request.args.get('url') or request.args.get('normalizedUrl')
        print('Received URL:', url)
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        resp = requests.get(url, timeout=10)
        print('requests.get status:', resp.status_code)
        if resp.status_code != 200:
            return jsonify({"error": f"Failed to fetch URL: {resp.status_code}"}), 400

        soup = BeautifulSoup(resp.content, 'lxml')
        elements = soup.find_all(['input', 'button', 'select', 'textarea'])

        xpaths = []
        for el in elements:
            xpath = generate_xpath(el)
            # Prefer id, name, or class, only add xpath if none exist
            element_info = {
                'tag': el.name,
                'id': el.get('id', ''),
                'name': el.get('name', ''),
                'class': el.get('class', ''),
                'placeholder': el.get('placeholder', '')
            }
            # Only add xpath if no id, name, or class
            if not element_info['id'] and not element_info['name'] and not (element_info['class'] and len(element_info['class']) > 0):
                element_info['xpath'] = xpath
            xpaths.append(element_info)

        stored_xpaths[url] = xpaths

        return jsonify({
            "message": "XPaths extracted and stored",
            "count": len(xpaths),
            "xpaths": xpaths
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/xpaths', methods=['GET'])
def get_xpaths():
    url = request.args.get('url')
    if not url or url not in stored_xpaths:
        return jsonify({"xpaths": []}), 200
    return jsonify({"xpaths": stored_xpaths[url]}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
