import streamlit as st
st.set_page_config(page_title="Contact Us", page_icon=":contact:")

st.title('Contact Us')
st.sidebar.success("Menu")
def contact_us():
    st.markdown("""
    Having any problem with our website?? 
                
    Feel free to reach out to us at pinocchio@gmail.com
    """)

if __name__ == "__main__":
    contact_us()