import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the tasks for anchoring bias experiment
tasks = [
    {
        "id": "budapest",
        "name": "Population of Budapest",
        "question": "What is the population of Budapest, Hungary?",
        "actual_value": 1756000,  # Approximate population
        "unit": "people",
        "higher_lower_text": "The actual population is {} than the random number."
    },
    {
        "id": "un_africa",
        "name": "African Nations in UN",
        "question": "What percentage of United Nations member states are African nations?",
        "actual_value": 28,  # Approximate percentage
        "unit": "%",
        "higher_lower_text": "The actual percentage is {} than the random number."
    },
    {
        "id": "dev_salary",
        "name": "Software Engineer Salary",
        "question": "What is the average annual salary of a software engineer in Germany?",
        "actual_value": 65000,  # Approximate salary in EUR
        "unit": "€",
        "higher_lower_text": "The actual salary is {} than the random number."
    },
    {
        "id": "earth_sun",
        "name": "Earth-Sun Distance",
        "question": "What is the average distance between Earth and the Sun in kilometers?",
        "actual_value": 149600000,  # Approximate distance in km
        "unit": "km",
        "higher_lower_text": "The actual distance is {} than the random number."
    },
    {
        "id": "amazon_length",
        "name": "Length of Amazon River",
        "question": "What is the length of the Amazon River in kilometers?",
        "actual_value": 6400,  # Approximate length in km
        "unit": "km",
        "higher_lower_text": "The actual length is {} than the random number."
    }
]


tasks_dict = {task["id"]: task for task in tasks}

def init_anchoring_bias_state():
    if 'anchor' not in st.session_state:
        st.session_state.anchor = None
    if 'current_task' not in st.session_state:
        st.session_state.current_task = None
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = set()
    if 'higher_lower_guess' not in st.session_state:
        st.session_state.higher_lower_guess = None
    if 'guess_correct' not in st.session_state:
        st.session_state.guess_correct = None

def reset_anchoring_experiment():
    st.session_state.anchor = None
    st.session_state.current_task = None
    st.session_state.results = []
    st.session_state.completed_tasks = set()
    st.session_state.higher_lower_guess = None
    st.session_state.guess_correct = None

def go_to_task_selection():
    st.session_state.stage = 'task_selection'
    st.session_state.anchor = None
    st.session_state.current_task = None
    st.session_state.higher_lower_guess = None
    st.session_state.guess_correct = None

def retry_current_task():
    st.session_state.stage = 'generate_anchor'
    st.session_state.anchor = None
    st.session_state.higher_lower_guess = None
    st.session_state.guess_correct = None

def next_anchoring_task():
    # Find a task that hasn't been completed yet
    available_tasks = [task["id"] for task in tasks if task["id"] not in st.session_state.completed_tasks]
    if available_tasks:
        st.session_state.current_task = available_tasks[0]
        st.session_state.stage = 'generate_anchor'
        st.session_state.anchor = None
        st.session_state.higher_lower_guess = None
        st.session_state.guess_correct = None
    else:
        st.session_state.stage = 'task_selection'
        st.session_state.current_task = None
        st.session_state.higher_lower_guess = None
        st.session_state.guess_correct = None

def display_anchoring_intro():
    st.subheader("Anchoring Bias Experiment")
    
    st.markdown("""
    ## Welcome to the Anchoring Bias Simulator!
    
    **What is anchoring bias?**
    
    Anchoring bias is a cognitive bias where people rely too heavily on the first piece of information they encounter (the "random number") 
    when making decisions or estimates.
    
    **How this experiment works:**
    1. You'll be given a random number
    2. You'll guess if the actual value is higher or lower than this random number
    3. You'll make your best estimate of the actual value
    4. We'll show you how the random number might have influenced your estimate
    
    Let's see how susceptible you are to anchoring bias!
    """)
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Experiment"):
            st.session_state.stage = 'task_selection'
            st.rerun()
    
    with col2:
        if st.button("Back to Main Menu"):
            st.session_state.stage = "intro"
            st.session_state.bias_type = None
            st.rerun()

