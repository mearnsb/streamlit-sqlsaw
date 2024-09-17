import os
import tempfile
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide")
st.title("Upload")

def process_csv_upload(file):
    if file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Display the dataframe
            st.write("Preview of the uploaded CSV:")
            st.dataframe(df.head())
            
            # Create 'data' directory if it doesn't exist
            #data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
            data_dir = os.path.join('./data')
            os.makedirs(data_dir, exist_ok=True)
            
            # Save to the 'data' directory
            file_path = os.path.join(data_dir, file.name)
            df.to_csv(file_path, index=False)
            st.success(f"File successfully uploaded and saved as {file_path}")
            
            # # Save to a temporary file
            # with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            #     df.to_csv(tmp_file.name, index=False)
            #     st.success(f"File successfully uploaded and saved temporarily as {tmp_file.name}")
                
            # You can process the dataframe further here if needed
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload a CSV file.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    process_csv_upload(uploaded_file)

# SIDEBAR
# Files
with st.sidebar.expander(f"**files**", expanded=True):
    csv_files=[]
    for root, dirs, files in os.walk("./data/"):
          for file in files:
                 if "checkpoints" not in file and "checkpoints" not in root and "__pycache__" not in root:
                     filename=os.path.join(root, file)
                     if ".csv" in file:
                         csv_files.append(filename)

    st.write(csv_files)
