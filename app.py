import streamlit as st
import openai
import os
from time import sleep

# Set page configuration - using a simple text icon instead of emoji
st.set_page_config(
    page_title="Prompt Enhancer App",
    page_icon=":)",
    layout="wide"
)

# App title and description
st.title("AI Prompt Enhancer")
st.markdown("""
This app takes your basic prompt elements and enhances them into a more effective prompt for AI models.
Fill in the fields below and click 'Enhance Prompt' to generate an optimized version.
""")

# Function to enhance prompt using OpenAI
def enhance_prompt(role, context, task, api_key, model_name):
    # Configure OpenAI with API key
    client = openai.OpenAI(api_key=api_key)
    
    # Construct the base prompt
    base_prompt = f"""
    Role: {role}
    Context: {context}
    Task: {task}
    
    Please enhance this prompt to make it more effective for AI interactions.
    The enhanced prompt should:
    1. Include clear formatting instructions for the answer
    2. Request the AI to clarify assumptions before responding
    3. Be well-structured and detailed
    4. Include any relevant context from the original prompt
    5. Maintain the original intent of the task
    """
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert prompt engineer who specializes in crafting effective prompts for AI models."},
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return the enhanced prompt
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error: {str(e)}"

# Create sidebar for API key input and model selection
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    # Model selection dropdown
    model_name = st.selectbox(
        "Select OpenAI Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="GPT-3.5-Turbo is widely available. GPT-4 models require special access."
    )
    
    st.markdown("**Note:** Your API key is not stored and is only used for this session.")
    
    # Add example button
    if st.button("Load Example"):
        example_role = "Financial Advisor"
        example_context = "I'm planning for retirement in 15 years and want to optimize my investments."
        example_task = "Suggest an investment strategy based on my risk tolerance and timeline."
    else:
        example_role = ""
        example_context = ""
        example_task = ""

# Main form
with st.form("prompt_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.text_area("Role (Who should the AI be?)", 
                           value=example_role, 
                           height=100,
                           help="e.g., 'Financial Advisor', 'Python Expert', 'Marketing Specialist'")
    
    with col2:
        context = st.text_area("Context (Background information)", 
                              value=example_context, 
                              height=100,
                              help="Provide relevant background information for the AI")
    
    task = st.text_area("Task (What should the AI do?)", 
                       value=example_task, 
                       height=150,
                       help="Clearly describe what you want the AI to accomplish")
    
    submitted = st.form_submit_button("Enhance Prompt")

# Process form submission
if submitted:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar.")
    elif not role or not task:
        st.warning("Please fill in at least the Role and Task fields.")
    else:
        with st.spinner("Enhancing your prompt..."):
            # Add a slight delay to show the spinner
            sleep(1)
            enhanced_prompt = enhance_prompt(role, context, task, api_key, model_name)
            
        if enhanced_prompt.startswith("Error:"):
            st.error(enhanced_prompt)
        else:
            st.success("Prompt enhancement complete!")
            
            # Display the enhanced prompt
            st.header("Enhanced Prompt")
            st.text_area("Copy this enhanced prompt:", value=enhanced_prompt, height=400)
            
            # Add a copy button
            if st.button("Copy to Clipboard"):
                st.toast("Prompt copied to clipboard!")

# Add instructions at the bottom
st.markdown("---")
st.markdown("""
### How to use this app:
1. Enter your OpenAI API key in the sidebar
2. Select an appropriate model (GPT-3.5-Turbo is recommended for most users)
3. Fill in the Role, Context, and Task fields
4. Click 'Enhance Prompt' to generate an improved version
5. Copy the enhanced prompt to use with your preferred AI model
""")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and OpenAI GPT-3.5/GPT-4")