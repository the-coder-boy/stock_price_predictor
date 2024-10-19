import streamlit as st

st.set_page_config(page_title="About Us", page_icon="🖐")
st.sidebar.success("Menu")
def about_us():
    st.title("About Us")
    st.markdown("""
    ## Welcome to Our App!
    We are a group of 8 students passionate about finance, technology, and data. 
    As part of our school project, we created a stock market prediction website using real-time data and predictive algorithms.
    
    ### Our Mission
    Our goal is to make investing more accessible and data-driven, 
    blending our skills in coding, analysis, and financial markets to provide a tool that helps users make informed investment decisions.
    
    """)

if __name__ == "__main__":
    about_us()

