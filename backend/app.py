from flask import Flask, jsonify
import azure.functions as func

# Create Flask app
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Hello from Flask in Azure Function (Python 3.11)!"})

# Azure Function HTTP Trigger
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="/")
def main(req: func.HttpRequest) -> func.HttpResponse:
    with flask_app.test_request_context(
        path=req.url,
        method=req.method,
        data=req.get_body(),
        headers=req.headers
    ):
        response = flask_app.full_dispatch_request()
        return func.HttpResponse(
            response.get_data(as_text=True),
            status_code=response.status_code,
            mimetype=response.mimetype
        )
