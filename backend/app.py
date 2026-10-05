from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return {"message": "MediaTruth backend is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MediaTruth backend"
    }


if __name__ == "__main__":
    app.run(debug=True)