def display_task_selection():
    st.markdown("## Select a Task")
    st.markdown("Choose one of the following estimation tasks to test your susceptibility to anchoring bias:")
    
    
    cols = st.columns(3)
    
    # Display tasks in columns
    for i, task in enumerate(tasks):
        with cols[i % 3]:
            task_id = task["id"]
            completed = "✅ " if task_id in st.session_state.completed_tasks else ""
            if st.button(f"{completed}{task['name']}", key=f"task_{task_id}"):
                st.session_state.current_task = task_id
                st.session_state.stage = 'generate_anchor'
                st.rerun()
    
    # Show results button if at least one task has been completed
    if st.session_state.completed_tasks:
        st.markdown("---")
        if st.button("View All Results"):
            st.session_state.stage = 'all_results'
            st.rerun()
    
    
    st.markdown("---")
    if st.button("Back to Main Menu"):
        st.session_state.stage = "intro"
        st.session_state.bias_type = None
        st.rerun()

def display_generate_anchor():
    current_task = tasks_dict[st.session_state.current_task]
    
    st.markdown(f"## Task: {current_task['name']}")
    st.markdown(f"**{current_task['question']}**")
    
    st.markdown("### First, let's generate a random number")
    st.markdown("Click the button below to generate a random number.")
    
    # Generate a random anchor that's significantly different from the actual value
    if st.button("Generate Random Number"):
        lower_bound = int(current_task['actual_value'] * 0.3)
        upper_bound = int(current_task['actual_value'] * 2.5)
        st.session_state.anchor = random.randint(lower_bound, upper_bound)
        st.session_state.stage = 'show_anchor'
        st.rerun()
    
    
    if st.button("Back to Task Selection", key="back_to_tasks_1"):
        go_to_task_selection()
        st.rerun()

