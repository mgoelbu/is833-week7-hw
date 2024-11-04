import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, RoutingChain
from langchain.chat_models import ChatOpenAI

# Initialize ChatOpenAI with the API key
llm = ChatOpenAI(openai_api_key=st.secrets["MyOpenAIKey"], model="gpt-4")

# Streamlit setup
st.title("Airline Experience Feedback")

# User feedback input
user_feedback = st.text_input("Share with us your experience of the latest trip.", "")

# Template to classify feedback type
classification_template = """Classify the feedback into one of the following categories:
1. "negative_airline" if the feedback is negative and specifically related to services provided by the airline (e.g., lost luggage, bad food, rude staff, delayed baggage).
2. "negative_other" if the feedback is negative but due to reasons beyond the airline's control (e.g., weather delay, security checkpoint delay, airport infrastructure issues).
3. "positive" if the feedback is positive.

Please respond with only one word: "negative_airline", "negative_other", or "positive".

Feedback:
{feedback}
"""

# Classification chain
classification_prompt = PromptTemplate(input_variables=["feedback"], template=classification_template)
classification_chain = LLMChain(llm=llm, prompt=classification_prompt)

# Manually define the responses
negative_airline_response = "We apologize for the inconvenience caused by our services. Our customer service team will contact you shortly."
negative_other_response = "We're sorry for the inconvenience. However, the situation was beyond our control. We appreciate your understanding."
positive_response = "Thank you for your positive feedback! We're glad you had a great experience with us."

# RoutingChain Setup
responses = {
    "negative_airline": negative_airline_response,
    "negative_other": negative_other_response,
    "positive": positive_response
}

# Run the chain if user feedback is provided
if user_feedback:
    try:
        # Get classification result
        classification_result = classification_chain.run({"feedback": user_feedback}).strip().lower()
        
        # Display the appropriate response based on classification
        response_text = responses.get(classification_result, "We're sorry, but we couldn't determine the nature of your feedback.")
        st.write(response_text)
        
    except Exception as e:
        st.error(f"An error occurred while processing your feedback: {e}")
