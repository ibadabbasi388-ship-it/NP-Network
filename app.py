import streamlit as st
import pandas as pd
import webbrowser
import os
import time
import urllib.parse
from datetime import datetime, timedelta

# Auto-Enter library
try:
    import pyautogui
except:
    pass

# --- DATABASE SETUP ---
DB_FILE = "np_network_db.csv"
BRAND = "NP NETWORK"

# File check aur create karne ka sahi tariqa
if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=["Name", "Phone", "JoiningDate", "ExpiryDate", "Status"])
    df_init.to_csv(DB_FILE, index=False)

st.set_page_config(page_title=BRAND, layout="wide")
st.title(f"🌐 {BRAND} - Final Billing System")

# Data Load karna
def load_data():
    return pd.read_csv(DB_FILE)

data = load_data()

PAYMENT_INFO = """
*Payment Details:*
💰 Easypaisa: 03175067421 (Shahbaz Abbasi)
🏦 Bank: 083601114190332 (Ibad Abbasi)
Meezan Bank
"""

# --- SIDEBAR: ADD CUSTOMER (SAVE FIX) ---
with st.sidebar:
    st.header("➕ Add New Customer")
    n = st.text_input("Customer Name")
    p = st.text_input("WhatsApp (03xxxxxxxxx)")
    j_date = st.date_input("Joining Date", datetime.now())
    
    if st.button("Save To Database"):
        if n and p:
            # Number Format Fix
            num = ''.join(filter(str.isdigit, p)) 
            if num.startswith("0"): num = "92" + num[1:]
            elif not num.startswith("92"): num = "92" + num
            
            e_date = (j_date + timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Naya data
            new_data = pd.DataFrame([[n, num, j_date.strftime("%Y-%m-%d"), e_date, "Unpaid"]], 
                                    columns=["Name", "Phone", "JoiningDate", "ExpiryDate", "Status"])
            
            # File mein save karna
            new_data.to_csv(DB_FILE, mode='a', header=False, index=False)
            st.success(f"✅ {n} Save ho gaya!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Naam aur Number likhna lazmi hai!")

# --- DISPLAY & AUTO MESSAGES ---
st.subheader("📋 Customer List")
if not data.empty:
    for index, row in data.iterrows():
        is_unpaid = row['Status'] == "Unpaid"
        bg = "#FFEBEE" if is_unpaid else "#E8F5E9"
        
        st.markdown(f"""<div style="background-color:{bg}; padding:15px; border-radius:10px; margin-bottom:5px; color:black; border:1px solid #ccc;">
            <b>{row['Name']}</b> | 📞 {row['Phone']} | 📅 Expiry: {row['ExpiryDate']} | <b>{row['Status']}</b>
        </div>""", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if is_unpaid:
            if c1.button(f"Mark Paid & Send Msg ✅", key=f"paid_{index}"):
                # Update status
                full_df = pd.read_csv(DB_FILE)
                full_df.at[index, 'Status'] = "Paid"
                full_df.to_csv(DB_FILE, index=False)
                
                # Auto WhatsApp
                p_msg = f"Thank you {row['Name']}! ✅ Payment mil gaya hai. Internet active hai.\nRegards: {BRAND}"
                webbrowser.open(f"https://web.whatsapp.com/send?phone={row['Phone']}&text={urllib.parse.quote(p_msg)}")
                time.sleep(20)
                pyautogui.press('enter')
                st.rerun()
        
        if c2.button("Delete 🗑️", key=f"del_{index}"):
            full_df = pd.read_csv(DB_FILE)
            full_df.drop(index).to_csv(DB_FILE, index=False)
            st.rerun()
else:
    st.info("Abhi koi customer save nahi hai.")