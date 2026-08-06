from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from scipy.sparse import hstack
from features import tokenize_url, extract_features

app = FastAPI(title="Phishing URL Classifier")

vectorizer = joblib.load("vectorizer.pkl")
model = joblib.load("model.pkl")

class URLRequest(BaseModel):
    url: str

@app.post("/predict")
def predict(request: URLRequest):
    url = request.url
    tfidf_vec = vectorizer.transform([url])
    struct_features = extract_features(url).values.reshape(1, -1)
    X = hstack([tfidf_vec, struct_features])

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0].max()

    return {
        "url": url,
        "prediction": prediction,
        "confidence": round(float(probability), 4)
    }