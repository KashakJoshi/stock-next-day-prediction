from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 👉 your pipeline
from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# =========================
# UI
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


# =========================
# API (IMPORTANT)
# =========================
@app.get("/predict")
def predict(ticker: str, date: str):

    try:
        result = run_prediction_pipeline(ticker, date)

        return result

    except Exception as e:
        return {"error": str(e)}