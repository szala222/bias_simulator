
import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Define Wason task functions
def is_ascending_sequence(sequence):
    """Check if a sequence is strictly ascending."""
    if len(sequence) < 2:
        return False
    return all(sequence[i] < sequence[i+1] for i in range(len(sequence)-1))

# This function checks if the user might be testing the common misconception
# that the rule is "increasing by 2 each time"
def is_potentially_confirming(sequence):
    """Determine if a sequence is potentially confirming a +2 pattern."""
    if len(sequence) < 3:
        return False
    
    # Check if the sequence follows a +2 pattern or any other simple arithmetic pattern
    differences = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
    return len(set(differences)) == 1  

def reset_wason_task():
    """Reset the Wason task state."""
    st.session_state.wason_sequences_tested = []
    st.session_state.wason_rule_guesses = []
    st.session_state.wason_confirming_tests = 0
    st.session_state.wason_disconfirming_tests = 0
    
# Define confirmation bias scenario experiment
scenarios = [
    {
        "id": "health_study",
        "title": "Health Study Evaluation",
        "description": "A new study has been published suggesting that coffee may help prevent certain diseases.",
        "stance_question": "Are you a coffee drinker?",
        "stance_options": ["I drink a lot of coffee", "I drink coffee occasionally", "I rarely drink coffee", "I never drink coffee"],
        "hypothesis": "Coffee is beneficial for health",
        "evidence": [
            {
                "id": "e1",
                "text": "The study was funded by a major coffee industry association, creating a potential conflict of interest.",
                "type_for_coffee_drinker": "contradicting",
                "type_for_non_drinker": "supporting",
                "explanation": "Financial conflicts of interest can bias research design and interpretation of results."
            },
            {
                "id": "e2",
                "text": "The study found that regular coffee drinkers had a 23% lower risk of heart disease compared to non-drinkers.",
                "type_for_coffee_drinker": "supporting",
                "type_for_non_drinker": "contradicting",
                "explanation": "This is a clear, substantial health benefit that supports the hypothesis."
            },
            {
                "id": "e3",
                "text": "Three previous large-scale studies found no significant health benefits from coffee consumption.",
                "type_for_coffee_drinker": "contradicting",
                "type_for_non_drinker": "supporting",
                "explanation": "This directly contradicts the current findings, suggesting they might not be reliable."
            },
            {
                "id": "e4",
                "text": "The researchers only found a correlation and stated clearly that they cannot prove coffee directly causes health benefits.",
                "type_for_coffee_drinker": "contradicting",
                "type_for_non_drinker": "supporting",
                "explanation": "Without establishing causation, we cannot be sure coffee is responsible for any observed benefits."
            },
            {
                "id": "e5",
                "text": "Brain scans showed increased blood flow in cognitive regions after coffee consumption in a controlled sub-study.",
                "type_for_coffee_drinker": "supporting",
                "type_for_non_drinker": "contradicting",
                "explanation": "This provides a potential biological mechanism for how coffee might improve health."
            },
            {
                "id": "e6",
                "text": "Participants who consumed more than 5 cups daily showed increased anxiety and sleep disturbances compared to moderate drinkers.",
                "type_for_coffee_drinker": "contradicting",
                "type_for_non_drinker": "supporting",
                "explanation": "This suggests potential negative health effects at higher consumption levels."
            },
            {
                "id": "e7",
                "text": "When researchers controlled for age, smoking, exercise and diet, the positive association between coffee and health remained strong.",
                "type_for_coffee_drinker": "supporting",
                "type_for_non_drinker": "contradicting",
                "explanation": "This methodological strength increases confidence that coffee itself is related to the health outcome."
            },
            {
                "id": "e8",
                "text": "The beneficial compounds in coffee identified in the study have been independently verified to have antioxidant properties in laboratory tests.",
                "type_for_coffee_drinker": "supporting",
                "type_for_non_drinker": "contradicting",
                "explanation": "This provides additional scientific support for why coffee might have health benefits."
            }
        ]
    },
    {
        "id": "political_policy",
        "title": "Political Policy Evaluation",
        "description": "A progressive politician from the left has proposed a new economic policy focused on increasing corporate taxation to fund expanded social programs.",
        "stance_question": "What is your political leaning?",
        "stance_options": ["Strongly liberal/left", "Moderately liberal/left", "Moderately conservative/right", "Strongly conservative/right"],
        "hypothesis": "The proposed economic policy will benefit the country",
        "evidence": [
            {
                "id": "e1",
                "text": "The policy was implemented in three Nordic countries and resulted in measurable economic growth in all cases.",
                "type_for_left": "supporting",
                "type_for_right": "contradicting",
                "explanation": "Real-world success in comparable situations suggests potential effectiveness, though contexts may differ."
            },
            {
                "id": "e2",
                "text": "A coalition of business leaders predict the policy would lead to job losses due to capital flight.",
                "type_for_left": "contradicting",
                "type_for_right": "supporting",
                "explanation": "Business perspective suggests economic risks, though may represent self-interest."
            },
            {
                "id": "e3",
                "text": "Independent analysis shows the policy would cost 3 times more than initially proposed by its supporters.",
                "type_for_left": "contradicting",
                "type_for_right": "supporting",
                "explanation": "Significantly higher costs affect feasibility and value proposition of the policy."
            },
            {
                "id": "e4",
                "text": "In regions where elements of this policy were tested, unemployment decreased by 12% within the first year.",
                "type_for_left": "supporting",
                "type_for_right": "contradicting",
                "explanation": "Early testing provides concrete evidence of positive economic impact."
            },
            {
                "id": "e5",
                "text": "Computer modeling by the Federal Reserve predicts the policy would initially slow economic growth for 3-5 years before any benefits appear.",
                "type_for_left": "contradicting",
                "type_for_right": "supporting",
                "explanation": "Significant negative short-term impact could outweigh potential long-term benefits."
            },
            {
                "id": "e6",
                "text": "A detailed implementation plan shows how the policy could be funded without increasing the national deficit.",
                "type_for_left": "supporting",
                "type_for_right": "contradicting",
                "explanation": "Financial sustainability strengthens the case for the policy's overall value."
            }
        ]
    },
    {
        "id": "product_review",
        "title": "Product Purchase Decision",
        "description": "You're considering buying a smartphone from Apple.",
        "stance_question": "What has been your experience with Apple products?",
        "stance_options": ["Very positive experiences", "Somewhat positive experiences", "Mixed experiences", "Somewhat negative experiences", "Very negative experiences", "No prior experience"],
        "hypothesis": "The new Apple smartphone is a good purchase",
        "evidence": [
            {
                "id": "e1",
                "text": "The phone has received mixed reviews from tech experts.",
                "type_for_positive": "contradicting",
                "type_for_negative": "supporting",
                "type_for_neutral": "neutral",
                "explanation": "Expert opinions are divided, suggesting some potential concerns."
            },
            {
                "id": "e2",
                "text": "The battery life is shorter than competing models.",
                "type_for_positive": "contradicting",
                "type_for_negative": "supporting",
                "type_for_neutral": "contradicting",
                "explanation": "Inferior battery performance could affect daily usability."
            },
            {
                "id": "e3",
                "text": "Apple is offering a significant discount on this model.",
                "type_for_positive": "supporting",
                "type_for_negative": "contradicting",
                "type_for_neutral": "supporting",
                "explanation": "Good price may improve value proposition, though could indicate clearing stock."
            },
            {
                "id": "e4",
                "text": "Your friend who bought this phone is very satisfied with it.",
                "type_for_positive": "supporting",
                "type_for_negative": "contradicting",
                "type_for_neutral": "supporting",
                "explanation": "Personal recommendation from someone you trust, though represents only one experience."
            },
            {
                "id": "e5",
                "text": "Customer reviews mention the phone occasionally freezes.",
                "type_for_positive": "contradicting",
                "type_for_negative": "supporting",
                "type_for_neutral": "contradicting",
                "explanation": "Reported technical issues could affect user experience."
            },
            {
                "id": "e6",
                "text": "The phone's camera received awards for quality.",
                "type_for_positive": "supporting",
                "type_for_negative": "contradicting",
                "type_for_neutral": "supporting",
                "explanation": "Recognized excellence in a key feature for many users."
            }
        ]
    }
]

