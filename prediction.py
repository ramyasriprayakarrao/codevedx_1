def predict_next_month(records):
    """
    Predict next month's usage with simple linear regression calculated
    using basic Python arithmetic (no sklearn or external packages).
    """
    if len(records) < 2:
        return "Please add at least 2 months of usage data before predicting."

    x_values = list(range(1, len(records) + 1))
    y_values = [float(record["units"]) for record in records]

    n = len(x_values)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    denominator = sum((x - mean_x) ** 2 for x in x_values)
    if denominator == 0:
        return "Not enough variation in the month sequence to make a prediction."

    slope = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in zip(x_values, y_values)
    ) / denominator

    intercept = mean_y - slope * mean_x
    next_month_number = n + 1
    prediction = max(0.0, intercept + slope * next_month_number)

    return (
        f"Estimated usage for the next month: {prediction:.2f} units\\n"
        "Note: This is a simple educational estimate based on the trend "
        "in the records you entered. It is not a guaranteed forecast."
    )
