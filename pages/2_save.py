import streamlit as st
import pandas as pd 
import snippets

st.title("Save")
         
#Sidebar
labels = ["Text","Image","URL"]
menu = ["Create","Read","Update","Delete"]
choice = st.sidebar.selectbox("Menu",menu)
#snippets.delete_table()
snippets.create_table()
view = "View All"
select = "Select "

# Data 
def get_items():
    columns = ["RowId", "Name", "Content","label","Date"]
    result = snippets.view_all_data()
    clean_df = pd.DataFrame(result,columns=columns)
    return clean_df


if choice == "Create":
    st.subheader("Create")
    col1,col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
    
    with col2:
        updt_dt = st.date_input("Date")
    
    label = st.text_input("Label") 
    content = st.text_area("Text")
    
    if st.button("Add "):
        snippets.add(name, content, label, updt_dt)
        st.success("Added ::{} :: ".format(content))

    with st.expander(view, expanded=True):
        st.dataframe(get_items())

elif choice == "Read":
    st.subheader("Read")
    with st.expander(view):
        st.dataframe(get_items())

    with st.expander("label"):
        df = get_items()['label'].value_counts().to_frame()
        df = df.reset_index()
        st.dataframe(df)

    #p1 = px.pie(df,names='index',values='label')
    #st.plotly_chart(p1,use_container_width=True)

elif choice == "Update":
    st.subheader("Update")
    names = dict(snippets.view_all_names())
    list_of_contents = [i[0] for i in snippets.view_all_names()]
    selected_content = st.selectbox("Select Item" , list_of_contents, format_func=lambda x: names[x])
    rs = snippets.get_by_id(selected_content)
    
    if rs:
        s_num = rs[0][0]
        s_name = rs[0][1]
        s_content = rs[0][2]
        s_label = rs[0][3]
        s_updt_dt = rs[0][4]
        
        col1,col2 = st.columns(2)
    
    with col1:
        new_name = st.text_input("Name", s_name)
      

    with col2:
        #new_label = st.selectbox(s_label, labels)
        new_updt_dt = st.date_input("date", value="default_value_today")

    new_label = st.text_input("label", value=s_label)
    new_content = st.text_area("Content", s_content, height=300)
      
    if st.button("Update Content "):
        snippets.edit(new_name, new_content, new_label, new_updt_dt, s_num)
        st.success("Updated ::{} ::To {}".format(new_name, new_content))

    with st.expander("View Content", expanded=True):
        st.dataframe(get_items())

elif choice == "Delete":
    st.subheader("Delete")
    del_names = dict(snippets.view_all_names())
    unique_list = [i[0] for i in snippets.view_all_names()]
    delete_by_id =  st.selectbox(select, unique_list, format_func=lambda x: del_names[x])
    print(type(delete_by_id))
    if st.button("Delete"):
        snippets.delete_by_id(delete_by_id)
        st.warning("Deleted: '{}'".format(str(delete_by_id)))

    id_filter = st.text_input("ID Filter:", "")

    if st.button('Delete list of row ids'):
        print("DELETE_BUTTON_CLICKED: ")
        if len(id_filter) > 0: 
            print(id_filter)
            id_filter_array = id_filter.split()
        
            for i in id_filter_array:
                print(i)
                print(type(i))
                snippets.delete_by_id(i)
        else:
            st.info("Copy paste row ids from table into input field") 
    
    with st.expander(view, expanded=True):
        st.data_editor(get_items(), column_config={
        "RowId": st.column_config.NumberColumn(format="%d", step=None) #format="$ %.2f"
  })

#else:
  #st.subheader("About")
  #st.info("DropFact")
      