def display_show_anchor():
    current_task = tasks_dict[st.session_state.current_task]
    
    st.markdown(f"## Task: {current_task['name']}")
    st.markdown(f"**{current_task['question']}**")
    
    st.markdown(f"### Your random number: {st.session_state.anchor:,}")
    
    st.markdown("### Do you think the actual value is higher or lower than the random number?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("HIGHER than the random number"):
            st.session_state.higher_lower_guess = "higher"
            actual_comparison = "higher" if current_task['actual_value'] > st.session_state.anchor else "lower"
            st.session_state.guess_correct = (st.session_state.higher_lower_guess == actual_comparison)
            st.session_state.stage = 'estimate'
            st.rerun()
    
    with col2:
        if st.button("LOWER than the random number"):
            st.session_state.higher_lower_guess = "lower"
            actual_comparison = "higher" if current_task['actual_value'] > st.session_state.anchor else "lower"
            st.session_state.guess_correct = (st.session_state.higher_lower_guess == actual_comparison)
            st.session_state.stage = 'estimate'
            st.rerun()
    
    
    if st.button("Back to Task Selection", key="back_to_tasks_2"):
        go_to_task_selection()
        st.rerun()

def display_show_guess_result():
    current_task = tasks_dict[st.session_state.current_task]
    
    st.markdown(f"## Task: {current_task['name']}")
    st.markdown(f"**{current_task['question']}**")
    
    st.markdown(f"### Your random number: {st.session_state.anchor:,}")
    
    
    actual_comparison = "higher" if current_task['actual_value'] > st.session_state.anchor else "lower"
    
    if st.session_state.guess_correct:
        st.success(f"✅ You were correct! The actual value is {actual_comparison} than the random number.")
    else:
        st.error(f"❌ Actually, the true value is {actual_comparison} than the random number.")
    
    if st.button("Continue to Estimation"):
        st.session_state.stage = 'estimate'
        st.rerun()
    
    
    if st.button("Back to Task Selection", key="back_to_tasks_3"):
        go_to_task_selection()
        st.rerun()

def display_estimate():
    current_task = tasks_dict[st.session_state.current_task]
    
    st.markdown(f"## Task: {current_task['name']}")
    st.markdown(f"**{current_task['question']}**")
    
    st.markdown(f"### Your random number: {st.session_state.anchor:,}")
    
    st.markdown("### Now, make your best estimate")
    
    
    user_estimate = st.number_input(
        f"Your estimate ({current_task['unit']})",
        min_value=0,
        max_value=int(current_task['actual_value'] * 5),
        step=1,
        format="%d"
    )
    
    if st.button("Submit Estimate"):
        # Calculate the percentage difference from actual value
        percentage_diff = abs(user_estimate - current_task['actual_value']) / current_task['actual_value'] * 100
        
        # Calculate the anchor influence (how close the estimate is to the anchor vs. actual value)
        if st.session_state.anchor != current_task['actual_value']:  
            anchor_pull = abs(user_estimate - current_task['actual_value']) / abs(st.session_state.anchor - current_task['actual_value'])
            anchor_pull = min(anchor_pull, 1.0)  
        else:
            anchor_pull = 0
            
        
        st.session_state.results = [r for r in st.session_state.results if r["task_id"] != current_task["id"]]
        
        # Add the new result
        st.session_state.results.append({
            "task_id": current_task['id'],
            "task": current_task['name'],
            "anchor": st.session_state.anchor,
            "actual_value": current_task['actual_value'],
            "estimate": user_estimate,
            "percentage_diff": percentage_diff,
            "anchor_pull": anchor_pull,
            "unit": current_task['unit'],
            "higher_lower_guess": st.session_state.higher_lower_guess,
            "guess_correct": st.session_state.guess_correct
        })
        
        
        st.session_state.completed_tasks.add(current_task['id'])
        
        
        st.session_state.stage = 'task_result'
        st.rerun()
    
    
    if st.button("Back to Task Selection", key="back_to_tasks_4"):
        go_to_task_selection()
        st.rerun()

def display_task_result():
    current_task = tasks_dict[st.session_state.current_task]
    
    
    result = next((r for r in st.session_state.results if r["task_id"] == current_task["id"]), None)
    
    if not result:
        st.error("Something went wrong. Result not found.")
        if st.button("Back to Home"):
            go_to_task_selection()
            st.rerun()
    else:
        st.markdown(f"## Results: {current_task['name']}")
        
       
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Your Estimate vs. Actual Value")
            
            
            comparison_data = {
                "Value": [f"{int(result['anchor']):,} {result['unit']}", 
                          f"{int(result['estimate']):,} {result['unit']}", 
                          f"{int(result['actual_value']):,} {result['unit']}"],
                "Description": ["Your Random Number", "Your Estimate", "Actual Value"]
            }
            st.table(pd.DataFrame(comparison_data))
            
            
            guess_result = "Correct" if result.get('guess_correct', False) else "Incorrect"
            st.markdown(f"**Higher/Lower Guess:** {result.get('higher_lower_guess', 'Not provided')} (was {guess_result})")
            
            
            error_percentage = abs(result['estimate'] - result['actual_value']) / result['actual_value'] * 100
            
            st.markdown(f"### Estimation Error: {error_percentage:.1f}%")
            
            
            distance_to_anchor = abs(result['estimate'] - result['anchor'])
            distance_to_actual = abs(result['estimate'] - result['actual_value'])
            
            
            if distance_to_anchor < distance_to_actual:
                st.markdown("**Strong Anchoring Effect Detected**: Your estimate was closer to the random number than to the actual value.")
            elif (result['anchor'] < result['actual_value'] and result['estimate'] < result['actual_value']) or \
                 (result['anchor'] > result['actual_value'] and result['estimate'] > result['actual_value']):
                st.markdown("**Moderate Anchoring Effect Detected**: Your estimate was biased in the direction of the random number.")
            else:
                st.markdown("**No Clear Anchoring Effect**: Your estimate did not follow the direction of the random number.")
        
        with col2:
            st.markdown("### Visualization")
            
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            
            labels = ['Random Number', 'Your Estimate', 'Actual Value']
            values = [result['anchor'], result['estimate'], result['actual_value']]
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            
            
            bars = ax.bar(labels, values, color=colors)
            ax.set_title(current_task['name'])
            ax.set_ylabel(result['unit'])
            
            
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05 * max(values),
                        f'{int(height):,}',
                        ha='center', va='bottom', rotation=0)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        st.markdown("""
        ### Understanding Anchoring Bias
        
        Anchoring bias occurs when we rely too heavily on the first piece of information we encounter (the random number).
        Even when we know the random number is arbitrary, it can still influence our judgment.
        
        This effect is powerful in many real-world scenarios:
        - Salary negotiations
        - Price perceptions in shopping
        - Judicial sentencing
        - Medical diagnoses
        """)
        
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Try Again"):
                retry_current_task()
                st.rerun()
        
        with col2:
            if st.button("Next Question"):
                next_anchoring_task()
                st.rerun()
        
        with col3:
            if st.button("Back to Home"):
                go_to_task_selection()
                st.rerun()

