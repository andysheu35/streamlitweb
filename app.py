from sqlalchemy import true
import streamlit as st
import numpy as np
import time
import pandas as pd
import plotly.graph_objects as px

st.set_page_config(layout="wide")
st.title("冰水主機節電操作")

placeholder = st.empty()
data = pd.read_csv("冰水主機節電操作結果.csv")
data1 = pd.read_csv("冰水機sv與塗料溫度.csv")
data2 = pd.read_csv("202203_v2__2_.csv")
index = 10
index1 = 10
while true:
    df = data[1:index]
    df1 = data1[1:index1]
    df2 = data2[1:index]
    temp = data1["Prediction value of prediction target"][index1]
    room_temp = data['room_temp'][index]

    power_reduce = np.sum(df["power"]) - \
        np.sum(df["Prediction value of prediction target"])

    power_reduce_percent = (power_reduce/np.sum(df["power"]))*100
    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric(label="節電量(kwh)", value=round(power_reduce, 2),
                    delta=f"{round(power_reduce_percent, 2)}%")
        col2.metric(label="塗料溫度", value=f"{round(temp, 2)}°C"
                    )
        col3.metric(label="室溫", value=f"{round(room_temp, 2)}°C"
                    )

        fig, fig1 = st.columns(2)
        with fig:
            st.markdown("### 用電量")
            chart = px.Figure()
            chart.add_trace(px.Scatter(x=df["date_time"], y=df["Prediction value of prediction target"], name="最佳化電量",
                                       line_shape='linear'))
            chart.add_trace(px.Scatter(x=df["date_time"], y=df["power"], name="原始用電量",

                                       line_shape='linear'))
            chart.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ))

            st.write(chart)
        with fig1:
            st.markdown("### 塗料溫度")
            chart = px.Figure()
            chart.add_trace(px.Scatter(x=df1["date_time"], y=df1["Prediction value of prediction target"], name="調整後塗料溫度",
                                       line_shape='linear'))
            chart.add_trace(px.Scatter(x=df1["date_time"], y=df["middle"], name="原始塗料溫度",

                                       line_shape='linear'))
            chart.add_hline(y=24)
            chart.add_hline(y=26)
            chart.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ))

            st.write(chart)

        fig2, fig3 = st.columns(2)
        with fig2:
            st.markdown("### AI冰水主機SV設定值")
            chart = px.Figure()
            chart.add_trace(px.Scatter(
                x=df["date_time"], y=df["SV"], name="AI設定SV", line_shape="linear"))
            chart.add_trace(px.Scatter(
                x=df["date_time"], y=df2["SV"], name="原始SV", line_shape="linear"))
            chart.update_layout(legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ))
            st.write(chart)
        with fig3:
            st.markdown("### 室溫")
            chart = px.Figure()
            chart.add_trace(px.Scatter(
                x=df["date_time"], y=df["room_temp"], line_shape="linear"))
            st.write(chart)
        index += 1
        index1 += 1
        if index > 416:
            index = 10
        if index1 > len(data1)-1:
            index1 = 10
        time.sleep(1.5)
