import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Hotel Booking Dashboard", layout="wide")

sns.set_style("whitegrid")

MONTH_ORDER = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


@st.cache_data
def load_data():
    df = pd.read_csv("hotel_booking.csv")
    df['country'] = df['country'].fillna('')
    df['total_nights'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['made_changes'] = df['booking_changes'] > 0
    df['room_mismatch'] = df['reserved_room_type'] != df['assigned_room_type']

    def lead_time_bucket(days):
        if days <= 7:
            return '0-7 days'
        elif days <= 30:
            return '8-30 days'
        elif days <= 90:
            return '31-90 days'
        elif days <= 180:
            return '91-180 days'
        else:
            return '180+ days'

    df['lead_time_bucket'] = df['lead_time'].apply(lead_time_bucket)
    return df


df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")
hotel_filter = st.sidebar.multiselect(
    "Hotel", options=df['hotel'].unique(), default=list(df['hotel'].unique())
)
year_filter = st.sidebar.multiselect(
    "Arrival Year", options=sorted(df['arrival_date_year'].unique()),
    default=sorted(df['arrival_date_year'].unique())
)

filtered = df[df['hotel'].isin(hotel_filter) & df['arrival_date_year'].isin(year_filter)]

# ---------- HEADER ----------
st.title("🏨 Hotel Booking Data Analysis")
st.markdown("---")

# ---------- TOP METRICS ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Bookings", f"{len(filtered):,}")
col2.metric("Cancellation Rate", f"{filtered['is_canceled'].mean()*100:.1f}%")
col3.metric("Average Daily Rate", f"{filtered['adr'].mean():.2f}")
col4.metric("Repeat Guests", f"{filtered['is_repeated_guest'].mean()*100:.1f}%")

st.markdown("---")

# ---------- TABS ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "❌ Cancellation Drivers", "💰 Revenue", "👥 Guest Profile", "🏢 Operations"]
)

# ================= TAB 1: OVERVIEW =================
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Cancellation Rate by Hotel Type")
        cancel_by_hotel = filtered.groupby('hotel')['is_canceled'].mean() * 100
        fig, ax = plt.subplots()
        bars = ax.bar(cancel_by_hotel.index, cancel_by_hotel.values, color=['#2c7fb8', '#e34a33'])
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.1f}%', ha='center')
        ax.set_ylabel("Cancellation Rate (%)")
        st.pyplot(fig)

    with c2:
        st.subheader("Bookings by Customer Type")
        customer_counts = filtered['customer_type'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(customer_counts.values, labels=customer_counts.index, autopct='%1.1f%%',
               colors=sns.color_palette('Set2'))
        st.pyplot(fig)

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Top 10 Guest Countries")
        top_countries = filtered[filtered['country'] != ''].groupby('country').size().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        top_countries.plot(kind='barh', color='#31a354', ax=ax)
        ax.invert_yaxis()
        ax.set_xlabel("Number of Bookings")
        st.pyplot(fig)

    with c4:
        st.subheader("Length of Stay Distribution")
        nights_data = filtered[filtered['total_nights'] <= 14]['total_nights']
        fig, ax = plt.subplots()
        sns.histplot(nights_data, bins=14, color='#756bb1', discrete=True, ax=ax)
        ax.set_xlabel("Total Nights")
        st.pyplot(fig)

    st.subheader("Bookings per Month by Hotel")
    bookings_month_hotel = filtered.groupby(['arrival_date_month', 'hotel']).size().unstack().reindex(MONTH_ORDER)
    st.bar_chart(bookings_month_hotel)

# ================= TAB 2: CANCELLATION DRIVERS =================
with tab2:
    st.subheader("Cancellation Rate by Arrival Month")
    cancel_by_month = filtered.groupby('arrival_date_month')['is_canceled'].mean().reindex(MONTH_ORDER) * 100
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(cancel_by_month.index, cancel_by_month.values, marker='o', color='#e34a33')
    ax.set_ylabel("Cancellation Rate (%)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Cancellation Rate by Market Segment and Deposit Type")
    st.caption("Non Refund deposits show a near-universal cancellation rate, concentrated in Group bookings via travel agents.")
    pivot = filtered.pivot_table(values='is_canceled', index='market_segment', columns='deposit_type', aggfunc='mean') * 100
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind='bar', ax=ax, color=['#2c7fb8', '#e34a33', '#31a354'])
    ax.set_ylabel("Cancellation Rate (%)")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Cancellation by Lead Time")
        bucket_order = ['0-7 days', '8-30 days', '31-90 days', '91-180 days', '180+ days']
        cancel_by_lead = filtered.groupby('lead_time_bucket')['is_canceled'].mean().reindex(bucket_order) * 100
        fig, ax = plt.subplots()
        bars = ax.bar(cancel_by_lead.index, cancel_by_lead.values, color='#e34a33')
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.1f}%', ha='center', fontsize=8)
        plt.xticks(rotation=30)
        ax.set_ylabel("Cancellation Rate (%)")
        st.pyplot(fig)

    with c2:
        st.subheader("Booking Changes vs. Cancellation")
        changes_analysis = filtered.groupby('made_changes')['is_canceled'].mean() * 100
        fig, ax = plt.subplots()
        labels = ['No Changes', 'Changes Made']
        bars = ax.bar(labels, changes_analysis.values, color=['#e34a33', '#31a354'])
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 1, f'{h:.1f}%', ha='center')
        ax.set_ylabel("Cancellation Rate (%)")
        st.pyplot(fig)

    st.subheader("What Drives Cancellation? (Correlation Heatmap)")
    numeric_cols = ['is_canceled', 'lead_time', 'adr', 'booking_changes', 'previous_cancellations',
                     'previous_bookings_not_canceled', 'total_of_special_requests',
                     'required_car_parking_spaces', 'days_in_waiting_list', 'adults',
                     'stays_in_weekend_nights', 'stays_in_week_nights', 'is_repeated_guest']
    corr_matrix = filtered[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0, square=True, linewidths=0.5, ax=ax)
    st.pyplot(fig)

