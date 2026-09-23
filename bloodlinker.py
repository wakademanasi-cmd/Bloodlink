import streamlit as st
import pandas as pd
from collections import deque
from datetime import date, timedelta, datetime


# ============================================================
# BLOODLINK
# Smart Blood Inventory & Allocation System
# Academic Demonstration Edition v1.0
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="BLOODLINK | Blood Bank Management",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# APPLICATION THEME
# ============================================================

st.markdown(
    """
<style>
    /* GLOBAL */
    .stApp { background-color: #f5f7fb; }
    
    .main .block-container { 
        padding-top: 2rem; 
        padding-bottom: 3rem; 
        padding-left: 6rem;
        padding-right: 6rem;
        max-width: 1400px; 
    }
    
    .stMarkdown, .stText, label, p, li { color: #1f2937; }
    h1, h2, h3, h4, h5, h6 { color: #111827 !important; }

    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e5e7eb; }
    section[data-testid="stSidebar"] * { color: #1f2937; }
    .sidebar-brand { font-size: 28px; font-weight: 800; color: #b91c1c !important; letter-spacing: 1px; margin-bottom: 2px; text-align: center; }
    .sidebar-subtitle { color: #6b7280 !important; font-size: 12px; line-height: 1.5; text-align: center; margin-bottom: 25px;}

    /* SOFT BREATHING ANIMATION */
    @keyframes soft-breathe {
        0%, 100% { box-shadow: 2px 2px 5px rgba(0,0,0,0.15); }
        50% { box-shadow: 4px 4px 18px rgba(0,0,0,0.4); }
    }

    /* ======================================================
       FIX FOR STREAMLIT CLOUD POSITIONING BUG
       ====================================================== */
    .stApp, .main, .block-container, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        transform: none !important;
        contain: none !important;
        perspective: none !important;
    }

    /* ======================================================
       SPLIT EDGE NAVIGATION (Fixed Left and Right Edges)
       ====================================================== */
    
    div[data-testid="stRadio"] {
        position: absolute !important;
        pointer-events: none !important;
        z-index: 99999 !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: block !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* Base shape for ALL collapsed edge icons */
    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        position: fixed !important;
        height: 55px !important;
        width: 55px !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        overflow: hidden !important; 
        transition: width 0.4s cubic-bezier(0.25, 1, 0.5, 1), background-color 0.3s ease !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        animation: soft-breathe 4s infinite ease-in-out !important;
    }

    /* FORCE NO-WRAP TO PREVENT TEXT SQUISHING IN THE CLOUD */
    div[data-testid="stRadio"] div[role="radiogroup"] > label * {
        white-space: nowrap !important;
        overflow: hidden !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        animation: none !important;
    }

    /* LEFT SIDE TABS (1 to 4) */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(-n+4) {
        left: 0 !important;
        right: auto !important;
        border-radius: 0 28px 28px 0 !important;
        border-left: none !important;
        padding: 0 10px 0 15px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(-n+4) p {
        margin: 0 0 0 10px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(-n+4):has(input:checked) {
        border-right: 6px solid white !important;
    }

    /* RIGHT SIDE TABS (5 to 8) */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(n+5) {
        right: 0 !important;
        left: auto !important; /* CRITICAL FIX: Overrides Streamlit default left: 0 */
        border-radius: 28px 0 0 28px !important;
        border-right: none !important;
        padding: 0 15px 0 20px !important; 
        display: flex !important;
        justify-content: flex-end !important; 
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(n+5) p {
        text-align: right !important; 
        width: 100% !important;
        margin: 0 8px 0 0 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(n+5):has(input:checked) {
        border-left: 6px solid white !important;
    }

    /* EXPAND WIDTH ON HOVER */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover { 
        width: 220px !important; 
        box-shadow: 0 8px 20px rgba(0,0,0,0.25) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) { 
        width: 65px !important; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked):hover { 
        width: 220px !important; 
    }

    /* TEXT INSIDE NAVIGATION TABS */
    div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-size: 20px !important; 
        font-weight: 700 !important;
        color: white !important;
        line-height: 55px !important;
    }

    /* "DATA ENTRY" TITLE FOR LEFT TABS */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1)::before {
        content: "DATA ENTRY";
        position: fixed;
        left: 15px;
        top: calc(15vh - 35px); 
        font-size: 13px;
        font-weight: 800;
        color: #7f1d1d;
        background-color: #fecaca;
        padding: 5px 12px;
        border-radius: 20px;
        letter-spacing: 1px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        pointer-events: none; 
    }

    /* "PROGRAM DONORS" TITLE FOR RIGHT TABS */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5)::before {
        content: "PROGRAM DONORS";
        position: fixed;
        right: 15px;
        top: calc(15vh - 35px); 
        font-size: 13px;
        font-weight: 800;
        color: #7f1d1d;
        background-color: #fecaca;
        padding: 5px 12px;
        border-radius: 20px;
        letter-spacing: 1px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        pointer-events: none; 
    }

    /* VERTICAL SPACING FOR TABS */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1),
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5) { top: 15vh !important; }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2),
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(6) { top: 38vh !important; }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3),
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(7) { top: 61vh !important; }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4),
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(8) { top: 84vh !important; }

    /* VIBRANT COLOR PALETTE */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(1) { background-color: #e91e63 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(2) { background-color: #2196f3 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(3) { background-color: #4caf50 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(4) { background-color: #ff9800 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(5) { background-color: #9c27b0 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(6) { background-color: #00bcd4 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(7) { background-color: #f44336 !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:nth-child(8) { background-color: #3f51b5 !important; }


    /* ======================================================
       HERO & PAGE FONTS
       ====================================================== */
    .hero { 
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 100%); 
        border-radius: 18px; 
        padding: 32px; 
        margin-bottom: 25px; 
        box-shadow: 0 10px 30px rgba(127, 29, 29, 0.18); 
        text-align: center;
    }
    .hero-title { 
        color: #ffffff !important; 
        font-size: 48px; 
        font-weight: normal; 
        margin: 0; 
        font-family: 'Algerian', 'Georgia', 'Times New Roman', serif !important;
        letter-spacing: 2px;
    }
    .hero-subtitle { 
        color: #fee2e2 !important; 
        font-size: 24px !important; 
        font-family: 'Brush Script MT', 'Lucida Handwriting', cursive !important; 
        margin-top: 8px; 
    }

    /* NATIVE STREAMLIT METRICS FONT SIZING (e.g., Allocate Patient Data) */
    [data-testid="stMetricValue"] > div { font-size: 22px !important; }
    [data-testid="stMetricLabel"] > div > p { font-size: 16px !important; color: #6b7280 !important; }

    /* METRIC CARDS & GENERAL UI */
    .section-title { font-size: 23px; font-weight: 750; color: #111827 !important; margin-top: 25px; margin-bottom: 5px; }
    .section-description { font-size: 14px; color: #6b7280 !important; margin-bottom: 18px; }
    .metric-card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 15px; padding: 20px; min-height: 125px; box-shadow: 0 3px 12px rgba(0,0,0,0.04); }
    .metric-title { color: #6b7280 !important; font-size: 12px; font-weight: 700; letter-spacing: 0.7px; }
    .metric-value { color: #111827 !important; font-size: 30px; font-weight: 800; margin-top: 7px; }
    .metric-description { color: #9ca3af !important; font-size: 12px; margin-top: 3px; }
    .blood-card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 18px; text-align: center; box-shadow: 0 3px 10px rgba(0,0,0,0.035); }
    .blood-group { color: #b91c1c !important; font-size: 23px; font-weight: 800; }
    .blood-units { color: #111827 !important; font-size: 27px; font-weight: 800; margin-top: 5px; }
    .blood-label { color: #6b7280 !important; font-size: 12px; margin-top: 2px; }
    .info-card { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 20px; margin-bottom: 15px; box-shadow: 0 3px 10px rgba(0,0,0,0.03); }
    .info-card-title { color: #111827 !important; font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    .info-card-text { color: #4b5563 !important; font-size: 14px; line-height: 1.6; }
    .custom-success { background-color: #ecfdf5; border-left: 5px solid #10b981; border-radius: 8px; padding: 15px; color: #065f46 !important; }
    .custom-warning { background-color: #fff7ed; border-left: 5px solid #f97316; border-radius: 8px; padding: 15px; color: #9a3412 !important; }
    .custom-danger { background-color: #fef2f2; border-left: 5px solid #dc2626; border-radius: 8px; padding: 15px; color: #991b1b !important; }
    .custom-info { background-color: #eff6ff; border-left: 5px solid #2563eb; border-radius: 8px; padding: 15px; color: #1e40af !important; }
    .workflow-step { background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px; text-align: center; color: #374151 !important; font-size: 13px; font-weight: 700; box-shadow: 0 2px 7px rgba(0,0,0,0.03); }
    .stack-item { background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 11px; margin: 5px 0; text-align: center; color: #991b1b !important; font-weight: 700; }
    .queue-item { background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px; margin: 6px 0; color: #1e40af !important; font-weight: 600; }
    .footer { text-align: center; color: #9ca3af !important; font-size: 12px; padding: 35px 0 10px 0; }
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# CONSTANTS
# ============================================================

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

COMPATIBILITY = {
    "A+": ["A+", "O+"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "O+"],
    "B-": ["B-", "O-"],
    "AB+": ["AB+", "A+", "B+", "O+", "AB-", "A-", "B-", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"]
}

PRIORITY_RANK = {
    "Emergency": 1,
    "Urgent": 2,
    "Normal": 3
}


# ============================================================
# STACK
# ============================================================

class BloodCompatibilityStack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def peek(self):
        if self.items:
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items.copy()


# ============================================================
# QUEUE
# ============================================================

class PatientQueue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, patient):
        self.items.append(patient)

    def dequeue(self):
        if self.items:
            return self.items.popleft()
        return None

    def peek(self):
        if self.items:
            return self.items[0]
        return None

    def size(self):
        return len(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def get_items(self):
        return list(self.items)


# ============================================================
# INITIAL DATA
# ============================================================

def initialize_data():
    if "patients" not in st.session_state:
        st.session_state.patients = [
            {"Patient ID": "P001", "Patient Name": "Aarav Sharma", "Blood Group": "O+", "Units Required": 2, "Priority": "Emergency", "Hospital": "City General Hospital", "Request Time": "09:15"},
            {"Patient ID": "P002", "Patient Name": "Meera Joshi", "Blood Group": "A+", "Units Required": 1, "Priority": "Urgent", "Hospital": "City General Hospital", "Request Time": "09:30"},
            {"Patient ID": "P003", "Patient Name": "Rohan Patil", "Blood Group": "B+", "Units Required": 2, "Priority": "Normal", "Hospital": "District Hospital", "Request Time": "09:45"}
        ]

    if "inventory" not in st.session_state:
        today = date.today()
        st.session_state.inventory = [
            {"Unit ID": "BLD001", "Blood Group": "O+", "Units": 5, "Collection Date": today - timedelta(days=10), "Expiry Date": today + timedelta(days=25)},
            {"Unit ID": "BLD002", "Blood Group": "O-", "Units": 3, "Collection Date": today - timedelta(days=20), "Expiry Date": today + timedelta(days=15)},
            {"Unit ID": "BLD003", "Blood Group": "A+", "Units": 4, "Collection Date": today - timedelta(days=7), "Expiry Date": today + timedelta(days=28)},
            {"Unit ID": "BLD004", "Blood Group": "A-", "Units": 2, "Collection Date": today - timedelta(days=12), "Expiry Date": today + timedelta(days=18)},
            {"Unit ID": "BLD005", "Blood Group": "B+", "Units": 3, "Collection Date": today - timedelta(days=5), "Expiry Date": today + timedelta(days=32)},
            {"Unit ID": "BLD006", "Blood Group": "AB+", "Units": 2, "Collection Date": today - timedelta(days=8), "Expiry Date": today + timedelta(days=29)}
        ]

    if "history" not in st.session_state:
        st.session_state.history = []

    if "patient_counter" not in st.session_state:
        st.session_state.patient_counter = 4

    if "unit_counter" not in st.session_state:
        st.session_state.unit_counter = 7


initialize_data()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_total_inventory():
    return sum(item["Units"] for item in st.session_state.inventory if item["Expiry Date"] >= date.today())

def get_inventory_by_group():
    result = {}
    for group in BLOOD_GROUPS:
        result[group] = sum(item["Units"] for item in st.session_state.inventory if item["Blood Group"] == group and item["Expiry Date"] >= date.today())
    return result

def get_expiry_alerts():
    today = date.today()
    alerts = []
    for item in st.session_state.inventory:
        days_left = (item["Expiry Date"] - today).days
        if days_left < 0:
            alerts.append({
                "Unit ID": item["Unit ID"], "Blood Group": item["Blood Group"], "Units": item["Units"],
                "Expiry Date": item["Expiry Date"], "Days Remaining": days_left, "Status": "EXPIRED"
            })
        elif days_left <= 7:
            alerts.append({
                "Unit ID": item["Unit ID"], "Blood Group": item["Blood Group"], "Units": item["Units"],
                "Expiry Date": item["Expiry Date"], "Days Remaining": days_left, "Status": "EXPIRING SOON"
            })
    return alerts

def build_patient_queue():
    # Stable sort inherently preserves FIFO request insertion ordering for matching priorities
    patients = sorted(st.session_state.patients, key=lambda patient: PRIORITY_RANK[patient["Priority"]])
    queue = PatientQueue()
    for patient in patients:
        queue.enqueue(patient)
    return queue

def build_compatibility_stack(blood_group):
    stack = BloodCompatibilityStack()
    compatible_groups = COMPATIBILITY[blood_group]
    # Push in reverse so the first compatible group becomes the TOP element
    for group in reversed(compatible_groups):
        stack.push(group)
    return stack

def allocate_blood(patient):
    required = patient["Units Required"]
    stack = build_compatibility_stack(patient["Blood Group"])
    plan = []
    remaining = required

    while not stack.is_empty() and remaining > 0:
        donor_group = stack.pop()
        matching_units = [
            item for item in st.session_state.inventory
            if item["Blood Group"] == donor_group
            and item["Expiry Date"] >= date.today()
            and item["Units"] > 0
        ]
        
        # First-expiring usable blood is selected first
        matching_units.sort(key=lambda item: item["Expiry Date"])

        for item in matching_units:
            if remaining <= 0:
                break
            quantity = min(item["Units"], remaining)
            plan.append({
                "Unit ID": item["Unit ID"],
                "Blood Group": item["Blood Group"],
                "Units": quantity
            })
            remaining -= quantity

    # --------------------------------------------------------
    # Insufficient blood - abort safely without mutating inventory
    # --------------------------------------------------------
    if remaining > 0:
        return False, [], required - remaining

    # --------------------------------------------------------
    # Deduct inventory
    # --------------------------------------------------------
    for allocation in plan:
        for item in st.session_state.inventory:
            if item["Unit ID"] == allocation["Unit ID"]:
                item["Units"] -= allocation["Units"]
                break

    st.session_state.inventory = [item for item in st.session_state.inventory if item["Units"] > 0]

    # --------------------------------------------------------
    # Record allocation
    # --------------------------------------------------------
    st.session_state.history.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Patient ID": patient["Patient ID"],
        "Patient": patient["Patient Name"],
        "Blood Group": patient["Blood Group"],
        "Units": required,
        "Priority": patient["Priority"],
        "Allocated From": ", ".join([f"{item['Blood Group']} ({item['Units']})" for item in plan]),
        "Status": "ALLOCATED"
    })

    st.session_state.patients = [p for p in st.session_state.patients if p["Patient ID"] != patient["Patient ID"]]
    return True, plan, required


# ============================================================
# SIDEBAR (Kept strictly for resetting demo data)
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🩸BLOODLINK🩸</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Smart Blood Inventory & Allocation System</div>', unsafe_allow_html=True)

    if st.button("🔄 Reset Demo Data", use_container_width=True):
        for key in ["patients", "inventory", "history", "patient_counter", "unit_counter", "allocation_result"]:
            st.session_state.pop(key, None)
        initialize_data()
        st.session_state.reset_success = True
        st.rerun()

    if st.session_state.get("reset_success", False):
        st.success("Demo data restored.")
        st.session_state.reset_success = False


# ============================================================
# EDGE NAVIGATION WIDGET
# Notice how the last 4 strings have emojis on the right 
# so they appear correctly when anchored to the right edge.
# ============================================================

page = st.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard", 
        "👤 Patient", 
        "🩸 Inventory", 
        "⚡ Allocate", 
        "Queue 📋", 
        "Stack 📚", 
        "Alerts ⏳", 
        "Analytics 📊"
    ],
    label_visibility="collapsed"
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
<div class="hero">
    <div class="hero-title">🩸BLOODLINK🩸</div>
    <div class="hero-subtitle">Smart Blood Inventory & Allocation System</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "🏠 Dashboard":
    st.markdown('<div class="section-title">System Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Monitor blood inventory, patient requests, priority queues and expiry alerts.</div>', unsafe_allow_html=True)

    total_inventory = get_total_inventory()
    pending_requests = len(st.session_state.patients)
    emergency_requests = sum(1 for patient in st.session_state.patients if patient["Priority"] == "Emergency")
    expiry_alerts = len(get_expiry_alerts())

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"""<div class="metric-card"><div class="metric-title">AVAILABLE BLOOD</div><div class="metric-value">{total_inventory}</div><div class="metric-description">Usable blood units</div></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="metric-card"><div class="metric-title">PENDING REQUESTS</div><div class="metric-value">{pending_requests}</div><div class="metric-description">Patients waiting</div></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class="metric-card"><div class="metric-title">EMERGENCY REQUESTS</div><div class="metric-value">{emergency_requests}</div><div class="metric-description">Highest priority</div></div>""", unsafe_allow_html=True)
    with c4: st.markdown(f"""<div class="metric-card"><div class="metric-title">EXPIRY ALERTS</div><div class="metric-value">{expiry_alerts}</div><div class="metric-description">Units requiring attention</div></div>""", unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-title">Blood Inventory</div>', unsafe_allow_html=True)
    inventory_groups = get_inventory_by_group()
    cols = st.columns(4)
    
    for index, group in enumerate(BLOOD_GROUPS):
        with cols[index % 4]:
            st.markdown(f"""<div class="blood-card"><div class="blood-group">{group}</div><div class="blood-units">{inventory_groups[group]}</div><div class="blood-label">available units</div></div>""", unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-title">System Workflow</div>', unsafe_allow_html=True)
    workflow = st.columns(5)
    workflow_data = [("👤", "Patient Request"), ("📋", "Priority Queue"), ("📚", "Compatibility Stack"), ("🩸", "Inventory Check"), ("✅", "Allocation")]
    
    for column, (icon, title) in zip(workflow, workflow_data):
        with column:
            st.markdown(f"""<div class="workflow-step">{icon}<br>{title}</div>""", unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-title">Priority Patient Requests</div>', unsafe_allow_html=True)
    queue = build_patient_queue()
    if queue.is_empty():
        st.success("No pending patient requests.")
    else:
        st.dataframe(pd.DataFrame(queue.get_items()), use_container_width=True, hide_index=True)

    st.markdown("")
    left, right = st.columns(2)
    with left: st.markdown("""<div class="info-card"><div class="info-card-title">📋 Queue — Patient Requests</div><div class="info-card-text">Patient requests are organized using a priority-based queue.<br><br><b>Priority order:</b> Emergency → Urgent → Normal<br><br><b>Operations:</b> Enqueue • Dequeue • Peek</div></div>""", unsafe_allow_html=True)
    with right: st.markdown("""<div class="info-card"><div class="info-card-title">📚 Stack — Compatibility</div><div class="info-card-text">Compatible donor blood groups are represented using a LIFO stack.<br><br>The allocation engine pops compatible groups while searching available inventory.<br><br><b>Operations:</b> Push • Pop • Peek</div></div>""", unsafe_allow_html=True)

# ============================================================
# PAGE 2 — PATIENT MANAGEMENT
# ============================================================

elif page == "👤 Patient":
    st.markdown('<div class="section-title">Patient Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Register patient requests and add them to the priority queue.</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1.7])
    with left:
        st.subheader("➕ Add Patient")
        with st.form("patient_form", clear_on_submit=True):
            name = st.text_input("Patient Name")
            blood_group = st.selectbox("Required Blood Group", BLOOD_GROUPS)
            units = st.number_input("Units Required", min_value=1, max_value=20, value=1)
            priority = st.selectbox("Priority", ["Emergency", "Urgent", "Normal"])
            hospital = st.text_input("Hospital / Medical Center")
            submitted = st.form_submit_button("Add Patient to Queue", use_container_width=True)

            if submitted:
                if not name.strip():
                    st.error("Please enter a patient name.")
                else:
                    patient_id = f"P{st.session_state.patient_counter:03d}"
                    st.session_state.patient_counter += 1
                    st.session_state.patients.append({
                        "Patient ID": patient_id, "Patient Name": name.strip(), "Blood Group": blood_group,
                        "Units Required": units, "Priority": priority,
                        "Hospital": hospital.strip() if hospital.strip() else "Not specified",
                        "Request Time": datetime.now().strftime("%H:%M")
                    })
                    st.success(f"{patient_id} added successfully.")

    with right:
        st.subheader("Pending Patient Requests")
        queue = build_patient_queue()
        if queue.is_empty():
            st.info("No pending patient requests.")
        else:
            st.dataframe(pd.DataFrame(queue.get_items()), use_container_width=True, hide_index=True)

# ============================================================
# PAGE 3 — BLOOD INVENTORY
# ============================================================

elif page == "🩸 Inventory":
    st.markdown('<div class="section-title">Blood Inventory</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Add and monitor blood units, collection dates and expiry dates.</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1.7])
    with left:
        st.subheader("➕ Add Blood Stock")
        with st.form("inventory_form", clear_on_submit=True):
            blood_group = st.selectbox("Blood Group", BLOOD_GROUPS, key="inventory_group")
            units = st.number_input("Number of Units", min_value=1, max_value=100, value=1)
            collection_date = st.date_input("Collection Date", value=date.today())
            expiry_date = st.date_input("Expiry Date", value=date.today() + timedelta(days=35))
            submitted = st.form_submit_button("Add Blood Stock", use_container_width=True)

            if submitted:
                if expiry_date <= collection_date:
                    st.error("Expiry date must be after collection date.")
                else:
                    unit_id = f"BLD{st.session_state.unit_counter:03d}"
                    st.session_state.unit_counter += 1
                    st.session_state.inventory.append({
                        "Unit ID": unit_id, "Blood Group": blood_group, "Units": units,
                        "Collection Date": collection_date, "Expiry Date": expiry_date
                    })
                    st.success(f"{unit_id} added successfully.")

    with right:
        st.subheader("Current Inventory")
        if st.session_state.inventory:
            inventory_df = pd.DataFrame(st.session_state.inventory)
            inventory_df["Status"] = inventory_df["Expiry Date"].apply(
                lambda expiry: "EXPIRED" if expiry < date.today() else ("EXPIRING SOON" if (expiry - date.today()).days <= 7 else "AVAILABLE")
            )
            st.dataframe(inventory_df, use_container_width=True, hide_index=True)
        else:
            st.info("Inventory is empty.")

# ============================================================
# PAGE 4 — SMART ALLOCATION
# ============================================================

elif page == "⚡ Allocate":
    st.markdown('<div class="section-title">Smart Blood Allocation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Process the highest-priority request using compatibility and earliest-expiry allocation logic.</div>', unsafe_allow_html=True)

    if "allocation_result" in st.session_state:
        res = st.session_state.allocation_result
        if res["status"] == "success":
            st.success(res["msg"])
            st.subheader("Allocation Details")
            st.dataframe(pd.DataFrame(res["plan"]), use_container_width=True, hide_index=True)
            st.info("The patient has been removed from the pending queue.")
        else:
            st.error(res["msg"])
            st.warning("No inventory was deducted.")
        
        del st.session_state.allocation_result
        st.markdown("---")

    queue = build_patient_queue()

    if queue.is_empty():
        st.success("There are no pending patient requests.")
    else:
        patient = queue.peek()
        st.subheader("Next Patient")
        
        patient_columns = st.columns(5)
        details = [("Patient", patient["Patient Name"]), ("Blood Group", patient["Blood Group"]), ("Units", patient["Units Required"]), ("Priority", patient["Priority"]), ("Hospital", patient["Hospital"])]
        
        for column, (label, value) in zip(patient_columns, details):
            with column:
                st.metric(label, value)

        st.markdown("---")
        st.subheader("Compatibility Stack")
        
        stack = build_compatibility_stack(patient["Blood Group"])
        compatible_groups = stack.get_items()

        if compatible_groups:
            stack_columns = st.columns(len(compatible_groups))
            for column, group in zip(stack_columns, compatible_groups):
                with column:
                    st.markdown(f"""<div class="stack-item">🩸 {group}</div>""", unsafe_allow_html=True)

        st.caption("TOP → compatible donor groups are examined using the stack.")
        st.markdown("---")

        if st.button("⚡ Allocate Blood to Next Patient", type="primary", use_container_width=True):
            success, plan, amount = allocate_blood(patient)
            
            if success:
                st.session_state.allocation_result = {
                    "status": "success",
                    "msg": f"{amount} unit(s) successfully allocated to {patient['Patient Name']}.",
                    "plan": plan
                }
            else:
                st.session_state.allocation_result = {
                    "status": "error",
                    "msg": f"Insufficient compatible inventory. Only {amount} of {patient['Units Required']} required unit(s) are available."
                }
            
            st.rerun()

# ============================================================
# PAGE 5 — QUEUE
# ============================================================

elif page == "Queue 📋":
    st.markdown('<div class="section-title">Patient Priority Queue</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Visualization of the queue used to prioritize patient requests.</div>', unsafe_allow_html=True)

    queue = build_patient_queue()
    c1, c2, c3 = st.columns(3)
    
    with c1: st.metric("QUEUE SIZE", queue.size())
    with c2: st.metric("FRONT", queue.peek()["Patient ID"] if queue.peek() else "EMPTY")
    with c3: 
        items = queue.get_items()
        st.metric("REAR", items[-1]["Patient ID"] if items else "EMPTY")

    st.markdown("---")
    if queue.is_empty():
        st.success("Queue is empty.")
    else:
        st.subheader("Queue Visualization")
        st.caption("FRONT → highest-priority request → REAR")
        
        for index, patient in enumerate(queue.get_items()):
            st.markdown(f"""<div class="queue-item"><b>{index + 1}. {patient["Patient ID"]}</b> &nbsp; | &nbsp; {patient["Patient Name"]} &nbsp; | &nbsp; Blood: <b>{patient["Blood Group"]}</b> &nbsp; | &nbsp; Units: <b>{patient["Units Required"]}</b> &nbsp; | &nbsp; Priority: <b>{patient["Priority"]}</b></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Queue Operations")
    operation_columns = st.columns(3)
    
    with operation_columns[0]: st.markdown("""<div class="info-card"><div class="info-card-title">ENQUEUE</div><div class="info-card-text">Adds a new patient request to the queue.</div></div>""", unsafe_allow_html=True)
    with operation_columns[1]: st.markdown("""<div class="info-card"><div class="info-card-title">DEQUEUE</div><div class="info-card-text">Removes a patient after successful processing.</div></div>""", unsafe_allow_html=True)
    with operation_columns[2]: st.markdown("""<div class="info-card"><div class="info-card-title">PEEK</div><div class="info-card-text">Views the next patient without removing them.</div></div>""", unsafe_allow_html=True)

# ============================================================
# PAGE 6 — STACK
# ============================================================

elif page == "Stack 📚":
    st.markdown('<div class="section-title">Blood Compatibility Stack</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Explore compatible donor groups using the LIFO stack.</div>', unsafe_allow_html=True)

    selected_group = st.selectbox("Select Patient Blood Group", BLOOD_GROUPS)
    stack = build_compatibility_stack(selected_group)
    
    st.subheader(f"Compatible Donor Groups for {selected_group}")
    items = stack.get_items()
    
    if items:
        st.markdown("**TOP**")
        for group in reversed(items):
            st.markdown(f"""<div class="stack-item">🩸 {group}</div>""", unsafe_allow_html=True)
        st.markdown("**BOTTOM**")

    st.markdown("---")
    st.subheader("Stack Operations")
    st.markdown("The stack follows the **LIFO (Last-In-First-Out)** principle.")
    
    c1, c2 = st.columns(2)
    with c1: st.metric("STACK SIZE", stack.size())
    with c2: st.metric("TOP ELEMENT", stack.peek() if stack.peek() else "EMPTY")
    st.markdown("")
    st.info("During allocation, compatible blood groups are examined through stack POP operations.")

# ============================================================
# PAGE 7 — EXPIRY & ALERTS
# ============================================================

elif page == "Alerts ⏳":
    st.markdown('<div class="section-title">Expiry Monitoring & Alerts</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Identify expired and soon-to-expire blood units.</div>', unsafe_allow_html=True)

    alerts = get_expiry_alerts()
    expired = [alert for alert in alerts if alert["Status"] == "EXPIRED"]
    expiring = [alert for alert in alerts if alert["Status"] == "EXPIRING SOON"]

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("TOTAL ALERTS", len(alerts))
    with c2: st.metric("EXPIRING SOON", len(expiring))
    with c3: st.metric("EXPIRED", len(expired))

    st.markdown("---")
    if expired:
        st.markdown("""<div class="custom-danger"><b>⚠ EXPIRED INVENTORY</b><br><br>These units have passed their expiry date and are excluded from allocation.</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(expired), use_container_width=True, hide_index=True)

    if expiring:
        st.markdown("""<div class="custom-warning"><b>⚠ EXPIRING SOON</b><br><br>These units have seven or fewer days remaining before expiry.</div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(expiring), use_container_width=True, hide_index=True)

    if not alerts:
        st.markdown("""<div class="custom-success"><b>✓ INVENTORY STATUS: HEALTHY</b><br><br>No units are currently expired or within the seven-day warning window.</div>""", unsafe_allow_html=True)

# ============================================================
# PAGE 8 — ANALYTICS
# ============================================================

elif page == "Analytics 📊":
    st.markdown('<div class="section-title">Analytics & Allocation History</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Review inventory distribution and completed allocations.</div>', unsafe_allow_html=True)

    st.subheader("Blood Group Inventory Distribution")
    inventory_groups = get_inventory_by_group()
    chart_df = pd.DataFrame({"Blood Group": list(inventory_groups.keys()), "Available Units": list(inventory_groups.values())})
    st.bar_chart(chart_df.set_index("Blood Group"))

    total_allocations = len(st.session_state.history)
    allocated_units = sum(record["Units"] for record in st.session_state.history)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("COMPLETED ALLOCATIONS", total_allocations)
    with c2: st.metric("UNITS ALLOCATED", allocated_units)
    with c3: st.metric("PENDING PATIENTS", len(st.session_state.patients))

    st.markdown("---")
    st.subheader("Allocation History")
    
    if st.session_state.history:
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)
    else:
        st.info("No allocation has been completed yet.")

    st.markdown("---")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    BLOODLINK • Smart Blood Inventory & Allocation System<br>
</div>
""",
    unsafe_allow_html=True
)