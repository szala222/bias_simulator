import streamlit as st
import random
import pandas as pd
import matplotlib as plt
import numpy as np
from datetime import datetime

# Define experiment scenarios for risk/choice framing (classic gain vs loss)
risk_scenarios = [
    {
        "id": "disease_problem",
        "title": "Public Health Decision",
        "description": "Imagine a rare disease outbreak is expected to kill 600 people if no action is taken.",
        "positive_frame": {
            "option_a": "Program A: 200 people will be saved.",
            "option_b": "Program B: 1/3 probability that 600 people will be saved, and 2/3 probability that no people will be saved."
        },
        "negative_frame": {
            "option_a": "Program A: 400 people will die.",
            "option_b": "Program B: 1/3 probability that nobody will die, and 2/3 probability that 600 people will die."
        },
        "explanation": "This is the classic 'Asian Disease Problem' from Tversky and Kahneman's research. People tend to be risk-averse when outcomes are framed as gains (positive frame) and risk-seeking when outcomes are framed as losses (negative frame), even though the actual outcomes are identical."
    },
    {
        "id": "cancer_treatment",
        "title": "Medical Treatment Decision",
        "description": "As a doctor, you need to recommend a treatment option to a patient with cancer.",
        "positive_frame": {
            "option_a": "Treatment A: 50% survival rate after five years.",
            "option_b": "Treatment B: All patients survive the first year, but only 10% survive after five years."
        },
        "negative_frame": {
            "option_a": "Treatment A: 50% mortality rate after five years.",
            "option_b": "Treatment B: No patients die in the first year, but 90% die after five years."
        },
        "explanation": "Medical decisions are highly susceptible to framing effects. The same treatment outcomes can seem more or less appealing depending on whether they are framed in terms of survival (positive) or mortality (negative)."
    },
    {
        "id": "evacuation_plan",
        "title": "Emergency Evacuation Plan",
        "description": "As an emergency manager, you must recommend an evacuation plan for a town of 1,000 residents threatened by an approaching hurricane.",
        "positive_frame": {
            "option_a": "Plan A: 400 residents will safely evacuate.",
            "option_b": "Plan B: 40% chance that all 1,000 residents will safely evacuate, and 60% chance that no residents will safely evacuate."
        },
        "negative_frame": {
            "option_a": "Plan A: 600 residents will not safely evacuate.",
            "option_b": "Plan B: 40% chance that no residents will fail to evacuate safely, and 60% chance that all 1,000 residents will fail to evacuate safely."
        },
        "explanation": "In emergency situations, how the potential outcomes are framed can significantly influence both decision-makers and the public. The same evacuation plan might be perceived differently depending on whether the focus is on lives saved or lives lost."
    }
]

# Define scenarios for attribute framing (product rating experiment)
attribute_scenarios = [
    {
        "id": "ground_beef",
        "title": "Ground Beef Evaluation",
        "description": "You're considering buying this ground beef for a family barbecue.",
        "positive_frame": "This ground beef is 80% lean.",
        "negative_frame": "This ground beef contains 20% fat.",
        "rating_question": "How would you rate the quality of this product?",
        "explanation": "This is a classic example of attribute framing. The same product described as '80% lean' is typically rated more favorably than when it's described as '20% fat', even though these statements are logically equivalent."
    },
    {
        "id": "medical_procedure",
        "title": "Medical Procedure Evaluation",
        "description": "You're considering undergoing an elective medical procedure.",
        "positive_frame": "This procedure has a 90% success rate.",
        "negative_frame": "This procedure has a 10% failure rate.",
        "rating_question": "How likely would you be to undergo this procedure?",
        "explanation": "Medical statistics presented in a positive frame (success rate) are usually perceived as more favorable and lead to higher consent rates than when presented in a negative frame (failure rate), despite being mathematically identical."
    },
    {
        "id": "battery_life",
        "title": "Smartphone Battery Evaluation",
        "description": "You're considering buying this new smartphone model.",
        "positive_frame": "This smartphone retains 70% of its battery capacity after 2 years of use.",
        "negative_frame": "This smartphone loses 30% of its battery capacity after 2 years of use.",
        "rating_question": "How would you rate the battery performance of this smartphone?",
        "explanation": "Technical specifications can be framed to emphasize either positive or negative aspects. The same battery performance described in terms of 'capacity retained' sounds better than when described in terms of 'capacity lost.'"
    },
    {
        "id": "customer_satisfaction",
        "title": "Customer Service Evaluation",
        "description": "You're considering signing up with this internet service provider.",
        "positive_frame": "This internet service provider has an 85% customer satisfaction rate.",
        "negative_frame": "This internet service provider has a 15% customer dissatisfaction rate.",
        "rating_question": "How would you rate the quality of this company's customer service?",
        "explanation": "Service quality metrics framed positively (satisfaction rate) typically elicit more favorable evaluations than when framed negatively (dissatisfaction rate), influencing customer acquisition decisions."
    }
]

