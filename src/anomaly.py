def detect_anomalies(df, threshold=50):
    df['altitude_diff'] = df['altitude'].diff()
    df['anomaly'] = df['altitude_diff'].abs() > threshold
    return df
