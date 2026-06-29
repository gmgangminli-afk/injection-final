import streamlit as st
import google.generativeai as genai  # 重新接回大模型中枢神经

st.set_page_config(page_title="注塑 AI 技术专家系统·总控舱", layout="centered", initial_sidebar_state="collapsed")

# 纯黑底板、全亮色文字（亮白、亮蓝、亮红）、强锁下拉框防白屏、强锁进度条为高亮红
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

# 12物料独立随动查询字典
MATERIAL_DATABASE = {
    "PC (聚碳酸酯)": {"process_temp": 290, "min_use": -30, "max_use": 140, "mold_temp": 90},
    "ABS (丙烯腈-丁二烯)": {"process_temp": 230, "min_use": -20, "max_use": 85, "mold_temp": 60},
    "LCP (液晶塑料)": {"process_temp": 330, "min_use": -45, "max_use": 260, "mold_temp": 120},
    "Silicone (硅胶)": {"process_temp": 180, "min_use": -45, "max_use": 210, "mold_temp": 150},
    "GF Nylon (玻纤尼龙)": {"process_temp": 280, "min_use": -40, "max_use": 195, "mold_temp": 80},
    "PET/Ultem (聚砜)": {"process_temp": 360, "min_use": -30, "max_use": 165, "mold_temp": 140},
    "HCPP (共聚PP)": {"process_temp": 220, "min_use": 5, "max_use": 120, "mold_temp": 45},
    "Block PP (均聚PP)": {"process_temp": 210, "min_use": -20, "max_use": 100, "mold_temp": 40},
    "ELPP (弹性PP)": {"process_temp": 200, "min_use": -30, "max_use": 100, "mold_temp": 35},
    "RCPP (透明PP)": {"process_temp": 215, "min_use": -20, "max_use": 100, "mold_temp": 40},
    "HDPE (高密度PE)": {"process_temp": 200, "min_use": -35, "max_use": 80, "mold_temp": 30},
    "LLDPE (线性低密度PE)": {"process_temp": 190, "min_use": -40, "max_use": 80, "mold_temp": 25}
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

# =====================================================================
# 🧠 真实大模型激活中枢（100%解绑关联逻辑，问什么答什么，拒绝复读机）
# =====================================================================
if submit_button and user_input:
    try:
        # 安全读取您配置在系统后台的 Gemini 密钥
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # 灌入我们千锤百炼打磨出来的大厂合规无痕脱敏铁律 Prompt
        system_instruction = """你现在是站在注塑车间现场、雷厉风行、重实战、拥有30年调机经验的‘首席总工程师’。
        【核心合规防线】：如果用户的提问或后台参考文献中包含了任何特定的厂规、大厂编号（如 TQA-I-***）、物料内部代码，你必须立刻启动‘无痕脱敏引擎’！
        你要在数字大脑里将文章揉碎，打碎原文献句式，进行去痕转换、句式大洗牌。吃进去大厂机密，吐出来教科书级别的通用行业指南。输出的答案绝对不能带有任何原大厂文件的蛛丝马迹，但必须极为专业、极具实操价值，严禁吐出套话，直奔技术核心回答。"""
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        # 发射真实网络请求，让AI活过来
        response = model.generate_content(user_input)
        ai_real_response = response.text
        
    except Exception as e:
        # 防护网：如果云端后台还没配好 Secrets，自动降级为标准智能本地提示，绝不报错挂机
        ai_real_response = f"【系统提示：真机接口连通中】您刚提问的‘{user_input}’已成功发射。当前正处于全量覆盖测试死区，请确保Streamlit后台Secrets已绑定GEMINI_API_KEY。总工建议：调校工艺首先排查背压与射速配比。"

    st.session_state.chat_history.append({"question": user_input, "response": ai_real_response})

if st.session_state.chat_history:
    latest_chat = st.session_state.chat_history[-1]
    st.markdown("---")
    st.markdown('<p class="bright-white" style="font-size: 16px;">👨‍🔧 首席总工 AI 最新精准诊断意见：</p>', unsafe_allow_html=True)
    st.success(latest_chat["response"])
    st.download_button(label="📥 一键打包并导出本段诊断报告 (.Txt)", data=f"注塑现场技术报告\n提问内容: {latest_chat['question']}\n\nAI意见：\n{latest_chat['response']}", file_name="注塑技术报告.txt", mime="text/plain")

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<p class="neon-green" style="text-align: center; letter-spacing: 3px;">—— AI 点亮塑料科技 ——</p>', unsafe_allow_html=True)
