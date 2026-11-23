
import sqlite3
from pathlib import Path
from datetime import date, datetime
from contextlib import contextmanager

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "agency.db"

PROJECT_STATUSES = [
    "Pending",
    "In Progress",
    "Completed",
    "On Hold"
]

INVOICE_STATUSES = ["Unpaid", "Paid", "Overdue"]

PAYMENT_METHODS = [
    "Credit Card",
    "Bank Transfer",
    "Cash",
    "Check"
]

st.set_page_config(
    page_title="Agency Management | Dashboard",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_connection():
    if not DATABASE.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE}"
        )

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def database():
    conn = get_connection()

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def fetch_all(query, params=()):
    with database() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def fetch_one(query, params=()):
    with database() as conn:
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None


def execute_query(query, params=()):
    with database() as conn:
        cursor = conn.execute(query, params)
        return cursor.lastrowid


def get_dataframe(query, params=()):
    return pd.DataFrame(fetch_all(query, params))


def money(value):
    return f"${float(value or 0):,.2f}"


def notify_error(error):
    if isinstance(error, sqlite3.IntegrityError):
        message = str(error)

        if "UNIQUE" in message:
            st.error("This record already exists. Check for duplicate values.")
        elif "FOREIGN KEY" in message:
            st.error("This operation references an invalid or related record.")
        elif "CHECK" in message:
            st.error("One or more values violate database rules.")
        elif "NOT NULL" in message:
            st.error("Please complete all required fields.")
        else:
            st.error("The database rejected this operation.")

    elif isinstance(error, ValueError):
        st.error(str(error))

    else:
        st.error("The operation could not be completed.")


def refresh():
    st.rerun()


def validate_required(*values):
    if any(not str(value).strip() for value in values):
        raise ValueError("Please fill out all required fields.")


def validate_email(email):
    email = email.strip()

    if (
        "@" not in email
        or " " in email
        or "." not in email.split("@")[-1]
    ):
        raise ValueError("Please enter a valid email address.")

    return email


def validate_date_order(start, end):
    if end is not None and end < start:
        raise ValueError(
            "The completion date cannot be before the start date."
        )


def project_options():
    projects = fetch_all("""
        SELECT p.project_id, p.project_name, c.business_name
        FROM Projects p
        JOIN Clients c ON p.client_id = c.client_id
        ORDER BY p.project_name
    """)

    return {
        f"{p['project_name']} — {p['business_name']} (#{p['project_id']})":
        p["project_id"]
        for p in projects
    }


def client_options():
    clients = fetch_all("""
        SELECT client_id, business_name
        FROM Clients
        ORDER BY business_name
    """)

    return {
        f"{c['business_name']} (#{c['client_id']})":
        c["client_id"]
        for c in clients
    }


def service_options():
    services = fetch_all("""
        SELECT service_id, service_name
        FROM Services
        ORDER BY service_name
    """)

    return {
        f"{s['service_name']} (#{s['service_id']})":
        s["service_id"]
        for s in services
    }


def invoice_options():
    invoices = fetch_all("""
        SELECT i.invoice_id, i.total_amount, p.project_name
        FROM Invoices i
        JOIN Projects p ON i.project_id = p.project_id
        ORDER BY i.invoice_id
    """)

    return {
        f"Invoice #{i['invoice_id']} — {i['project_name']} "
        f"({money(i['total_amount'])})":
        i["invoice_id"]
        for i in invoices
    }


# ============================================================
# DARK DASHBOARD STYLING
# ============================================================



# ============================================================
# DARK DASHBOARD STYLING - IMPROVED TEXT CONTRAST
# ============================================================

