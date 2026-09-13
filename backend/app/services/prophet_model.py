"""Prophet time-series model for cash flow prediction."""
import pandas as pd
from prophet import Prophet


def predict_prophet(df: pd.DataFrame, company_id: int, horizon: int = 3):
    df = df.sort_values("period").reset_index(drop=True)
    if len(df) < 6:
        raise ValueError("Need at least 6 periods")

    prophet_df = pd.DataFrame({
        "ds": pd.to_datetime(df["period"] + "-01"),
        "y": df["operating_cash_flow"].astype(float),
    })

    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
    )
    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=horizon, freq="MS")
    forecast = model.predict(future)
    tail = forecast.tail(horizon)

    return {
        "predictions": tail["yhat"].round(2).tolist(),
        "lower_bound": tail["yhat_lower"].round(2).tolist(),
        "upper_bound": tail["yhat_upper"].round(2).tolist(),
        "model": "Prophet",
    }
