import streamlit as st
import google.generativeai as genai
import json
import random
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_trivia_questions(topic):
    prompt = f"""
    Generate 7 trivia questions about {topic}.
    Respond with JSON only. Do NOT include markdown fences or explanation.
    Format: [{{"question": "...", "answer": "..."}}, ...]
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-2.5-pro"
        response = model.generate_content(prompt)
        text = response.text

        # Parse JSON from the text
        data = json.loads(text)
        random.shuffle(data)
        return data
    except Exception as e:
        st.error(f"Could not get questions: {e}")
        return []

st.markdown(
    """
    <style>
    html, body, .main, [class^='css'] {
        font-size: 28px !important;
    }
    .title {
        font-size: 48px !important;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .question-heading {
        font-size: 35px !important;
        font-weight: 600;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .stButton>button {
        font-size: 28px !important;
        padding: 0.5em 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="title">🎉 AI Trivia with Gemini 2.5</div>', unsafe_allow_html=True)

# Initialize session state
if 'round_questions' not in st.session_state:
    st.session_state.round_questions = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False
if 'trivia_topic' not in st.session_state:
    st.session_state.trivia_topic = "General Knowledge"

# Enter topic and start new round button
if not st.session_state.round_questions:
    topic = st.text_input("Enter a trivia topic:", value=st.session_state.trivia_topic)
    if st.button("Start New Trivia Round"):
        st.session_state.trivia_topic = topic
        questions = get_trivia_questions(topic)
        if questions:
            st.session_state.round_questions = questions
            st.session_state.current_index = 0
            st.session_state.show_answer = False
        st.rerun()

elif st.session_state.round_questions:
    q = st.session_state.round_questions[st.session_state.current_index]

    st.markdown(f'<div class="question-heading">Question {st.session_state.current_index + 1}</div>', unsafe_allow_html=True)
    st.write(q["question"])

    if not st.session_state.show_answer:
        if st.button("Show Answer"):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success(f"Answer: {q['answer']}")
        if st.session_state.current_index < len(st.session_state.round_questions) - 1:
            if st.button("Next Question"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
        else:
            st.info("🏁 End of round!")
            if st.button("Play Another Round"):
                st.session_state.round_questions = []
                st.session_state.current_index = 0
                st.session_state.show_answer = False
                st.rerun()
