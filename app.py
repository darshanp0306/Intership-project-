import streamlit as st
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Sentiment Analysis of Product Reviews (SDG 12)")

# --- Single review section ---
st.header("Single Review Sentiment Analysis")
review = st.text_area("Enter product review text here:")
if st.button("Analyze Sentiment"):
    if review:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        st.write(f"Sentiment Score (Polarity): {polarity:.2f}")
        if polarity > 0.1:
            st.success("Positive Sentiment 😊")
        elif polarity < -0.1:
            st.error("Negative Sentiment 😟")
        else:
            st.warning("Neutral Sentiment 😐")
    else:
        st.info("Please enter some text to analyze.")

# --- Batch review section ---
st.header("Batch Review Sentiment Analysis: Upload Reviews CSV or Excel")
uploaded_file = st.file_uploader(
    "Choose a CSV/Excel file with a 'review' column",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    # Read DataFrame based on file type
    file_name = uploaded_file.name.lower()
    if file_name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a CSV or Excel file.")
        st.stop()
    
    # Check for required 'review' column
    if 'review' not in df.columns:
        st.error("The uploaded file must have a column named 'review'.")
        st.stop()

    # Sentiment analysis for each review
    sentiments = []
    for text in df['review']:
        blob = TextBlob(str(text))
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiments.append("Positive")
        elif polarity < -0.1:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")
    df['Sentiment'] = sentiments

    # Display the table
    st.write(df)

    # Pie chart of sentiment distribution
    sentiment_counts = df['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=['#4CAF50', '#FFEB3B', '#F44336']  # Green=Positive, Yellow=Neutral, Red=Negative
    )
    ax.axis('equal')
    st.subheader('Overall Sentiment Distribution')
    st.pyplot(fig)

    # Download analyzed results
    to_write = io.StringIO()
    df.to_csv(to_write, index=False)
    st.download_button(
        label="Download Sentiment Results",
        data=to_write.getvalue(),
        file_name="sentiment_results.csv",
        mime="text/csv"
    )

    # Investment suggestion
    total_reviews = sentiment_counts.sum()
    positive = sentiment_counts.get("Positive", 0)
    neutral = sentiment_counts.get("Neutral", 0)
    negative = sentiment_counts.get("Negative", 0)

    st.subheader("Investment Suggestion")
    if total_reviews == 0:
        st.info("Not enough review data to make a suggestion.")
    else:
        pos_ratio = positive / total_reviews
        neg_ratio = negative / total_reviews

        if pos_ratio > 0.7:
            st.success("Most reviews are positive. It looks promising—you may consider investing in this product!")
        elif neg_ratio > 0.3:
            st.error("There are significant negative reviews. You should be cautious about investing.")
        else:
            st.warning("The sentiment is mixed. Review details before making a final investment decision.")
