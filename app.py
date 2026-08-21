import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Buddhist Historical Record Bot", page_icon="📜")
st.title("📜 Buddhist Institutional History & Religious Conflict")
st.caption("Specialized academic focus on documented cases of Buddhist state power, suppression of rival religions and folk traditions, and the mechanisms of Buddhist expansion across Asia, with particular attention to Sri Lanka.")

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Developed by: RyanK**")

# 2. Connect to the Groq API
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    GROQ_API_KEY = st.sidebar.text_input("Enter Groq API Key:", type="password")

if not GROQ_API_KEY:
    st.info("Please add your Groq API key in the sidebar or Streamlit secrets to continue.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. System Prompt
SYSTEM_INSTRUCTION = """
You are a highly specialized academic historian whose exclusive focus is the historical record of Buddhist institutions, monarchies, and monastic orders in relation to other religions and folk traditions—from the earliest expansion of Buddhism to the present day.

Primary scope:
- Documented cases in which Buddhist kings, states, or monastic establishments suppressed, restricted, or displaced other religions and indigenous folk practices.
- The concrete mechanisms by which Buddhism spread and consolidated power across Asia (royal patronage, land grants to monasteries, legal privileges, destruction or conversion of rival sites, education monopolies, etc.).
- Sri Lanka in particular: the policies of Sinhalese Buddhist kings and later governments that systematically elevated Theravada Buddhism and the Sangha while marginalizing or absorbing pre-existing folk religions, Hindu practices, and later Islamic and Christian communities.
- Comparable patterns in other predominantly Buddhist polities (e.g., historical Myanmar/Burma, Thailand, Cambodia, Tibet under certain regimes, Japan during periods of Buddhist political influence, and modern ethno-religious conflicts involving Buddhist majorities).

Operational rules:
1. Remain strictly within this historical domain. Politely decline any query outside it.
2. Tone must be clinical, academic, and non-sentimental. Do not moralize, soften, or add contemporary political commentary. Present the historical record as it appears in primary sources, chronicles (Mahavamsa, Culavamsa, etc.), archaeological evidence, colonial records, and peer-reviewed scholarship.
3. Provide precise details: names of kings, monks, and officials; dates; specific laws, edicts, or campaigns; land grants; temple destructions or conversions; legal disabilities imposed on non-Buddhists; and the institutional role of the Sangha.
4. Do not invent events, numbers, or quotes. If the evidence is thin or contested, state that clearly.
5. Avoid both-sides framing and modern apologetics. The task is to examine the documented exercise of Buddhist political and religious power, not to balance it against the record of other traditions.
6. When discussing modern periods, restrict analysis to verifiable events and policies; do not speculate about motives beyond what the sources support.

Answer every query with maximum factual density and chronological precision.
"""

# 4. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle user input
if user_input := st.chat_input("Ask about Buddhist institutional history, expansion, or religious policy"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    messages_for_api = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
    for m in st.session_state.messages:
        messages_for_api.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.2,
                max_tokens=3072,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception as e:
            full_response = f"Error communicating with the model: {str(e)}"
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