# ================= TAB 3: REVENUE =================
with tab3:
    st.subheader("Average Daily Rate by Month")
    adr_by_month = filtered.groupby('arrival_date_month')['adr'].mean().reindex(MONTH_ORDER)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(adr_by_month.index, adr_by_month.values, color='#2c7fb8')
    plt.xticks(rotation=45)
    ax.set_ylabel("Average Price")
    st.pyplot(fig)

    st.subheader("Price vs. Cancellation Rate by Market Segment")
    revenue_by_segment = filtered.groupby('market_segment').agg(
        avg_price=('adr', 'mean'),
        cancellation_rate=('is_canceled', 'mean')
    )
    revenue_by_segment['cancellation_rate'] *= 100
    revenue_by_segment = revenue_by_segment.sort_values('avg_price', ascending=False)
    plot_data = revenue_by_segment.drop('Undefined', errors='ignore')

    fig, ax1 = plt.subplots(figsize=(10, 5))
    x = range(len(plot_data))
    ax1.bar(x, plot_data['avg_price'], color='#2c7fb8')
    ax1.set_ylabel('Average Price (ADR)', color='#2c7fb8')
    ax1.set_xticks(x)
    ax1.set_xticklabels(plot_data.index, rotation=45, ha='right')
    ax2 = ax1.twinx()
    ax2.plot(x, plot_data['cancellation_rate'], color='#e34a33', marker='o', linewidth=2)
    ax2.set_ylabel('Cancellation Rate (%)', color='#e34a33')
    st.pyplot(fig)

    st.dataframe(revenue_by_segment.style.format({"avg_price": "{:.2f}", "cancellation_rate": "{:.1f}%"}))

# ================= TAB 4: GUEST PROFILE =================
with tab4:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Repeat Guests vs. First-Time Guests")
        repeat_analysis = filtered.groupby('is_repeated_guest').agg(
            cancellation_rate=('is_canceled', 'mean'),
            avg_price=('adr', 'mean')
        )
        repeat_analysis['cancellation_rate'] *= 100
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        labels = ['First-Time', 'Repeat']
        axes[0].bar(labels, repeat_analysis['cancellation_rate'], color=['#e34a33', '#31a354'])
        axes[0].set_title("Cancellation Rate (%)")
        axes[1].bar(labels, repeat_analysis['avg_price'], color=['#2c7fb8', '#756bb1'])
        axes[1].set_title("Average Price")
        st.pyplot(fig)

    with c2:
        st.subheader("Meal Plan Preference by Hotel")
        meal_by_hotel_pct = filtered.groupby('hotel')['meal'].value_counts(normalize=True).unstack().fillna(0) * 100
        fig, ax = plt.subplots(figsize=(10, 4))
        meal_by_hotel_pct.T.plot(kind='bar', ax=ax, color=['#2c7fb8', '#e34a33'])
        ax.set_ylabel("Percentage of Bookings (%)")
        plt.xticks(rotation=0)
        st.pyplot(fig)

    st.subheader("Top 10 Repeat Clients")
    hotel_choice = st.selectbox("Choose hotel", options=filtered['hotel'].unique())
    top10 = (filtered[filtered['hotel'] == hotel_choice]
             .groupby(['name', 'email']).size()
             .sort_values(ascending=False).head(10))
    st.dataframe(top10.reset_index(name='bookings'))

# ================= TAB 5: OPERATIONS =================
with tab5:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Booking Outcome by Hotel")
        status_by_hotel_pct = filtered.groupby('hotel')['reservation_status'].value_counts(normalize=True).unstack() * 100
        fig, ax = plt.subplots(figsize=(8, 5))
        status_by_hotel_pct.T.plot(kind='bar', ax=ax, color=['#2c7fb8', '#e34a33'])
        ax.set_ylabel("Percentage (%)")
        plt.xticks(rotation=0)
        st.pyplot(fig)

    with c2:
        st.subheader("Bookings by Distribution Channel")
        channel_by_hotel = filtered.groupby(['hotel', 'distribution_channel']).size().unstack().fillna(0).astype(int)
        fig, ax = plt.subplots(figsize=(8, 5))
        channel_by_hotel.T.plot(kind='bar', ax=ax, color=['#2c7fb8', '#e34a33'])
        ax.set_ylabel("Number of Bookings")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    st.subheader("Room Type Mismatch Among Completed Stays")
    completed = filtered[filtered['is_canceled'] == 0]
    mismatch_by_hotel = completed.groupby('hotel')['room_mismatch'].mean() * 100
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(mismatch_by_hotel.index, mismatch_by_hotel.values, color=['#2c7fb8', '#e34a33'])
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f'{h:.1f}%', ha='center')
    ax.set_ylabel("Mismatch Rate (%)")
    st.pyplot(fig)

    st.subheader("Bookings per Year by Hotel")
    st.caption("Note: 2015 and 2017 are partial years in this dataset.")
    bookings_year_hotel = filtered.groupby(['arrival_date_year', 'hotel']).size().unstack()
    st.bar_chart(bookings_year_hotel)

st.markdown("---")