# Define scenarios for goal framing (investment decision experiment)
goal_scenarios = [
    {
        "id": "retirement_saving",
        "title": "Retirement Savings Decision",
        "description": "You're deciding whether to increase your monthly retirement savings contribution.",
        "gain_frame": "By increasing your retirement savings now, you could gain an additional $240,000 in your retirement fund by age 65.",
        "loss_frame": "By not increasing your retirement savings now, you could lose out on an additional $240,000 in your retirement fund by age 65.",
        "neutral_frame": "Increasing your retirement savings now would change your retirement fund by an additional $240,000 by age 65.",
        "question": "How likely are you to increase your retirement savings contribution?",
        "explanation": "When it comes to long-term financial decisions, emphasizing the potential losses from inaction (loss frame) often motivates stronger action than emphasizing potential gains or neutral statements, despite the identical financial outcomes."
    },
    {
        "id": "energy_efficient",
        "title": "Energy Efficient Appliance Purchase",
        "description": "You're considering replacing your old refrigerator with a more energy-efficient model that costs $200 more upfront.",
        "gain_frame": "By purchasing the energy-efficient refrigerator, you'll gain $50 in savings each year on your electricity bill.",
        "loss_frame": "By not purchasing the energy-efficient refrigerator, you'll lose $50 each year on your electricity bill.",
        "neutral_frame": "The energy-efficient refrigerator would change your electricity bill by $50 each year.",
        "question": "How likely are you to purchase the energy-efficient refrigerator?",
        "explanation": "Environmental and efficiency decisions are often influenced by framing. Emphasizing ongoing losses tends to be more motivating than emphasizing equivalent gains, influencing consumer purchasing behavior for energy-efficient products."
    },
    {
        "id": "health_screening",
        "title": "Health Screening Decision",
        "description": "You're deciding whether to schedule a recommended preventive health screening that will take 2 hours and cost $50 after insurance.",
        "gain_frame": "By getting this screening, you increase your chance of early detection and successful treatment if a problem exists.",
        "loss_frame": "By skipping this screening, you decrease your chance of early detection and successful treatment if a problem exists.",
        "neutral_frame": "This screening affects your chance of early detection and successful treatment if a problem exists.",
        "question": "How likely are you to schedule the health screening?",
        "explanation": "Health promotion messages are significantly influenced by framing. Loss-framed messages (emphasizing risks of not acting) are often more effective for detection behaviors like screenings, while gain-framed messages can be more effective for prevention behaviors."
    }
]

# Create dictionaries for easy scenario lookup by ID
risk_dict = {scenario["id"]: scenario for scenario in risk_scenarios}
attribute_dict = {scenario["id"]: scenario for scenario in attribute_scenarios}
goal_dict = {scenario["id"]: scenario for scenario in goal_scenarios}

def init_framing_effect_state():
    if 'framing_experiment_type' not in st.session_state:
        st.session_state.framing_experiment_type = None
    if 'framing_scenario_selected' not in st.session_state:
        st.session_state.framing_scenario_selected = None
    if 'framing_frame_type' not in st.session_state:
        st.session_state.framing_frame_type = None
    if 'framing_user_choice' not in st.session_state:
        st.session_state.framing_user_choice = None
    if 'framing_user_rating' not in st.session_state:
        st.session_state.framing_user_rating = None
    if 'framing_results' not in st.session_state:
        st.session_state.framing_results = []
    if 'framing_completed_scenarios' not in st.session_state:
        st.session_state.framing_completed_scenarios = set()

def reset_framing_experiment():
    st.session_state.framing_experiment_type = None
    st.session_state.framing_scenario_selected = None
    st.session_state.framing_frame_type = None
    st.session_state.framing_user_choice = None
    st.session_state.framing_user_rating = None
    st.session_state.framing_completed_scenarios = set()

def go_to_framing_type_selection():
    st.session_state.stage = 'framing_type_selection'
    st.session_state.framing_experiment_type = None
    st.session_state.framing_scenario_selected = None
    st.session_state.framing_frame_type = None
    st.session_state.framing_user_choice = None
    st.session_state.framing_user_rating = None

def display_framing_intro():
    st.subheader("Framing Effect Experiment")
    
    st.markdown("""
    ## Welcome to the Framing Effect Simulator!
    
    **What is the framing effect?**
    
    The framing effect is a cognitive bias where people react differently to information depending on how it's presented (or "framed"). 
    Even when the same facts are presented, changing the wording or context can significantly influence decisions and judgments.
    
    ### Key types of framing:
    
    1. **Risk/Choice Framing** - How options with risk or uncertainty are presented can affect decisions
       - Example: "200 lives saved" vs "400 lives lost" in public health decisions
    
    2. **Attribute Framing** - How a single attribute of an object is described affects its evaluation
       - Example: "80% lean beef" vs "20% fat beef" for the same product
    
    3. **Goal Framing** - How the consequences of an action or inaction are emphasized
       - Example: "Gain something by acting" vs "Lose something by not acting"
    
    This simulator will let you experience all three types of framing and see how they might influence your own decisions.
    
    Let's explore how framing affects your decisions!
    """)
    
    # Create two columns for buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Experiment"):
            st.session_state.stage = 'framing_type_selection'
            st.rerun()
    
    with col2:
        if st.button("Back to Main Menu"):
            st.session_state.stage = "intro"
            st.session_state.bias_type = None
            st.rerun()

