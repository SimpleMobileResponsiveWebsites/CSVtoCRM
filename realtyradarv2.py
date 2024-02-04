import streamlit as st
import pandas as pd
from io import StringIO

def to_csv(df):
    """Convert DataFrame to CSV string."""
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def main():
    st.title('Realty Radar')

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a dataset", type="csv")
    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        # Show the full dataset
        st.write("### Full Dataset:")
        st.dataframe(df)
        # Download button for full dataset
        st.download_button(
            label="Download Full Dataset",
            data=to_csv(df),
            file_name="full_dataset.csv",
            mime="text/csv",
        )

        # Handling duplicates
        st.write("### Handle Duplicate Names with Different Service Areas")
        # Grouping by name and creating a list for each column
        grouped_df = df.groupby('Name').agg(lambda x: list(set(x))).reset_index()
        st.dataframe(grouped_df)
        # Download button for handled duplicates
        st.download_button(
            label="Download Handled Duplicates",
            data=to_csv(grouped_df),
            file_name="handled_duplicates.csv",
            mime="text/csv",
        )

        # Detailed view of a selected realtor
        st.write("### Detailed Realtor View")
        selected_realtor = st.selectbox("Select a Realtor", df['Name'].unique())
        if selected_realtor:
            realtor_data = df[df['Name'] == selected_realtor]
            st.write(realtor_data)
            # Download button for realtor data
            st.download_button(
                label="Download Realtor Data",
                data=to_csv(realtor_data),
                file_name=f"{selected_realtor}_data.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
