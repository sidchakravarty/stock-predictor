from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from model import predict, convert

app = FastAPI()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

# pydantic model
class StockIn(BaseModel):
    ticker: str
    days: int

class StockOut(StockIn):
    forecast: dict


@app.post("/predict", response_model=StockOut, status_code=200)
def get_prediction(payload: StockIn):
    ticker = payload.ticker
    days = payload.days

    predictions = predict(ticker, days)

    if not predictions:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {
        "ticker": ticker, 
        "days": days,
        "forecast": convert(predictions)}
    return response_object

# (sp-fastapi) sid@deeplearningrig:~/FourthBrain/stock-predictor/app$ /home/sid/anaconda3/envs/sp-fastapi/bin/uvicorn  main:app --reload
# http://127.0.0.1:8000/docs#/default/get_prediction_predict_post