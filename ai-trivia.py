import streamlit as st
import google.generativeai as genai
import json
import random
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_trivia_questions():
    prompt = """
    Generate 7 general knowledge trivia questions.
    Respond with JSON only. Do NOT include markdown fences or explanation.
    Format: [{"question": "...", "answer": "..."}, ...]
    """
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")  # or use "gemini-2.5-pro"
        response = model.generate_content(prompt)
        text = response.text

        # Parse JSON from the text
        data = json.loads(text)
        random.shuffle(data)
        return data
    except Exception as e:
        st.error(f"Could not get questions: {e}")
        return []

# Streamlit app UI
st.title("🎉 AI Trivia with Gemini 2.5")

# Initialize session state
if 'round_questions' not in st.session_state:
    st.session_state.round_questions = []
    st.session_state.current_index = 0
    st.session_state.show_answer = False

# Start new round button
if not st.session_state.round_questions:
    if st.button("Start New Trivia Round"):
        questions = get_trivia_questions()
        if questions:
            st.session_state.round_questions = questions
            st.session_state.current_index = 0
            st.session_state.show_answer = False
        st.rerun()

elif st.session_state.round_questions:
    q = st.session_state.round_questions[st.session_state.current_index]

    st.header(f"Question {st.session_state.current_index + 1}")
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
                questions = get_trivia_questions()
                if questions:
                    st.session_state.round_questions = questions
                    st.session_state.current_index = 0
                    st.session_state.show_answer = False
                else:
                    st.session_state.round_questions = []
                st.rerun()
