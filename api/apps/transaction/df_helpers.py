import pandera as pa

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
