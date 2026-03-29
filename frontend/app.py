import streamlit as st
import requests

# ================================
# CONFIG
# ================================
PREDICT_URL = "http://127.0.0.1:8000/predict"
FEEDBACK_URL = "http://127.0.0.1:8000/feedback"

st.set_page_config(
    page_title="NeuroSenti 2.0",
    page_icon="🧠",
    layout="centered"
)

# ================================
# SESSION STATE
# ================================
if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "show_feedback_form" not in st.session_state:
    st.session_state.show_feedback_form = False

# ================================
# HEADER
# ================================
st.title("🧠 NeuroSenti 2.0")
st.markdown("### Human-in-the-Loop Sentiment Intelligence System")
st.caption("Streamlit • FastAPI • TensorFlow")

# ================================
# INPUT
# ================================
text = st.text_area(
    "Enter text for sentiment analysis",
    height=180,
    placeholder="The film is a sophisticated vehicle for ideological manipulation."
)

# ================================
# PREDICT
# ================================
if st.button("Analyze Sentiment 🚀", use_container_width=True):
    if not text.strip():
        st.warning("⚠️ Please enter some text")
    else:
        try:
            response = requests.post(
                PREDICT_URL,
                json={"text": text},
                timeout=10
            )
            response.raise_for_status()
            st.session_state.prediction = response.json()
            st.session_state.text = text
        except Exception as e:
            st.error("❌ Backend not reachable")
            st.code(str(e))

# ================================
# RESULT
# ================================
if st.session_state.prediction:
    data = st.session_state.prediction
    sentiment = data["sentiment"]
    confidence = data["confidence"]

    st.success("✅ Prediction Complete")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "### 🟢 Positive" if sentiment == "Positive" else "### 🔴 Negative"
        )
    with col2:
        st.metric("Confidence", f"{confidence * 100:.2f}%")

    st.divider()
    st.subheader("🧠 Was this prediction correct?")

    col_yes, col_no = st.columns(2)

    with col_yes:
        if st.button("✅ Yes, Correct"):
            st.success("Thanks! Prediction confirmed.")

    with col_no:
        if st.button("❌ No, Wrong"):
            st.session_state.show_feedback_form = True

    # ================================
    # FEEDBACK FORM
    # ================================
    if st.session_state.show_feedback_form:
        correct_label = st.radio(
            "Select the correct sentiment:",
            ["Positive", "Negative"]
        )

        if st.button("Submit Feedback"):
            payload = {
                "text": st.session_state.text,
                "model_prediction": sentiment,
                "confidence": confidence,
                "correct_label": correct_label
            }

            fb_response = requests.post(FEEDBACK_URL, json=payload)

            if fb_response.status_code == 200:
                st.success("✅ Feedback stored successfully!")
                st.session_state.show_feedback_form = False
            else:
                st.error("❌ Failed to store feedback")

# ================================
# VISUAL FLOWCHART (GRAPHVIZ)
# ================================
st.divider()
st.subheader("🔁 System Architecture & Learning Flow")

st.graphviz_chart("""
digraph NeuroSenti {
    rankdir=TB;
    node [shape=box, style=rounded, fontsize=10];

    User [label="User\\n(Streamlit UI)"];
    PredictAPI [label="POST /predict\\nFastAPI"];
    Preprocess [label="Text Preprocessing\\nTokenizer + Padding"];
    Model [label="CNN–BiLSTM Model\\n(.h5 TensorFlow)"];
    Output [label="Prediction Output\\nSentiment + Confidence"];
    Decision [label="User Feedback\\nCorrect ?"];
    Done [label="Prediction Accepted"];
    FeedbackAPI [label="POST /feedback\\nFastAPI"];
    Storage [label="Feedback Storage\\n(JSON / Database)"];
    Retrain [label="Offline Retraining\\n(Phase 5)"];
    NewModel [label="Updated Model Version"];

    User -> PredictAPI;
    PredictAPI -> Preprocess;
    Preprocess -> Model;
    Model -> Output;
    Output -> Decision;

    Decision -> Done [label="Yes"];
    Decision -> FeedbackAPI [label="No"];

    FeedbackAPI -> Storage;
    Storage -> Retrain;
    Retrain -> NewModel;
    NewModel -> Model;
}
""")

# ================================
# FOOTER
# ================================
st.divider()
st.caption("NeuroSenti 2.0 • Human-in-the-Loop ML System • Phase 4 Complete")
