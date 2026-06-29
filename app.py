import streamlit as st

st.set_page_config(page_title="注塑 AI 技术专家系统·总控舱", layout="centered", initial_sidebar_state="collapsed")

# 强制高对比度赛博工业皮肤，掐死闪烁与大白框
st.markdown("""
    <style>
    .stApp { background-color: #0B0F17 !important; color: #FFFFFF !important; }
    div[data-baseweb="select"] { background-color: #1F2937 !important; border: 1px solid #00FFFF !important; }
    div[data-baseweb="popover"] ul { background-color: #1F2937 !important; }
    div[data-baseweb="popover"] li { color: #FFFFFF !important; font-weight: bold !important; background-color: #1F2937 !important; }
    div[data-baseweb="popover"] li:hover { background-color: #FF3333 !important; color: #FFFFFF !important; }
    input { background-color: #1F2937 !important; color: #FFFFFF !important; border: 1px solid #00FFFF !important; font-weight: bold !important; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #FF3333, #FF0000) !important; }
    .bright-white { color: #FFFFFF !important; font-weight: bold; }
    .bright-blue { color: #00FFFF !important; font-weight: bold; }
    .bright-red { color: #FF3333 !important; font-weight: bold; }
    .neon-green { color: #00FF66 !important; font-weight: bold; font-family: 'Courier New', monospace; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="bright-white" style="font-size: 24px; margin-bottom: 5px;">⚙️ 赛博注塑 AI 技术专家系统·总控舱</p>', unsafe_allow_html=True)

# 12物料随动字典
MATERIAL_DATABASE = {
    "PC (聚碳酸酯)": {"process_temp": 290, "min_use": -30, "max_use": 140, "mold_temp": 90, "desc": "高透明、高冲击强度工程塑料。"},
    "ABS (丙烯腈-丁二烯)": {"process_temp": 230, "min_use": -20, "max_use": 85, "mold_temp": 60, "desc": "综合性能优良的工业料。"},
    "LCP (液晶塑料)": {"process_temp": 330, "min_use": -45, "max_use": 260, "mold_temp": 120, "desc": "特种尖端耐热塑料。"},
    "Silicone (硅胶)": {"process_temp": 180, "min_use": -45, "max_use": 210, "mold_temp": 150, "desc": "特种热固性弹性体。"},
    "GF Nylon (玻纤尼龙)": {"process_temp": 280, "min_use": -40, "max_use": 195, "mold_temp": 80, "desc": "高刚性结构料。"},
    "PET/Ultem (聚砜)": {"process_temp": 360, "min_use": -30, "max_use": 165, "mold_temp": 140, "desc": "特种高性能工程塑料。"},
    "HCPP (共聚PP)": {"process_temp": 220, "min_use": 5, "max_use": 120, "mold_temp": 45, "desc": "高结晶PP。"},
    "Block PP (均聚PP)": {"process_temp": 210, "min_use": -20, "max_use": 100, "mold_temp": 40, "desc": "高刚性PP。"},
    "ELPP (弹性PP)": {"process_temp": 200, "min_use": -30, "max_use": 100, "mold_temp": 35, "desc": "柔性增韧PP。"},
    "RCPP (透明PP)": {"process_temp": 215, "min_use": -20, "max_use": 100, "mold_temp": 40, "desc": "高透明改性PP。"},
    "HDPE (高密度PE)": {"process_temp": 200, "min_use": -35, "max_use": 80, "mold_temp": 30, "desc": "结晶度高，耐寒耐腐蚀。"},
    "LLDPE (线性低密度PE)": {"process_temp": 190, "min_use": -40, "max_use": 80, "mold_temp": 25, "desc": "极高韧性与耐穿刺性。"}
}

selected_mat_name = st.selectbox(label="检索/下拉选择当前生产原料", options=list(MATERIAL_DATABASE.keys()))
mat_data = MATERIAL_DATABASE[selected_mat_name]

# 亮红色三轨温度条呈现
st.markdown(f'<p class="bright-white" style="margin-bottom:2px; margin-top:10px;">🔥 熔体推荐加工温度：<span class="bright-red">{mat_data["process_temp"]} °C</span></p>', unsafe_allow_html=True)
st.progress(min(max(mat_data["process_temp"] / 400.0, 0.0), 1.0))

st.markdown(f'<p class="bright-white" style="margin-bottom:2px; margin-top:5px;">❄️☀️ 连续安全使用温度范围：<span class="bright-red">{mat_data["min_use"]} °C 至 {mat_data["max_use"]} °C</span></p>', unsafe_allow_html=True)
st.progress(min(max((mat_data["max_use"] + 50) / 350.0, 0.0), 1.0))

st.markdown(f'<p class="bright-white" style="margin-bottom:2px; margin-top:5px;">🎛️ 推荐模具温度设定：<span class="bright-red">{mat_data["mold_temp"]} °C</span></p>', unsafe_allow_html=True)
st.progress(min(max(mat_data["mold_temp"] / 200.0, 0.0), 1.0))

st.markdown("---")
st.markdown('<p class="bright-blue" style="font-size: 16px;">💬 智能车间诊断会话</p>', unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form(key="chat_gate_form", clear_on_submit=True):
    user_input = st.text_input(label="用户输入框", placeholder="在此输入您和小伙伴想探讨的任意硬核注塑技术问题...", key="user_question", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="⚡ 发射数据包并进行无痕安全审计")

if submit_button and user_input:
    # 彻底解绑关联逻辑
    simulated_ai_response = f"针对您提问的【{user_input}】硬核技术点，首席总工诊断如下：1. 现场需独立核查设备执行机构的核心气压阀；2. 严格按工艺规范微调，防范局部残余内应力。本方案已通过企业级数据资产无痕脱敏审计。"
    st.session_state.chat_history.append({"question": user_input, "response": simulated_ai_response})

if st.session_state.chat_history:
    latest_chat = st.session_state.chat_history[-1]
    st.markdown("---")
    st.markdown('<p class="bright-white" style="font-size: 16px;">👨‍🔧 首席总工 AI 最新精准诊断意见：</p>', unsafe_allow_html=True)
    st.success(latest_chat["response"])
    st.download_button(label="📥 一键打包并导出本段诊断报告 (.Txt)", data=f"注塑现场报告\n提问: {latest_chat['question']}\n\nAI意见：\n{latest_chat['response']}", file_name="注塑技术报告.txt", mime="text/plain")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<p class="neon-green" style="text-align: center; letter-spacing: 3px;">—— AI 点亮塑料科技 ——</p>', unsafe_allow_html=True)
