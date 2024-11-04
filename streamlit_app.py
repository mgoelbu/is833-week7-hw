import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# Initialize ChatOpenAI with the API key
llm = ChatOpenAI(openai_api_key=st.secrets["MyOpenAIKey"], model="gpt-4o-mini")

# Streamlit setup
st.title("Travel Experience Feedback")

# User feedback input
user_experience = st.text_input("Tell us about your recent travel experience.", "")

# Template to categorize experience type
experience_template = """Categorize the experience into one of the following types:
1. "airline_issue" if the experience was negative and due to something the airline controlled (e.g., lost baggage, poor customer service, delayed flight).
2. "external_issue" if the experience was negative but due to factors outside the airline's control (e.g., bad weather, security delays).
3. "positive_experience" if the feedback is positive.

Please respond with only one word: "airline_issue", "external_issue", or "positive_experience".

Experience:
{experience}
"""

# Classification chain
experience_prompt = PromptTemplate(input_variables=["experience"], template=experience_template)
experience_chain = LLMChain(llm=llm, prompt=experience_prompt)

# Define response messages
airline_issue_response = "We apologize for the inconvenience caused by our services. Our support team will reach out to you shortly."
external_issue_response = "We're sorry for the inconvenience, but this issue was beyond our control. Thank you for your understanding."
positive_experience_response = "Thank you for your feedback! We’re delighted that you had a great experience with us."

# Run the chain if user experience is provided
if user_experience:
    try:
        # Get experience categorization result
        experience_type = experience_chain.run({"experience": user_experience})

        # Display the appropriate response based on experience type
        if experience_type == "airline_issue":
            st.write(airline_issue_response)
        elif experience_type == "external_issue":
            st.write(external_issue_response)
        elif experience_type == "positive_experience":
            st.write(positive_experience_response)
        else:
            st.write("Thank you for your feedback.")  # Fallback for unexpected results
            
    except Exception as e:
        st.error(f"An error occurred while processing your experience: {e}")
