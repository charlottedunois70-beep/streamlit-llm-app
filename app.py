from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.error("環境変数 OPENAI_API_KEY が設定されていません。")
    st.stop()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def ask_expert(user_input: str, expert_type: str) -> str:
    expert_roles = {
        "キャリアアドバイザー": "あなたは就職や転職の専門家です。キャリア形成に役立つアドバイスをしてください。",
        "栄養士": "あなたは栄養学の専門家です。健康的な食生活や栄養バランスについてアドバイスをしてください。",
        "旅行プランナー": "あなたは旅行の専門家です。旅行プランを提案したりおすすめスポットを紹介してください。"
    }
    
    system_message = expert_roles.get(expert_type, "あなたは親切なアシスタントです。")

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input),
    ]
    result = llm(messages)
    return result.content

st.title("専門家に質問アプリ")
st.write("""
キャリアアドバイザー、栄養士、旅行プランナーの中から専門家を選んで質問してください。")

### 操作方法
1. 専門家の種類をラジオボタンで選びます  
2. テキストを入力フォームに入力します  
3. 「送信」ボタンを押すと、専門家からの回答が表示されます
""")
expert_type = st.radio(
    "専門家の種類を選択してください:", 
    ["キャリアアドバイザー", "栄養士", "旅行プランナー"]
)
user_input = st.text_input("質問を入力してください:", "")

if st.button("質問する"):
    if user_input.strip():
        with st.spinner("専門家に質問中..."):
            answer = ask_expert(user_input, expert_type)
            st.write("回答:")
            st.write(answer)
    else:
        st.warning("質問を入力してください。")


