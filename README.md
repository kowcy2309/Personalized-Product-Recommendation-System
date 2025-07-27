# Personalized-Product-Recommendation-System
This Streamlit app delivers personalized product recommendations using content-based filtering on user purchase history and product metadata like descriptions, ratings, prices, and brands. It includes features like price range filters, rating thresholds, brand comparisons, and even popular product suggestions for new users.

# 🎯 Personalized Product Recommendation System

This Streamlit-based web application offers intelligent product recommendations based on user preferences and purchase history. It uses natural language processing (TF-IDF + SVD) and cosine similarity to match users with the most relevant products. The tool also includes filtering options like price, rating, and brand.

---

## 🔍 Key Features

- 📂 Upload product data as a `.csv` file
- 🔍 Intelligent **content-based filtering** using TF-IDF & cosine similarity
- 📊 Dynamic **price and rating filters**
- 🏷️ **Brand-specific recommendations**
- 🎯 Tailored suggestions for:
  - Returning users (based on purchase history)
  - New users (via product input)
- 📈 **Price comparison chart** between original and discounted prices
- 🌟 "Top Popular Products" for new users

---

## 📁 Sample Input File Format (CSV)

Your CSV should include columns like:

```csv
UserID,Product_id,BrandName,Description,Category,Individual_category,OriginalPrice (in Rs),DiscountPrice (in Rs),Ratings,Reviews,URL
101,2001,BrandA,"Smartphone with AMOLED screen",Electronics,Mobile,20000,15999,4.3,1200,http://example.com/product/2001
# 🎯 Personalized Product Recommendation System

This Streamlit-based web application offers intelligent product recommendations based on user preferences and purchase history. It uses natural language processing (TF-IDF + SVD) and cosine similarity to match users with the most relevant products. The tool also includes filtering options like price, rating, and brand.

---

## 🔍 Key Features

- 📂 Upload product data as a `.csv` file
- 🔍 Intelligent **content-based filtering** using TF-IDF & cosine similarity
- 📊 Dynamic **price and rating filters**
- 🏷️ **Brand-specific recommendations**
- 🎯 Tailored suggestions for:
  - Returning users (based on purchase history)
  - New users (via product input)
- 📈 **Price comparison chart** between original and discounted prices
- 🌟 "Top Popular Products" for new users

---

## 📁 Sample Input File Format (CSV)

Your CSV should include columns like:

```csv
UserID,Product_id,BrandName,Description,Category,Individual_category,OriginalPrice (in Rs),DiscountPrice (in Rs),Ratings,Reviews,URL
101,2001,BrandA,"Smartphone with AMOLED screen",Electronics,Mobile,20000,15999,4.3,1200,http://example.com/product/2001
