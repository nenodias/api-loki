import traceback
from datetime import datetime
from flask import Flask, request
from config_logging import handler

app = Flask(__name__)
app.logger.addHandler(handler)

@app.errorhandler(Exception)
def handle_bad_request(e):
    app.logger.error(
        "Erro desconhecido", 
        extra={"tags": {"service": "app.py", "level":"ERROR", "error": str(e), "stacktrace":traceback.format_exc()}},
    )
    return 'bad request!', 400

@app.route('/')
def index():
    app.logger.info("Hello world called", extra={"tags": {"service": "app.py", "level":"INFO"}})
    app.logger.error(
        "Something happened", 
        extra={"tags": {"service": "app.py", "level":"ERROR"}},
    )
    return "Hello world"

@app.route('/hello/<name>')
def hello(name):
    n = request.args.get('numero')
    soma = n ** 2
    app.logger.info("Hello %s called" %(name), extra={"tags": {
        "service": "app.py",
        "name": name, "timestamp": datetime.now().isoformat(),
        "level":"INFO"
        }
    })
    return "Hello %s  = %s"%(name, soma)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, load_dotenv=True)
