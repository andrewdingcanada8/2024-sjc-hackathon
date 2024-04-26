import streamlit as st
import re
import os
from generate_response import gen_resp, gen_general_resp, gen_ux_resp
from bs4 import BeautifulSoup

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('Generative User Interfaces Demo')
    st.session_state.key = st.text_input('OpenAI Key')

introduction = \
"""
Welcome to my Generative User Interfaces demo. I put this together over a weekend and hope you enjoy it!

While interactive with LLMs through chat interfaces serve as a solid foundation, I firmly believe there's immense potential for more intuitive and effective forms of human-AI collaboration.
This is a simple demo I put together to explore how it might feel if our interfaces were not pre-determined, but generated in real-time according to our needs.

Note: Currently there is no real request being made or connected apis. So you can't actually book an uber even if you click book.

You can ask me things below and see what kinds of UI I might generate:
1. Book me a hotel next weekend near Whistler Blackcomb
2. Help me brainstorm milkshake recipes
3. or anything else

"""
# Store LLM generated responses
if "messages" not in st.session_state.keys():    st.session_state.messages = [{"role": "assistant", "content": introduction}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": introduction}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

def needs_ux(s):
    pattern = r"needs_additional_information\s*=\s*True"
    match = re.search(pattern, s, re.IGNORECASE)
    if match:
        start_index = match.end()
        return s[start_index:]
    else:
        return None

# output = """<!DOCTYPE html>
# <html>
# <head>
#     <title>Uber Ride Booking Form</title>
# </head>
# <body>
#     <h2>Uber Ride Booking</h2>
#     <form>
#         <!-- Pickup Location -->
#         <label for="pickupLocation">Pickup Location:</label><br>
#         <input type="text" id="pickupLocation" name="pickupLocation" required><br>

#         <!-- Destination -->
#         <label for="destination">Destination:</label><br>
#         <input type="text" id="destination" name="destination" required><br>

#         <!-- Ride Type -->
#         <fieldset>
#             <legend>Ride Type:</legend>
#             <input type="radio" id="uberX" name="rideType" value="uberX" required>
#             <label for="uberX">UberX</label><br>
#             <input type="radio" id="uberBlack" name="rideType" value="uberBlack">
#             <label for="uberBlack">Uber Black</label><br>
#             <input type="radio" id="uberXL" name="rideType" value="uberXL">
#             <label for="uberXL">UberXL</label><br>
#             <input type="radio" id="uberSUV" name="rideType" value="uberSUV">
#             <label for="uberSUV">UberSUV</label>
#         </fieldset>

#         <!-- Special Requirements -->
#         <label for="specialRequirements">Special Requirements:</label><br>
#         <textarea id="specialRequirements" name="specialRequirements" rows="4" cols="50"></textarea><br>

#         <input type="submit" value="Request Uber">
#     </form>
# </body>
# </html>
# """

def format_html(html: str) -> str:
    # Using BeautifulSoup to parse and prettify the HTML, which will also remove unnecessary whitespace
    soup = BeautifulSoup(html, 'html.parser')
    formatted_html = soup.prettify()

    # Splitting the formatted HTML into lines
    lines = formatted_html.split('\n')

    # Removing empty lines
    non_empty_lines = [line for line in lines if line.strip() != '']

    # Joining the non-empty lines back into a string
    cleaned_html = '\n'.join(non_empty_lines)

    return cleaned_html


# with st.chat_message("assistant"):
#     st.markdown(output, unsafe_allow_html=True)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant" and prompt:
    if not st.session_state.key:
        st.warning("Please provide OpenAPI key in sidebar")
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                output = gen_general_resp(prompt, st.session_state.key)
            ux_str = needs_ux(output)
            if ux_str is None:
                st.write(output)
            else:
                with st.spinner("Creating Experience..."):
                    output = gen_ux_resp(ux_str, st.session_state.key)

                output = format_html(output)
                st.markdown(output, unsafe_allow_html=True)
