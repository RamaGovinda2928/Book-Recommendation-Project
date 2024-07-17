import streamlit as st
import pandas as pd
import joblib
import string
import pickle as pk
import base64
st.title("Book Recommendation System")
st.write("Welcome to the Book Recommendation System. Use the sidebar to input details.")

import streamlit as st

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
background_image = "image.jpg"
add_bg_from_local(background_image)



def get_recommendations(user_id, n, fil_model, all_books):
    user_unrated_books = df[df['user_id'] == user_id]['book_title'].unique()
    all_books = df['book_title'].unique()
    to_predict = [book for book in all_books if book not in user_unrated_books]

    test_data = [(user_id, book, 0) for book in to_predict]
    predictions = fil_model.test(test_data)

    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]

    recommended_books = [item[1] for item in top_n]

    return recommended_books

# Load your trained model
# Replace 'model.pkl' with your actual model file
fil_model = pk.load(open('collaborative_filtering.pkl','rb'))

# Load your DataFrame - replace with actual data loading logic
# Assuming `df_all` is loaded from a CSV or created somehow
df = pd.read_csv('books_data.csv')  # Replace with your data loading mechanism

# Sidebar for user input
st.sidebar.header("User Input")
user_id = st.sidebar.number_input("Enter your User_ID:", min_value=1, step=1)
number_of_recommendations = st.sidebar.number_input("Enter the number of books you want to be recommended:", min_value=1, step=1, value=5)

# Extract all unique book titles
all_books = df['book_title'].unique()

# Display recommendations when the button is clicked
if st.sidebar.button('Get Recommendations'):
    recommendations = get_recommendations(user_id, number_of_recommendations, fil_model, all_books)

    if recommendations:
        st.subheader(f"Top {number_of_recommendations} book recommendations for User_ID: {user_id}")
        for i, book in enumerate(recommendations, 1):
            st.write(f"{i}. {book}")
    else:
        st.write("No recommendations found.")
