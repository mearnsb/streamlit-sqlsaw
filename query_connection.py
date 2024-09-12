import streamlit as st
import pandas as pd 
import duckdb
def query_connection():
    file_path = "query.db"
    con = duckdb.connect(database=file_path)
    return con