def display_all_results():
    st.markdown("## All Results")
    
    if not st.session_state.results:
        st.warning("You haven't completed any tasks yet.")
    else:
        
        results_df = pd.DataFrame(st.session_state.results)
        
        
        st.markdown("### Summary of Your Estimates")
        
        # Format the table 
        display_df = results_df.copy()
        for i, row in display_df.iterrows():
            display_df.loc[i, 'anchor'] = f"{int(row['anchor']):,} {row['unit']}"
            display_df.loc[i, 'actual_value'] = f"{int(row['actual_value']):,} {row['unit']}"
            display_df.loc[i, 'estimate'] = f"{int(row['estimate']):,} {row['unit']}"
            display_df.loc[i, 'percentage_diff'] = f"{row['percentage_diff']:.1f}%"
            
            
            if 'higher_lower_guess' in row and 'guess_correct' in row:
                guess_result = "✅" if row['guess_correct'] else "❌"
                display_df.loc[i, 'higher_lower_guess'] = f"{row['higher_lower_guess']} {guess_result}"
            else:
                display_df.loc[i, 'higher_lower_guess'] = "N/A"
        
        
        display_columns = ['task', 'anchor', 'higher_lower_guess', 'estimate', 'actual_value', 'percentage_diff']
        available_columns = [col for col in display_columns if col in display_df.columns]
        
        st.table(display_df[available_columns])
        
        
        st.markdown("### Visualization of Anchoring Effect")
        
        
        num_tasks = len(results_df)
        fig, axes = plt.subplots(1, num_tasks, figsize=(5*num_tasks, 5))
        
        
        if num_tasks == 1:
            axes = [axes]
            
        for i, (_, result) in enumerate(results_df.iterrows()):
            # Create data for the plot
            labels = ['Random Number', 'Your Estimate', 'Actual Value']
            values = [result['anchor'], result['estimate'], result['actual_value']]
            colors = ['#ff9999', '#66b3ff', '#99ff99']
            
            
            bars = axes[i].bar(labels, values, color=colors)
            axes[i].set_title(result['task'])
            axes[i].set_ylabel(result['unit'])
            
            for bar in bars:
                height = bar.get_height()
                axes[i].text(bar.get_x() + bar.get_width()/2., height + 0.05 * max(values),
                        f'{int(height):,}',
                        ha='center', va='bottom', rotation=0)
        
        plt.tight_layout()
        st.pyplot(fig)
                
        st.markdown("### Analysis of Anchoring Effect")
        
        avg_error = results_df['percentage_diff'].mean()
        
        strong_effect_count = 0
        moderate_effect_count = 0
        no_effect_count = 0
        
        for _, row in results_df.iterrows():
            distance_to_anchor = abs(row['estimate'] - row['anchor'])
            distance_to_actual = abs(row['estimate'] - row['actual_value'])
            
            if distance_to_anchor < distance_to_actual:
                strong_effect_count += 1
            elif (row['anchor'] < row['actual_value'] and row['estimate'] < row['actual_value']) or \
                 (row['anchor'] > row['actual_value'] and row['estimate'] > row['actual_value']):
                moderate_effect_count += 1
            else:
                no_effect_count += 1
        
        total_tasks = len(results_df)
        strong_percent = (strong_effect_count / total_tasks) * 100
        moderate_percent = (moderate_effect_count / total_tasks) * 100
        no_effect_percent = (no_effect_count / total_tasks) * 100
        
        # Create a pie chart of anchoring effects
        fig, ax = plt.subplots(figsize=(8, 6))
        effect_labels = ['Strong Effect', 'Moderate Effect', 'No Clear Effect']
        effect_sizes = [strong_effect_count, moderate_effect_count, no_effect_count]
        effect_colors = ['#ff6666', '#ffcc66', '#66cc66']
        

        if sum(effect_sizes) > 0:
            effect_labels = [f"{label} ({size/sum(effect_sizes)*100:.1f}%)" for label, size in zip(effect_labels, effect_sizes)]
            
            ax.pie(effect_sizes, labels=effect_labels, colors=effect_colors, autopct='%1.1f%%',
                   startangle=90, shadow=True)
            ax.axis('equal')  
            plt.title('Types of Anchoring Effects Observed')
            
            st.pyplot(fig)
        
        # Calculate higher/lower guess accuracy
        if 'guess_correct' in results_df.columns:
            correct_guesses = results_df['guess_correct'].sum()
            guess_accuracy = (correct_guesses / len(results_df)) * 100
            st.markdown(f"**Higher/Lower Guess Accuracy:** {guess_accuracy:.1f}%")
        
        st.markdown(f"**Average Estimation Error:** {avg_error:.1f}%")
        st.markdown(f"**Strong Anchoring Effect:** {strong_percent:.1f}% of tasks (estimate closer to anchor than actual value)")
        st.markdown(f"**Moderate Anchoring Effect:** {moderate_percent:.1f}% of tasks (estimate biased in same direction as anchor)")
        st.markdown(f"**No Clear Anchoring Effect:** {no_effect_percent:.1f}% of tasks")
        
        # Interpretation
        st.markdown("### What This Means")
        
        if strong_percent + moderate_percent > 75:
            st.markdown("""
            **Strong Anchoring Effect Detected**
            
            Your estimates were strongly influenced by the random number values. This is a common cognitive bias 
            that affects most people, even when they're aware of it.
            """)
        elif strong_percent + moderate_percent > 50:
            st.markdown("""
            **Moderate Anchoring Effect Detected**
            
            Your estimates show some influence from the random number values, though you were able to 
            resist the effect in some cases.
            """)
        else:
            st.markdown("""
            **Minimal Anchoring Effect Detected**
            
            You showed resistance to the anchoring effect in most tasks. This is uncommon and suggests 
            you may be less susceptible to this particular cognitive bias.
            """)
        
        st.markdown("""
        ### Understanding Anchoring Bias
        
        Anchoring bias occurs when we rely too heavily on the first piece of information we encounter (the random number).
        Even when we know the random number is arbitrary, it can still influence our judgment.
        
        **Real-world implications:**
        - **Negotiations:** Initial offers strongly influence the final outcome
        - **Shopping:** "Original" prices affect our perception of discounts
        - **Decision-making:** Initial data points can skew our analysis
        - **Medical diagnoses:** First symptoms can anchor a doctor's thinking
        
        **How to mitigate anchoring bias:**
        - Be aware of potential anchors
        - Consider multiple reference points
        - Deliberately challenge your initial estimates
        - Seek information from diverse sources
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Back to Task Selection"):
                go_to_task_selection()
                st.rerun()
        
        with col2:
            if st.button("Start Over"):
                reset_anchoring_experiment()
                st.session_state.stage = "intro"
                st.rerun()

def run_anchoring_bias_simulator():
    init_anchoring_bias_state()
    
    # Run the appropriate function based on the current stage
    if st.session_state.stage == "bias_intro" and st.session_state.bias_type == "anchoring":
        display_anchoring_intro()
    elif st.session_state.stage == "task_selection":
        display_task_selection()
    elif st.session_state.stage == "generate_anchor":
        display_generate_anchor()
    elif st.session_state.stage == "show_anchor":
        display_show_anchor()
    elif st.session_state.stage == "show_guess_result":
        display_show_guess_result()
    elif st.session_state.stage == "estimate":
        display_estimate()
    elif st.session_state.stage == "task_result":
        display_task_result()
    elif st.session_state.stage == "all_results":
        display_all_results()