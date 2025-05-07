from flask import Flask
from svg_api import convert_svg_to_eps_route
from florence2_api import process_image_api_route, process_image_urls_api_route

app = Flask(__name__)

app.add_url_rule('/convert_svg_to_eps', view_func=convert_svg_to_eps_route, methods=['POST'])
app.add_url_rule('/process_image', view_func=process_image_api_route, methods=['POST'])
app.add_url_rule('/process_image_urls', view_func=process_image_urls_api_route, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
