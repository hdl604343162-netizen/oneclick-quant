# app_desktop_csv.py
import os, sys, json, glob, subprocess
import pandas as pd
import numpy as np
import streamlit as st
from io_helpers import read_any

APP_DATA_DIR = "./data"; APP_OUT_DIR = "./bt_out"
os.makedirs(APP_DATA_DIR, exist_ok=True); os.makedirs(APP_OUT_DIR, exist_ok=True)
PY = sys.executable
st.set_page_config(page_title="One-Click Quant (CSV build)", layout="wide")
st.title("🧩 一键量化（CSV兼容版，无需安装任何编译工具）")
st.info("此版本默认用 CSV 存取，避免安装 pyarrow/fastparquet。若你已具备 Parquet 引擎，依然可以上传/读取 Parquet。")

tabs = st.tabs(["下载数据","单品种回测示例","组合回测示例","看板/导出"])

def run_cmd(args, timeout=None):
    try:
        p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        return p.returncode==0, p.stdout
    except Exception as e:
        return False, str(e)

with tabs[0]:
    st.header("下载历史数据")
    symbol = st.text_input("交易对", "BTCUSDT")
    interval = st.selectbox("K线周期", ["1m","5m","15m","30m","1h","4h","1d","1w","1M"], index=5)
    start = st.text_input("开始时间", "2024-01-01")
    end = st.text_input("结束时间", "2024-03-01")
    if st.button("下载K线（保存CSV）", use_container_width=True):
        ok, log = run_cmd([PY,"quant_tool.py","download","--dtype","klines","--symbol",symbol,"--interval",interval,"--start",start,"--end",end,"--out",APP_DATA_DIR,"--fmt","csv"])
        st.success("完成" if ok else "失败"); st.code(log)

with tabs[1]:
    st.header("单品种回测（CSV）")
    pattern = st.text_input("CSV 路径/通配", "./data/klines_BTCUSDT_1h_*.csv")
    if st.button("运行示例MA20/50"):
        ok, log = run_cmd([PY,"quant_tool.py","backtest","--data",pattern,"--fast","20","--slow","50","--fee-bps","1","--slip-bps","1","--initial-cash","10000","--out",APP_OUT_DIR,"--fmt","csv"])
        st.success("完成" if ok else "失败"); st.code(log)

with tabs[2]:
    st.header("组合回测（CSV）")
    tasks = st.text_area("组合任务 JSON", value='''[
  {"symbol":"BTCUSDT","pattern":"./data/klines_BTCUSDT_1h_*.csv","strategy":"MA","params":{"fast":20,"slow":50}},
  {"symbol":"ETHUSDT","pattern":"./data/klines_ETHUSDT_1h_*.csv","strategy":"MOMENTUM","params":{"lookback":60}}
]''', height=160)
    if st.button("运行组合（invvol）"):
        ok, log = run_cmd([PY,"backtest_cli.py","--tasks",tasks,"--allocator","invvol","--lookback","60","--fee-bps","1","--slip-bps","1","--out",APP_OUT_DIR])
        st.success("完成" if ok else "失败"); st.code(log)

with tabs[3]:
    st.header("看板/导出")
    up = st.file_uploader("上传 portfolio_equity（CSV 或 Parquet——若你的环境支持）", type=["csv","parquet"])
    if up:
        if up.name.endswith(".csv"):
            df = pd.read_csv(up)
        else:
            try:
                df = pd.read_parquet(up)
            except Exception:
                st.error("你的环境不支持 Parquet 读取，请改为 CSV 上传。"); df=None
        if df is not None:
            import matplotlib.pyplot as plt
            eq = df.iloc[:,0]
            fig, ax = plt.subplots(); ax.plot(eq.values); ax.set_title("Equity"); st.pyplot(fig)
