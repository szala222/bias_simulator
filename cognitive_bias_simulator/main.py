import streamlit as st
import confirmation_bias as cb
import anchoring_bias as ab
import framing_effect as fe

# Set page configuration
st.set_page_config(
    page_title="Cognitive Bias Simulator",
    page_icon="🧠",
    layout="wide"
)


if 'stage' not in st.session_state:
    st.session_state.stage = 'intro'
if 'bias_type' not in st.session_state:
    st.session_state.bias_type = None

def reset_all():
    st.session_state.stage = 'intro'
    st.session_state.bias_type = None
    cb.reset_all_confirmation()
    ab.reset_anchoring_experiment()
    fe.reset_framing_experiment()

def main():
    st.title("🧠 Cognitive Bias Simulator")

    # Main application logic
    if st.session_state.stage == 'intro':
        st.subheader("Welcome to the Cognitive Bias Simulator!")
        
        st.markdown("""
        This simulator helps you understand how cognitive biases affect your thinking and decision-making.
        
        ### Available Bias Simulations:
        
        **1. Confirmation Bias**
        - The tendency to search for, interpret, and recall information in a way that confirms one's preexisting beliefs.
        - Try the classic Wason 2-4-6 task or evaluate evidence in realistic scenarios.
        
        **2. Anchoring Bias**
        - The tendency to rely too heavily on the first piece of information encountered (the "anchor").
        - Make estimates after being exposed to an anchor value.
        
        **3. Framing Effect**
        - The tendency to react differently to information depending on how it's presented or "framed".
        - Experience how different presentations of the same information affect your decisions.
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Explore Confirmation Bias"):
                st.session_state.bias_type = "confirmation"
                st.session_state.stage = "bias_intro"
                st.rerun()
        
        with col2:
            if st.button("Explore Anchoring Bias"):
                st.session_state.bias_type = "anchoring"
                st.session_state.stage = "bias_intro"
                st.rerun()
        
        with col3:
            if st.button("Explore Framing Effect"):
                st.session_state.bias_type = "framing"
                st.session_state.stage = "bias_intro"
                st.rerun()
    
    # Run the appropriate bias simulator based on the user's selection
    elif st.session_state.bias_type == "confirmation":
        cb.run_confirmation_bias_simulator()
    elif st.session_state.bias_type == "anchoring":
        ab.run_anchoring_bias_simulator()
    elif st.session_state.bias_type == "framing":
        fe.run_framing_effect_simulator()

    st.markdown("---")
    st.markdown("Created with Streamlit • Cognitive Bias Simulator")

if __name__ == "__main__":
    main()