import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime, date

# ---------------------------------------------------------
# PAGE CONFIG & BRANDING THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="Silver Line Homoeopathic ERP",
    page_icon="logo.png",  # Yahan 🌿 ki jaga logo.png kar diya hai
    layout="wide",
    initial_sidebar_state="expanded"
)

# LOGIN CREDENTIALS SETTINGS
USER_CREDENTIALS = {
    "Dr.Afzal": "global123"  # Yahan se aap Password change kar sakte hain
}

# Custom CSS for Senior-Friendly UI & Silver Line Homoeopathic Theme
st.markdown("""
    <style>
    /* Theme Colors: Emerald Green (#2e7d32) & Vibrant Blue (#0288d1) */
    .main {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    html, body, [class*="css"] {
        font-size: 18px !important; /* Senior-Friendly Large Text */
    }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #1b5e20 !important;
    }
    .brand-header {
        background: linear-gradient(135deg, #2e7d32, #0288d1);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .brand-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 1px;
    }
    .brand-header p {
        margin: 5px 0 0 0;
        font-size: 16px;
        opacity: 0.9;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOGIN SYSTEM FUNCTION
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_login():
    st.markdown("""
        <div class="brand-header">
            <h1>SILVER LINE HOMOEOPATHIC</h1>
            <p>System Security Access Control</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 Software Login")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
                st.session_state.authenticated = True
                st.success("✅ Access Granted!")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password")

if not st.session_state.authenticated:
    check_login()
    st.stop()

# Logout Option in Sidebar Bottom
if st.sidebar.button("🔒 Logout"):
    st.session_state.authenticated = False
    st.rerun()

# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect('silver_line_erp.db', check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, buy_price REAL, mrp REAL,
                    category TEXT, size TEXT, batch TEXT,
                    mfg_date TEXT, exp_date TEXT, barcode TEXT,
                    company TEXT, amount_paid REAL, stock INTEGER)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, phone TEXT, email TEXT, address TEXT, credit_limit REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT, customer_id INTEGER, salesman_id INTEGER,
                    total_amount REAL, discount REAL, net_amount REAL,
                    tax_hsn REAL, warranty_note TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER, product_id INTEGER, quantity INTEGER, price REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS doctors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT, name TEXT, clinic TEXT, phone TEXT, city TEXT, address TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS dealers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, business TEXT, phone TEXT, cnic TEXT, city TEXT, address TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT, category TEXT, amount REAL, notes TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS staff (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, designation TEXT, phone TEXT, salary REAL, fuel_allowance REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS staff_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_id INTEGER, date TEXT, sale_amount REAL, recovery_amount REAL, bonus REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)''')
    
    default_cats = ["Ampoules", "Balm", "Capsules", "Drops", "Malt, Jelly", 
                    "Ointment", "Oil", "Oral Liquid", "Patches", "Syrup", 
                    "Supplements", "Sachets", "Tablet", "Cream", "Mother Tincture"]
    for cat in default_cats:
        c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
    
    conn.commit()

init_db()

# ---------------------------------------------------------
# MAIN HEADER WITH LOGO
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 4])

with col_logo:
    try:
        st.image("logo.png", width=120)
    except:
        st.write("🌿")

with col_title:
    st.markdown("""
        <div class="brand-header" style="text-align: left; padding: 15px 25px;">
            <h1 style="margin: 0; font-size: 28px;">SILVER LINE HOMOEOPATHIC</h1>
            <p style="margin: 0; opacity: 0.9;">Advanced Management & Enterprise Resource Planning (ERP)</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MAIN NAVIGATION MENU & SIDEBAR LOGO
# ---------------------------------------------------------
try:
    st.sidebar.image("logo.png", use_container_width=True)
except:
    st.sidebar.write("🌿 **SILVER LINE HOMOEOPATHIC**")

st.sidebar.title("📌 Main Menu")
menu = [
    "📦 Inventory Management",
    "🛒 Sales & Billing (POS)",
    "👨‍⚕️ Doctor & Dealer Accounts",
    "📊 Financials & P&L",
    "👥 Staff & Commission Management"
]
choice = st.sidebar.radio("Select Module:", menu)

# =========================================================
# MODULE 1: INVENTORY MANAGEMENT
# =========================================================
if choice == "📦 Inventory Management":
    st.header("📦 Inventory & Stock Control")
    inv_tabs = st.tabs(["➕ Add Product", "📋 View Stock List", "⚙️ Manage Categories"])
    
    with inv_tabs[0]:
        st.subheader("Add New Inventory Item")
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                p_name = st.text_input("A) Product Name*")
                p_buy = st.number_input("B) Buy Price (PKR)", min_value=0.0)
                p_mrp = st.number_input("C) MRP (Retail Price)", min_value=0.0)
                
                cats_df = pd.read_sql_query("SELECT name FROM categories", conn)
                p_type = st.selectbox("D) Product Type", cats_df['name'].tolist() if not cats_df.empty else ["General"])
            
            with col2:
                p_size = st.text_input("E) Size / Pack Detail (e.g. 120 mL, 20s Pack, 50g)")
                p_batch = st.text_input("F) Batch Number")
                p_mfg = st.date_input("G) Mfg Date")
                p_exp = st.date_input("H) Exp Date")
                
            with col3:
                p_barcode = st.text_input("I) Barcode Number (Serialized)")
                p_company = st.text_input("J) Company", value="Silver Line Homoeopathic")
                p_paid = st.number_input("K) Amount Paid", min_value=0.0)
                p_stock = st.number_input("Initial Stock Quantity", min_value=1, step=1)
            
            btn_save = st.form_submit_button("💾 Save Product")
            if btn_save and p_name:
                c.execute('''INSERT INTO products 
                             (name, buy_price, mrp, category, size, batch, mfg_date, exp_date, barcode, company, amount_paid, stock)
                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                          (p_name, p_buy, p_mrp, p_type, p_size, p_batch, str(p_mfg), str(p_exp), p_barcode, p_company, p_paid, p_stock))
                conn.commit()
                st.success(f"✅ Product '{p_name}' successfully added to database!")

    with inv_tabs[1]:
        st.subheader("Inventory Records & Tracking")
        search_kw = st.text_input("🔍 Search Stock by Name, Category or Barcode:")
        query = "SELECT * FROM products"
        if search_kw:
            query += f" WHERE name LIKE '%{search_kw}%' OR category LIKE '%{search_kw}%' OR barcode LIKE '%{search_kw}%'"
        df_stock = pd.read_sql_query(query, conn)
        st.dataframe(df_stock, use_container_width=True)

    with inv_tabs[2]:
        st.subheader("Manage Product Categories")
        new_cat = st.text_input("Add New Product Type Category:")
        if st.button("Add Category") and new_cat:
            try:
                c.execute("INSERT INTO categories (name) VALUES (?)", (new_cat,))
                conn.commit()
                st.success(f"Category '{new_cat}' added!")
                st.rerun()
            except:
                st.warning("Category already exists.")

