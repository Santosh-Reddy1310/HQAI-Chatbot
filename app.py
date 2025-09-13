import streamlit as st
from ai_client import ask_llm
import qmodule
import utils
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
utils.ensure_static_dir()

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Hybrid Quantum AI Chatbot",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    .quantum-metric {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    .error-box {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔮 Hybrid Quantum AI Chatbot — Enhanced MVP")
st.markdown("Advanced Classical LLM + Quantum Computing Simulation powered by Qiskit")

# ----------------- SESSION STATE -----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "metrics" not in st.session_state:
    st.session_state.metrics = {"classical": [], "quantum": []}

if "quantum_stats" not in st.session_state:
    st.session_state.quantum_stats = {"circuits": 0, "ops": 0}
else:
    st.session_state.quantum_stats.setdefault("circuits", 0)
    st.session_state.quantum_stats.setdefault("ops", 0)

if "error_log" not in st.session_state:
    st.session_state.error_log = []

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.header("⚙️ Settings")

    provider = os.getenv("LLM_PROVIDER", "openrouter")
    st.info(f"LLM Provider: **{provider.title()}**")

    st.subheader("🔬 Quantum Controls")
    quantum_mode = st.checkbox("Enable Quantum Mode", value=True,
                               help="Augment responses with quantum computations")

    quantum_complexity = st.selectbox(
        "Quantum Complexity",
        ["Basic", "Intermediate", "Advanced"],
        index=0,
        help="Choose quantum algorithm complexity"
    )

    # Demos
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Entanglement Demo"):
            try:
                with st.spinner("Generating quantum circuit..."):
                    path = qmodule.quantum_entanglement_demo()
                    st.session_state.quantum_stats["circuits"] += 1
                    st.success("Circuit generated!")
                    st.image(path, caption="Bell State Circuit", width=300)
            except Exception as e:
                st.error(f"Quantum demo failed: {str(e)}")

    with col2:
        if st.button("🎲 Quantum Random"):
            try:
                with st.spinner("Quantum randomization..."):
                    bit = qmodule.quantum_random_bit()
                    st.session_state.quantum_stats["ops"] += 1
                    st.success(f"Quantum bit: **{bit}**")
            except Exception as e:
                st.error(f"Quantum random failed: {str(e)}")

    # Quantum stats
    st.subheader("📊 Quantum Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Circuits", st.session_state.quantum_stats["circuits"])
    col2.metric("Ops", st.session_state.quantum_stats["ops"])

    if st.session_state.error_log:
        with st.expander("⚠️ Error Log", expanded=False):
            for error in st.session_state.error_log[-5:]:
                st.text(f"{error['time']}: {error['message']}")

# ----------------- MAIN CHAT -----------------
st.subheader("💬 Chat Interface")

# Display chat history
chat_container = st.container()
with chat_container:
    for msg in st.session_state.history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])
                if "Quantum" in msg["content"]:
                    st.caption("🔬 Enhanced with quantum computation")

# Chat input
user_input = st.chat_input("Ask the Hybrid Quantum AI something...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking... (Classical + Quantum processing)"):
            try:
                # Measure response time
                start = time.time()

                system_context = f"""
                You are an advanced AI assistant with hybrid quantum-classical capabilities.
                The user asked: '{user_input}'

                Quantum Mode: {'Enabled' if quantum_mode else 'Disabled'}
                Complexity Level: {quantum_complexity}

                Provide a helpful, accurate response. If quantum mode is enabled,
                mention how quantum computing concepts relate to the query when relevant.
                """

                llm_response = ask_llm(system_context)

                # Quantum enhancement
                if quantum_mode:
                    try:
                        if quantum_complexity == "Basic":
                            options = [
                                "Quantum randomness suggests exploring multiple approaches",
                                "Quantum superposition indicates considering parallel solutions",
                                "Quantum entanglement implies interconnected possibilities"
                            ]
                            quantum_choice, bits = qmodule.quantum_random_choice(options)
                            quantum_note = f"\n\n🔬 **Quantum Enhancement**: {quantum_choice} (bits: `{bits}`)"
                        elif quantum_complexity == "Intermediate":
                            qmodule.quantum_optimization_demo()
                            quantum_note = "\n\n🔬 **Quantum Optimization**: Applied variational algorithm concepts."
                        else:
                            qmodule.quantum_ml_feature_map([0.5, 1.0, 0.3])
                            quantum_note = "\n\n🔬 **Quantum ML**: Feature mapping + amplitude encoding applied."

                        final_response = llm_response + quantum_note
                        st.session_state.quantum_stats["ops"] += 1
                    except Exception as q_error:
                        final_response = llm_response + "\n\n⚠️ *Quantum enhancement unavailable*"
                        st.session_state.error_log.append(
                            {"time": utils.timestamp(), "message": f"Quantum error: {str(q_error)}"}
                        )
                else:
                    final_response = llm_response

                # Measure time
                elapsed = round(time.time() - start, 2)
                if quantum_mode:
                    st.session_state.metrics["quantum"].append(elapsed)
                else:
                    st.session_state.metrics["classical"].append(elapsed)

                # Show response
                st.write(final_response)
                st.caption(f"⏱️ Response Time: {elapsed} sec")

                st.session_state.history.append({"role": "assistant", "content": final_response})

            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.error_log.append({"time": utils.timestamp(), "message": str(e)})
                st.session_state.history.append({"role": "assistant", "content": error_msg})

# ----------------- FOOTER -----------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit, Qiskit, and advanced LLMs. "
    f"Running in {'🔬 Quantum' if quantum_mode else '⚛️ Classical'} mode."
)

# ----------------- PERFORMANCE SUMMARY -----------------
st.subheader("📈 Performance Metrics")

if st.session_state.metrics["classical"] or st.session_state.metrics["quantum"]:
    avg_classical = (
        sum(st.session_state.metrics["classical"]) / len(st.session_state.metrics["classical"])
        if st.session_state.metrics["classical"]
        else 0
    )
    avg_quantum = (
        sum(st.session_state.metrics["quantum"]) / len(st.session_state.metrics["quantum"])
        if st.session_state.metrics["quantum"]
        else 0
    )

    col1, col2 = st.columns(2)
    col1.metric("Avg Classical Response Time", f"{avg_classical:.2f} sec")
    col2.metric("Avg Quantum Response Time", f"{avg_quantum:.2f} sec")
else:
    st.info("No performance data yet. Start chatting to measure response times.")
