from flask import Flask
from svg_api import convert_svg_to_eps_route
from florence2_api import process_image_api_route, process_image_urls_api_route
from oss_api import upload_file_to_oss_route
from img2video_api import process_images_to_video_route
from svg2cmyk_api import convert_svg_to_cmyk_pdf_route
from img2square_api import process_images_to_square_route

app = Flask(__name__)

app.add_url_rule(
    "/convert_svg_to_eps", view_func=convert_svg_to_eps_route, methods=["POST"]
)
app.add_url_rule("/process_image", view_func=process_image_api_route, methods=["POST"])
app.add_url_rule(
    "/process_image_urls", view_func=process_image_urls_api_route, methods=["POST"]
)
app.add_url_rule("/upload_to_oss", view_func=upload_file_to_oss_route, methods=["POST"])
app.add_url_rule(
    "/create_video", view_func=process_images_to_video_route, methods=["POST"]
)
app.add_url_rule(
    "/convert_svg_to_cmyk_pdf",
    view_func=convert_svg_to_cmyk_pdf_route,
    methods=["POST"],
)
app.add_url_rule(
    "/convert_to_square",
    view_func=process_images_to_square_route,
    methods=["POST"],
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
