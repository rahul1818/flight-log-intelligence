import streamlit as st
import pandas as pd
import requests

st.title("✈️ Flight Log Intelligence System")

file = st.file_uploader("Upload Flight Log", type=["csv"])

def ask_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response']

def convert_log_to_text(df):
    logs = []
    for index, row in df.iterrows():
        logs.append(
            f"Time: {index}, Altitude: {row['altitude']}, Speed: {row['speed']}, Pitch: {row['pitch']}, Roll: {row['roll']}"
        )
    return "\n".join(logs)

if file:
    df = pd.read_csv(file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    st.subheader("Flight Data")
    st.write(df)

    st.subheader("Altitude Graph")
    st.line_chart(df['altitude'])

    df['altitude_diff'] = df['altitude'].diff()
    df['anomaly'] = df['altitude_diff'].abs() > 50

    st.subheader("Anomalies")
    st.write(df[df['anomaly'] == True])

    if st.button("Analyze Flight"):
        prompt = f"""
Analyze flight anomalies and provide root cause.

{convert_log_to_text(df)}
"""

        result = ask_llm(prompt)
        st.subheader("AI Analysis")
        st.text(result)