scenarios_dict = {scenario["id"]: scenario for scenario in scenarios}

# Helper function to determine evidence type based on user's stance
def get_evidence_type(evidence, scenario_id, user_stance):
    """Determine if evidence is supporting or contradicting based on user's stance"""
    
    # For political policy scenario
    if scenario_id == "political_policy":
        if "liberal/left" in user_stance:
            return evidence.get("type_for_left", "neutral")
        else:  # conservative/right
            return evidence.get("type_for_right", "neutral")
            
    # For health study (coffee) scenario
    elif scenario_id == "health_study":
        if "a lot of coffee" in user_stance or "coffee occasionally" in user_stance:
            return evidence.get("type_for_coffee_drinker", "neutral")
        else:  # Rarely or never drinks coffee
            return evidence.get("type_for_non_drinker", "neutral")
            
    # For product review (Apple) scenario
    elif scenario_id == "product_review":
        if "Very positive" in user_stance or "Somewhat positive" in user_stance:
            return evidence.get("type_for_positive", "neutral")
        elif "negative" in user_stance:
            return evidence.get("type_for_negative", "neutral")
        else:  # Mixed or no experience
            return evidence.get("type_for_neutral", "neutral")
    
    # For other scenarios or fallback
    else:
        return evidence.get("type", "neutral")

