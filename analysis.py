import streamlit as st
import pandas as pd

# ========== 🎨 UI CONFIGURATION ==========
st.set_page_config(page_title="Ahsan's Data handler", page_icon="📊", layout="wide")

# Custom CSS for Styling
st.markdown("""
     <style>
    /* Custom Font & Background */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: white;
    }

    /* Buttons */
    .stButton > button {
        background-color: #3498db;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #2980b9;
        transform: scale(1.05);
    }

    /* Header Styling */
    .stTitle {
        color: #2c3e50;
    }

    /* DataFrame Styling */
    .stDataFrame {
        border: 2px solid #ddd;
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ========== 🚀 SIDEBAR ==========
st.sidebar.header("📂 Upload Data File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

# ========== 🚀 MAIN APP ==========
st.title(" Ahsan's Data Handling App")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Store data in session state
    if "data" not in st.session_state:
        st.session_state.data = df

    # Data Preview
    st.subheader("📜 Data Preview")
    st.dataframe(df, use_container_width=True)

    # Editable Data Table
    st.subheader("✏️ Edit Data")
    edited_df = st.data_editor(st.session_state.data, num_rows="dynamic")
    st.session_state.data = edited_df

    # Sorting Feature
    st.subheader("🔽 Sort Data")
    sort_column = st.selectbox("Sort by column:", df.columns)
    if st.button("Sort Now"):
        st.session_state.data = st.session_state.data.sort_values(by=sort_column)
        st.success(f"✅ Sorted by {sort_column}")

    # Filtering Feature
    st.subheader("🔍 Search & Filter")
    search_query = st.text_input("Enter keyword to filter data:")
    if search_query:
        filtered_df = st.session_state.data[
            st.session_state.data.apply(lambda row: row.astype(str).str.contains(search_query).any(), axis=1)
        ]
        st.write("Filtered Results:")
        st.dataframe(filtered_df, use_container_width=True)

    # Download Edited Data
    st.subheader("⬇️ Download Edited Data")
    csv = st.session_state.data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="edited_data.csv",
        mime="text/csv"
    )

else:
    st.info("📂 Upload a CSV file to start!")
