from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 👉 IMPORT YOUR PIPELINE
from prediction_engine.pipeline_run.run_pipeline import run_prediction_pipeline

app = FastAPI()

# HTML templates
templates = Jinja2Templates(directory="templates")

# ===== UI ROUTE =====
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ===== API ROUTE =====
@app.get("/predict")
def predict(ticker: str, date: str):

    try:
        result = run_prediction_pipeline(ticker, date)

        # ✅ IMPORTANT FIX (no dict inside dict mistake)
        return result  

    except Exception as e:
        return {"error": str(e)}