def reset_scenario_task():
    #Reset the scenario task state.
    st.session_state.scenario_selected = None
    st.session_state.evidence_ratings = {}
    st.session_state.confirming_bias_score = 0
    if 'user_stance' in st.session_state and st.session_state.scenario_selected in st.session_state.user_stance:
        del st.session_state.user_stance[st.session_state.scenario_selected]
    if 'stance_strength' in st.session_state and st.session_state.scenario_selected in st.session_state.stance_strength:
        del st.session_state.stance_strength[st.session_state.scenario_selected]

def init_confirmation_bias_state():

    if 'bias_type' not in st.session_state:
        st.session_state.bias_type = None
    
    
    if 'wason_sequences_tested' not in st.session_state:
        st.session_state.wason_sequences_tested = []
    if 'wason_rule_guesses' not in st.session_state:
        st.session_state.wason_rule_guesses = []
    if 'wason_confirming_tests' not in st.session_state:
        st.session_state.wason_confirming_tests = 0
    if 'wason_disconfirming_tests' not in st.session_state:
        st.session_state.wason_disconfirming_tests = 0
        
    
    if 'scenario_selected' not in st.session_state:
        st.session_state.scenario_selected = None
    if 'evidence_ratings' not in st.session_state:
        st.session_state.evidence_ratings = {}
    if 'confirming_bias_score' not in st.session_state:
        st.session_state.confirming_bias_score = 0
    
    if 'user_stance' not in st.session_state:
        st.session_state.user_stance = {}
    if 'stance_strength' not in st.session_state:
        st.session_state.stance_strength = {}

def reset_all_confirmation():
    st.session_state.bias_type = None
    reset_wason_task()
    reset_scenario_task()
    st.session_state.user_stance = {}
    st.session_state.stance_strength = {}