st.markdown("""
<style>
    /* Main application background */
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    /* General text and headings */
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp span {
        color: #e2e8f0;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4 {
        color: #ffffff !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #f1f5f9;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #172236;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
    }

    [data-testid="stMetricLabel"] p {
        color: #cbd5e1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Forms */
    [data-testid="stForm"] {
        background-color: #121d30;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
    }

    /* Text input fields */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
    }

    /* Input placeholders */
    input::placeholder,
    textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1;
    }

    /* Dropdowns and select boxes */
    [data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }

    [data-baseweb="select"] span {
        color: #ffffff !important;
    }

    /* Dropdown options */
    [data-baseweb="popover"] {
        background-color: #1e293b !important;
    }

    [role="listbox"] {
        background-color: #1e293b !important;
    }

    [role="option"] {
        color: #f8fafc !important;
        background-color: #1e293b !important;
    }

    [role="option"]:hover {
        background-color: #334155 !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #cbd5e1 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #60a5fa !important;
    }

    /* Buttons */
    .stButton button,
    .stFormSubmitButton button {
        background-color: #2563eb;
        color: #ffffff !important;
        border: 1px solid #3b82f6;
        border-radius: 9px;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {
        background-color: #1d4ed8;
        color: #ffffff !important;
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #172236;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Custom dashboard text */
    .section-label {
        color: #93c5fd !important;
        text-transform: uppercase;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
    }

    .subtle-text {
        color: #cbd5e1 !important;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 23px;
        font-weight: 800;
        color: #ffffff !important;
    }

    .brand-subtitle {
        color: #cbd5e1 !important;
        font-size: 12px;
        margin-bottom: 25px;
    }

    /* Dividers */
    hr {
        border-color: #334155;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="brand-title">◈ AgencyOS</div>'
        '<div class="brand-subtitle">AGENCY MANAGEMENT</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Workspace",
        [
            "Dashboard",
            "Clients",
            "Projects",
            "Services",
            "Invoices",
            "Payments"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("CS 465 — Database Application")
    st.caption("SQLite • Streamlit • Python")


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():
    st.title("Dashboard")
    st.markdown(
        '<div class="subtle-text">'
        'Overview of your agency performance and activity.'
        '</div>',
        unsafe_allow_html=True
    )

    stats = fetch_one("""
        SELECT
            (SELECT COUNT(*) FROM Clients) AS clients,
            (SELECT COUNT(*) FROM Projects) AS projects,
            (SELECT COUNT(*) FROM Projects
             WHERE status = 'In Progress') AS active_projects,
            (SELECT COALESCE(SUM(amount), 0)
             FROM Payments) AS revenue
    """)

    balances = fetch_one("""
        SELECT COALESCE(SUM(
            CASE WHEN balance_due > 0 THEN balance_due ELSE 0 END
        ), 0) AS outstanding
        FROM InvoiceBalances
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Clients", stats["clients"])
    col2.metric("Total Projects", stats["projects"])
    col3.metric("Active Projects", stats["active_projects"])
    col4.metric("Revenue Collected", money(stats["revenue"]))

    st.write("")
    st.metric("Outstanding Invoice Balances", money(balances["outstanding"]))

    left, right = st.columns(2)

    with left:
        st.subheader("Projects by Status")

        status_df = get_dataframe("""
            SELECT status, COUNT(*) AS total
            FROM Projects
            GROUP BY status
            ORDER BY total DESC
        """)

        if not status_df.empty:
            fig = px.pie(
                status_df,
                names="status",
                values="total",
                hole=0.65,
                color_discrete_sequence=[
                    "#3b82f6",
                    "#22c55e",
                    "#f59e0b",
                    "#8b5cf6"
                ]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0b1120",
                plot_bgcolor="#0b1120",
                margin=dict(l=10, r=10, t=20, b=10),
                legend_title_text=""
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No projects available.")

    with right:
        st.subheader("Monthly Revenue")

        revenue_df = get_dataframe("""
            SELECT
                substr(payment_date, 1, 7) AS month,
                SUM(amount) AS revenue
            FROM Payments
            GROUP BY substr(payment_date, 1, 7)
            ORDER BY month
        """)

        if not revenue_df.empty:
            fig = px.bar(
                revenue_df,
                x="month",
                y="revenue",
                labels={
                    "month": "Month",
                    "revenue": "Revenue ($)"
                },
                color_discrete_sequence=["#3b82f6"]
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0b1120",
                plot_bgcolor="#0b1120",
                margin=dict(l=10, r=10, t=20, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No payment history available.")

    st.subheader("Recent Payments")

    recent = get_dataframe("""
        SELECT
            pay.payment_id,
            c.business_name AS client,
            p.project_name AS project,
            pay.payment_date,
            pay.amount,
            pay.payment_method
        FROM Payments pay
        JOIN Invoices i ON pay.invoice_id = i.invoice_id
        JOIN Projects p ON i.project_id = p.project_id
        JOIN Clients c ON p.client_id = c.client_id
        ORDER BY pay.payment_date DESC, pay.payment_id DESC
        LIMIT 8
    """)

    if not recent.empty:
        st.dataframe(
            recent,
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No payments recorded.")


# ============================================================
# CLIENT MANAGEMENT
# ============================================================

def show_clients():
    st.title("Client Management")
    st.caption("Browse, search, create, and update client records.")

    browse_tab, add_tab, edit_tab = st.tabs([
        "Browse Clients",
        "Add Client",
        "Edit Client"
    ])

    with browse_tab:
        search = st.text_input(
            "Search clients",
            placeholder="Search by business or contact name..."
        )

        clients = get_dataframe("""
            SELECT
                client_id,
                business_name,
                contact_name,
                email,
                phone,
                address
            FROM Clients
            WHERE business_name LIKE ?
               OR contact_name LIKE ?
            ORDER BY business_name
        """, (f"%{search}%", f"%{search}%"))

        st.dataframe(
            clients,
            hide_index=True,
            use_container_width=True
        )

        st.caption(f"{len(clients)} client(s) found")

        st.subheader("Client Project Details")

        options = client_options()

        if options:
            selected = st.selectbox(
                "Select a client",
                list(options.keys()),
                key="client_details"
            )

            projects = get_dataframe("""
                SELECT
                    p.project_id,
                    p.project_name,
                    p.status,
                    p.start_date,
                    p.complete_date,
                    p.total_cost
                FROM Projects p
                JOIN Clients c ON p.client_id = c.client_id
                WHERE c.client_id = ?
                ORDER BY p.start_date DESC
            """, (options[selected],))

            if not projects.empty:
                st.dataframe(
                    projects,
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("This client has no projects.")

    with add_tab:
        st.subheader("Register New Client")

        with st.form("add_client_form"):
            business = st.text_input("Business Name *")
            contact = st.text_input("Contact Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            address = st.text_input("Address")

            submitted = st.form_submit_button(
                "Add Client",
                type="primary"
            )

            if submitted:
                try:
                    validate_required(
                        business, contact, email, phone
                    )

                    clean_email = validate_email(email)

                    execute_query("""
                        INSERT INTO Clients (
                            business_name,
                            contact_name,
                            email,
                            phone,
                            address
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        business.strip(),
                        contact.strip(),
                        clean_email,
                        phone.strip(),
                        address.strip()
                    ))

                    st.success("Client added successfully.")

                except Exception as error:
                    notify_error(error)

    with edit_tab:
        st.subheader("Update Client Information")

        options = client_options()

        if options:
            selected = st.selectbox(
                "Choose a client",
                list(options.keys()),
                key="edit_client"
            )

            client_id = options[selected]

            client = fetch_one("""
                SELECT *
                FROM Clients
                WHERE client_id = ?
            """, (client_id,))

            with st.form(f"edit_client_form_{client_id}"):
                business = st.text_input(
                    "Business Name",
                    value=client["business_name"]
                )

                contact = st.text_input(
                    "Contact Name",
                    value=client["contact_name"]
                )

                email = st.text_input(
                    "Email",
                    value=client["email"]
                )

                phone = st.text_input(
                    "Phone",
                    value=client["phone"]
                )

                address = st.text_input(
                    "Address",
                    value=client["address"] or ""
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if submitted:
                    try:
                        validate_required(
                            business, contact, email, phone
                        )

                        clean_email = validate_email(email)

                        execute_query("""
                            UPDATE Clients
                            SET business_name = ?,
                                contact_name = ?,
                                email = ?,
                                phone = ?,
                                address = ?
                            WHERE client_id = ?
                        """, (
                            business.strip(),
                            contact.strip(),
                            clean_email,
                            phone.strip(),
                            address.strip(),
                            client_id
                        ))

                        st.success("Client updated successfully.")

                    except Exception as error:
                        notify_error(error)


# ============================================================
# PROJECT MANAGEMENT
# ============================================================

def show_projects():
    st.title("Project Management")
    st.caption("Track website projects and manage their progress.")

    browse_tab, add_tab, update_tab, services_tab = st.tabs([
        "Browse Projects",
        "New Project",
        "Update Project",
        "Assigned Services"
    ])

    with browse_tab:
        col1, col2 = st.columns(2)

        with col1:
            status = st.selectbox(
                "Filter by status",
                ["All"] + PROJECT_STATUSES
            )

        with col2:
            search = st.text_input(
                "Search projects",
                placeholder="Project name..."
            )

        projects = get_dataframe("""
            SELECT
                p.project_id,
                p.project_name,
                c.business_name AS client,
                p.status,
                p.start_date,
                p.complete_date,
                p.total_cost
            FROM Projects p
            JOIN Clients c ON p.client_id = c.client_id
            WHERE (? = 'All' OR p.status = ?)
              AND p.project_name LIKE ?
            ORDER BY p.start_date DESC
        """, (status, status, f"%{search}%"))

        st.dataframe(
            projects,
            hide_index=True,
            use_container_width=True
        )

        st.caption(f"{len(projects)} project(s) found")

    with add_tab:
        st.subheader("Create New Project")

        options = client_options()

        if options:
            with st.form("new_project_form"):
                client = st.selectbox(
                    "Client",
                    list(options.keys())
                )

                name = st.text_input("Project Name *")
                status = st.selectbox(
                    "Project Status",
                    PROJECT_STATUSES
                )

                start = st.date_input("Start Date")
                cost = st.number_input(
                    "Total Cost",
                    min_value=0.0,
                    step=100.0
                )

                submitted = st.form_submit_button(
                    "Create Project",
                    type="primary"
                )

                if submitted:
                    try:
                        validate_required(name)

                        execute_query("""
                            INSERT INTO Projects (
                                client_id,
                                project_name,
                                start_date,
                                status,
                                total_cost
                            )
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            options[client],
                            name.strip(),
                            start.isoformat(),
                            status,
                            cost
                        ))

                        st.success("Project created successfully.")

                    except Exception as error:
                        notify_error(error)
        else:
            st.warning("Add a client before creating a project.")

    with update_tab:
        st.subheader("Update Existing Project")

        options = project_options()

        if options:
            selected = st.selectbox(
                "Select Project",
                list(options.keys()),
                key="update_project"
            )

            project_id = options[selected]

            project = fetch_one("""
                SELECT *
                FROM Projects
                WHERE project_id = ?
            """, (project_id,))

            with st.form(f"update_project_form_{project_id}"):
                status = st.selectbox(
                    "Status",
                    PROJECT_STATUSES,
                    index=PROJECT_STATUSES.index(
                        project["status"]
                    )
                )

                cost = st.number_input(
                    "Total Cost",
                    min_value=0.0,
                    value=float(project["total_cost"] or 0),
                    step=100.0
                )

                completed = st.checkbox(
                    "Set completion date",
                    value=project["complete_date"] is not None
                )

                completion_date = None

                if completed:
                    completion_date = st.date_input(
                        "Completion Date",
                        value=(
                            date.fromisoformat(
                                project["complete_date"]
                            )
                            if project["complete_date"]
                            else date.today()
                        )
                    )

                submitted = st.form_submit_button(
                    "Update Project",
                    type="primary"
                )

                if submitted:
                    try:
                        start_date = date.fromisoformat(
                            project["start_date"]
                        )

                        validate_date_order(
                            start_date,
                            completion_date
                        )

                        execute_query("""
                            UPDATE Projects
                            SET status = ?,
                                total_cost = ?,
                                complete_date = ?
                            WHERE project_id = ?
                        """, (
                            status,
                            cost,
                            (
                                completion_date.isoformat()
                                if completion_date
                                else None
                            ),
                            project_id
                        ))

                        st.success("Project updated successfully.")

                    except Exception as error:
                        notify_error(error)

    with services_tab:
        st.subheader("Services Assigned to Projects")

        assigned = get_dataframe("""
            SELECT
                p.project_name,
                c.business_name AS client,
                s.service_name,
                ps.agreed_price,
                ps.date_added
            FROM ProjectServices ps
            JOIN Projects p ON ps.project_id = p.project_id
            JOIN Clients c ON p.client_id = c.client_id
            JOIN Services s ON ps.service_id = s.service_id
            ORDER BY p.project_name, s.service_name
        """)

        st.dataframe(
            assigned,
            hide_index=True,
            use_container_width=True
        )

        st.divider()
        st.subheader("Assign a Service")

        projects = project_options()
        services = service_options()

        if projects and services:
            with st.form("assign_service_form"):
                project = st.selectbox(
                    "Project",
                    list(projects.keys())
                )

                service = st.selectbox(
                    "Service",
                    list(services.keys())
                )

                price = st.number_input(
                    "Agreed Price",
                    min_value=0.0,
                    step=50.0
                )

                added = st.date_input("Date Added")

                submitted = st.form_submit_button(
                    "Assign Service",
                    type="primary"
                )

                if submitted:
                    try:
                        execute_query("""
                            INSERT INTO ProjectServices (
                                project_id,
                                service_id,
                                agreed_price,
                                date_added
                            )
                            VALUES (?, ?, ?, ?)
                        """, (
                            projects[project],
                            services[service],
                            price,
                            added.isoformat()
                        ))

                        st.success("Service assigned successfully.")

                    except Exception as error:
                        notify_error(error)


# ============================================================
# SERVICE MANAGEMENT
# ============================================================

def show_services():
    st.title("Agency Services")
    st.caption("Manage your agency's service catalog.")

    browse_tab, add_tab, edit_tab = st.tabs([
        "Service Catalog",
        "Add Service",
        "Edit Service"
    ])

    with browse_tab:
        services = get_dataframe("""
            SELECT
                service_id,
                service_name,
                description,
                base_price
            FROM Services
            ORDER BY service_name
        """)

        st.dataframe(
            services,
            hide_index=True,
            use_container_width=True
        )

    with add_tab:
        with st.form("add_service_form"):
            name = st.text_input("Service Name *")
            description = st.text_area("Description")
            price = st.number_input(
                "Base Price",
                min_value=0.0,
                step=50.0
            )

            submitted = st.form_submit_button(
                "Add Service",
                type="primary"
            )

            if submitted:
                try:
                    validate_required(name)

                    execute_query("""
                        INSERT INTO Services (
                            service_name,
                            description,
                            base_price
                        )
                        VALUES (?, ?, ?)
                    """, (
                        name.strip(),
                        description.strip(),
                        price
                    ))

                    st.success("Service added successfully.")

                except Exception as error:
                    notify_error(error)

    with edit_tab:
        options = service_options()

        if options:
            selected = st.selectbox(
                "Select Service",
                list(options.keys())
            )

            service_id = options[selected]

            service = fetch_one("""
                SELECT *
                FROM Services
                WHERE service_id = ?
            """, (service_id,))

            with st.form(f"edit_service_form_{service_id}"):
                name = st.text_input(
                    "Service Name",
                    value=service["service_name"]
                )

                description = st.text_area(
                    "Description",
                    value=service["description"] or ""
                )

                price = st.number_input(
                    "Base Price",
                    min_value=0.0,
                    value=float(service["base_price"]),
                    step=50.0
                )

                submitted = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if submitted:
                    try:
                        validate_required(name)

                        execute_query("""
                            UPDATE Services
                            SET service_name = ?,
                                description = ?,
                                base_price = ?
                            WHERE service_id = ?
                        """, (
                            name.strip(),
                            description.strip(),
                            price,
                            service_id
                        ))

                        st.success("Service updated successfully.")

                    except Exception as error:
                        notify_error(error)


# ============================================================
# INVOICE MANAGEMENT
# ============================================================

def show_invoices():
    st.title("Invoices & Billing")
    st.caption("Manage invoices and monitor outstanding balances.")

    browse_tab, create_tab, status_tab = st.tabs([
        "Invoice Balances",
        "Create Invoice",
        "Update Status"
    ])

    with browse_tab:
        filter_choice = st.selectbox(
            "Balance Filter",
            ["All Invoices", "Outstanding", "Fully Paid"]
        )

        invoices = get_dataframe("""
            SELECT
                i.invoice_id,
                c.business_name AS client,
                p.project_name,
                i.invoice_date,
                i.due_date,
                i.status,
                b.total_amount,
                b.amount_paid,
                b.balance_due
            FROM Invoices i
            JOIN Projects p ON i.project_id = p.project_id
            JOIN Clients c ON p.client_id = c.client_id
            JOIN InvoiceBalances b ON i.invoice_id = b.invoice_id
            WHERE (
                ? = 'All Invoices'
                OR (? = 'Outstanding' AND b.balance_due > 0)
                OR (? = 'Fully Paid' AND b.balance_due <= 0)
            )
            ORDER BY i.due_date DESC
        """, (
            filter_choice,
            filter_choice,
            filter_choice
        ))

        if not invoices.empty:
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Invoiced",
                money(invoices["total_amount"].sum())
            )

            col2.metric(
                "Amount Paid",
                money(invoices["amount_paid"].sum())
            )

            col3.metric(
                "Balance Due",
                money(invoices["balance_due"].sum())
            )

        st.dataframe(
            invoices,
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            "Balances are calculated directly from the "
            "InvoiceBalances SQL view."
        )

    with create_tab:
        st.subheader("Create New Invoice")

        projects = project_options()

        if projects:
            with st.form("create_invoice_form"):
                project = st.selectbox(
                    "Project",
                    list(projects.keys())
                )

                invoice_date = st.date_input(
                    "Invoice Date",
                    value=date.today()
                )

                due_date = st.date_input(
                    "Due Date",
                    value=date.today()
                )

                amount = st.number_input(
                    "Invoice Amount",
                    min_value=0.01,
                    value=100.0,
                    step=50.0
                )

                status = st.selectbox(
                    "Status",
                    INVOICE_STATUSES
                )

                submitted = st.form_submit_button(
                    "Create Invoice",
                    type="primary"
                )

                if submitted:
                    try:
                        if due_date < invoice_date:
                            raise ValueError(
                                "Due date cannot be before invoice date."
                            )

                        execute_query("""
                            INSERT INTO Invoices (
                                project_id,
                                invoice_date,
                                due_date,
                                total_amount,
                                status
                            )
                            VALUES (?, ?, ?, ?, ?)
                        """, (
                            projects[project],
                            invoice_date.isoformat(),
                            due_date.isoformat(),
                            amount,
                            status
                        ))

                        st.success("Invoice created successfully.")

                    except Exception as error:
                        notify_error(error)

    with status_tab:
        st.subheader("Update Invoice Status")

        options = invoice_options()

        if options:
            selected = st.selectbox(
                "Select Invoice",
                list(options.keys())
            )

            invoice_id = options[selected]

            invoice = fetch_one("""
                SELECT status
                FROM Invoices
                WHERE invoice_id = ?
            """, (invoice_id,))

            with st.form(f"invoice_status_form_{invoice_id}"):
                status = st.selectbox(
                    "Status",
                    INVOICE_STATUSES,
                    index=INVOICE_STATUSES.index(
                        invoice["status"]
                    )
                )

                submitted = st.form_submit_button(
                    "Update Status",
                    type="primary"
                )

                if submitted:
                    try:
                        execute_query("""
                            UPDATE Invoices
                            SET status = ?
                            WHERE invoice_id = ?
                        """, (status, invoice_id))

                        st.success("Invoice status updated.")

                    except Exception as error:
                        notify_error(error)


# ============================================================
# PAYMENT MANAGEMENT
# ============================================================

def show_payments():
    st.title("Payment Management")
    st.caption("Record client payments and review transaction history.")

    history_tab, record_tab = st.tabs([
        "Payment History",
        "Record Payment"
    ])

    with history_tab:
        payments = get_dataframe("""
            SELECT
                pay.payment_id,
                pay.invoice_id,
                c.business_name AS client,
                p.project_name,
                pay.payment_date,
                pay.amount,
                pay.payment_method
            FROM Payments pay
            JOIN Invoices i ON pay.invoice_id = i.invoice_id
            JOIN Projects p ON i.project_id = p.project_id
            JOIN Clients c ON p.client_id = c.client_id
            ORDER BY pay.payment_date DESC, pay.payment_id DESC
        """)

        if not payments.empty:
            st.metric(
                "Total Payments Received",
                money(payments["amount"].sum())
            )

        st.dataframe(
            payments,
            hide_index=True,
            use_container_width=True
        )

    with record_tab:
        st.subheader("Record New Payment")

        balances = fetch_all("""
            SELECT
                invoice_id,
                project_name,
                business_name,
                balance_due
            FROM InvoiceBalances
            WHERE balance_due > 0
            ORDER BY invoice_id
        """)

        options = {
            f"#{b['invoice_id']} — {b['business_name']} "
            f"— {money(b['balance_due'])} due":
            b["invoice_id"]
            for b in balances
        }

        if options:
            with st.form("record_payment_form"):
                selected = st.selectbox(
                    "Invoice",
                    list(options.keys())
                )

                invoice_id = options[selected]

                payment_date = st.date_input(
                    "Payment Date",
                    value=date.today()
                )

                amount = st.number_input(
                    "Payment Amount",
                    min_value=0.01,
                    value=100.0,
                    step=50.0
                )

                method = st.selectbox(
                    "Payment Method",
                    PAYMENT_METHODS
                )

                submitted = st.form_submit_button(
                    "Record Payment",
                    type="primary"
                )

                if submitted:
                    try:
                        # The balance check and payment insert are
                        # performed in one transaction.
                        with database() as conn:
                            balance = conn.execute("""
                                SELECT balance_due
                                FROM InvoiceBalances
                                WHERE invoice_id = ?
                            """, (invoice_id,)).fetchone()

                            if balance is None:
                                raise ValueError(
                                    "Invoice could not be found."
                                )

                            if amount > balance["balance_due"] + 0.000001:
                                raise ValueError(
                                    "Payment exceeds the outstanding "
                                    f"balance of {money(balance['balance_due'])}."
                                )

                            conn.execute("""
                                INSERT INTO Payments (
                                    invoice_id,
                                    payment_date,
                                    amount,
                                    payment_method
                                )
                                VALUES (?, ?, ?, ?)
                            """, (
                                invoice_id,
                                payment_date.isoformat(),
                                amount,
                                method
                            ))

                            remaining = balance["balance_due"] - amount

                            if remaining <= 0.000001:
                                conn.execute("""
                                    UPDATE Invoices
                                    SET status = 'Paid'
                                    WHERE invoice_id = ?
                                """, (invoice_id,))

                        st.success(
                            "Payment recorded successfully. "
                            f"Remaining balance: {money(max(remaining, 0))}"
                        )

                    except Exception as error:
                        notify_error(error)

        else:
            st.success("All invoices are fully paid.")


# ============================================================
# APPLICATION ROUTING
# ============================================================

try:
    if page == "Dashboard":
        show_dashboard()

    elif page == "Clients":
        show_clients()

    elif page == "Projects":
        show_projects()

    elif page == "Services":
        show_services()

    elif page == "Invoices":
        show_invoices()

    elif page == "Payments":
        show_payments()

except FileNotFoundError:
    st.error(
        "The agency.db database file was not found. "
        "Place it in the same folder as app.py."
    )

except sqlite3.Error:
    st.error(
        "A database error occurred. Check that your database "
        "contains the required tables and view."
    )
