import streamlit as st
import pandas as pd
from scipy import stats

def run_anova(data):
    """
    Perform One-Way ANOVA analysis on the provided data.
    Data is expected to be in a pandas DataFrame with one column for groups and another for values.
    """
    groups = data.groupby('Group')['Value'].apply(list).to_dict()  # Convert data into a dictionary
    f_val, p_val = stats.f_oneway(*groups.values())  # Perform ANOVA
    return f_val, p_val

# Streamlit app title
st.title('One-Way ANOVA Analysis')

# Instructions
st.write("Input your data in the following format (including headers):")
st.code("Group,Value\nA,1\nA,2\nB,3\nB,4\nC,5\nC,6")

# Textarea for input
user_input = st.text_area("Paste your data here:", height=300)

# Button to perform ANOVA
if st.button('Run ANOVA'):
    # Convert input data into a DataFrame
    try:
        from io import StringIO
        data = pd.read_csv(StringIO(user_input), header=0)
        # Validate data
        if 'Group' in data.columns and 'Value' in data.columns:
            # Run ANOVA
            f_val, p_val = run_anova(data)
            st.write(f"F-Value: {f_val:.4f}")
            st.write(f"P-Value: {p_val:.4f}")
            if p_val < 0.05:
                st.write("Result: Significant differences found between groups.")
            else:
                st.write("Result: No significant differences found between groups.")
        else:
            st.error("Error: Data must contain 'Group' and 'Value' columns.")
    except Exception as e:
        st.error(f"Error processing input data: {e}")