def display_confirmation_intro():
    """Display the confirmation bias introduction page"""
    st.subheader("Confirmation Bias")
    
    st.markdown("""
    ### What is Confirmation Bias?
    
    Confirmation bias is the tendency to search for, interpret, and recall information in a way that confirms one's preexisting beliefs or hypotheses while giving less consideration to alternative possibilities.
    
    ### How it affects us:
    - We tend to search for evidence that supports our existing beliefs
    - We interpret ambiguous evidence as supporting our beliefs
    - We remember details that reinforce our point of view
    - We rarely seek out information that challenges our views
    
    ### In this simulator, you can experience confirmation bias through:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Wason's 2-4-6 Task**
        
        A classic cognitive psychology experiment where you need to discover a rule by testing sequences of numbers.
        """)
        if st.button("Try the Wason Task"):
            st.session_state.stage = "wason_intro"
            st.rerun()
    
    with col2:
        st.markdown("""
        **Evidence Evaluation Scenarios**
        
        Review evidence about a topic and see how your prior beliefs might influence which information you find most compelling.
        """)
        if st.button("Try Evidence Evaluation"):
            st.session_state.stage = "scenario_selection"
            st.rerun()
    
    
    st.markdown("---")
    if st.button("Back to Main Menu"):
        st.session_state.stage = "intro"
        st.session_state.bias_type = None
        st.rerun()

def display_wason_intro():
    
    st.subheader("Wason's 2-4-6 Task")
    
    st.markdown("""
    ### Instructions
    
    In this task, you need to discover a rule that generates sequences of three numbers.
    
    - You'll be given an initial sequence that follows the rule: **2, 4, 6**
    - You can test other sequences to see if they follow the rule
    - Your goal is to figure out what the rule is
    
    Most people find this task surprisingly challenging due to confirmation bias.
    
    Ready to discover the rule?
    """)
    
    if st.button("Begin the Task"):
        st.session_state.stage = "wason_task"
        st.rerun()
    
    if st.button("Back to Confirmation Bias Menu"):
        st.session_state.stage = "bias_intro"
        st.rerun()

