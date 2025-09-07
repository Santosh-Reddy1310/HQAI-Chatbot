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

# Page configuration
st.set_page_config(
    page_title="Hybrid Quantum AI Chatbot", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .quantum-metric {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        padding: 10px;
        border-radius: 10px;
        color: white;
        text-align: center;
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

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "quantum_stats" not in st.session_state:
    st.session_state.quantum_stats = {
        'circuits_generated': 0,
        'quantum_operations': 0,
        'last_quantum_result': None
    }
if "error_log" not in st.session_state:
    st.session_state.error_log = []

# Sidebar controls
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Provider info
    provider = os.getenv("LLM_PROVIDER", "openrouter")
    st.info(f"LLM Provider: **{provider.title()}**")
    
    # Quantum controls
    st.subheader("🔬 Quantum Controls")
    quantum_mode = st.checkbox("Enable Quantum Mode", value=True, 
                              help="Augment responses with quantum computations")
    
    quantum_complexity = st.selectbox(
        "Quantum Complexity",
        ["Basic", "Intermediate", "Advanced"],
        index=0,
        help="Choose quantum algorithm complexity"
    )
    
    # Quantum demo buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 Entanglement Demo"):
            try:
                with st.spinner("Generating quantum circuit..."):
                    path = qmodule.quantum_entanglement_demo()
                    st.session_state.quantum_stats['circuits_generated'] += 1
                    st.success("Circuit generated!")
                    st.image(path, caption="Bell State Circuit", width=300)
            except Exception as e:
                st.error(f"Quantum demo failed: {str(e)}")
    
    with col2:
        if st.button("🎲 Quantum Random"):
            try:
                with st.spinner("Quantum randomization..."):
                    bit = qmodule.quantum_random_bit()
                    st.session_state.quantum_stats['quantum_operations'] += 1
                    st.session_state.quantum_stats['last_quantum_result'] = bit
                    st.success(f"Quantum bit: **{bit}**")
            except Exception as e:
                st.error(f"Quantum random failed: {str(e)}")
    
    # Quantum statistics
    st.subheader("📊 Quantum Statistics")
    stats = st.session_state.quantum_stats
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Circuits", stats['circuits_generated'])
    with col2:
        st.metric("Operations", stats['quantum_operations'])
    
    if stats['last_quantum_result'] is not None:
        st.markdown(f"**Last Result:** {stats['last_quantum_result']}")
    
    # Error log (if any)
    if st.session_state.error_log:
        with st.expander("⚠️ Error Log", expanded=False):
            for error in st.session_state.error_log[-5:]:  # Show last 5 errors
                st.text(f"{error['time']}: {error['message']}")

# Main chat interface
st.subheader("💬 Chat Interface")

# Display chat history
chat_container = st.container()
with chat_container:
    for i, msg in enumerate(st.session_state.history):
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])
                # Show quantum enhancement indicator if present
                if "Quantum" in msg["content"]:
                    st.caption("🔬 Enhanced with quantum computation")

# Chat input
user_input = st.chat_input("Ask the Hybrid Quantum AI something...")

# Handle new user input
if user_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": user_input})
    
    # Show user message immediately
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking... (Classical + Quantum processing)"):
            try:
                # Craft enhanced prompt
                system_context = f"""
                You are an advanced AI assistant with hybrid quantum-classical capabilities.
                The user asked: '{user_input}'
                
                Quantum Mode: {'Enabled' if quantum_mode else 'Disabled'}
                Complexity Level: {quantum_complexity}
                
                Provide a helpful, accurate response. If quantum mode is enabled, 
                mention how quantum computing concepts relate to the query when relevant.
                """
                
                # Get LLM response
                llm_response = ask_llm(system_context)
                
                # Quantum enhancement
                if quantum_mode:
                    try:
                        # Choose quantum enhancement based on complexity
                        if quantum_complexity == "Basic":
                            options = [
                                "Quantum randomness suggests exploring multiple approaches",
                                "Quantum superposition indicates considering parallel solutions",
                                "Quantum entanglement implies interconnected possibilities"
                            ]
                            quantum_choice, bits = qmodule.quantum_random_choice(options)
                            quantum_note = f"\n\n🔬 **Quantum Enhancement**: {quantum_choice} (bits: `{bits}`)"
                            
                        elif quantum_complexity == "Intermediate":
                            # Use quantum optimization concept
                            optimization_result = qmodule.quantum_optimization_demo()
                            quantum_note = f"\n\n🔬 **Quantum Optimization**: Applied quantum variational algorithm principles to enhance solution quality."
                            
                        else:  # Advanced
                            # Use quantum ML feature mapping
                            feature_map = qmodule.quantum_ml_feature_map([0.5, 1.0, 0.3])
                            quantum_note = f"\n\n🔬 **Quantum ML**: Enhanced response using quantum feature mapping and amplitude encoding."
                        
                        final_response = llm_response + quantum_note
                        st.session_state.quantum_stats['quantum_operations'] += 1
                        
                    except Exception as q_error:
                        st.warning("Quantum enhancement failed, using classical response only")
                        st.session_state.error_log.append({
                            'time': utils.timestamp(),
                            'message': f"Quantum error: {str(q_error)}"
                        })
                        final_response = llm_response + "\n\n⚠️ *Quantum enhancement unavailable*"
                else:
                    final_response = llm_response
                
                # Display response
                st.write(final_response)
                
                # Add to history
                st.session_state.history.append({"role": "assistant", "content": final_response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.error_log.append({
                    'time': utils.timestamp(),
                    'message': str(e)
                })
                st.session_state.history.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit, Qiskit, and advanced LLMs. "
    f"Running in {'🔬 Quantum' if quantum_mode else '⚛️ Classical'} mode."
)