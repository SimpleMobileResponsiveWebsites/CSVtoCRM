import streamlit as st
import pandas as pd

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

        # Handling duplicates
        st.write("### Handle Duplicate Names with Different Service Areas")
        # Grouping by name and creating a list for each column
        grouped_df = df.groupby('Name').agg(lambda x: list(set(x))).reset_index()

        st.dataframe(grouped_df)

        # Detailed view of a selected realtor
        st.write("### Detailed Realtor View")
        selected_realtor = st.selectbox("Select a Realtor", df['Name'].unique())

        if selected_realtor:
            realtor_data = df[df['Name'] == selected_realtor]
            st.write(realtor_data)

if __name__ == "__main__":
    main()
