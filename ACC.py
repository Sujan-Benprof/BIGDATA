# import pandas as pd
# import matplotlib.pyplot as plt
# import streamlit as st

# df = pd.read_csv("/Users/tamangsujan/Documents/webform/700.csv")
# df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# st.title("🚦 Kathmandu Accident Visualizer")

# location = st.selectbox("🌍 Select Location:", sorted(df['Location'].dropna().unique()))
# dates = sorted(list(set(pd.to_datetime(df['Date'].dropna()).dt.date)))



# start_date, end_date = st.select_slider(
#     "📅 Select Date Range:",
#     options=dates,
#     value=(dates[0], dates[-1])
# )

# filtered = df[
#     (df['Location'] == location) &
#     (df['Date'] >= pd.to_datetime(start_date)) &
#     (df['Date'] <= pd.to_datetime(end_date))
# ]

# st.write(f"📍 Location: {location}")
# st.write(f"🗓️ From {start_date} to {end_date}")
# st.write(f"🔢 Total Accidents: {len(filtered)}")

# if not filtered.empty:
#     filtered['Quarter'] = filtered['Date'].dt.to_period('Q').astype(str)
#     counts = filtered.groupby('Quarter').size()

#     st.subheader("📊 Accidents per Quarter")
#     fig, ax = plt.subplots(figsize=(8, 4))
#     counts.plot(kind='bar', color='mediumseagreen', ax=ax)
#     ax.set_xlabel("Quarter")
#     ax.set_ylabel("Accidents")
#     ax.set_title("Accidents per Quarter")
#     st.pyplot(fig)
# else:
#     st.warning("⚠️ No accident data found for this selection.")
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import date, timedelta

# 📥 Load data
df = pd.read_csv("700.csv")
df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')

# 🏷️ Title
st.title("🚦 Kathmandu Accident Visualizer")

# 🇳🇵 Location selection
location_list = sorted(df['Location'].dropna().unique())
location = st.selectbox("🇳🇵 Select Location:", location_list)

# 📅 Date range selection based on full dataset
date_options = sorted(df['Date'].dropna().dt.date.unique())
start_date, end_date = st.select_slider(
    "📅 Select Date Range:",
    options=date_options,
    value=(date_options[0], date_options[-1])
)

# 🎯 Filter data
filtered = df[
    (df['Location'] == location) &
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

# 📊 Display summary
st.write(f"📍 Location: {location}")
st.write(f"🗓️ From {start_date} to {end_date}")
st.write(f"🔢 Total Accidents: {len(filtered)}")

# 📈 Plot if data exists
if not filtered.empty:
    filtered = filtered.copy()
    filtered['Quarter'] = filtered['Date'].dt.to_period('Q').astype(str)
    quarter_counts = filtered.groupby('Quarter').size()

    st.subheader("📊 Accidents per Quarter")
    fig, ax = plt.subplots(figsize=(8, 5))
    quarter_counts.plot(kind='bar', color='mediumseagreen', ax=ax)
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Number of Accidents")
    ax.set_title("Accidents per Quarter")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    # 🔮 Ride Safety Prediction for Tomorrow
    tomorrow = date.today() + timedelta(days=1)
    st.subheader(f"🔮 Ride analysis)")

    total_accidents = df[df['Location'] == location].shape[0]

    if total_accidents > 50:
        status = "❌ High Risk – This area has a high accident rate. Avoid non-essential travel."
    elif 40 <= total_accidents <= 50:
        status = "⚠️ Average Risk – Stay alert and follow traffic rules closely."
    else:
        status = "✅ Safe to Ride – This area has relatively low accident history."

    st.markdown(f"""
    **📍 Location:** `{location}`  
    **📊 Total Historical Accidents:** `{total_accidents}`  
    → **Recommendation for {tomorrow.strftime('%A')}:** {status}
    """)

else:
    st.warning("⚠️ No accident data found for this selection.")