def display_framing_type_selection():
    st.markdown("## Select a Framing Experiment")
    st.markdown("Choose one of the following experiments to test your susceptibility to different types of framing effects:")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Risk/Choice Framing")
        st.markdown("Experience how different presentations of risk can affect your decisions, even when the outcomes are identical.")
        if st.button("Try Risk Framing"):
            st.session_state.framing_experiment_type = "risk"
            st.session_state.stage = 'framing_scenario_selection'
            st.rerun()
    
    with col2:
        st.markdown("### Attribute Framing")
        st.markdown("See how the same product attribute can be perceived differently when framed positively or negatively.")
        if st.button("Try Attribute Framing"):
            st.session_state.framing_experiment_type = "attribute"
            st.session_state.stage = 'framing_scenario_selection'
            st.rerun()
    
    with col3:
        st.markdown("### Goal Framing")
        st.markdown("Discover how emphasizing gains vs. losses can influence your motivation and choices.")
        if st.button("Try Goal Framing"):
            st.session_state.framing_experiment_type = "goal"
            st.session_state.stage = 'framing_scenario_selection'
            st.rerun()
    
    # Show results button if at least one experiment has been completed
    if st.session_state.framing_results:
        st.markdown("---")
        if st.button("View All Results"):
            st.session_state.stage = 'framing_all_results'
            st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("Back to Main Menu"):
        st.session_state.stage = "intro"
        st.rerun()

def display_framing_scenario_selection():
    if st.session_state.framing_experiment_type is None:
        st.error("No experiment type selected. Please go back and select an experiment type.")
        if st.button("Back to Framing Type Selection"):
            go_to_framing_type_selection()
            st.rerun()
        return
    
    experiment_type = st.session_state.framing_experiment_type
    
    # Set title based on experiment type
    if experiment_type == "risk":
        st.markdown("## Risk/Choice Framing Scenarios")
        scenarios = risk_scenarios
    elif experiment_type == "attribute":
        st.markdown("## Attribute Framing Scenarios")
        scenarios = attribute_scenarios
    elif experiment_type == "goal":
        st.markdown("## Goal Framing Scenarios")
        scenarios = goal_scenarios
    else:
        st.error(f"Unknown experiment type: {experiment_type}")
        return
    
    st.markdown("Select a scenario to test how framing affects your decisions:")
    
    # Create a grid layout for scenarios
    cols = st.columns(2)
    
    # Display scenarios in columns
    for i, scenario in enumerate(scenarios):
        with cols[i % 2]:
            scenario_id = scenario["id"]
            completed = "✅ " if scenario_id in st.session_state.framing_completed_scenarios else ""
            if st.button(f"{completed}{scenario['title']}", key=f"scenario_{scenario_id}"):
                st.session_state.framing_scenario_selected = scenario_id
                
                # Randomly assign a frame type to avoid bias
                if experiment_type == "risk":
                    st.session_state.framing_frame_type = random.choice(["positive", "negative"])
                elif experiment_type == "attribute":
                    st.session_state.framing_frame_type = random.choice(["positive", "negative"])
                elif experiment_type == "goal":
                    st.session_state.framing_frame_type = random.choice(["gain", "loss", "neutral"])
                
                st.session_state.stage = 'framing_experiment'
                st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("Back to Framing Type Selection"):
        go_to_framing_type_selection()
        st.rerun()

