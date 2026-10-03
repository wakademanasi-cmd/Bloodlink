import streamlit as st
import pandas as pd
from collections import deque
from datetime import date, timedelta, datetime
from sqlalchemy import text
import random
import string


# ============================================================
# BLOODLINK
# Smart Blood Inventory & Allocation System
# Database-Integrated Edition v2.0
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
# FIXED EDGE TITLES (Raw HTML bypasses CSS clipping)
# ============================================================

st.markdown("""
    <div style="position: fixed; left: 15px; top: calc(15vh - 35px); font-size: 13px; font-weight: 800; color: #7f1d1d; background-color: #fecaca; padding: 5px 12px; border-radius: 20px; letter-spacing: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 999999; pointer-events: none;">DATA ENTRY</div>
    <div style="position: fixed; right: 15px; top: calc(15vh - 35px); font-size: 13px; font-weight: 800; color: #7f1d1d; background-color: #fecaca; padding: 5px 12px; border-radius: 20px; letter-spacing: 1px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); z-index: 999999; pointer-events: none;">PROGRAM DONORS</div>
""", unsafe_allow_html=True)


# ============================================================
# APPLICATION THEME & CLOUD CSS FIXES
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
       SPLIT EDGE NAVIGATION (Ultimate Cloud Resilience Fix)
       ====================================================== */
    
    [data-testid="stRadio"] {
        position: absolute !important;
        width: 0px !important;
        height: 0px !important;
        overflow: visible !important;
        z-index: 999999 !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
    }

    /* HIDE NATIVE CIRCLES (Targeting the radio input visual dot safely) */
    [data-testid="stRadio"] [role="radiogroup"] label > div:first-child:not(:has(p)),
    [data-testid="stRadio"] [role="radiogroup"] label input {
        display: none !important;
        width: 0px !important;
        height: 0px !important;
        opacity: 0 !important;
    }

    /* BASE TAB STYLING */
    [data-testid="stRadio"] [role="radiogroup"] label {
        position: fixed !important;
        height: 55px !important;
        width: 55px !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        overflow: hidden !important; 
        transition: width 0.4s cubic-bezier(0.25, 1, 0.5, 1), background-color 0.3s ease !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        cursor: pointer !important;
        pointer-events: auto !important;
        z-index: 999999 !important;
        animation: soft-breathe 4s infinite ease-in-out !important;
    }

    /* FORCE TEXT HORIZONTAL */
    [data-testid="stRadio"] [role="radiogroup"] label div,
    [data-testid="stRadio"] [role="radiogroup"] label p,
    [data-testid="stRadio"] [role="radiogroup"] label span {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    [data-testid="stRadio"] [role="radiogroup"] label p {
        font-size: 18px !important; 
        font-weight: 700 !important;
        margin: 0 !important;
        padding-left: 14px !important;
    }

    /* ==========================================
       POSITIONING & COLORS 
       ========================================== */
    
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(1), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(1) label { left: 0 !important; right: auto !important; top: 15vh !important; border-radius: 0 28px 28px 0 !important; border-left: none !important; background-color: #e91e63 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(2), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(2) label { left: 0 !important; right: auto !important; top: 38vh !important; border-radius: 0 28px 28px 0 !important; border-left: none !important; background-color: #2196f3 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(3), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(3) label { left: 0 !important; right: auto !important; top: 61vh !important; border-radius: 0 28px 28px 0 !important; border-left: none !important; background-color: #4caf50 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(4), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(4) label { left: 0 !important; right: auto !important; top: 84vh !important; border-radius: 0 28px 28px 0 !important; border-left: none !important; background-color: #ff9800 !important; }

    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(5), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(5) label { right: 0 !important; left: auto !important; top: 15vh !important; border-radius: 28px 0 0 28px !important; border-right: none !important; background-color: #9c27b0 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(5) p, [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(5) label p { padding-left: 10px !important; }

    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(6), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(6) label { right: 0 !important; left: auto !important; top: 38vh !important; border-radius: 28px 0 0 28px !important; border-right: none !important; background-color: #00bcd4 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(6) p, [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(6) label p { padding-left: 10px !important; }

    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(7), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(7) label { right: 0 !important; left: auto !important; top: 61vh !important; border-radius: 28px 0 0 28px !important; border-right: none !important; background-color: #f44336 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(7) p, [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(7) label p { padding-left: 10px !important; }

    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(8), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(8) label { right: 0 !important; left: auto !important; top: 84vh !important; border-radius: 28px 0 0 28px !important; border-right: none !important; background-color: #3f51b5 !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(8) p, [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(8) label p { padding-left: 10px !important; }

    /* HOVER & ACTIVE EFFECTS */
    [data-testid="stRadio"] [role="radiogroup"] label:hover { width: 220px !important; box-shadow: 0 8px 20px rgba(0,0,0,0.25) !important; animation: none !important; }
    [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) { width: 65px !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important; animation: none !important; }
    [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked):hover { width: 220px !important; }

    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(-n+4):has(input:checked), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(-n+4) label:has(input:checked) { border-right: 6px solid white !important; }
    [data-testid="stRadio"] [role="radiogroup"] > label:nth-child(n+5):has(input:checked), [data-testid="stRadio"] [role="radiogroup"] > div:nth-child(n+5) label:has(input:checked) { border-left: 6px solid white !important; }

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
    .hero-title { color: #ffffff !important; font-size: 48px; font-weight: normal; margin: 0; font-family: 'Algerian', 'Georgia', 'Times New Roman', serif !important; letter-spacing: 2px; }
    .hero-subtitle { color: #fee2e2 !important; font-size: 24px !important; font-family: 'Brush Script MT', 'Lucida Handwriting', cursive !important; margin-top: 8px; }

    /* METRIC CARDS & GENERAL UI */
    [data-testid="stMetricValue"] > div { font-size: 22px !important; }
    [data-testid="stMetricLabel"] > div > p { font-size: 16px !important; color: #6b7280 !important; }
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
# CONSTANTS & CLASSES
# ============================================================

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

COMPATIBILITY = {
    "A+": ["A+", "O+"], "A-": ["A-", "O-"], "B+": ["B+", "O+"], "B-": ["B-", "O-"],
    "AB+": ["AB+", "A+", "B+", "O+", "AB-", "A-", "B-", "O-"], "AB-": ["AB-", "A-", "B-", "O-"],
    "O+": ["O+", "O-"], "O-": ["O-"]
}

PRIORITY_RANK = {"Emergency": 1, "Urgent": 2, "Normal": 3}

class BloodCompatibilityStack:
    def __init__(self): self.items = []
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if self.items else None
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def get_items(self): return self.items.copy()

class PatientQueue:
    def __init__(self): self.items = deque()
    def enqueue(self, patient): self.items.append(patient)
    def dequeue(self): return self.items.popleft() if self.items else None
    def peek(self): return self.items[0] if self.items else None
    def size(self): return len(self.items)
    def is_empty(self): return len(self.items) == 0
    def get_items(self): return list(self.items)

def generate_id(prefix):
    return f"{prefix}{''.join(random.choices(string.digits, k=4))}"

# ============================================================
# LIVE SUPABASE DATABASE CONNECTION
# ============================================================

conn = st.connection("supabase", type="sql")

def get_patients():
    df = conn.query("SELECT * FROM patients;", ttl=0)
    if df.empty: return []
    df = df.rename(columns={"patient_id": "Patient ID", "patient_name": "Patient Name", "blood_group": "Blood Group", "units_required": "Units Required", "priority": "Priority", "hospital": "Hospital", "request_time": "Request Time"})
    return df.to_dict(orient="records")

def get_inventory():
    df = conn.query("SELECT * FROM inventory;", ttl=0)
    if df.empty: return []
    df = df.rename(columns={"unit_id": "Unit ID", "blood_group": "Blood Group", "units": "Units", "collection_date": "Collection Date", "expiry_date": "Expiry Date"})
    df['Collection Date'] = pd.to_datetime(df['Collection Date']).dt.date
    df['Expiry Date'] = pd.to_datetime(df['Expiry Date']).dt.date
    return df.to_dict(orient="records")

def get_history():
    df = conn.query("SELECT * FROM allocation_history ORDER BY id DESC;", ttl=0)
    if df.empty: return []
    df = df.rename(columns={"timestamp": "Timestamp", "patient_id": "Patient ID", "patient_name": "Patient", "blood_group": "Blood Group", "units": "Units", "priority": "Priority", "allocated_from": "Allocated From", "status": "Status"})
    return df.to_dict(orient="records")

def reset_demo_data():
    with conn.session as s:
        s.execute(text("DELETE FROM allocation_history;"))
        s.execute(text("DELETE FROM inventory;"))
        s.execute(text("DELETE FROM patients;"))
        
        patients_data = [
            {"pid": "P001", "name": "Aarav Sharma", "bg": "O+", "units": 2, "pri": "Emergency", "hosp": "City General Hospital", "time": "09:15"},
            {"pid": "P002", "name": "Meera Joshi", "bg": "A+", "units": 1, "pri": "Urgent", "hosp": "City General Hospital", "time": "09:30"},
            {"pid": "P003", "name": "Rohan Patil", "bg": "B+", "units": 2, "pri": "Normal", "hosp": "District Hospital", "time": "09:45"}
        ]
        for p in patients_data:
            s.execute(text("INSERT INTO patients (patient_id, patient_name, blood_group, units_required, priority, hospital, request_time) VALUES (:pid, :name, :bg, :units, :pri, :hosp, :time)"), p)
            
        today = date.today()
        inv_data = [
            {"uid": "BLD001", "bg": "O+", "u": 5, "cd": today - timedelta(days=10), "ed": today + timedelta(days=25)},
            {"uid": "BLD002", "bg": "O-", "u": 3, "cd": today - timedelta(days=20), "ed": today + timedelta(days=15)},
            {"uid": "BLD003", "bg": "A+", "u": 4, "cd": today - timedelta(days=7), "ed": today + timedelta(days=28)},
            {"uid": "BLD004", "bg": "A-", "u": 2, "cd": today - timedelta(days=12), "ed": today + timedelta(days=18)},
            {"uid": "BLD005", "bg": "B+", "u": 3, "cd": today - timedelta(days=5), "ed": today + timedelta(days=32)},
            {"uid": "BLD006", "bg": "AB+", "u": 2, "cd": today - timedelta(days=8), "ed": today + timedelta(days=29)}
        ]
        for i in inv_data:
            s.execute(text("INSERT INTO inventory (unit_id, blood_group, units, collection_date, expiry_date) VALUES (:uid, :bg, :u, :cd, :ed)"), i)
        s.commit()

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_total_inventory():
    return sum(item["Units"] for item in get_inventory() if item["Expiry Date"] >= date.today())

def get_inventory_by_group():
    result = {group: 0 for group in BLOOD_GROUPS}
    for item in get_inventory():
        if item["Expiry Date"] >= date.today():
            result[item["Blood Group"]] += item["Units"]
    return result

def get_expiry_alerts():
    today = date.today()
    alerts = []
    for item in get_inventory():
        days_left = (item["Expiry Date"] - today).days
        if days_left < 0:
            alerts.append({"Unit ID": item["Unit ID"], "Blood Group": item["Blood Group"], "Units": item["Units"], "Expiry Date": item["Expiry Date"], "Days Remaining": days_left, "Status": "EXPIRED"})
        elif days_left <= 7:
            alerts.append({"Unit ID": item["Unit ID"], "Blood Group": item["Blood Group"], "Units": item["Units"], "Expiry Date": item["Expiry Date"], "Days Remaining": days_left, "Status": "EXPIRING SOON"})
    return alerts

def build_patient_queue():
    patients = sorted(get_patients(), key=lambda patient: PRIORITY_RANK[patient["Priority"]])
    queue = PatientQueue()
    for patient in patients: queue.enqueue(patient)
    return queue

def build_compatibility_stack(blood_group):
    stack = BloodCompatibilityStack()
    for group in reversed(COMPATIBILITY[blood_group]): stack.push(group)
    return stack

def allocate_blood(patient):
    required = patient["Units Required"]
    stack = build_compatibility_stack(patient["Blood Group"])
    plan = []
    remaining = required
    inventory_list = get_inventory()

    while not stack.is_empty() and remaining > 0:
        donor_group = stack.pop()
        matching_units = [item for item in inventory_list if item["Blood Group"] == donor_group and item["Expiry Date"] >= date.today() and item["Units"] > 0]
        matching_units.sort(key=lambda item: item["Expiry Date"])

        for item in matching_units:
            if remaining <= 0: break
            quantity = min(item["Units"], remaining)
            plan.append({"Unit ID": item["Unit ID"], "Blood Group": item["Blood Group"], "Units": quantity})
            remaining -= quantity

    if remaining > 0: return False, [], required - remaining

    # Execute permanent database updates securely
    with conn.session as s:
        for allocation in plan:
            for item in inventory_list:
                if item["Unit ID"] == allocation["Unit ID"]:
                    new_units = item["Units"] - allocation["Units"]
                    if new_units <= 0:
                        s.execute(text("DELETE FROM inventory WHERE unit_id = :uid"), {"uid": item["Unit ID"]})
                    else:
                        s.execute(text("UPDATE inventory SET units = :u WHERE unit_id = :uid"), {"u": new_units, "uid": item["Unit ID"]})
                    break
        
        alloc_str = ", ".join([f"{item['Blood Group']} ({item['Units']})" for item in plan])
        s.execute(text("INSERT INTO allocation_history (timestamp, patient_id, patient_name, blood_group, units, priority, allocated_from, status) VALUES (:ts, :pid, :pname, :bg, :u, :pri, :af, :stat)"),
            {"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pid": patient["Patient ID"], "pname": patient["Patient Name"], "bg": patient["Blood Group"], "u": required, "pri": patient["Priority"], "af": alloc_str, "stat": "ALLOCATED"}
        )
        s.execute(text("DELETE FROM patients WHERE patient_id = :pid"), {"pid": patient["Patient ID"]})
        s.commit()

    return True, plan, required


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown('<div class="sidebar-brand">🩸 BLOODLINK</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Smart Blood Inventory & Allocation System</div>', unsafe_allow_html=True)

    if st.button("🔄 Reset Demo Data", use_container_width=True):
        reset_demo_data()
        st.session_state.allocation_result = None
        st.success("Database wiped and demo data restored.")
        st.rerun()


# ============================================================
# EDGE NAVIGATION WIDGET
# ============================================================

page = st.radio(
    "NAVIGATION",
    ["🏠 Dashboard", "👤 Patient", "🩸 Inventory", "⚡ Allocate", "Queue 📋", "Stack 📚", "Alerts ⏳", "Analytics 📊"],
    label_visibility="collapsed"
)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """<div class="hero"><div class="hero-title">🩸 BLOODLINK</div><div class="hero-subtitle">Smart Blood Inventory & Allocation System</div></div>""",
    unsafe_allow_html=True
)

# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "🏠 Dashboard":
    st.markdown('<div class="section-title">System Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Monitor blood inventory, patient requests, priority queues and expiry alerts.</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"""<div class="metric-card"><div class="metric-title">AVAILABLE BLOOD</div><div class="metric-value">{get_total_inventory()}</div><div class="metric-description">Usable blood units</div></div>""", unsafe_allow_html=True)
    with c2: st.markdown(f"""<div class="metric-card"><div class="metric-title">PENDING REQUESTS</div><div class="metric-value">{len(get_patients())}</div><div class="metric-description">Patients waiting</div></div>""", unsafe_allow_html=True)
    with c3: st.markdown(f"""<div class="metric-card"><div class="metric-title">EMERGENCY REQUESTS</div><div class="metric-value">{sum(1 for p in get_patients() if p["Priority"] == "Emergency")}</div><div class="metric-description">Highest priority</div></div>""", unsafe_allow_html=True)
    with c4: st.markdown(f"""<div class="metric-card"><div class="metric-title">EXPIRY ALERTS</div><div class="metric-value">{len(get_expiry_alerts())}</div><div class="metric-description">Units requiring attention</div></div>""", unsafe_allow_html=True)
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
    for column, (icon, title) in zip(workflow, [("👤", "Patient Request"), ("📋", "Priority Queue"), ("📚", "Compatibility Stack"), ("🩸", "Inventory Check"), ("✅", "Allocation")]):
        with column: st.markdown(f"""<div class="workflow-step">{icon}<br>{title}</div>""", unsafe_allow_html=True)
    st.markdown("")

    st.markdown('<div class="section-title">Priority Patient Requests</div>', unsafe_allow_html=True)
    queue = build_patient_queue()
    if queue.is_empty(): st.success("No pending patient requests.")
    else: st.dataframe(pd.DataFrame(queue.get_items()), use_container_width=True, hide_index=True)

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
                if not name.strip(): st.error("Please enter a patient name.")
                else:
                    patient_id = generate_id("P")
                    with conn.session as s:
                        s.execute(text("INSERT INTO patients (patient_id, patient_name, blood_group, units_required, priority, hospital, request_time) VALUES (:pid, :name, :bg, :units, :pri, :hosp, :time)"),
                            {"pid": patient_id, "name": name.strip(), "bg": blood_group, "units": units, "pri": priority, "hosp": hospital.strip() if hospital.strip() else "Not specified", "time": datetime.now().strftime("%H:%M")})
                        s.commit()
                    st.success(f"{patient_id} added successfully.")

    with right:
        st.subheader("Pending Patient Requests")
        queue = build_patient_queue()
        if queue.is_empty(): st.info("No pending patient requests.")
        else: st.dataframe(pd.DataFrame(queue.get_items()), use_container_width=True, hide_index=True)

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
                if expiry_date <= collection_date: st.error("Expiry date must be after collection date.")
                else:
                    unit_id = generate_id("BLD")
                    with conn.session as s:
                        s.execute(text("INSERT INTO inventory (unit_id, blood_group, units, collection_date, expiry_date) VALUES (:uid, :bg, :u, :cd, :ed)"),
                            {"uid": unit_id, "bg": blood_group, "u": units, "cd": collection_date, "ed": expiry_date})
                        s.commit()
                    st.success(f"{unit_id} added successfully.")

    with right:
        st.subheader("Current Inventory")
        inv_data = get_inventory()
        if inv_data:
            inventory_df = pd.DataFrame(inv_data)
            inventory_df["Status"] = inventory_df["Expiry Date"].apply(lambda expiry: "EXPIRED" if expiry < date.today() else ("EXPIRING SOON" if (expiry - date.today()).days <= 7 else "AVAILABLE"))
            st.dataframe(inventory_df, use_container_width=True, hide_index=True)
        else: st.info("Inventory is empty.")

# ============================================================
# PAGE 4 — SMART ALLOCATION
# ============================================================

elif page == "⚡ Allocate":
    st.markdown('<div class="section-title">Smart Blood Allocation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Process the highest-priority request using compatibility and earliest-expiry allocation logic.</div>', unsafe_allow_html=True)

    if "allocation_result" in st.session_state and st.session_state.allocation_result:
        res = st.session_state.allocation_result
        if res["status"] == "success":
            st.success(res["msg"])
            st.subheader("Allocation Details")
            st.dataframe(pd.DataFrame(res["plan"]), use_container_width=True, hide_index=True)
            st.info("The patient has been removed from the pending queue.")
        else:
            st.error(res["msg"])
            st.warning("No inventory was deducted.")
        st.session_state.allocation_result = None
        st.markdown("---")

    queue = build_patient_queue()

    if queue.is_empty():
        st.success("There are no pending patient requests.")
    else:
        patient = queue.peek()
        st.subheader("Next Patient")
        
        patient_columns = st.columns(5)
        for column, (label, value) in zip(patient_columns, [("Patient", patient["Patient Name"]), ("Blood Group", patient["Blood Group"]), ("Units", patient["Units Required"]), ("Priority", patient["Priority"]), ("Hospital", patient["Hospital"])]):
            with column: st.metric(label, value)

        st.markdown("---")
        st.subheader("Compatibility Stack")
        stack = build_compatibility_stack(patient["Blood Group"])
        compatible_groups = stack.get_items()

        if compatible_groups:
            stack_columns = st.columns(len(compatible_groups))
            for column, group in zip(stack_columns, compatible_groups):
                with column: st.markdown(f"""<div class="stack-item">🩸 {group}</div>""", unsafe_allow_html=True)

        st.caption("TOP → compatible donor groups are examined using the stack.")
        st.markdown("---")

        if st.button("⚡ Allocate Blood to Next Patient", type="primary", use_container_width=True):
            success, plan, amount = allocate_blood(patient)
            
            if success: st.session_state.allocation_result = {"status": "success", "msg": f"{amount} unit(s) successfully allocated to {patient['Patient Name']}.", "plan": plan}
            else: st.session_state.allocation_result = {"status": "error", "msg": f"Insufficient compatible inventory. Only {amount} of {patient['Units Required']} required unit(s) are available."}
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
    if queue.is_empty(): st.success("Queue is empty.")
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
        for group in reversed(items): st.markdown(f"""<div class="stack-item">🩸 {group}</div>""", unsafe_allow_html=True)
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

    history_data = get_history()
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("COMPLETED ALLOCATIONS", len(history_data))
    with c2: st.metric("UNITS ALLOCATED", sum(record["Units"] for record in history_data))
    with c3: st.metric("PENDING PATIENTS", len(get_patients()))

    st.markdown("---")
    st.subheader("Allocation History")
    
    if history_data: st.dataframe(pd.DataFrame(history_data), use_container_width=True, hide_index=True)
    else: st.info("No allocation has been completed yet.")

    st.markdown("---")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""<div class="footer">BLOODLINK • Smart Blood Inventory & Allocation System<br></div>""", unsafe_allow_html=True)
