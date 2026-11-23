
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IT Support Ticket Dashboard",
    page_icon="🎫",
    layout="wide"
)

st.title("IT Support Ticket Dashboard")
st.write("Monitor and manage IT support incidents.")

# 1. Sample ticket data
if "tickets" not in st.session_state:
    st.session_state.tickets = [
        {
            "Ticket ID": 101,
            "Title": "Laptop Wi-Fi not working",
            "Priority": "High",
            "Status": "Open",
            "Assigned To": "IT Support",
            "Description": "Laptop cannot connect to Wi-Fi."
        },
        {
            "Ticket ID": 102,
            "Title": "Outlook is not opening",
            "Priority": "Medium",
            "Status": "In Progress",
            "Assigned To": "Alex",
            "Description": "Outlook application is not opening."
        },
        {
            "Ticket ID": 103,
            "Title": "Password reset request",
            "Priority": "Low",
            "Status": "Resolved",
            "Assigned To": "IT Support",
            "Description": "User requested a password reset."
        },
        {
            "Ticket ID": 104,
            "Title": "Shared drive unavailable",
            "Priority": "High",
            "Status": "Open",
            "Assigned To": "Morgan",
            "Description": "User cannot access the shared drive."
        },
        {
            "Ticket ID": 105,
            "Title": "Printer setup request",
            "Priority": "Low",
            "Status": "Closed",
            "Assigned To": "Alex",
            "Description": "Printer installation is complete."
        },
        {
            "Ticket ID": 106,
            "Title": "Teams microphone issue",
            "Priority": "Medium",
            "Status": "Resolved",
            "Assigned To": "Morgan",
            "Description": "Microphone settings were corrected."
        }
    ]

# 2. Convert data into a table
tickets = pd.DataFrame(st.session_state.tickets)

# 3. Display ticket counts
st.subheader("Ticket Summary")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Tickets", len(tickets))
col2.metric(
    "Open",
    int((tickets["Status"] == "Open").sum())
)
col3.metric(
    "In Progress",
    int((tickets["Status"] == "In Progress").sum())
)
col4.metric(
    "Resolved",
    int((tickets["Status"] == "Resolved").sum())
)
col5.metric(
    "Closed",
    int((tickets["Status"] == "Closed").sum())
)

st.divider()

# 4. Create status and priority filters
st.subheader("Find Incidents")

col1, col2 = st.columns(2)

with col1:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Open", "In Progress", "Resolved", "Closed"]
    )

with col2:
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"]
    )

search = st.text_input("Search by Ticket ID or Title")

# 5. Apply selected filters
filtered = tickets.copy()

if status_filter != "All":
    filtered = filtered[
        filtered["Status"] == status_filter
    ]

if priority_filter != "All":
    filtered = filtered[
        filtered["Priority"] == priority_filter
    ]

if search.strip():
    search_text = search.strip()

    filtered = filtered[
        filtered["Ticket ID"].astype(str).str.contains(
            search_text, case=False
        )
        | filtered["Title"].str.contains(
            search_text, case=False
        )
    ]

# 6. Display matching incidents
st.subheader(f"Incidents Found: {len(filtered)}")

st.dataframe(
    filtered[
        ["Ticket ID", "Title", "Priority", "Status", "Assigned To"]
    ],
    use_container_width=True,
    hide_index=True
)

# 7. View individual incident details
if not filtered.empty:
    st.subheader("Incident Details")

    selected_id = st.selectbox(
        "Select Ticket ID",
        filtered["Ticket ID"].tolist()
    )

    incident = next(
        ticket for ticket in st.session_state.tickets
        if ticket["Ticket ID"] == selected_id
    )

    st.write("**Title:**", incident["Title"])
    st.write("**Priority:**", incident["Priority"])
    st.write("**Status:**", incident["Status"])
    st.write("**Assigned To:**", incident["Assigned To"])
    st.write("**Description:**", incident["Description"])

# 8. Create a new ticket
st.divider()
st.subheader("Create New Ticket")

with st.form("create_ticket"):
    title = st.text_input("Incident Title")
    description = st.text_area("Incident Description")

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"],
        key="new_priority"
    )

    status = st.selectbox(
        "Initial Status",
        ["Open", "In Progress", "Resolved", "Closed"],
        key="new_status"
    )

    assigned_to = st.text_input(
        "Assigned To",
        value="IT Support"
    )

    submitted = st.form_submit_button("Create Ticket")

    if submitted:
        if not title.strip():
            st.error("Please enter an incident title.")
        else:
            new_id = max(
                [t["Ticket ID"] for t in st.session_state.tickets],
                default=100
            ) + 1

            st.session_state.tickets.append({
                "Ticket ID": new_id,
                "Title": title.strip(),
                "Priority": priority,
                "Status": status,
                "Assigned To": assigned_to.strip() or "Unassigned",
                "Description": description.strip()
            })

            st.success(f"Ticket {new_id} created successfully!")
            st.rerun()
