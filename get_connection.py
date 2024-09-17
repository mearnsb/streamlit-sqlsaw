import streamlit as st
import pandas as pd 
import duckdb

def get_connection():
    file_path = "file.db"
    con = duckdb.connect(database=file_path)    
    return con

#def connect_to_duckdb(file_path):
#    con = duckdb.connect(database=file_path)
#    return con
#file_path = "file.db"
#connection = connect_to_duckdb(file_path)