import streamlit as st
import pandas as pd
from io import StringIO

def to_csv(df):
    """Convert DataFrame to CSV string."""
    output = StringIO()  # Correctly use StringIO from the io module
    df.to_csv(output, index=False)
    return output.getvalue()

# Initialize session state variables if they don't exist
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

def display_sales_input_form():
    """Display input fields for sales-related information and allow download."""
    with st.form("sales_info"):
        st.write("## Sales Conversation Details")
        # Define and order input fields
        data = {
            "Contact Name": st.text_input("Contact Name"),
            "Contacts": st.text_input("Additional Contacts"),
            "Stage": st.selectbox("Stage", ["Initial Contact", "Negotiation", "Closed"]),
            "Contacts by Day": st.number_input("Contacts by Day", min_value=0),
            "Pipeline": st.text_input("Pipeline"),
            "Conversation": st.text_area("Conversation"),
            "Information Sent": st.text_input("Information Sent"),
            "Follow up Date": st.date_input("Follow up Date"),
            "Follow up Time": st.time_input("Follow up Time"),
            "Contact Method": st.text_input("Contact Method"),
            "Contact Information": st.text_input("Contact Information"),
            "Prices Spoken": st.text_input("Prices Spoken"),
            "Projects Spoken About": st.text_input("Projects Spoken About"),
            "Units Spoken About": st.text_input("Units Spoken About"),
            "Estimated Deal Value": st.text_input("Estimated Deal Value"),
            "Close Probability": st.slider("Close Probability", min_value=0, max_value=100, value=50),
            "Invoice Name": st.text_input("Invoice Name"),
            "Appointment Date": st.date_input("Appointment Date"),
            "Appointment Time": st.time_input("Appointment Time"),
            "Won": st.checkbox("Won"),
            "Revenue": st.number_input("Revenue", min_value=0.0, format="%.2f"),
        }

        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.form_submitted = True
            st.session_state.form_data = data

def main():
    st.title('Realty Radar')
    uploaded_file = st.file_uploader("Upload a dataset", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Full Dataset:")
        st.dataframe(df)

    display_sales_input_form()

    if st.session_state.form_submitted:
        df_submitted = pd.DataFrame([st.session_state.form_data])
        st.write("### Submitted Sales Conversation Details", df_submitted)
        csv = to_csv(df_submitted)
        st.download_button("Download Sales Conversation Details", data=csv, file_name="sales_conversation_details.csv", mime="text/csv")

if __name__ == "__main__":
    main()
