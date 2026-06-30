import streamlit as st
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="小安 - 照顧者儀表板",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 小安 - 照顧者儀表板")
st.caption(f"最後更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- Sidebar ---
st.sidebar.header("👤 患者選擇")

# Load patient profiles from knowledge folder
knowledge_dir = Path(os.environ.get("USERPROFILE", ".")) / ".nanobot" / "knowledge"

# List available patient files (if they exist)
patient_files = list(knowledge_dir.glob("patient_*.txt"))

if patient_files:
    patient_names = [f.stem.replace("patient_", "") for f in patient_files]
    selected_patient = st.sidebar.selectbox("選擇患者", patient_names)
else:
    # Create a demo patient if no real data exists
    st.sidebar.info("未找到患者檔案，使用示範數據")
    selected_patient = "陳婆婆"

# --- Main Content ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🧠 認知訓練表現", "78%", "+5%")

with col2:
    st.metric("💊 用藥依從性", "92%", "+3%")

with col3:
    st.metric("❤️ 情緒狀態", "良好", "穩定")

# --- Cognitive Performance Chart ---
st.subheader("🧠 認知訓練表現（過去7天）")

# Example data (replace with real data from your knowledge base)
cognitive_data = pd.DataFrame({
    "日期": ["一", "二", "三", "四", "五", "六", "日"],
    "記憶力": [70, 75, 72, 80, 85, 82, 78],
    "語言": [65, 70, 68, 75, 80, 78, 76],
    "計算": [80, 82, 85, 83, 88, 85, 82]
})

st.line_chart(cognitive_data.set_index("日期"))

# --- Medication Adherence ---
st.subheader("💊 用藥記錄")

medication_data = pd.DataFrame({
    "藥物": ["多奈哌齊", "卡巴拉汀"],
    "今日服用": ["✅ 已服", "⏳ 未服"],
    "本週依從率": ["100%", "85%"]
})

st.table(medication_data)

# --- Warning System ---
st.subheader("⚠️ 警示")

warnings = [
    "⚠️ 患者過去3日有2次未按時服藥",
    "ℹ️ 認知訓練分數持續上升 +5%",
    "✅ 情緒狀態保持穩定"
]

for warning in warnings:
    if "⚠️" in warning:
        st.warning(warning)
    elif "ℹ️" in warning:
        st.info(warning)
    else:
        st.success(warning)

# --- Patient Profile ---
with st.expander("👤 患者檔案"):
    st.write(f"**姓名：** {selected_patient}")
    st.write("**年齡：** 72歲")
    st.write("**診斷：** 輕度認知障礙 (MCI)")
    st.write("**照顧者：** 陳先生 (兒子)")
    st.write("**最近更新：** 2026-06-30")

# --- Chat History ---
with st.expander("💬 最近對話"):
    st.write("📄 2026-06-30 10:30 - 查詢藥物副作用")
    st.write("📄 2026-06-29 14:20 - 認知訓練活動")
    st.write("📄 2026-06-29 09:00 - 情緒支援查詢")

# --- Footer ---
st.divider()
st.caption("小安 - 認知健康助理 | 數據僅供參考")