# =========================================================
# MODULE 2: SALES & BILLING (POS)
# =========================================================
elif choice == "🛒 Sales & Billing (POS)":
    st.header("🛒 Point of Sale & Billing System")
    
    with st.expander("⚙️ Bill Customization & Header Settings"):
        bill_title = st.text_input("Bill Heading", value="SILVER LINE HOMOEOPATHIC")
        bill_warranty = st.text_area("Warranty & Terms", value="Warranty valid as per Silver Line Homoeopathic terms. Goods once sold are not returnable after 7 days.")
    
    col_cust, col_item = st.columns([1, 2])
    
    with col_cust:
        st.subheader("1. Customer & Salesman")
        cust_name = st.text_input("Customer Name*")
        cust_phone = st.text_input("Customer Phone")
        cust_address = st.text_input("Customer Address")
        
        staff_df = pd.read_sql_query("SELECT id, name FROM staff", conn)
        salesman_id = st.selectbox("Salesman", options=staff_df['id'].tolist(), format_func=lambda x: staff_df[staff_df['id']==x]['name'].values[0] if not staff_df.empty else "Default") if not staff_df.empty else None

    with col_item:
        st.subheader("2. Add Products to Cart")
        prod_df = pd.read_sql_query("SELECT * FROM products WHERE stock > 0", conn)
        
        if not prod_df.empty:
            p_selected = st.selectbox("Select Product", options=prod_df['id'].tolist(), format_func=lambda x: f"{prod_df[prod_df['id']==x]['name'].values[0]} | Stock: {prod_df[prod_df['id']==x]['stock'].values[0]} | Price: PKR {prod_df[prod_df['id']==x]['mrp'].values[0]}")
            
            p_detail = prod_df[prod_df['id'] == p_selected].iloc[0]
            
            if pd.to_datetime(p_detail['exp_date']) <= pd.to_datetime('today') + pd.Timedelta(days=90):
                st.warning(f"⚠️ NEAR-EXPIRY ALERT: Expiry date is {p_detail['exp_date']}")
            
            q_cols = st.columns(3)
            qty = q_cols[0].number_input("Quantity", min_value=1, max_value=int(p_detail['stock']), value=1)
            disc = q_cols[1].number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0)
            gst = q_cols[2].number_input("GST/HSN (%)", min_value=0.0, value=0.0)
            
            cost_p = p_detail['buy_price']
            sell_p = p_detail['mrp']
            margin = ((sell_p - cost_p) / sell_p * 100) if sell_p > 0 else 0
            st.caption(f"💡 Profit Margin Visibility: **{margin:.1f}%** | Last Cost: PKR {cost_p}")

            if st.button("➕ Add Item to Invoice"):
                if 'cart' not in st.session_state:
                    st.session_state.cart = []
                net_price = (sell_p * (1 - disc/100)) * (1 + gst/100)
                st.session_state.cart.append({
                    "id": p_selected, "name": p_detail['name'], "qty": qty,
                    "unit_price": sell_p, "discount": disc, "gst": gst, "total": net_price * qty
                })
                st.success("Added to Cart!")

    if 'cart' in st.session_state and len(st.session_state.cart) > 0:
        st.write("---")
        st.subheader("🛒 Current Invoice Summary")
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df[['name', 'qty', 'unit_price', 'discount', 'gst', 'total']], use_container_width=True)
        
        grand_total = cart_df['total'].sum()
        extra_cash_disc = st.number_input("Extra Cash Discount (%):", min_value=0.0, max_value=100.0, value=0.0)
        final_bill = grand_total * (1 - extra_cash_disc/100)
        
        st.markdown(f"### 💵 Final Bill Amount: **PKR {final_bill:.2f}**")
        
        if st.button("🖨️ Complete Sale & Print Bill"):
            today_str = str(date.today())
            c.execute('''INSERT INTO sales (date, customer_id, salesman_id, total_amount, discount, net_amount, tax_hsn, warranty_note)
                         VALUES (?,?,?,?,?,?,?,?)''', (today_str, 0, salesman_id, grand_total, extra_cash_disc, final_bill, 0, bill_warranty))
            sale_id = c.lastrowid
            
            for item in st.session_state.cart:
                c.execute("INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?,?,?,?)",
                          (sale_id, item['id'], item['qty'], item['unit_price']))
                c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (item['qty'], item['id']))
            
            conn.commit()
            st.session_state.cart = []
            st.success("✅ Sale Recorded Successfully!")

