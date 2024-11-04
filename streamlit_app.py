import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

# Initialize ChatOpenAI with the API key
llm = ChatOpenAI(openai_api_key=st.secrets["MyOpenAIKey"], model="gpt-4o-mini")

# Streamlit setup
st.title("Airline Experience Feedback")

# User feedback input
user_feedback = st.text_input("Tell us about your recent travel experience", "")

# Template to classify feedback type
classification_template = """
**Task:** Please analyze the following customer feedback and classify it into one of the three categories below:

1. **negative_airline**: The feedback is negative and directly relates to services provided by the airline. Examples include lost luggage, unsatisfactory in-flight meals, rude or unhelpful staff, or delays caused by airline operations (e.g., delayed baggage handling).

2. **negative_external**: The feedback is negative but pertains to issues beyond the airline's control. This covers situations like delays due to adverse weather conditions, long waits at security checkpoints, or problems with airport facilities and infrastructure.

3. **positive**: The feedback is positive, reflecting satisfaction or praise regarding any aspect of the travel experience.

**Your goal is to assign the most appropriate category to the feedback.**

Please respond with only one word: "negative_airline", "negative_external", or "positive".

**Feedback:**
{feedback}
"""

# Classification chain
classification_prompt = PromptTemplate(input_variables=["feedback"], template=classification_template)
classification_chain = LLMChain(llm=llm, prompt=classification_prompt)

# Manually define the responses
negative_airline_response = "We apologize for the inconvenience caused by our services. Our customer service team will contact you shortly."
negative_external_response = "We're sorry for the inconvenience. However, the situation was beyond our control. We appreciate your understanding. Please continue to travel with us!"
positive_response = "Thank you for your positive feedback! We're glad you had a great experience with us."

# Run the chain if user feedback is provided
if user_feedback:
    try:
        # Get classification result
        classification_result = classification_chain.run({"feedback": user_feedback})
        st.write("Classification result:", classification_result)

        # Display the appropriate response based on classification
        if classification_result == "negative_airline":
            st.write(negative_airline_response)
        elif classification_result == "negative_other":
            st.write(negative_other_response)
        elif classification_result == "positive":
            st.write(positive_response)
        else:
            st.write("Unexpected classification result:", classification_result)  # Fallback for unexpected results
            
    except Exception as e:
        st.error(f"An error occurred while processing your feedback: {e}")