def display_risk_framing_experiment():
    scenario_id = st.session_state.framing_scenario_selected
    frame_type = st.session_state.framing_frame_type
    
    if scenario_id not in risk_dict:
        st.error(f"Unknown scenario: {scenario_id}")
        return
    
    scenario = risk_dict[scenario_id]
    
    st.markdown(f"## {scenario['title']}")
    st.markdown(f"### Scenario")
    st.markdown(scenario["description"])
    
    st.markdown("### Your Options:")
    
    # Get the appropriate frame based on random assignment
    if frame_type == "positive":
        option_a = scenario["positive_frame"]["option_a"]
        option_b = scenario["positive_frame"]["option_b"]
    else:  # negative frame
        option_a = scenario["negative_frame"]["option_a"]
        option_b = scenario["negative_frame"]["option_b"]
    
    # Present options
    st.markdown(f"**Option A:** {option_a}")
    st.markdown(f"**Option B:** {option_b}")
    
    st.markdown("### Which option would you choose?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Option A"):
            st.session_state.framing_user_choice = "A"
            
            # Record the result
            result = {
                "experiment_type": "risk",
                "scenario_id": scenario_id,
                "scenario_title": scenario["title"],
                "frame_type": frame_type,
                "user_choice": "A",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.framing_results.append(result)
            st.session_state.framing_completed_scenarios.add(scenario_id)
            st.session_state.stage = 'framing_result'
            st.rerun()
    
    with col2:
        if st.button("Option B"):
            st.session_state.framing_user_choice = "B"
            
            # Record the result
            result = {
                "experiment_type": "risk",
                "scenario_id": scenario_id,
                "scenario_title": scenario["title"],
                "frame_type": frame_type,
                "user_choice": "B",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.framing_results.append(result)
            st.session_state.framing_completed_scenarios.add(scenario_id)
            st.session_state.stage = 'framing_result'
            st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("Back to Scenario Selection"):
        st.session_state.framing_scenario_selected = None
        st.session_state.stage = 'framing_scenario_selection'
        st.rerun()

def display_attribute_framing_experiment():
    scenario_id = st.session_state.framing_scenario_selected
    frame_type = st.session_state.framing_frame_type
    
    if scenario_id not in attribute_dict:
        st.error(f"Unknown scenario: {scenario_id}")
        return
    
    scenario = attribute_dict[scenario_id]
    
    st.markdown(f"## {scenario['title']}")
    st.markdown(f"### Scenario")
    st.markdown(scenario["description"])
    
    # Display the framed information
    if frame_type == "positive":
        st.markdown(f"### Product Information:")
        st.markdown(f"**{scenario['positive_frame']}**")
    else:  # negative frame
        st.markdown(f"### Product Information:")
        st.markdown(f"**{scenario['negative_frame']}**")
    
    # Rating question
    st.markdown(f"### {scenario['rating_question']}")
    rating = st.slider("Rate from 1 (Very Negative) to 10 (Very Positive)", 1, 10, 5)
    
    if st.button("Submit Rating"):
        st.session_state.framing_user_rating = rating
        
        # Record the result
        result = {
            "experiment_type": "attribute",
            "scenario_id": scenario_id,
            "scenario_title": scenario["title"],
            "frame_type": frame_type,
            "user_rating": rating,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.session_state.framing_results.append(result)
        st.session_state.framing_completed_scenarios.add(scenario_id)
        st.session_state.stage = 'framing_result'
        st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("Back to Scenario Selection"):
        st.session_state.framing_scenario_selected = None
        st.session_state.stage = 'framing_scenario_selection'
        st.rerun()

def display_goal_framing_experiment():
    scenario_id = st.session_state.framing_scenario_selected
    frame_type = st.session_state.framing_frame_type
    
    if scenario_id not in goal_dict:
        st.error(f"Unknown scenario: {scenario_id}")
        return
    
    scenario = goal_dict[scenario_id]
    
    st.markdown(f"## {scenario['title']}")
    st.markdown(f"### Scenario")
    st.markdown(scenario["description"])
    
    # Display the framed message
    st.markdown(f"### Consider this information:")
    if frame_type == "gain":
        st.markdown(f"**{scenario['gain_frame']}**")
    elif frame_type == "loss":
        st.markdown(f"**{scenario['loss_frame']}**")
    else:  # neutral frame
        st.markdown(f"**{scenario['neutral_frame']}**")
    
    # Likelihood question
    st.markdown(f"### {scenario['question']}")
    likelihood = st.slider("Rate from 1 (Very Unlikely) to 10 (Very Likely)", 1, 10, 5)
    
    if st.button("Submit Response"):
        st.session_state.framing_user_rating = likelihood
        
        # Record the result
        result = {
            "experiment_type": "goal",
            "scenario_id": scenario_id,
            "scenario_title": scenario["title"],
            "frame_type": frame_type,
            "user_rating": likelihood,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.session_state.framing_results.append(result)
        st.session_state.framing_completed_scenarios.add(scenario_id)
        st.session_state.stage = 'framing_result'
        st.rerun()
    
    # Back button
    st.markdown("---")
    if st.button("Back to Scenario Selection"):
        st.session_state.framing_scenario_selected = None
        st.session_state.stage = 'framing_scenario_selection'
        st.rerun()

def display_framing_result():
    experiment_type = st.session_state.framing_experiment_type
    scenario_id = st.session_state.framing_scenario_selected
    
    if experiment_type == "risk":
        if scenario_id not in risk_dict:
            st.error(f"Unknown scenario: {scenario_id}")
            return
        scenario = risk_dict[scenario_id]
    elif experiment_type == "attribute":
        if scenario_id not in attribute_dict:
            st.error(f"Unknown scenario: {scenario_id}")
            return
        scenario = attribute_dict[scenario_id]
    elif experiment_type == "goal":
        if scenario_id not in goal_dict:
            st.error(f"Unknown scenario: {scenario_id}")
            return
        scenario = goal_dict[scenario_id]
    else:
        st.error(f"Unknown experiment type: {experiment_type}")
        return
    
    st.markdown(f"## Results: {scenario['title']}")
    
    # Find the most recent result for this scenario
    result = next((r for r in reversed(st.session_state.framing_results) 
                  if r["scenario_id"] == scenario_id), None)
    
    if not result:
        st.error("Could not find result data.")
        return
    
    # Display different results based on experiment type
    if experiment_type == "risk":
        frame_type = result["frame_type"]
        user_choice = result["user_choice"]
        
        st.markdown("### Your Decision:")
        st.markdown(f"You were presented with the **{frame_type} frame** and chose **Option {user_choice}**.")
        
        st.markdown("### What This Experiment Shows:")
        st.markdown("""
        In this classic risk framing experiment, the options presented are mathematically equivalent 
        regardless of frame, but people tend to make different choices depending on how the options are presented:
        
        - When presented with a **positive frame** (focusing on lives saved), people tend to be **risk-averse** 
          and choose the sure option (Option A)
          
        - When presented with a **negative frame** (focusing on lives lost), people tend to be **risk-seeking** 
          and choose the gamble (Option B)
        """)
        
        # Add reference data from classical studies
        st.markdown("### Classical Research Findings:")
        
        # Create a comparison between classical results and user's choice
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        # These are approximate percentages from the original Asian Disease Problem study
        classical_data = {
            'positive': {'A': 72, 'B': 28},  
            'negative': {'A': 22, 'B': 78}   
        }
        
        # Set up data for plotting
        frames = ['Positive Frame', 'Negative Frame']
        option_a_data = [classical_data['positive']['A'], classical_data['negative']['A']]
        option_b_data = [classical_data['positive']['B'], classical_data['negative']['B']]
        
        
        barWidth = 0.3
        
        
        r1 = np.arange(len(frames))
        r2 = [x + barWidth for x in r1]
        
        
        ax.bar(r1, option_a_data, width=barWidth, label='Option A (Sure Option)', color='skyblue')
        ax.bar(r2, option_b_data, width=barWidth, label='Option B (Risky Option)', color='salmon')
        
        # Add user's choice as a marker
        if frame_type == 'positive':
            marker_x = r1[0] if user_choice == 'A' else r2[0]
            ax.plot(marker_x, classical_data['positive']['A' if user_choice == 'A' else 'B'], 
                   'ko', markersize=10, label='Your Choice')
        else:  
            marker_x = r1[1] if user_choice == 'A' else r2[1]
            ax.plot(marker_x, classical_data['negative']['A' if user_choice == 'A' else 'B'], 
                   'ko', markersize=10, label='Your Choice')
        
        
        ax.set_xlabel('Frame Type')
        ax.set_ylabel('Percentage of Participants (%)')
        ax.set_title('Choices in Classical Framing Study (Tversky & Kahneman, 1981)')
        ax.set_xticks([r + barWidth/2 for r in range(len(frames))])
        ax.set_xticklabels(frames)
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for i, v in enumerate(option_a_data):
            ax.text(r1[i], v + 3, f"{v}%", ha='center')
        for i, v in enumerate(option_b_data):
            ax.text(r2[i], v + 3, f"{v}%", ha='center')
        
        
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("""
        The graph above shows results from Tversky and Kahneman's classic 1981 study on framing effects published in Science (Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. Science, 211(4481), 453-458). 
        
        In their experiment:
        - When presented with the **positive frame** (lives saved), **72%** of participants chose the sure option (A) 
          and **28%** chose the risky option (B)
        - When presented with the **negative frame** (lives lost), only **22%** chose the sure option (A)
          while **78%** chose the risky option (B)
        
        This dramatic reversal of preferences, based solely on how the identical problem was framed, 
        demonstrates the power of framing effects in decision-making under uncertainty.
        
        The black dot shows your own choice compared to the classical findings.
        """)
        
        st.markdown("### The Complete Scenario:")
        st.markdown(f"**Positive Frame:**")
        st.markdown(f"- Option A: {scenario['positive_frame']['option_a']}")
        st.markdown(f"- Option B: {scenario['positive_frame']['option_b']}")
        st.markdown(f"**Negative Frame:**")
        st.markdown(f"- Option A: {scenario['negative_frame']['option_a']}")
        st.markdown(f"- Option B: {scenario['negative_frame']['option_b']}")
        
        
        st.markdown("### Explanation:")
        st.markdown(scenario["explanation"])
    
    elif experiment_type == "attribute":
        frame_type = result["frame_type"]
        user_rating = result["user_rating"]
        
        st.markdown("### Your Evaluation:")
        st.markdown(f"You were presented with the **{frame_type} frame** and gave a rating of **{user_rating}/10**.")
        
        st.markdown("### What This Experiment Shows:")
        st.markdown("""
        In attribute framing experiments, a single attribute is described in either a positive or negative light:
        
        - **Positive frames** typically lead to more favorable evaluations
        - **Negative frames** typically lead to less favorable evaluations
        
        This happens even though the information conveyed is logically equivalent.
        """)
        
        # Add reference data from classical studies
        st.markdown("### Classical Research Findings:")
        
       
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        # These are representative values converted to a 10-point scale
        classical_data = {
            'positive': 7.2,  
            'negative': 5.1   
        }
        
        
        frames = ['Positive Frame', 'Negative Frame']
        classical_ratings = [classical_data['positive'], classical_data['negative']]
        
       
        x = np.arange(len(frames))
        width = 0.35
        
        ax.bar(x - width/2, classical_ratings, width, label='Average Ratings in Classical Studies', color='lightblue')
        
        
        user_data = [user_rating if frame_type == 'positive' else None, 
                    user_rating if frame_type == 'negative' else None]
        user_data = [0 if v is None else v for v in user_data]  
        
        # Only show the user bar for the frame they actually saw
        if frame_type == 'positive':
            ax.bar(x[0] + width/2, user_data[0], width, label='Your Rating', color='orange')
        else:
            ax.bar(x[1] + width/2, user_data[1], width, label='Your Rating', color='orange')
        
        
        ax.set_xlabel('Frame Type')
        ax.set_ylabel('Average Rating (1-10 scale)')
        ax.set_title('Ratings in Attribute Framing Studies')
        ax.set_xticks(x)
        ax.set_xticklabels(frames)
        ax.set_ylim(0, 10)
        
        
        for i, v in enumerate(classical_ratings):
            ax.text(x[i] - width/2, v + 0.3, f"{v}", ha='center')
        
        
        if frame_type == 'positive':
            ax.text(x[0] + width/2, user_data[0] + 0.3, f"{user_data[0]}", ha='center')
        else:
            ax.text(x[1] + width/2, user_data[1] + 0.3, f"{user_data[1]}", ha='center')
        
        
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("""
        The graph above shows representative results from attribute framing studies like Levin & Gaeth's 1988 research published in the Journal of Consumer Research (Levin, I. P., & Gaeth, G. J. (1988). How consumers are affected by the framing of attribute information before and after consuming the product. Journal of Consumer Research, 15(3), 374-378).
        
        In these studies:
        - Products described with **positive frames** (e.g., "75% lean") received average ratings around **7.2/10**
        - The same products described with **negative frames** (e.g., "25% fat") received lower ratings around **5.1/10**
        
        This consistent difference in evaluations demonstrates how attribute framing can significantly influence 
        product perceptions and consumer judgments, despite conveying identical information.
        
        The orange bar shows your own rating compared to the classical findings.
        """)
        
        st.markdown("### The Complete Scenario:")
        st.markdown(f"**Positive Frame:** {scenario['positive_frame']}")
        st.markdown(f"**Negative Frame:** {scenario['negative_frame']}")
        
        
        st.markdown("### Explanation:")
        st.markdown(scenario["explanation"])
    
    elif experiment_type == "goal":
        frame_type = result["frame_type"]
        user_rating = result["user_rating"]
        
        frame_type_display = {
            "gain": "gain frame (emphasizing benefits of taking action)",
            "loss": "loss frame (emphasizing costs of not taking action)",
            "neutral": "neutral frame (stating the facts without emphasis)"
        }.get(frame_type, frame_type)
        
        st.markdown("### Your Response:")
        st.markdown(f"You were presented with the **{frame_type_display}** and indicated a likelihood of **{user_rating}/10**.")
        
        st.markdown("### What This Experiment Shows:")
        st.markdown("""
        In goal framing experiments, the same outcome is framed in terms of gains, losses, or neutral facts:
        
        - **Gain frames** emphasize the benefits of performing an action
        - **Loss frames** emphasize the costs of not performing an action
        - **Neutral frames** present information without emphasizing gains or losses
        
        Research typically shows that loss frames are more persuasive than gain frames, with neutral frames 
        usually falling somewhere in between.
        """)
        
        # Add reference data from classical studies
        st.markdown("### Classical Research Findings:")
        
        # Create a comparison chart with classical goal framing studies
        fig, ax = plt.subplots(figsize=(10, 6))
        
        
        classical_data = {
            'gain': 6.4,    
            'loss': 7.3,    
            'neutral': 5.9  
        }
        
        
        frames = ['Gain Frame', 'Loss Frame', 'Neutral Frame']
        classical_ratings = [classical_data['gain'], classical_data['loss'], classical_data['neutral']]
        
        
        x = np.arange(len(frames))
        width = 0.35
        
        
        colors = ['green', 'red', 'blue']
        ax.bar(x - width/2, classical_ratings, width, label='Average Ratings in Research', color=colors)
        
        # Add user's rating
        user_data = [
            user_rating if frame_type == 'gain' else None,
            user_rating if frame_type == 'loss' else None,
            user_rating if frame_type == 'neutral' else None
        ]
        
        # Only show the user bar for the frame they actually saw
        if frame_type == 'gain':
            ax.bar(x[0] + width/2, user_data[0], width, label='Your Rating', color='orange')
        elif frame_type == 'loss':
            ax.bar(x[1] + width/2, user_data[1], width, label='Your Rating', color='orange')
        else:  # neutral
            ax.bar(x[2] + width/2, user_data[2], width, label='Your Rating', color='orange')
        
        
        ax.set_xlabel('Frame Type')
        ax.set_ylabel('Average Likelihood Rating (1-10 scale)')
        ax.set_title('Likelihood Ratings in Goal Framing Studies')
        ax.set_xticks(x)
        ax.set_xticklabels(frames)
        ax.set_ylim(0, 10)
        
        
        for i, v in enumerate(classical_ratings):
            ax.text(x[i] - width/2, v + 0.3, f"{v}", ha='center')
        
        
        if frame_type == 'gain':
            ax.text(x[0] + width/2, user_data[0] + 0.3, f"{user_data[0]}", ha='center')
        elif frame_type == 'loss':
            ax.text(x[1] + width/2, user_data[1] + 0.3, f"{user_data[1]}", ha='center')
        else:  # neutral
            ax.text(x[2] + width/2, user_data[2] + 0.3, f"{user_data[2]}", ha='center')
        
        
        ax.legend()
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("""
        The graph above shows representative results from goal framing research and meta-analyses, particularly drawing from Levin, Schneider, & Gaeth's 1998 review in Organizational Behavior and Human Decision Processes (Levin, I. P., Schneider, S. L., & Gaeth, G. J. (1998). All frames are not created equal: A typology and critical analysis of framing effects. Organizational Behavior and Human Decision Processes, 76(2), 149-188) and O'Keefe & Jensen's 2007 meta-analysis (O'Keefe, D. J., & Jensen, J. D. (2007). The relative persuasiveness of gain-framed and loss-framed messages for encouraging disease prevention behaviors: A meta-analytic review. Journal of Health Communication, 12(7), 623-644).
        
        In these studies:
        - **Loss frames** that emphasize costs of inaction are typically most effective, with average likelihood ratings around **7.3/10**
        - **Gain frames** that emphasize benefits of action are moderately effective, with average ratings around **6.4/10**
        - **Neutral frames** that simply state facts are least effective, with average ratings around **5.9/10**
        
        This pattern is particularly strong for detection behaviors (like health screenings) 
        and prevention behaviors (like using sunscreen), though the exact differences vary by domain.
        
        The orange bar shows your own likelihood rating compared to the research findings.
        """)
        
        st.markdown("### The Complete Scenario:")
        st.markdown(f"**Gain Frame:** {scenario['gain_frame']}")
        st.markdown(f"**Loss Frame:** {scenario['loss_frame']}")
        st.markdown(f"**Neutral Frame:** {scenario['neutral_frame']}")
        
        
        st.markdown("### Explanation:")
        st.markdown(scenario["explanation"])
    
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Try Another Scenario"):
            st.session_state.framing_scenario_selected = None
            st.session_state.stage = 'framing_scenario_selection'
            st.rerun()
    
    with col2:
        if st.button("Try Different Framing Type"):
            go_to_framing_type_selection()
            st.rerun()
    
    with col3:
        if st.button("View All Results"):
            st.session_state.stage = 'framing_all_results'
            st.rerun()

def display_framing_all_results():
    st.markdown("## All Framing Effect Results")
    
    if not st.session_state.framing_results:
        st.warning("You haven't completed any framing experiments yet.")
        if st.button("Try an Experiment"):
            go_to_framing_type_selection()
            st.rerun()
        return
    
    # Create tabs for different experiment types
    tab1, tab2, tab3 = st.tabs(["Risk/Choice Framing", "Attribute Framing", "Goal Framing"])
    
    with tab1:
        risk_results = [r for r in st.session_state.framing_results if r["experiment_type"] == "risk"]
        if risk_results:
            st.markdown("### Risk/Choice Framing Results")
            
            
            risk_df = pd.DataFrame(risk_results)
            
            
            display_df = risk_df.copy()
            display_df["frame_type"] = display_df["frame_type"].str.capitalize()
            display_df = display_df.rename(columns={
                "scenario_title": "Scenario",
                "frame_type": "Frame Type",
                "user_choice": "Your Choice",
                "timestamp": "Date/Time"
            })
            
            st.dataframe(display_df[["Scenario", "Frame Type", "Your Choice", "Date/Time"]])
            
            # Visualize choice patterns
            if len(risk_results) >= 2:
                st.markdown("### Visualization of Choice Patterns")
                
                
                frame_choices = risk_df.groupby(["frame_type", "user_choice"]).size().reset_index(name="count")
                
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                
                bar_width = 0.35
                r1 = np.arange(2)  
                r2 = [x + bar_width for x in r1]  
                
                
                positive_data = frame_choices[frame_choices["frame_type"] == "positive"]
                negative_data = frame_choices[frame_choices["frame_type"] == "negative"]
                
                
                pos_a = positive_data[positive_data["user_choice"] == "A"]["count"].sum() if not positive_data[positive_data["user_choice"] == "A"].empty else 0
                pos_b = positive_data[positive_data["user_choice"] == "B"]["count"].sum() if not positive_data[positive_data["user_choice"] == "B"].empty else 0
                neg_a = negative_data[negative_data["user_choice"] == "A"]["count"].sum() if not negative_data[negative_data["user_choice"] == "A"].empty else 0
                neg_b = negative_data[negative_data["user_choice"] == "B"]["count"].sum() if not negative_data[negative_data["user_choice"] == "B"].empty else 0
                
                
                ax.bar(r1[0], pos_a, width=bar_width, label='Option A', color='skyblue')
                ax.bar(r2[0], pos_b, width=bar_width, label='Option B', color='lightgreen')
                ax.bar(r1[1], neg_a, width=bar_width, color='skyblue')
                ax.bar(r2[1], neg_b, width=bar_width, color='lightgreen')
                
                
                ax.set_ylabel('Number of Choices')
                ax.set_title('Choices by Frame Type')
                ax.set_xticks([r + bar_width/2 for r in range(2)])
                ax.set_xticklabels(['Positive Frame', 'Negative Frame'])
                ax.legend()
                
                plt.tight_layout()
                st.pyplot(fig)
                
                
                st.markdown("""
                ### Interpretation:
                
                In typical risk framing experiments, researchers observe:
                
                - With positive frames (e.g., lives saved), people tend to choose the sure option (Option A)
                - With negative frames (e.g., lives lost), people tend to choose the risky option (Option B)
                
                This pattern is evidence of the framing effect, as the information and expected outcomes are identical 
                in both frames, yet decisions change based on presentation.
                """)
        else:
            st.info("You haven't completed any risk framing experiments yet.")
    
    with tab2:
        attribute_results = [r for r in st.session_state.framing_results if r["experiment_type"] == "attribute"]
        if attribute_results:
            st.markdown("### Attribute Framing Results")
            
            
            attribute_df = pd.DataFrame(attribute_results)
            
            
            display_df = attribute_df.copy()
            display_df["frame_type"] = display_df["frame_type"].str.capitalize()
            display_df = display_df.rename(columns={
                "scenario_title": "Scenario",
                "frame_type": "Frame Type",
                "user_rating": "Your Rating",
                "timestamp": "Date/Time"
            })
            
            st.dataframe(display_df[["Scenario", "Frame Type", "Your Rating", "Date/Time"]])
            
            # Visualize rating patterns
            if len(attribute_results) >= 2:
                st.markdown("### Visualization of Rating Patterns")
                
                
                avg_ratings = attribute_df.groupby(["frame_type"])["user_rating"].mean().reset_index()
                
               
                fig, ax = plt.subplots(figsize=(10, 6))
                
                
                bars = ax.bar(avg_ratings["frame_type"], avg_ratings["user_rating"], color=['skyblue', 'salmon'])
                
                
                ax.set_ylabel('Average Rating')
                ax.set_xlabel('Frame Type')
                ax.set_title('Average Ratings by Frame Type')
                ax.set_ylim(0, 10)
                
                
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{height:.2f}', ha='center', va='bottom')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                
                st.markdown("""
                ### Interpretation:
                
                In attribute framing experiments, researchers typically observe:
                
                - Positive frames (e.g., "80% lean") lead to more favorable ratings
                - Negative frames (e.g., "20% fat") lead to less favorable ratings
                
                This pattern demonstrates how logically equivalent information, when framed differently,
                can significantly impact perceptions and evaluations.
                """)
        else:
            st.info("You haven't completed any attribute framing experiments yet.")
    
    with tab3:
        goal_results = [r for r in st.session_state.framing_results if r["experiment_type"] == "goal"]
        if goal_results:
            st.markdown("### Goal Framing Results")
            
            
            goal_df = pd.DataFrame(goal_results)
            
            
            display_df = goal_df.copy()
            display_df["frame_type"] = display_df["frame_type"].str.capitalize()
            display_df = display_df.rename(columns={
                "scenario_title": "Scenario",
                "frame_type": "Frame Type",
                "user_rating": "Your Likelihood Rating",
                "timestamp": "Date/Time"
            })
            
            st.dataframe(display_df[["Scenario", "Frame Type", "Your Likelihood Rating", "Date/Time"]])
            
            # Visualize rating patterns
            if len(goal_results) >= 2:
                st.markdown("### Visualization of Goal Framing Effect")
                
                
                avg_ratings = goal_df.groupby(["frame_type"])["user_rating"].mean().reset_index()
                
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                
                colors = {'gain': 'green', 'loss': 'red', 'neutral': 'blue'}
                
                
                bars = ax.bar(avg_ratings["frame_type"], avg_ratings["user_rating"], 
                             color=[colors.get(frame, 'gray') for frame in avg_ratings["frame_type"]])
                
                
                ax.set_ylabel('Average Likelihood Rating')
                ax.set_xlabel('Frame Type')
                ax.set_title('Average Likelihood Ratings by Frame Type')
                ax.set_ylim(0, 10)
                
                
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{height:.2f}', ha='center', va='bottom')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                
                st.markdown("""
                ### Interpretation:
                
                In goal framing experiments, researchers typically observe:
                
                - Loss frames (emphasizing what will be lost by not acting) often generate stronger motivation
                - Gain frames (emphasizing what will be gained by acting) typically have moderate effectiveness
                - Neutral frames (simply stating facts) usually have the least impact
                
                This pattern shows how emphasizing the consequences of action/inaction can influence motivation and decision likelihood,
                even when the actual outcome is identical.
                """)
        else:
            st.info("You haven't completed any goal framing experiments yet.")
    
    # Educational content about framing effects
    st.markdown("---")
    st.markdown("""
    ## Understanding the Framing Effect
    
    ### What is happening in these experiments?
    
    The framing effect demonstrates that our decisions are influenced not just by facts and logic,
    but by how information is presented to us. Even when the actual information is identical, different
    presentations can lead to dramatically different decisions.
    
    ### Why do framing effects occur?
    
    Several cognitive mechanisms contribute to framing effects:
    
    1. **Loss aversion**: People tend to feel losses more strongly than equivalent gains (Prospect Theory, Kahneman & Tversky, 1979)
    2. **Cognitive processing**: Different frames activate different mental schemas and associations
    3. **Emotional responses**: Frames can trigger different emotional reactions that influence judgment
    4. **Reference points**: Frames establish different reference points for evaluating options
    
    ### Real-world implications:
    
    Framing effects have significant implications in many domains:
    
    - **Politics**: How policies are described influences public support
    - **Marketing**: Product descriptions are carefully framed to maximize appeal
    - **Healthcare**: How treatment options are presented affects patient decisions
    - **Finance**: Investment options described in terms of gains or losses affect risk tolerance
    - **Environmental messaging**: Climate action described as preventing losses vs. securing gains
    
    ### How to mitigate framing effects:
    
    While framing effects are powerful, you can reduce their impact by:
    
    - Being aware of framing in messages you receive
    - Reframing problems in multiple ways before deciding
    - Focusing on actual outcomes rather than descriptions
    - Seeking objective measures and base rates
    - Considering both gains and losses for any decision
    
    ### References:
    
    - Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. Science, 211(4481), 453-458.
    - Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263-291.
    - Levin, I. P., Schneider, S. L., & Gaeth, G. J. (1998). All frames are not created equal: A typology and critical analysis of framing effects. Organizational Behavior and Human Decision Processes, 76(2), 149-188.
    - Levin, I. P., & Gaeth, G. J. (1988). How consumers are affected by the framing of attribute information before and after consuming the product. Journal of Consumer Research, 15(3), 374-378.
    
    Remember that awareness of cognitive biases is the first step toward mitigating them!
    """)
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Try More Experiments"):
            go_to_framing_type_selection()
            st.rerun()
    
    with col2:
        if st.button("Return to Main Menu"):
            st.session_state.stage = "intro"
            st.rerun()

def run_framing_effect_simulator():
    init_framing_effect_state()
    
    # Run the appropriate function based on the current stage
    if st.session_state.stage == "bias_intro" and st.session_state.bias_type == "framing":
        display_framing_intro()
    elif st.session_state.stage == "framing_type_selection":
        display_framing_type_selection()
    elif st.session_state.stage == "framing_scenario_selection":
        display_framing_scenario_selection()
    elif st.session_state.stage == "framing_experiment":
        if st.session_state.framing_experiment_type == "risk":
            display_risk_framing_experiment()
        elif st.session_state.framing_experiment_type == "attribute":
            display_attribute_framing_experiment()
        elif st.session_state.framing_experiment_type == "goal":
            display_goal_framing_experiment()
    elif st.session_state.stage == "framing_result":
        display_framing_result()
    elif st.session_state.stage == "framing_all_results":
        display_framing_all_results()
    # If none of the above stages match, display an error message
    else:
        st.error(f"Unknown stage: {st.session_state.stage}. Redirecting to main menu.")
        if st.button("Go to Main Menu"):
            st.session_state.stage = 'intro'
            st.rerun()

