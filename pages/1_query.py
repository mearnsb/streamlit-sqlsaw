import os
import glob
import pandas as pd
import json
import duckdb
import requests
from collections import defaultdict
from get_connection import get_connection
from query_connection import query_connection 
import sniplogs
from io import StringIO
from contextlib import redirect_stdout

# Streamlit 
import streamlit as st
import streamlit.components.v1 as components
from streamlit_ace import st_ace
st.title("Query")

# Functions
def connect_to_duckdb(file_path):
    con = duckdb.connect(database=file_path)
    return con

def run_code(code):
    f = StringIO()
    with redirect_stdout(f):
        exec(code)
    s = f.getvalue()
    return s

def load_snippets():
    connection = get_connection()        
    query = """ select * from snippets """
    df = connection.sql(query).to_df().iloc[::-1] 
    column_names = []
    column_content = []
    
    # Loop over the DataFrame and extract column name and content
    for column in df.columns:
        column_names.append(column)
        column_content.append(df[column].tolist())

    return column_content[1], column_content[2], df

def load_sniplogs():
    connection = get_connection()      
    query = """ select name, content, rowid from sniplogs where content is not null and content != '' """
    df = connection.sql(query).to_df().iloc[::-1] 
    column_names = []
    column_content = []

    # Loop DataFrame 
    for column in df.columns:
        column_names.append(column)
        column_content.append(df[column].tolist())

    return column_content[0], column_content[1], df

def load_files():
    file_names = glob.glob("data/*.csv")
    file_values = []
    for file_name in file_names:
        file_name = file_name.replace("\\", "/")
        parts = file_name.split("/")
        if parts[1] not in file_values:
            file_values.append(parts[1])
    file_values.sort()

    return file_names, file_values

code_snippet='''from query_connection import query_connection 
import streamlit as st
connection = query_connection()

query = """ 

select * from read_csv_auto("./data/fake_customers.csv") 

"""

d = connection.sql(query)
st.write(d.to_df())

'''

# Session
if 'last_code' not in st.session_state:
    st.session_state['last_code'] = code_snippet

if 'exec_box' not in st.session_state:
    st.session_state['exec_box'] = code_snippet

if 'current_code' not in st.session_state:
    st.session_state['current_code'] = code_snippet

if 'selected_query' not in st.session_state:
    st.session_state['selected_query'] = 'SANDBOX'

if 'state' not in st.session_state:
    st.session_state.state = 0

if 'output' not in st.session_state:
    st.session_state.output = ""

# GET SNIPPETS loaded once here
snippet_names, snippet_contents, snippet_df_content = load_snippets()
result_dict = dict(zip(snippet_names, snippet_contents))

# TABS
tab1, tab2, tab3 = st.tabs(["Code", "Files", "Saved"])

# TAB 1
# CODE 
with tab1:
    st.session_state['last_code'] = st.session_state['current_code']
    st.session_state['current_code'] = st.session_state['exec_box']

    # Display the selected snippet content
    with st.expander("Pinned", expanded=True):

        # Filter the dataframe for 'pinned' labels
        query_snippets = snippet_df_content[snippet_df_content['label'] == 'pinned']
        
        # Create a dropdown for query snippets with an empty default value
        selected_query = st.selectbox(
            "Select a pinned snippet:",
            options=["SANDBOX"] + query_snippets['name'].tolist(),
            index=0,
            key="query_selector"
        )

        if  selected_query != "SANDBOX" and selected_query != "None":
            st.code(result_dict[selected_query], language="sql")
            st.session_state['selected_query'] = selected_query

    with st.expander("Sandbox", expanded=True):    
        content = st_ace(
            value = f"{st.session_state['exec_box']}",
            language="python",
            font_size=14,
            tab_size=4,
            min_lines=10,
            auto_update=False,
            #theme = "clouds_midnight",
            key=f"ace-{st.session_state.state}",
        )
        
    if st.session_state['exec_box']:
        st.session_state['exec_box'] = content
        sniplogs.insert('input', content, 'sandbox') 
    
    try:
        c = run_code(content)
        st.session_state.output = c
    
    except Exception as e:
        st.exception(e)

# TAB 2
# CSV
with tab2:
    file_names, file_values = load_files()
    view_file_values = st.multiselect("Select files", file_values, file_values)
    #n = st.number_input("Files tile view width", 1, 5, 3)
    n = 1
    
    file_previews = []
    for file_name in file_names:
        if any(file_value in file_name for file_value in view_file_values):
            file_previews.append(file_name)
    groups = []
    for i in range(0, len(file_previews), n):
        groups.append(file_previews[i:i+n])
    
    for group in groups:
        cols = st.columns(n)
        for i, file_name in enumerate(group):
            #cols[i].image(file_name)
            import io

            # Open the file and read its content, limiting to 20 rows
            with open(file_name, 'r') as file:
                file_contents = ''.join(file.readlines()[:20])
                
            with cols[i]:
                st.subheader(file_name)
                st.code(file_contents)

    # Create a button to confirm the selection
    st.subheader("Delete")

    # Create a dropdown to select a file
    selected_file = st.selectbox("Select a file", file_names)

    if st.button("Delete csv"):
        # Use relative path for more reliable deletion
        relative_path = os.path.join(selected_file)
        full_path = os.path.abspath(relative_path)
        st.write(full_path)
        try:
            os.remove(full_path)
            st.success(f"Successfully deleted: {selected_file}")
        except OSError as e:
            st.error(f"Error deleting {selected_file}: {e}")

# TAB 3
# SAVED SNIPPETS
with tab3:
    # snippets loaded above 
    view_names = st.multiselect("Select saved snippets", snippet_names, snippet_names)
    n = st.number_input("Snippets tile view width", 1, 5, 1)
    
    view_content = []
    for snippet_name in snippet_names:
        if any(nm in snippet_name for nm in view_names):
            view_content.append(snippet_name)
    groups = []
    for i in range(0, len(view_content), n):
        groups.append(view_content[i:i+n])

    for group in groups:
        cols = st.columns(n)
        for i, snippet_name in enumerate(group):

            with cols[i]:
                st.subheader(snippet_name)
                st.code(result_dict[snippet_name])

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

# SIDEBAR
# Recent
with st.sidebar.expander(f"**recent**",expanded=False):
    
    try:
        sniplogs_names, sniplogs_contents, sniplogs_df = load_sniplogs()
        st.dataframe(sniplogs_df)
    except Exception as e: 
        st.write(str(e))