def display_wason_task():
    st.subheader("Wason's 2-4-6 Task")
    
    
    st.markdown("### The following sequence follows the rule:")
    st.markdown("**2, 4, 6**")
    
    st.markdown(f"**Sequences tested:** {len(st.session_state.wason_sequences_tested)}")
    
    st.markdown("### Test a new sequence")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num1 = st.number_input("First number", value=0)
    with col2:
        num2 = st.number_input("Second number", value=0) 
    with col3:
        num3 = st.number_input("Third number", value=0)
    
    sequence = [num1, num2, num3]
    
    if st.button("Test This Sequence"):
        follows_rule = is_ascending_sequence(sequence)
        
        is_confirming = is_potentially_confirming(sequence)
        
        if is_confirming:
            st.session_state.wason_confirming_tests += 1
        else:
            st.session_state.wason_disconfirming_tests += 1
        
        sequence_str = f"{num1}, {num2}, {num3}"
        
        st.session_state.wason_sequences_tested.append({
            "sequence": sequence_str,
            "follows_rule": follows_rule,
            "is_confirming": is_confirming,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
        st.rerun()
    
    # Display results of previous tests
    if st.session_state.wason_sequences_tested:
        st.markdown("### Previous tests:")
        
        test_data = []
        for test in st.session_state.wason_sequences_tested:
            test_data.append({
                "Sequence": test["sequence"],
                "Follows Rule": "✅ Yes" if test["follows_rule"] else "❌ No",
                "Time": test["timestamp"]
            })
        
        test_df = pd.DataFrame(test_data)
        st.table(test_df)
    
    # Guess the rule
    st.markdown("### When you're ready, guess the rule:")
    rule_guess = st.text_input("I think the rule is...")
    
    if st.button("Submit My Guess"):
        st.session_state.wason_rule_guesses.append(rule_guess)
        
        # Check if the guess is correct
        correct_phrases = ["ascending", "increasing", "goes up", "greater than", ">", "higher"]
        correct = any(phrase in rule_guess.lower() for phrase in correct_phrases)
        
        if correct:
            st.session_state.stage = "wason_success"
        else:
            st.session_state.stage = "wason_incorrect"
        st.rerun()

def display_wason_success():
    st.subheader("That's Correct! 🎉")
    
    st.markdown("""
    ### The rule is: "Any sequence of ascending numbers"
    
    That's right! The numbers just need to increase - they don't need to follow any specific pattern.
    
    This task demonstrates confirmation bias because most people:
    
    1. Form an initial hypothesis (often "increasing by 2" since the example was 2-4-6)
    2. Only test sequences that would confirm their hypothesis (like 5-7-9)
    3. Rarely test sequences that might disprove their hypothesis (like 1-2-3)
    
    ### Your Testing Strategy:
    """)
    
    # Calculate confirming vs disconfirming tests
    total_tests = st.session_state.wason_confirming_tests + st.session_state.wason_disconfirming_tests
    
    if total_tests > 0:
        confirming_percent = (st.session_state.wason_confirming_tests / total_tests) * 100
        disconfirming_percent = (st.session_state.wason_disconfirming_tests / total_tests) * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        categories = ['Confirming Tests', 'Disconfirming Tests']
        values = [st.session_state.wason_confirming_tests, st.session_state.wason_disconfirming_tests]
   
        bars = ax.bar(categories, values, color=['#ff9999', '#99ff99'])
        ax.set_title('Your Testing Strategy')
        ax.set_ylabel('Number of Tests')
       
        for i, bar in enumerate(bars):
            height = bar.get_height()
            percentage = confirming_percent if i == 0 else disconfirming_percent
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height} ({percentage:.1f}%)',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Provide interpretation
        if confirming_percent > 75:
            st.markdown("""
            **Strong confirmation bias detected.**
            
            You primarily tested sequences that would confirm your initial hypothesis rather than trying to disprove it.
            """)
        elif confirming_percent > 50:
            st.markdown("""
            **Moderate confirmation bias detected.**
            
            You tested more confirming than disconfirming sequences, showing some confirmation bias.
            """)
        else:
            st.markdown("""
            **Good scientific thinking!**
            
            You tested many disconfirming sequences, which is excellent scientific practice.
            This approach makes you more likely to discover the true rule.
            """)
   
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Try Again"):
            reset_wason_task()
            st.session_state.stage = "wason_intro"
            st.rerun()
    
    with col2:
        if st.button("Return to Main Menu"):
            reset_all_confirmation()
            st.session_state.stage = "intro"
            st.rerun()

def display_wason_incorrect():
    st.subheader("Not quite right...")
    
    st.markdown("""
    ### That's not the rule we're looking for.
    
    Keep testing more sequences to discover the pattern.
    
    **Hint:** Try testing some very different types of sequences to narrow down the possibilities.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Continue Testing"):
            st.session_state.stage = "wason_task"
            st.rerun()
    
    with col2:
        if st.button("Give Up and See Answer"):
            st.session_state.stage = "wason_success"
            st.rerun()

def display_scenario_selection():
    st.subheader("Evidence Evaluation Scenarios")
    
    st.markdown("""
    ### Instructions
    
    In this task, you'll evaluate evidence related to a scenario where you might have a pre-existing belief.
    
    - You'll be presented with a scenario and a hypothesis
    - You'll share your personal stance on the topic
    - You'll rate how important or relevant different pieces of evidence are
    - At the end, we'll analyze how your ratings might reveal confirmation bias
    
    Choose a scenario to begin:
    """)
    
    for scenario in scenarios:
        if st.button(scenario["title"]):
            st.session_state.scenario_selected = scenario["id"]
            st.session_state.stage = "scenario_task"
            st.rerun()
    
    if st.button("Back to Confirmation Bias Menu"):
        st.session_state.stage = "bias_intro"
        st.rerun()

def display_scenario_task():
    if st.session_state.scenario_selected is None:
        st.error("No scenario selected. Please go back and select a scenario.")
        if st.button("Back to Scenario Selection"):
            st.session_state.stage = "scenario_selection"
            st.rerun()
        return
        
    scenario = scenarios_dict[st.session_state.scenario_selected]
    
    st.subheader(scenario["title"])
    
    st.markdown(f"""
    ### Scenario
    
    {scenario["description"]}
    """)
    
    # Get user stance if not already provided
    if scenario["id"] not in st.session_state.user_stance:
        st.markdown(f"### {scenario['stance_question']}")
        stance = st.radio(
            "Select the option that best describes you:",
            scenario["stance_options"],
            key=f"stance_{scenario['id']}"
        )
        
        st.markdown("### How strongly do you hold this position?")
        strength = st.slider(
            "Strength of stance", 
            min_value=1,
            max_value=10,
            value=5,
            key=f"strength_{scenario['id']}"
        )
        
        if st.button("Continue"):
            st.session_state.user_stance[scenario["id"]] = stance
            st.session_state.stance_strength[scenario["id"]] = strength
            st.rerun()
    else:
        # Display the user's stance
        st.markdown(f"""
        ### Your Position
        
        **{st.session_state.user_stance[scenario["id"]]}** (Strength: {st.session_state.stance_strength[scenario["id"]]}/10)
        
        ### Hypothesis to Evaluate
        
        **{scenario["hypothesis"]}**
        
        ### Please rate how important or relevant each piece of evidence is for evaluating this hypothesis:
        
        (1 = Not important/relevant, 10 = Extremely important/relevant)
        """)
        
        # Shuffle the evidence to avoid order effects
        evidence_copy = scenario["evidence"].copy()
        random.Random(42).shuffle(evidence_copy)
        
        # Create sliders for each piece of evidence
        for evidence in evidence_copy:
            key = f"{scenario['id']}_{evidence['id']}"
            rating = st.slider(
                evidence["text"], 
                min_value=1, 
                max_value=10, 
                value=5,
                key=key
            )
            
            user_stance = st.session_state.user_stance[scenario["id"]]
            
            evidence_type = get_evidence_type(evidence, scenario["id"], user_stance)
            
            st.session_state.evidence_ratings[key] = {
                "rating": rating,
                "type": evidence_type
            }
        
        # Calculate the confirmation bias score
        if st.button("Submit Ratings"):
            supporting_ratings = []
            contradicting_ratings = []
            neutral_ratings = []
            
            for key, data in st.session_state.evidence_ratings.items():
                if key.startswith(scenario['id']):  
                    if data["type"] == "supporting":
                        supporting_ratings.append(data["rating"])
                    elif data["type"] == "contradicting":
                        contradicting_ratings.append(data["rating"])
                    else:
                        neutral_ratings.append(data["rating"])
            
            avg_supporting = sum(supporting_ratings) / len(supporting_ratings) if supporting_ratings else 0
            avg_contradicting = sum(contradicting_ratings) / len(contradicting_ratings) if contradicting_ratings else 0
            
            # Calculate confirmation bias score as the difference between average ratings
            st.session_state.confirming_bias_score = avg_supporting - avg_contradicting
            
            st.session_state.stage = "scenario_results"
            st.rerun()
        
        if st.button("Back to Scenario Selection"):
            reset_scenario_task()
            st.session_state.stage = "scenario_selection"
            st.rerun()

def display_scenario_results():
    if st.session_state.scenario_selected is None:
        st.error("No scenario selected. Please go back and select a scenario.")
        if st.button("Back to Scenario Selection"):
            st.session_state.stage = "scenario_selection"
            st.rerun()
        return
        
    scenario = scenarios_dict[st.session_state.scenario_selected]
    
    st.subheader(f"Results: {scenario['title']}")
    
    # Display the user's stance
    stance = st.session_state.user_stance[scenario["id"]]
    strength = st.session_state.stance_strength[scenario["id"]]
    
    st.markdown(f"""
    ### Your Position
    
    **{stance}** (Strength: {strength}/10)
    
    ### Your Confirmation Bias Score: {st.session_state.confirming_bias_score:.2f}
    
    This score represents the difference between how you rated supporting vs. contradicting evidence.
    A positive score suggests you valued confirming evidence more highly than disconfirming evidence.
    """)
    
    # If stance strength is high, add interpretation
    if strength > 7 and st.session_state.confirming_bias_score > 1:
        st.markdown("""
        **Note:** Your strong pre-existing stance may have influenced how you evaluated the evidence.
        People with stronger prior beliefs often show stronger confirmation bias effects.
        """)
    
    # For specific scenarios, add contextual explanations
    if scenario["id"] == "political_policy":
        st.markdown("""
        ### Political Context
        
        In this scenario, the same evidence is interpreted differently depending on political orientation.
        
        For left-leaning participants:
        - Evidence supporting progressive policies aligns with existing views
        - Evidence against these policies contradicts existing views
        
        For right-leaning participants:
        - Evidence against progressive policies aligns with existing views
        - Evidence supporting these policies contradicts existing views
        
        This reflects how in real-world political discussions, the same facts can be weighted 
        differently based on pre-existing political beliefs.
        """)
    elif scenario["id"] == "health_study":
        st.markdown("""
        ### Coffee Preference Context
        
        In this scenario, the same evidence may be interpreted differently depending on your coffee consumption habits.
        
        Coffee drinkers may find evidence supporting coffee's health benefits more compelling, 
        while non-drinkers might be more receptive to evidence questioning these benefits.
        
        This reflects how our pre-existing habits and preferences can influence how we evaluate
        information about those same habits.
        """)
    elif scenario["id"] == "product_review":
        st.markdown("""
        ### Brand Experience Context
        
        In this scenario, the same evidence may be interpreted differently depending on your previous
        experiences with Apple products.
        
        Those with positive experiences may find supporting evidence more compelling and may discount
        negative evidence, while those with negative experiences may do the opposite.
        
        This demonstrates how our past experiences with a brand can create expectations that influence
        how we evaluate new information about their products.
        """)
    
    # Interpret the score
    if st.session_state.confirming_bias_score > 3:
        st.markdown("""
        ### Strong confirmation bias detected
        
        You rated evidence that supported the hypothesis as significantly more important than evidence that contradicted it.
        """)
    elif st.session_state.confirming_bias_score > 1:
        st.markdown("""
        ### Moderate confirmation bias detected
        
        You showed some tendency to value supporting evidence more than contradicting evidence.
        """)
    elif st.session_state.confirming_bias_score > -1:
        st.markdown("""
        ### Minimal confirmation bias detected
        
        You rated supporting and contradicting evidence roughly equally.
        """)
    else:
        st.markdown("""
        ### Reverse bias detected
        
        You actually rated contradicting evidence as more important than supporting evidence.
        This could indicate a disconfirmation bias or critical thinking.
        """)
   
    st.markdown("### Your Evidence Ratings")
    
    # Prepare data for the chart
    supporting_ratings = []
    contradicting_ratings = []
    neutral_ratings = []
    supporting_texts = []
    contradicting_texts = []
    neutral_texts = []
    
    for evidence in scenario["evidence"]:
        key = f"{scenario['id']}_{evidence['id']}"
        if key in st.session_state.evidence_ratings:
            rating = st.session_state.evidence_ratings[key]["rating"]
            short_text = evidence["text"][:50] + "..." if len(evidence["text"]) > 50 else evidence["text"]
            
            evidence_type = get_evidence_type(evidence, scenario["id"], stance)
            
            if evidence_type == "supporting":
                supporting_ratings.append(rating)
                supporting_texts.append(short_text)
            elif evidence_type == "contradicting":
                contradicting_ratings.append(rating)
                contradicting_texts.append(short_text)
            else:
                neutral_ratings.append(rating)
                neutral_texts.append(short_text)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Supporting evidence
    if supporting_texts:
        y_pos = np.arange(len(supporting_texts))
        ax1.barh(y_pos, supporting_ratings, color='green', alpha=0.7)
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(supporting_texts)
        ax1.set_xlim(0, 10)
        ax1.set_title('Supporting Evidence')
        ax1.set_xlabel('Your Rating')
    else:
        ax1.text(0.5, 0.5, 'No supporting evidence rated', 
                 horizontalalignment='center', verticalalignment='center')
    
    # Contradicting evidence
    if contradicting_texts:
        y_pos = np.arange(len(contradicting_texts))
        ax2.barh(y_pos, contradicting_ratings, color='red', alpha=0.7)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(contradicting_texts)
        ax2.set_xlim(0, 10)
        ax2.set_title('Contradicting Evidence')
        ax2.set_xlabel('Your Rating')
    else:
        ax2.text(0.5, 0.5, 'No contradicting evidence rated', 
                 horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # If there are neutral ratings, display below the chart
    if neutral_ratings:
        st.markdown("### Neutral Evidence")
        neutral_data = []
        for i, text in enumerate(neutral_texts):
            neutral_data.append({
                "Evidence": text,
                "Your Rating": neutral_ratings[i]
            })
        st.table(pd.DataFrame(neutral_data))
    
    # Explain confirmation bias
    st.markdown("""
    ### Understanding Confirmation Bias
    
    Confirmation bias is the tendency to search for, interpret, and recall information in a way that confirms our pre-existing beliefs.
    
    It affects us in many ways:
    
    - **Selective perception**: We notice information that supports our views and overlook contradictory information
    - **Biased evaluation**: We scrutinize contradicting evidence more closely than supporting evidence
    - **Memory bias**: We recall information that reinforces our beliefs more easily
    
    ### Real-world impact:
    
    - Political polarization
    - Poor decision-making
    - "Filter bubbles" in social media
    - Resistance to changing our minds despite new evidence
    
    ### How to minimize confirmation bias:
    
    - Actively seek out opposing viewpoints
    - Consider the possibility that you might be wrong
    - Ask others to critique your thinking
    - Set up decision-making processes that reduce bias
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Try Another Scenario"):
            reset_scenario_task()
            st.session_state.stage = "scenario_selection"
            st.rerun()
    
    with col2:
        if st.button("Try Wason Task"):
            reset_scenario_task()
            st.session_state.stage = "wason_intro"
            st.rerun()
    
    with col3:
        if st.button("Return to Main Menu"):
            reset_all_confirmation()
            st.session_state.stage = "intro"
            st.rerun()

def run_confirmation_bias_simulator():
    """Main function to run the confirmation bias simulator based on the current stage"""
    init_confirmation_bias_state()
    
    # Run the appropriate function based on the current stage
    if st.session_state.stage == "bias_intro" and st.session_state.bias_type == "confirmation":
        display_confirmation_intro()
    elif st.session_state.stage == "wason_intro":
        display_wason_intro()
    elif st.session_state.stage == "wason_task":
        display_wason_task()
    elif st.session_state.stage == "wason_success":
        display_wason_success()
    elif st.session_state.stage == "wason_incorrect":
        display_wason_incorrect()
    elif st.session_state.stage == "scenario_selection":
        display_scenario_selection()
    elif st.session_state.stage == "scenario_task":
        display_scenario_task()
    elif st.session_state.stage == "scenario_results":
        display_scenario_results()
    else:
        st.error(f"Unknown stage: {st.session_state.stage}. Redirecting to main menu.")
        if st.button("Go to Main Menu"):
            st.session_state.stage = 'intro'
            st.rerun()

