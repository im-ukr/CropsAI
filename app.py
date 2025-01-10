
# Natural Language Text to SQL LLM Application
#Prompt --> LLM -->Gemini Pro --->Query -->SQL Database -->Response.
from dotenv import load_dotenv
load_dotenv() #load all the environment variables.

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

## Configure our API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and Provide SQL Query as Response.
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])

    # Clean the response to extract only the SQL query
    query = response.text.strip()  
    query = query.replace("```", "")  
    query = query.replace("\n", " ")  

    # Remove any leading "sql" or similar text
    if query.lower().startswith("sql"):
        query = query[3:].strip()

    # Remove any trailing or redundant characters
    query = query.strip(";")  
    query = query.strip()

    print(f"Sanitized SQL Query: {query}")
    return query

# Function to retrieve query from the SQL database.
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define Your Prompt
prompt=[
'''
You are an expert in converting English questions to SQL query! You are also expert in predicting crop yield i.e., Hectogram_per_Hectare! The SQL database has the name Crop with the following columns - Country, Item, Year, Hectogram_per_Hectare, Rainfall, Pesticides, Temperature. Here Item represents Crop name. So based on user inputs you need to predict Hectogram_per_Hectare in tonnes. Inputs can be Country, Crop, Year, Rainfall, Pesticides, Temperature. You need to give response as "Expected Crop yield is:" also you need to predict crop name having highest Hectogram_per_Hectare as per user inputs.
Example 1 - Which crop has highest yield in 2025 for country India; Example 2 - Tell me all the crops ?
The SQL command will be something like this SELECT * From Crop;
Also, the SQL code should not have ``` in beginning or end and sql word in output.
'''
]

import streamlit as st

# Page configuration
st.set_page_config(page_title="I can Predict your Crop Yield :)")
# Add custom CSS for styling
page_bg_color = """
<style>
header {
    display: flex;
    justify-content: center;
    align-items: center;
}
header img {
    width: 100%;
    height: 25vh;
    object-fit: cover; /* Ensure the image scales proportionally */
}
.sidebar-image {
    position: fixed;
    top: 50%;
    left: 200px;
    height:40vh;
    transform: translate(-50%, -50%);
    width: 200px; /* Adjust width as needed */
}
.right{
    position: fixed;
    top: 50%;
    right: 25px;
    transform: translate(-50%, -50%);
    width: 200px; /* Adjust width as needed */

}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# Add images
st.markdown('<header><img src="https://img.freepik.com/free-vector/radishes-growing-soil-cartoon_1308-105342.jpg?t=st=1736344930~exp=1736348530~hmac=27048602c211acca76d7639f041983bca3dd7171f07cc9885fa27b57bc38deca&w=1380" alt="Top Image"></header>', unsafe_allow_html=True)
st.markdown('<img class="sidebar-image" src="https://img.freepik.com/free-vector/carrot-root-soil-cartoon-style-isolated_1308-57336.jpg?t=st=1736347575~exp=1736351175~hmac=646a70445d1e5c30f97fc89515fe09f9c78e65345b0ba0d471cf455a73bec2c3&w=740" alt="Left Image">', unsafe_allow_html=True)
st.markdown('<img class="right" src="https://img.freepik.com/free-vector/corn-growing-brown-bag-white-background_1308-43614.jpg?t=st=1736349548~exp=1736353148~hmac=b12c802435978a1417576481bfb8fb942fa32e9b5476b33010ae4a16cc92fd99&w=360" alt="Right Image">', unsafe_allow_html=True)



st.header("Know your Yield with CropAI")
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and question:
    st.write(f"You asked: {question}")

    try:
        response = get_gemini_response(question, prompt)
        print(response)

        data = read_sql_query(response, "project.db")

        st.subheader("The Response is")
        for row in data:
            print(row)
            st.header(row)
    except sqlite3.OperationalError as e:
        st.error(f"SQL error: {e}")
        print(f"SQL error: {e}")

