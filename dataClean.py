import pandas as pd
import numpy as np
import streamlit as st

st.title("Data cleaning")

uploaded_file=st.file_uploader("Upload your CSV file")
threshold=0.5

#This function checks if a column can be converted to numeric type
def is_compatible_to_numeric(col_data):
    converted=pd.to_numeric(col_data, errors='coerce')
    valid_ratio=converted.notna().sum() / len(col_data)

    return valid_ratio>0.8

#This function checks if a column can be converted to datetime type
def is_compatible_to_datetime(col_data):
    converted=pd.to_datetime(col_data, errors='coerce')
    valid_ratio=converted.notna().sum() / len(col_data)

    return valid_ratio>0.8

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Information")
    rows=df.shape[0]
    cols=df.shape[1]
    missing_values=df.isnull().sum().sum()
    missing_per_col=df.isnull().sum()
    max_missing_col=missing_per_col.idxmax()
    duplicated_rows=df.duplicated().sum()

    col1, col2, col3, col4 = st.columns(4)
    
    #Displaying the mtrics of dataset
    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing_values)
    col4.metric("Duplicate Rows", duplicated_rows)
    if duplicated_rows!=0 and missing_values!=0:
       st.write(f"Column with most missing values: {max_missing_col}")

    st.subheader("Dataset")
    st.dataframe(df)

    if duplicated_rows==0 and missing_values==0:
        st.success("Your dataset is clean already having no missing and duplicate values")
    elif st.button("Clean Data"):
        cleaned_data=df.copy()
        cleaned_data=cleaned_data.drop_duplicates()
        cleaned_data = cleaned_data.replace(
            ["", " ", "N/A", "NA", "null", "NULL", "?", "-", "missing","nan","NAN"],
            np.nan
        )

        for col in cleaned_data.columns:
            missing_pcs = (cleaned_data[col].isnull().sum() / len(cleaned_data))
            if missing_pcs > threshold:
                cleaned_data =cleaned_data.drop(columns=[col])
                continue
            
            if cleaned_data[col].dtype in ['int64','float64']:
               cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].median())   
            elif is_compatible_to_numeric(cleaned_data[col]):
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
                cleaned_data[col] = cleaned_data[col].fillna(cleaned_data[col].median())
            elif is_compatible_to_datetime(cleaned_data[col]):
                cleaned_data[col] = pd.to_datetime(cleaned_data[col], errors='coerce')
                cleaned_data[col] = cleaned_data[col].ffill().bfill()
            else:
                cleaned_data[col] = cleaned_data[col].astype(str)
                cleaned_data[col] = cleaned_data[col].str.strip()
                cleaned_data[col] = cleaned_data[col].replace("nan", np.nan)
                cleaned_data[col] = cleaned_data[col].fillna("Unknown")  



        cleaned_data.columns=cleaned_data.columns.str.lower().str.replace(' ',"_")    


        st.subheader("Before vs After Comparison")

        compare_df = pd.DataFrame({
            "Metric": ["Rows", "Missing Values", "Duplicates"],
            "Before": [
                df.shape[0],
                df.isnull().sum().sum(),
                df.duplicated().sum()
            ],
            "After": [
                cleaned_data.shape[0],
                cleaned_data.isnull().sum().sum(),
                cleaned_data.duplicated().sum()
            ]
        })

        st.dataframe(compare_df)      

        st.subheader("Cleaned Dataset Preview")
        st.dataframe(cleaned_data) 


        csv = cleaned_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Cleaned Data",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )