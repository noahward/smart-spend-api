import pandas as pd
import pandera as pa
from rest_framework.exceptions import APIException

schema = pa.DataFrameSchema(
    {
        "date": pa.Column(pa.DateTime),
        "description": pa.Column(str),
        "withdrawal": pa.Column(float),
        "deposit": pa.Column(float),
        "new_balance": pa.Column(float),
    },
    strict=True,
    coerce=True,
)


def validate_df(df):
    if len(df.columns) != 5:
        raise APIException("Only unaltered TD statements are accepted")

    df.columns = ["date", "description", "withdrawal", "deposit", "new_balance"]
    df[["withdrawal", "deposit", "new_balance"]] = df[
        ["withdrawal", "deposit", "new_balance"]
    ].fillna(value=0)

    try:
        df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
    except pd.errors.OutOfBoundsDatetime:
        raise

    try:
        schema.validate(df)
    except pa.errors.SchemaError:
        raise

    return df
