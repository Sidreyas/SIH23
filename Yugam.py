import streamlit as st
import google.generativeai as genai
genai.configure(api_key='AIzaSyAnIm6lpzgoIdermHNHy0BFpzxe8ySJjK0')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

st.title("Yugam Bot")

with open(r'/home/sudharsan/Documents/PROJECTS/YUGAM24/event_paras.txt', encoding='utf-8') as file:
    content = file.read()

genai_prompt = '''

You need to assist the users for yugam  and recommend the best events and workshops according to their interest and behaviour through the conversational

You are a event recommender bot and your job is to recommend best event for me by seeing my interest and field of study

but also you want to ack like general conversation chatbot 

your repsonse might be like to manipulate the users to attend the events

read this below content question are based on this 

Yugam, the Techno-Cultural-Sports Fest of Kumaraguru Institutions, is striding into its 11th edition and features a variety of technical, cultural, and literary competitions, as well as pro shows, hackathons, conclaves, presentations, and socially responsible activities.

'''


warning_prompt = '''

Answer only to this question above i have mentioned based i have given details in first 

MUST WANT TO FOLLOW:
you always want to speak about the above content only , Do not generate any extra other content which is not in above content
if i asked question is related to recommending or suggesting or showing the events for me and you want to that question like title of event only, Do not generate any extra other content 
if i asked question is normal conversation chat question and i want to answer to that question only and do not generate extra content    
add some emoji in answer

DO NOT INCLUDE THIS BELOW THINGS IN OUTPUT :
do not generate code
do not answer to question none another than recommendation related question 
do not generate too much content for a single query and response shouldn't more than 150 words  

'''


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    

    
    prompt = prompt
    
    safety_ratings = {
    'HARM_CATEGORY_SEXUALLY_EXPLICIT':'block_none',
    'HARM_CATEGORY_HATE_SPEECH': 'block_none',
    'HARM_CATEGORY_HARASSMENT': 'block_none',
    'HARM_CATEGORY_DANGEROUS_CONTENT' : 'block_none'
    }
    
    response = chat.send_message(genai_prompt + '\n' + content + "\n" + " now my Question is " + prompt + warning_prompt ,stream=True,safety_settings=safety_ratings)
    # response = chat.send_message( prompt)

    
    
    store_data = ""
    with st.chat_message("assistant"):
        for chunk in response:
            result = chunk.text
            store_data += result 
            response = result
            # Display assistant response in chat message container
            
            st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": store_data})