# =========================================================
# MODULE 3: DOCTOR & DEALER ACCOUNTS
# =========================================================
elif choice == "👨‍⚕️ Doctor & Dealer Accounts":
    st.header("👨‍⚕️ Doctor & Dealer Account Records")
    acc_tab = st.tabs(["🩺 Doctor Accounts", "🤝 Dealer Accounts", "📅 Date-Wise Ledger Record"])
    
    with acc_tab[0]:
        st.subheader("Doctor Registration")
        with st.form("doc_form"):
            d_code = st.text_input("Account Code")
            d_name = st.text_input("Doctor Name")
            d_clinic = st.text_input("Clinic Name")
            d_phone = st.text_input("Phone Number")
            d_city = st.text_input("City")
            d_address = st.text_input("Address")
            if st.form_submit_button("Save Doctor Profile"):
                c.execute("INSERT INTO doctors (code, name, clinic, phone, city, address) VALUES (?,?,?,?,?,?)",
                          (d_code, d_name, d_clinic, d_phone, d_city, d_address))
                conn.commit()
                st.success("Doctor Added Successfully!")
        
        st.dataframe(pd.read_sql_query("SELECT * FROM doctors", conn), use_container_width=True)

    with acc_tab[1]:
        st.subheader("Dealer / Supplier Registration")
        with st.form("dealer_form"):
            dl_name = st.text_input("Dealer Name")
            dl_bus = st.text_input("Business Name")
            dl_phone = st.text_input("Phone Number")
            dl_cnic = st.text_input("CNIC Number")
            dl_city = st.text_input("City")
            dl_addr = st.text_input("Address")
            if st.form_submit_button("Save Dealer Profile"):
                c.execute("INSERT INTO dealers (name, business, phone, cnic, city, address) VALUES (?,?,?,?,?,?)",
                          (dl_name, dl_bus, dl_phone, dl_cnic, dl_city, dl_addr))
                conn.commit()
                st.success("Dealer Added Successfully!")
                
        st.dataframe(pd.read_sql_query("SELECT * FROM dealers", conn), use_container_width=True)

    with acc_tab[2]:
        st.subheader("Date-Wise Account Ledger & Sales Statement")
        sel_date = st.date_input("Select Date for Printable Statement:", value=date.today())
        
        if st.button("Generate Ledger View"):
            sales_df = pd.read_sql_query(f"SELECT * FROM sales WHERE date = '{str(sel_date)}'", conn)
            st.markdown(f"### 📋 Sales Ledger Statement - {sel_date}")
            st.dataframe(sales_df, use_container_width=True)

