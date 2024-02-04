import streamlit as st
import pandas as pd
from io import StringIO


def to_csv(df):
    """Convert DataFrame to CSV string."""
    output = StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()


def display_realtor_info(realtor_data):
    """Display detailed information for the selected realtor."""
    # Ensure column exists before accessing to avoid KeyError
    columns = realtor_data.columns
    st.write(f"**Name:** {realtor_data['Name'].iloc[0]}")
    st.write(f"**Phone Number:** {realtor_data['Phone Number'].iloc[0] if 'Phone Number' in columns else 'N/A'}")
    st.write(
        f"**Real Estate Agency:** {realtor_data['Real Estate Angency'].iloc[0] if 'Real Estate Angency' in columns else 'N/A'}")
    st.write(f"**NMLS Number:** {realtor_data['NMLS Number'].iloc[0] if 'NMLS Number' in columns else 'N/A'}")
    st.write(f"**Experience:** {realtor_data['Experience'].iloc[0] if 'Experience' in columns else 'N/A'}")

    if 'Areas Served' in columns:
        # Check if 'Areas Served' is not null and then process it
        if not pd.isna(realtor_data['Areas Served'].iloc[0]):
            areas_served_list = realtor_data['Areas Served'].iloc[0].split(',')
            areas_served = ', '.join([area.strip() for area in areas_served_list])
        else:
            areas_served = 'N/A'
        st.write(f"**Areas Served:** {areas_served}")
    else:
        st.write("**Areas Served:** N/A")

    st.write(
        f"**About The Realtor:** {realtor_data['About The Realtor'].iloc[0] if 'About The Realtor' in columns else 'N/A'}")
    st.write(
        f"**Realtor Profile:** {realtor_data['Realtor Profile'].iloc[0] if 'Realtor Profile' in columns else 'N/A'}")


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
            if not realtor_data.empty:
                display_realtor_info(realtor_data)
            else:
                st.write("No data available for the selected realtor.")

            # Download button for realtor data
            st.download_button(
                label="Download Realtor Data",
                data=to_csv(realtor_data),
                file_name=f"{selected_realtor}_data.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
