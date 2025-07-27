import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import streamlit as st
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

logo_path = "https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png"
st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{logo_path}" alt="Trigent Logo" style="max-width:100%;">
    </div>
    """,
    unsafe_allow_html=True  
)

st.title("Personalized Product Recommendation")
st.caption("This system leverages advanced machine learning techniques to provide personalized product recommendations based on users' past purchases, product descriptions, and selected filters like price range, ratings, and brand preferences. With features like content-based filtering, price comparison charts, and popular product suggestions for new users, this tool enhances customer experience, helping them discover relevant products efficiently.")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

def display_recommendations(recommendations, title):
    st.subheader(title)
    if not recommendations.empty:
        num_cards_in_row = 3
        for i in range(0, len(recommendations), num_cards_in_row):
            cols = st.columns(num_cards_in_row)
            for idx, col in enumerate(cols):
                if i + idx < len(recommendations):
                    row = recommendations.iloc[i + idx]
                    with col:
                        st.markdown(f"""
                        <style>
                            .card {{
                                background-color: #e0f7fa; 
                                border-radius: 10px; 
                                padding: 16px; 
                                margin-bottom: 20px; 
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); 
                                min-height: 26rem; 
                                transition: transform 0.2s, box-shadow 0.2s;
                            }}
                            .card:hover {{
                                transform: scale(1.05); 
                                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
                            }}
                        </style>
                        <div class="card">
                            <h4 style="margin-bottom:8px;">{row['BrandName']}</h4>
                            <p><strong>Description:</strong> {row['Description']}</p>
                            <p><strong>Category:</strong> {row['Category']}</p>
                            <p><strong>Original Price:</strong> Rs {row['OriginalPrice (in Rs)']}</p>
                            <p><strong>Discount Price:</strong> Rs {row['DiscountPrice (in Rs)']}</p>
                            <p><strong>Ratings:</strong> {row['Ratings']}</p>
                            <p><strong>Reviews:</strong> {row['Reviews']}</p>
                            <a href="{row['URL']}" target="_blank" style="display: inline-block; background-color: #007BFF; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;">View Product</a>
                        </div>
                        """, unsafe_allow_html=True)

if uploaded_file is not None:
    df_cleaned = pd.read_csv(uploaded_file, dtype={'DiscountOffer': str})
    df_cleaned = df_cleaned.head(10000)  
    df_cleaned['Product_id'] = df_cleaned['Product_id'].apply(lambda x: f'{int(x)}')
    st.subheader("Dataset Preview")
    st.write(df_cleaned)

    st.subheader("Select User ID to get recommendations based on past purchases")
    user_id_selected = st.selectbox("**Select User ID**", ['New User'] + df_cleaned['UserID'].unique().tolist())

    purchased_products = pd.DataFrame()  
    if user_id_selected != 'New User':
        purchased_products = df_cleaned[df_cleaned['UserID'] == user_id_selected]
        st.write(f"**Products previously purchased by User:** {user_id_selected}")
        st.dataframe(purchased_products[['Product_id', 'BrandName', 'Description', 'Category', 'DiscountPrice (in Rs)', 'Ratings']])
    else:
        st.write("**No previous purchases found for new users. Recommendations will be based on selected products.**")

    def content_based_recommendations(product_id, cosine_sim):
        idx = df_cleaned.index[df_cleaned['Product_id'] == product_id].tolist()[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:3] 
        product_indices = [i[0] for i in sim_scores]
        return df_cleaned.iloc[product_indices]

    def content_based_recommendations_current(product_id, cosine_sim):
        idx = df_cleaned.index[df_cleaned['Product_id'] == product_id].tolist()[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:13]  
        product_indices = [i[0] for i in sim_scores]
        return df_cleaned.iloc[product_indices]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_cleaned['Description'])

    svd = TruncatedSVD(n_components=100)
    reduced_matrix = svd.fit_transform(tfidf_matrix)

    cosine_sim = cosine_similarity(reduced_matrix)

    def get_product_suggestions(input_text, df):
        suggestions = df[df['Description'].str.contains(input_text, case=False, na=False)].head(20)
        return suggestions

    input_text = st.text_input("**Add Product**")

    if st.button("Get Suggestions"):

        if 'suggestions' in st.session_state:
            del st.session_state.suggestions
        if 'product_selected' in st.session_state:
            del st.session_state.product_selected

        with st.spinner('Fetching suggestions...'):
            time.sleep(5)

            if input_text:
                is_in_category = df_cleaned['Individual_category'].str.contains(input_text, case=False, na=False).any()
                
                is_in_description = df_cleaned['Description'].str.contains(input_text, case=False, na=False).any()

                if not is_in_category and is_in_description:
                    st.warning(f"{input_text} is not available, but you can see related products below:")

                    suggestions = get_product_suggestions(input_text, df_cleaned)
                    if not suggestions.empty:
                        st.session_state.suggestions = suggestions
                        st.session_state.product_selected = None  
                    else:
                        st.warning("No suggestions found.")

                elif not is_in_category and not is_in_description:
                    st.warning(f"{input_text} is not available.")
                else:
                    suggestions = get_product_suggestions(input_text, df_cleaned)
                    if not suggestions.empty:
                        st.session_state.suggestions = suggestions
                        st.session_state.product_selected = None  
                    else:
                        st.warning("No suggestions found.")
            else:
                st.warning("Please enter a product description.")


    if 'suggestions' in st.session_state:
        product_selected = st.selectbox("**Select a product from the suggestions:**", 
                                         st.session_state.suggestions['Description'].tolist(), 
                                         key='product_dropdown')

        if product_selected:
            st.session_state.product_selected = product_selected
            selected_product = st.session_state.suggestions[st.session_state.suggestions['Description'] == product_selected]
            
            if not selected_product.empty:
                product_id = selected_product['Product_id'].values[0]
                st.write(f"**Product ID Selected:** {product_id}")

                st.subheader("Selected Product Details")
                st.dataframe(selected_product)

                product_url = selected_product['URL'].values[0]  
                st.markdown(f"**Source:** [View Product]({product_url})", unsafe_allow_html=True)

                price_options = [
                    "0 to 1000", "1000 to 2000", "2000 to 3000", 
                    "3000 to 4000", "4000 to 5000", "5000 to 6000"
                ]
                selected_price_range = st.selectbox("Select Price Range", price_options)

                price_min, price_max = map(int, selected_price_range.split(" to "))

                rating_options = ["1 and above", "2 and above", "3 and above", "4 and above"]
                selected_rating = st.selectbox("Select Rating Filter", rating_options)

                min_rating = int(selected_rating.split(" ")[0])

                brand_options = df_cleaned['BrandName'].unique().tolist()
                selected_additional_brand = st.selectbox("**Select an Additional Brand (optional)**", ['None'] + brand_options)

                if st.button("Get Recommendations"):
                    with st.spinner('Fetching recommendations...'):
                        time.sleep(5)
                        
                        recommendations_from_previous = pd.DataFrame()
                        recommendations_from_selected = pd.DataFrame()

                        recommendations_from_selected = content_based_recommendations_current(product_id, cosine_sim)
                        recommendations_from_selected = recommendations_from_selected.drop_duplicates(subset='Product_id').reset_index(drop=True)

                        filtered_recommendations_selected = recommendations_from_selected[
                            (recommendations_from_selected['DiscountPrice (in Rs)'] >= price_min) & 
                            (recommendations_from_selected['DiscountPrice (in Rs)'] <= price_max) &
                            (recommendations_from_selected['Ratings'] >= min_rating)
                        ]
                        
                        if selected_additional_brand != 'None':
                            additional_brand_recommendations = df_cleaned[
                                (df_cleaned['BrandName'] == selected_additional_brand) &
                                (df_cleaned['Individual_category'] == selected_product['Individual_category'].values[0])  
                            ]


                            additional_brand_recommendations = additional_brand_recommendations[
                                (additional_brand_recommendations['DiscountPrice (in Rs)'] >= price_min) & 
                                (additional_brand_recommendations['DiscountPrice (in Rs)'] <= price_max) & 
                                (additional_brand_recommendations['Ratings'] >= min_rating)
                            ]
                            
                            additional_brand_recommendations = additional_brand_recommendations.head(4)
                            
        
                            filtered_recommendations_selected = pd.concat([filtered_recommendations_selected, additional_brand_recommendations])


                        def plot_price_comparison(filtered_recommendations, title):
                            if not filtered_recommendations.empty:
                                plt.figure(figsize=(10, 5))
                                plt.plot(filtered_recommendations['BrandName'], 
                                        filtered_recommendations['DiscountPrice (in Rs)'], 
                                        marker='o', label='Discount Price (Rs)', color='orange')
                                plt.plot(filtered_recommendations['BrandName'], 
                                        filtered_recommendations['OriginalPrice (in Rs)'], 
                                        marker='o', label='Original Price (Rs)', color='blue')

                                plt.title(title)
                                plt.xlabel('Product Brand')
                                plt.ylabel('Price (in Rs)')
                                plt.xticks(rotation=45)
                                plt.legend()
                                plt.grid(True)
                                plt.tight_layout()

                                st.pyplot(plt)
                            else:
                                st.write("No reccommandations available for the selected filters")

                        display_recommendations(filtered_recommendations_selected, "Recommendations Based on Selected Product")
                        plot_price_comparison(filtered_recommendations_selected, "Price Comparison of Selected Product Recommendations")

                        
                        if user_id_selected != 'New User':
                            for purchased_product_id in purchased_products['Product_id']:
                                recommendations = content_based_recommendations(purchased_product_id, cosine_sim)
                                recommendations_from_previous = pd.concat([recommendations_from_previous, recommendations])

                            recommendations_from_previous = recommendations_from_previous.drop_duplicates(subset='Product_id').reset_index(drop=True)

                            filtered_recommendations_previous = recommendations_from_previous[
                                (recommendations_from_previous['DiscountPrice (in Rs)'] >= price_min) & 
                                (recommendations_from_previous['DiscountPrice (in Rs)'] <= price_max) &
                                (recommendations_from_previous['Ratings'] >= min_rating)
                            ]

                            display_recommendations(filtered_recommendations_previous, "Recommendations Based on Previous Purchases")

                        if user_id_selected == 'New User':
                            with st.spinner('Fetching popular products...'):
                                popular_products = df_cleaned[(df_cleaned['Ratings'] > 4.0) & (df_cleaned['Reviews'] > 900)]
                                top_popular_products = popular_products.nlargest(10, 'Reviews')  

                                if not top_popular_products.empty:
                                    display_recommendations(top_popular_products, "Top Popular Products")
                                else:
                                    st.warning("No popular products found.")

footer_html = """
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<div style="text-align: center;">
    <p>
        Copyright © 2024 | <a href="https://trigent.com/ai/" target="_blank" aria-label="Trigent Website">Trigent Software Inc.</a> All rights reserved. |
        <a href="https://www.linkedin.com/company/trigent-software/" target="_blank" aria-label="Trigent LinkedIn"><i class="fab fa-linkedin"></i></a> |
        <a href="https://www.twitter.com/trigentsoftware/" target="_blank" aria-label="Trigent Twitter"><i class="fab fa-twitter"></i></a> |
        <a href="https://www.youtube.com/channel/UCNhAbLhnkeVvV6MBFUZ8hOw" target="_blank" aria-label="Trigent Youtube"><i class="fab fa-youtube"></i></a>
    </p>
</div>
"""
footer_css = """
<style>
.footer {
    position: fixed;
    z-index: 1000;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
[data-testid="stSidebarNavItems"] {
    max-height: 100%!important;
}
[data-testid="collapsedControl"] {
            display: none;
}
</style>
"""
footer = f"{footer_css}<div class='footer'>{footer_html}</div>"
st.markdown(footer, unsafe_allow_html=True)