# =========================================================
# MODULE 4: FINANCIALS, EXPENSES & P&L
# =========================================================
elif choice == "📊 Financials & P&L":
    st.header("📊 Financial Analytics & Profit/Loss Statement")
    
    fin_tabs = st.tabs(["📈 Profit & Loss Statement", "💸 Expense Tracker", "📊 Sales Analytics"])
    
    with fin_tabs[0]:
        st.subheader("Profit & Loss (P&L) Summary")
        
        total_sales = pd.read_sql_query("SELECT SUM(net_amount) as val FROM sales", conn)['val'].iloc[0] or 0.0
        total_expenses = pd.read_sql_query("SELECT SUM(amount) as val FROM expenses", conn)['val'].iloc[0] or 0.0
        
        cogs = total_sales * 0.6
        net_profit = total_sales - (cogs + total_expenses)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Revenue", f"PKR {total_sales:,.2f}")
        col2.metric("Est. Cost of Goods", f"PKR {cogs:,.2f}")
        col3.metric("Total Expenses", f"PKR {total_expenses:,.2f}")
        col4.metric("Net Profit", f"PKR {net_profit:,.2f}", delta=f"{net_profit:.2f}")

    with fin_tabs[1]:
        st.subheader("Record Daily Expenses")
        with st.form("exp_form"):
            e_cat = st.selectbox("Expense Category", ["Staff Fuel", "Electricity Bill", "Rent", "Refreshments", "Miscellaneous"])
            e_amt = st.number_input("Amount (PKR)", min_value=0.0)
            e_note = st.text_input("Expense Details / Notes")
            if st.form_submit_button("Record Expense"):
                c.execute("INSERT INTO expenses (date, category, amount, notes) VALUES (?,?,?,?)",
                          (str(date.today()), e_cat, e_amt, e_note))
                conn.commit()
                st.success("Expense Recorded!")
                
        st.dataframe(pd.read_sql_query("SELECT * FROM expenses", conn), use_container_width=True)

    with fin_tabs[2]:
        st.subheader("Interactive Visual Graphs")
        sales_data = pd.read_sql_query("SELECT date, net_amount FROM sales", conn)
        if not sales_data.empty:
            fig = px.bar(sales_data, x='date', y='net_amount', title="Daily Sales Revenue Trend", color_discrete_sequence=['#2e7d32'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data available for graph plotting.")

# =========================================================
# MODULE 5: STAFF MANAGEMENT & COMMISSIONS
# =========================================================
elif choice == "👥 Staff & Commission Management":
    st.header("👥 Staff Management & Performance Rewards")
    
    st_tabs = st.tabs(["👤 Staff Registration", "💰 Salary & Bonus Tracker"])
    
    with st_tabs[0]:
        st.subheader("Register New Staff Member")
        with st.form("staff_form"):
            s_name = st.text_input("Staff Name")
            s_desig = st.selectbox("Designation", ["Salesman", "Delivery Boy", "Cashier", "Manager"])
            s_phone = st.text_input("Phone Number")
            s_sal = st.number_input("Base Monthly Salary", min_value=0.0)
            s_fuel = st.number_input("Fuel Allowance", min_value=0.0)
            if st.form_submit_button("Save Staff Profile"):
                c.execute("INSERT INTO staff (name, designation, phone, salary, fuel_allowance) VALUES (?,?,?,?,?)",
                          (s_name, s_desig, s_phone, s_sal, s_fuel))
                conn.commit()
                st.success("Staff Profile Added!")
                
        st.dataframe(pd.read_sql_query("SELECT * FROM staff", conn), use_container_width=True)

    with st_tabs[1]:
        st.subheader("Staff Sales, Recovery & Tiered Rewards")
        s_df = pd.read_sql_query("SELECT * FROM staff", conn)
        if not s_df.empty:
            sel_staff = st.selectbox("Select Staff Member", options=s_df['id'].tolist(), format_func=lambda x: s_df[s_df['id']==x]['name'].values[0])
            
            rec_amount = st.number_input("Market Recovery Amount Brought", min_value=0.0)
            bonus_perc = st.number_input("Bonus / Commission Percentage (%)", min_value=0.0, value=2.0)
            
            calculated_bonus = rec_amount * (bonus_perc / 100)
            st.info(f"💡 Earned Recovery Bonus: **PKR {calculated_bonus:.2f}**")
            
            if st.button("Record Staff Performance Record"):
                c.execute("INSERT INTO staff_performance (staff_id, date, sale_amount, recovery_amount, bonus) VALUES (?,?,?,?,?)",
                          (sel_staff, str(date.today()), 0.0, rec_amount, calculated_bonus))
                conn.commit()
                st.success("Performance & Bonus Saved!")
