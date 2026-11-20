import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ==============================================================================
# AGROBUILD STREAMLIT MVP PROTOTYPE
# Grounded in Agrobuild Technical Design, Wireframes & Pilot Specifications
# ==============================================================================

# Page Configuration
st.set_page_config(
    page_title="Agrobuild MVP Prototype",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Phone Simulator & Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Phone Shell & Screen */
    .phone-container {
        max-width: 420px;
        margin: 0 auto;
        background: #1e2922;
        border-radius: 28px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 3px solid #2d3e33;
    }
    
    .phone-header {
        text-align: center;
        color: #8fae98;
        font-size: 0.8rem;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-family: monospace;
    }
    
    .ussd-screen {
        background-color: #0d1710;
        color: #d1ebd8;
        font-family: 'Courier New', Courier, monospace;
        padding: 18px;
        border-radius: 12px;
        min-height: 220px;
        white-space: pre-wrap;
        font-size: 0.95rem;
        line-height: 1.5;
        border: 1px solid #1f3825;
    }
    
    .demo-badge {
        background-color: #e2f0d9;
        color: #2b5727;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }

    .sms-chat {
        background-color: #f0f4f1;
        border-radius: 12px;
        padding: 15px;
        min-height: 250px;
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid #d0ded3;
    }

    .sms-msg-user {
        background-color: #2d6a4f;
        color: white;
        padding: 8px 14px;
        border-radius: 14px 14px 2px 14px;
        margin: 6px 0 6px auto;
        max-width: 80%;
        font-size: 0.9rem;
    }

    .sms-msg-system {
        background-color: #ffffff;
        color: #1b2a1f;
        padding: 8px 14px;
        border-radius: 14px 14px 14px 2px;
        margin: 6px auto 6px 0;
        max-width: 80%;
        font-size: 0.9rem;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. INITIALIZE SESSION STATE (DATABASE & DATA STORE)
# ==============================================================================

def init_session_state():
    """Initializes in-memory mock storage with realistic sample data."""
    
    # Farmer Profile & Consent
    if "farmer_profile" not in st.session_state:
        st.session_state.farmer_profile = {
            "phone": "08031234567",
            "state": "Osun",
            "area": "Ede North / Oshogbo",
            "crops": ["Maize", "Cassava", "Yam"],
            "language": "Yoruba",
            "consent_agreed": True,
            "registration_date": "2026-11-15"
        }
        
    # Problem Reports
    if "problem_reports" not in st.session_state:
        st.session_state.problem_reports = [
            {
                "id": 101,
                "phone": "08031234567",
                "crop": "Maize",
                "issue": "Pests (Fall Armyworm)",
                "channel": "USSD",
                "date": "2026-11-18 09:15",
                "state": "Osun",
                "status": "Pending",
                "expert_reply": ""
            },
            {
                "id": 102,
                "phone": "08029876543",
                "crop": "Cassava",
                "issue": "Disease (Mosaic Leaf Curl)",
                "channel": "SMS",
                "date": "2026-11-18 10:30",
                "state": "Osun",
                "status": "Answered",
                "expert_reply": "Apply neem oil extract or plant resistant cassava stems (TME 419). Ensure farm weed management."
            },
            {
                "id": 103,
                "phone": "08051112233",
                "crop": "Yam",
                "issue": "Soil or fertiliser",
                "channel": "USSD",
                "date": "2026-11-19 08:20",
                "state": "Oyo",
                "status": "Pending",
                "expert_reply": ""
            }
        ]
        
    # Market Prices (Sample benchmark data)
    if "market_prices" not in st.session_state:
        st.session_state.market_prices = [
            {"crop": "Maize", "market": "Oja Oba, Oshogbo", "state": "Osun", "price": "₦32,000 / 50kg bag", "date": "2026-11-18"},
            {"crop": "Rice", "market": "Bodija Market, Ibadan", "state": "Oyo", "price": "₦58,000 / 50kg bag", "date": "2026-11-18"},
            {"crop": "Cassava", "market": "Igbona Market, Oshogbo", "state": "Osun", "price": "₦18,000 / pickup load", "date": "2026-11-17"},
            {"crop": "Yam", "market": "Mile 12, Lagos", "state": "Lagos", "price": "₦45,000 / 100 tubers", "date": "2026-11-18"},
            {"crop": "Vegetables", "market": "Oja Oba, Oshogbo", "state": "Osun", "price": "₦4,500 / basket", "date": "2026-11-18"}
        ]
        
    # Produce Listings (Farmer Produce for Sale)
    if "produce_listings" not in st.session_state:
        st.session_state.produce_listings = [
            {"id": 201, "phone": "08031234567", "crop": "Maize", "quantity": "20 bags", "location": "Ede, Osun", "date": "2026-11-18 11:00", "consent_shared": True},
            {"id": 202, "phone": "08029876543", "crop": "Cassava", "quantity": "5 tonnes", "location": "Ilesa, Osun", "date": "2026-11-18 14:20", "consent_shared": True}
        ]
        
    # Farming Tips Lookup
    if "farming_tips" not in st.session_state:
        st.session_state.farming_tips = {
            "Maize": "Plant early at first rains. Space seeds 25cm apart in 75cm rows. Apply NPK 15:15:15 at 2 weeks.",
            "Rice": "Keep water levels consistent during flowering. Apply urea top-dressing at tillering stage.",
            "Cassava": "Use healthy stem cuttings (20-25cm long) planted at a 45-degree angle. Weed early in first 3 months.",
            "Yam": "Stake vines early to improve sunlight exposure and crop yield. Mulch seed heaps against heat.",
            "Vegetables": "Water early in the morning or late evening. Rotate crops to break pest cycles."
        }
        
    # USSD Session Navigation State
    if "ussd_active" not in st.session_state:
        st.session_state.ussd_active = False
    if "ussd_screen" not in st.session_state:
        st.session_state.ussd_screen = "MAIN"
    if "ussd_history" not in st.session_state:
        st.session_state.ussd_history = []
    if "ussd_temp_data" not in st.session_state:
        st.session_state.ussd_temp_data = {}
    if "ussd_output_msg" not in st.session_state:
        st.session_state.ussd_output_msg = ""

    # SMS Chat Log History
    if "sms_history" not in st.session_state:
        st.session_state.sms_history = [
            {"sender": "system", "text": "Welcome to Agrobuild SMS Service. Try sending: PRICE MAIZE, PROBLEM CASSAVA PESTS, SELL YAM 20BAGS, or TIP MAIZE."}
        ]

init_session_state()


# ==============================================================================
# 2. LOGO DISPLAY HELPER
# ==============================================================================

def render_sidebar_logo():
    """Renders logo if available in workspace, otherwise renders clean header badge."""
    logo_paths = [Path("logo.png"), Path("assets/logo.png"), Path("knowledge/logo.png")]
    found_logo = None
    for p in logo_paths:
        if p.exists():
            found_logo = p
            break
            
    if found_logo:
        st.sidebar.image(str(found_logo), use_container_width=True)
    else:
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 10px; background-color: #1f4d2e; color: white; border-radius: 8px; margin-bottom: 15px;">
            <h2 style="margin:0; font-family: Georgia, serif;">🌾 AGROBUILD</h2>
            <p style="margin:0; font-size: 0.8rem; opacity: 0.9;">USPF Changemaker Challenge 2026</p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# 3. USSD SIMULATOR ENGINE & STATE MACHINE
# ==============================================================================

def reset_ussd_session():
    st.session_state.ussd_active = False
    st.session_state.ussd_screen = "MAIN"
    st.session_state.ussd_history = []
    st.session_state.ussd_temp_data = {}
    st.session_state.ussd_output_msg = ""

def process_ussd_input(user_input):
    user_input = user_input.strip()
    current_screen = st.session_state.ussd_screen
    
    # Handle Global Session Navigation
    if user_input == "0" and current_screen != "MAIN":
        if st.session_state.ussd_history:
            st.session_state.ussd_screen = st.session_state.ussd_history.pop()
        else:
            st.session_state.ussd_screen = "MAIN"
        st.session_state.ussd_output_msg = ""
        return

    # Screen Logic Transitions
    if current_screen == "MAIN":
        if user_input == "1":
            st.session_state.ussd_history.append("MAIN")
            st.session_state.ussd_screen = "REPORT_CROP"
        elif user_input == "2":
            st.session_state.ussd_history.append("MAIN")
            st.session_state.ussd_screen = "PRICES_CROP"
        elif user_input == "3":
            st.session_state.ussd_history.append("MAIN")
            st.session_state.ussd_screen = "SELL_CROP"
        elif user_input == "4":
            st.session_state.ussd_history.append("MAIN")
            st.session_state.ussd_screen = "TIPS_CROP"
        elif user_input == "5":
            st.session_state.ussd_history.append("MAIN")
            st.session_state.ussd_screen = "LANGUAGE"
        else:
            st.session_state.ussd_output_msg = "Invalid choice. Select 1-5 or 0."

    elif current_screen == "REPORT_CROP":
        crops_map = {"1": "Maize", "2": "Rice", "3": "Cassava", "4": "Yam", "5": "Vegetables", "6": "Other"}
        if user_input in crops_map:
            st.session_state.ussd_temp_data["crop"] = crops_map[user_input]
            st.session_state.ussd_history.append("REPORT_CROP")
            st.session_state.ussd_screen = "REPORT_ISSUE"
        else:
            st.session_state.ussd_output_msg = "Invalid crop. Choose 1-6 or 0."

    elif current_screen == "REPORT_ISSUE":
        issues_map = {"1": "Pests", "2": "Disease", "3": "Soil or fertiliser", "4": "Weather or water", "5": "Other"}
        if user_input in issues_map:
            chosen_issue = issues_map[user_input]
            chosen_crop = st.session_state.ussd_temp_data.get("crop", "Crop")
            
            # Save new report to database
            new_id = len(st.session_state.problem_reports) + 101
            st.session_state.problem_reports.append({
                "id": new_id,
                "phone": st.session_state.farmer_profile["phone"],
                "crop": chosen_crop,
                "issue": chosen_issue,
                "channel": "USSD",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "state": st.session_state.farmer_profile["state"],
                "status": "Pending",
                "expert_reply": ""
            })
            
            st.session_state.ussd_screen = "CONFIRMATION"
            st.session_state.ussd_output_msg = f"Report received for {chosen_crop} ({chosen_issue}). An expert will reply by SMS within 48 hours.\n\n(Demo Simulation)"
        else:
            st.session_state.ussd_output_msg = "Invalid issue. Choose 1-5 or 0."

    elif current_screen == "PRICES_CROP":
        crops_map = {"1": "Maize", "2": "Rice", "3": "Cassava", "4": "Yam", "5": "Vegetables"}
        if user_input in crops_map:
            selected_crop = crops_map[user_input]
            matching = [p for p in st.session_state.market_prices if p["crop"] == selected_crop]
            if matching:
                p_info = matching[0]
                st.session_state.ussd_output_msg = f"MARKET PRICE ({selected_crop.upper()})\nMarket: {p_info['market']}\nPrice: {p_info['price']}\nDate: {p_info['date']}\n\n0. Back"
            else:
                st.session_state.ussd_output_msg = f"No price quote for {selected_crop} currently in database.\n\n0. Back"
        else:
            st.session_state.ussd_output_msg = "Invalid choice. Choose 1-5 or 0."

    elif current_screen == "SELL_CROP":
        crops_map = {"1": "Maize", "2": "Rice", "3": "Cassava", "4": "Yam", "5": "Vegetables"}
        if user_input in crops_map:
            st.session_state.ussd_temp_data["sell_crop"] = crops_map[user_input]
            st.session_state.ussd_screen = "SELL_QUANTITY"
            st.session_state.ussd_output_msg = f"Enter quantity for {crops_map[user_input]} (e.g. 20 bags, 50 tubers):\n\n0. Back"
        else:
            st.session_state.ussd_output_msg = "Invalid choice. Choose 1-5 or 0."

    elif current_screen == "SELL_QUANTITY":
        if user_input:
            sell_crop = st.session_state.ussd_temp_data.get("sell_crop", "Produce")
            new_id = len(st.session_state.produce_listings) + 201
            st.session_state.produce_listings.append({
                "id": new_id,
                "phone": st.session_state.farmer_profile["phone"],
                "crop": sell_crop,
                "quantity": user_input,
                "location": f"{st.session_state.farmer_profile['area']}, {st.session_state.farmer_profile['state']}",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "consent_shared": st.session_state.farmer_profile["consent_agreed"]
            })
            st.session_state.ussd_screen = "CONFIRMATION"
            st.session_state.ussd_output_msg = f"Produce listed: {sell_crop} ({user_input}). Matching buyers will be notified by SMS.\n\n(Demo Simulation)"

    elif current_screen == "TIPS_CROP":
        crops_map = {"1": "Maize", "2": "Rice", "3": "Cassava", "4": "Yam", "5": "Vegetables"}
        if user_input in crops_map:
            crop = crops_map[user_input]
            tip = st.session_state.farming_tips.get(crop, "Ensure adequate weeding and soil aeration.")
            st.session_state.ussd_output_msg = f"FARMING TIP ({crop.upper()}):\n{tip}\n\n0. Back"
        else:
            st.session_state.ussd_output_msg = "Invalid choice. Choose 1-5 or 0."

    elif current_screen == "LANGUAGE":
        lang_map = {"1": "English", "2": "Pidgin", "3": "Hausa", "4": "Yoruba", "5": "Igbo"}
        if user_input in lang_map:
            selected_lang = lang_map[user_input]
            st.session_state.farmer_profile["language"] = selected_lang
            st.session_state.ussd_output_msg = f"Language saved: {selected_lang}.\n\n(Demo: menus remain in English during prototype pilot)\n\n0. Back"
        else:
            st.session_state.ussd_output_msg = "Invalid language selection. Choose 1-5 or 0."

    elif current_screen == "CONFIRMATION":
        reset_ussd_session()


def get_ussd_screen_text():
    screen = st.session_state.ussd_screen
    msg = st.session_state.ussd_output_msg
    
    if msg and screen in ["PRICES_CROP", "TIPS_CROP", "LANGUAGE", "CONFIRMATION", "SELL_QUANTITY"]:
        return msg

    if screen == "MAIN":
        return "AGROBUILD USSD MENU\n1. Report farm problem\n2. Market prices\n3. Sell my produce\n4. Farming tips\n5. Language\n\n0. Exit Session"
    elif screen == "REPORT_CROP":
        return "REPORT A PROBLEM - CHOOSE CROP\n1. Maize\n2. Rice\n3. Cassava\n4. Yam\n5. Vegetables\n6. Other\n\n0. Back"
    elif screen == "REPORT_ISSUE":
        crop = st.session_state.ussd_temp_data.get('crop', 'Crop')
        return f"ISSUE FOR {crop.upper()}\n1. Pests\n2. Disease\n3. Soil or fertiliser\n4. Weather or water\n5. Other\n\n0. Back"
    elif screen == "PRICES_CROP":
        return "MARKET PRICES - CHOOSE CROP\n1. Maize\n2. Rice\n3. Cassava\n4. Yam\n5. Vegetables\n\n0. Back"
    elif screen == "SELL_CROP":
        return "SELL PRODUCE - CHOOSE CROP\n1. Maize\n2. Rice\n3. Cassava\n4. Yam\n5. Vegetables\n\n0. Back"
    elif screen == "TIPS_CROP":
        return "FARMING TIPS - CHOOSE CROP\n1. Maize\n2. Rice\n3. Cassava\n4. Yam\n5. Vegetables\n\n0. Back"
    elif screen == "LANGUAGE":
        return "SELECT LANGUAGE\n1. English\n2. Pidgin\n3. Hausa\n4. Yoruba\n5. Igbo\n\n0. Back"
    return "Session ended."


# ==============================================================================
# 4. SMS COMMAND PARSER & ENGINE
# ==============================================================================

def process_sms_command(raw_text):
    raw_text = raw_text.strip()
    if not raw_text:
        return
    
    # Append user command
    st.session_state.sms_history.append({"sender": "user", "text": raw_text})
    
    parts = raw_text.split()
    cmd = parts[0].upper()
    args = parts[1:]
    
    # Handle Command: PROBLEM or PEST
    if cmd in ["PROBLEM", "PEST"]:
        if len(args) >= 1:
            crop = args[0].capitalize()
            issue = " ".join(args[1:]).capitalize() if len(args) > 1 else "Unspecified pest/crop issue"
            
            # Save report
            new_id = len(st.session_state.problem_reports) + 101
            st.session_state.problem_reports.append({
                "id": new_id,
                "phone": st.session_state.farmer_profile["phone"],
                "crop": crop,
                "issue": issue,
                "channel": "SMS",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "state": st.session_state.farmer_profile["state"],
                "status": "Pending",
                "expert_reply": ""
            })
            reply = f"Agrobuild: Problem report for {crop} ({issue}) received. An agricultural expert will reply by SMS within 48 hours. (Ref #{new_id})"
        else:
            reply = "Agrobuild: Invalid format. Use: PROBLEM <crop> <issue> (e.g. PROBLEM MAIZE PESTS)"

    # Handle Command: PRICE
    elif cmd == "PRICE":
        if len(args) >= 1:
            crop = args[0].capitalize()
            state_filter = args[1].capitalize() if len(args) > 1 else None
            
            matching = [p for p in st.session_state.market_prices if p["crop"].lower() == crop.lower()]
            if state_filter:
                matching = [p for p in matching if p["state"].lower() == state_filter.lower()]
                
            if matching:
                p = matching[0]
                reply = f"Agrobuild Price: {p['crop']} in {p['market']} ({p['state']}) is {p['price']} as of {p['date']}."
            else:
                reply = f"Agrobuild: Sample price for {crop} is ₦30,000 - ₦45,000 depending on state. (Live feed in pilot)"
        else:
            reply = "Agrobuild: Invalid format. Use: PRICE <crop> [state] (e.g. PRICE RICE OSUN)"

    # Handle Command: SELL
    elif cmd == "SELL":
        if len(args) >= 2:
            crop = args[0].capitalize()
            quantity = args[1]
            state_loc = args[2].capitalize() if len(args) > 2 else st.session_state.farmer_profile["state"]
            
            new_id = len(st.session_state.produce_listings) + 201
            st.session_state.produce_listings.append({
                "id": new_id,
                "phone": st.session_state.farmer_profile["phone"],
                "crop": crop,
                "quantity": quantity,
                "location": f"{state_loc}",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "consent_shared": st.session_state.farmer_profile["consent_agreed"]
            })
            reply = f"Agrobuild: {quantity} of {crop} listed for sale in {state_loc}. Matching buyers will be notified."
        else:
            reply = "Agrobuild: Invalid format. Use: SELL <crop> <quantity> [state] (e.g. SELL MAIZE 20BAGS OSUN)"

    # Handle Command: TIP
    elif cmd == "TIP":
        if len(args) >= 1:
            crop = args[0].capitalize()
            tip = st.session_state.farming_tips.get(crop, "Rotate crops and maintain clean soil management to maximize yields.")
            reply = f"Agrobuild Tip ({crop}): {tip}"
        else:
            reply = "Agrobuild: Invalid format. Use: TIP <crop> (e.g. TIP YAM)"

    # Unrecognized Command
    else:
        reply = "Agrobuild: Command not recognized. Supported commands:\n• PROBLEM <crop> <issue>\n• PRICE <crop> [state]\n• SELL <crop> <qty> [state]\n• TIP <crop>"

    st.session_state.sms_history.append({"sender": "system", "text": reply})


# ==============================================================================
# 5. STREAMLIT USER INTERFACE & NAVIGATION
# ==============================================================================

render_sidebar_logo()

st.sidebar.title("Agrobuild MVP Platform")
app_mode = st.sidebar.radio(
    "Select Operating View:",
    [
        "📱 Farmer Phone Simulator (USSD & SMS)",
        "👤 Farmer Profile & Data Consent",
        "👨‍🌾 Expert Advisory Dashboard",
        "📊 Market Prices & Produce Listings",
        "📈 Problem Tracking & Analytics"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.85rem; color: #555;">
    <b>Agrobuild Pilot Status:</b> Osun State<br/>
    <b>Target:</b> 100 Smallholder Farmers<br/>
    <b>Channels:</b> USSD (*XXX#) & SMS Commands<br/>
    <b>NDPA 2023:</b> Privacy Compliant
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# VIEW 1: FARMER PHONE SIMULATOR (USSD & SMS)
# ------------------------------------------------------------------------------
if app_mode == "📱 Farmer Phone Simulator (USSD & SMS)":
    st.title("📱 Agrobuild Farmer Phone Simulator")
    st.markdown("Simulate a rural smallholder farmer interacting with Agrobuild on a basic feature phone without internet.")

    tab_ussd, tab_sms = st.tabs(["📟 USSD Code Simulator (*XXX#)", "💬 SMS Command Simulator"])

    # --- TAB A: USSD SIMULATOR ---
    with tab_ussd:
        st.markdown("<span class='demo-badge'>USSD Channel (*XXX#)</span>", unsafe_allow_html=True)
        st.info("Farmers dial the shortcode to navigate numbered menus. Uses simple keypads.")

        col_phone, col_info = st.columns([1, 1])

        with col_phone:
            st.markdown("""
            <div class='phone-container'>
                <div class='phone-header'>AGROBUILD USSD TERMINAL</div>
            """, unsafe_allow_html=True)

            # Display Screen Text
            if not st.session_state.ussd_active:
                screen_content = "AGROBUILD USSD SERVICE\n\nPress 'Dial *XXX#' below to open the menu session."
            else:
                screen_content = get_ussd_screen_text()

            st.markdown(f"<div class='ussd-screen'>{screen_content}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Controls
            if not st.session_state.ussd_active:
                if st.button("📞 Dial *XXX#", use_container_width=True, type="primary"):
                    st.session_state.ussd_active = True
                    st.session_state.ussd_screen = "MAIN"
                    st.session_state.ussd_output_msg = ""
                    st.rerun()
            else:
                with st.form(key="ussd_form", clear_on_submit=True):
                    user_code = st.text_input("Enter Option Number / Input:", placeholder="e.g. 1, 2, 0")
                    c_send, c_exit = st.columns([2, 1])
                    send_pressed = c_send.form_submit_button("Send Choice", use_container_width=True, type="primary")
                    exit_pressed = c_exit.form_submit_button("Cancel / End", use_container_width=True)

                    if send_pressed and user_code:
                        process_ussd_input(user_code)
                        st.rerun()
                    if exit_pressed:
                        reset_ussd_session()
                        st.rerun()

        with col_info:
            st.subheader("💡 USSD Menu Reference Wireframe")
            st.markdown("""
            * **Main Menu:**
                1. Report farm problem
                2. Market prices
                3. Sell my produce
                4. Farming tips
                5. Language
            * **Navigation Keys:**
                * `0` : Go Back / Main Menu
                * `Cancel` : End USSD Session
            * **Automated Actions:**
                * Submitting a problem report automatically queues it for agricultural experts on the Expert Advisory Dashboard.
                * Submitting produce listings publishes it to the Produce Exchange.
            """)

    # --- TAB B: SMS SIMULATOR ---
    with tab_sms:
        st.markdown("<span class='demo-badge'>SMS Channel</span>", unsafe_allow_html=True)
        st.info("Farmers who prefer texting can send keyword commands to Agrobuild's SMS gateway.")

        col_chat, col_guide = st.columns([1.2, 1])

        with col_chat:
            st.subheader("📲 Interactive SMS Box")
            
            # Render Messages
            chat_html = "<div class='sms-chat'>"
            for msg in st.session_state.sms_history:
                if msg["sender"] == "user":
                    chat_html += f"<div class='sms-msg-user'><b>Farmer:</b> {msg['text']}</div>"
                else:
                    chat_html += f"<div class='sms-msg-system'><b>Agrobuild:</b> {msg['text']}</div>"
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            with st.form(key="sms_form", clear_on_submit=True):
                sms_in = st.text_input("Type SMS Command:", placeholder="e.g. PROBLEM MAIZE PESTS or PRICE RICE OSUN")
                b_send = st.form_submit_button("Send SMS", use_container_width=True, type="primary")
                if b_send and sms_in:
                    process_sms_command(sms_in)
                    st.rerun()

        with col_guide:
            st.subheader("📜 Draft SMS Command Syntax")
            st.markdown("""
            | Action | Syntax Format | Example |
            | :--- | :--- | :--- |
            | **Report Problem** | `PROBLEM <crop> <issue>` | `PROBLEM MAIZE PESTS` |
            | **Report Pest** | `PEST <crop>` | `PEST CASSAVA` |
            | **Get Market Price** | `PRICE <crop> [state]` | `PRICE RICE OSUN` |
            | **Sell Produce** | `SELL <crop> <qty> [state]` | `SELL YAM 20BAGS OSUN` |
            | **Get Farming Tip** | `TIP <crop>` | `TIP YAM` |
            """)
            st.caption("Note: Commands are case-insensitive. Handles extra spaces gracefully.")


# ------------------------------------------------------------------------------
# VIEW 2: FARMER PROFILE & DATA CONSENT
# ------------------------------------------------------------------------------
elif app_mode == "👤 Farmer Profile & Data Consent":
    st.title("👤 Farmer Registration & Data Consent Check")
    st.markdown("Compliant with **Nigeria Data Protection Act (NDPA 2023)** notes. Captures minimal necessary farmer attributes.")

    with st.form(key="farmer_profile_form"):
        st.subheader("Farmer Attributes")
        c1, c2 = st.columns(2)
        phone = c1.text_input("Mobile Phone Number:", value=st.session_state.farmer_profile["phone"])
        state = c2.selectbox("Pilot State / Area:", ["Osun", "Oyo", "Ogun", "Lagos", "Kwara", "Kano"], index=0)
        
        area = c1.text_input("LGA / Community Area:", value=st.session_state.farmer_profile["area"])
        language = c2.selectbox("Preferred Communication Language:", ["Yoruba", "English", "Pidgin", "Hausa", "Igbo"])

        crops = st.multiselect("Primary Crops Grown:", ["Maize", "Cassava", "Yam", "Rice", "Vegetables", "Cocoa"], default=st.session_state.farmer_profile["crops"])

        st.markdown("---")
        st.subheader("🔒 Data Privacy & Consent Agreement")
        st.info("Notice: Agrobuild collects your phone number, location, and crop details solely to deliver agricultural advice, market prices, and buyer contacts. Your personal contact details are never shared with buyers without your explicit approval.")

        consent = st.checkbox("I agree to the collection and processing of my farming data as outlined above.", value=st.session_state.farmer_profile["consent_agreed"])

        submit_prof = st.form_submit_button("Save Farmer Profile & Preferences", type="primary")

        if submit_prof:
            st.session_state.farmer_profile = {
                "phone": phone,
                "state": state,
                "area": area,
                "crops": crops,
                "language": language,
                "consent_agreed": consent,
                "registration_date": datetime.now().strftime("%Y-%m-%d")
            }
            st.success("Farmer Profile & Privacy Consent successfully updated!")


# ------------------------------------------------------------------------------
# VIEW 3: EXPERT ADVISORY DASHBOARD
# ------------------------------------------------------------------------------
elif app_mode == "👨‍🌾 Expert Advisory Dashboard":
    st.title("👨‍🌾 Agricultural Expert Advisory Portal")
    st.markdown("Agronomists and extension officers review submitted farmer problem reports and respond via SMS/Voice.")

    reports_df = pd.DataFrame(st.session_state.problem_reports)
    
    # Key Metrics
    total_reports = len(reports_df)
    pending_cnt = len(reports_df[reports_df["status"] == "Pending"])
    answered_cnt = len(reports_df[reports_df["status"] == "Answered"])
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Submitted Reports", total_reports)
    m2.metric("Pending Advisory", pending_cnt, delta=f"{pending_cnt} urgent" if pending_cnt>0 else "Clear", delta_color="inverse")
    m3.metric("Resolved / Answered", answered_cnt)
    m4.metric("Target SLA Response Time", "< 48 Hours")

    st.markdown("---")
    st.subheader("📋 Submitted Farm Problem Reports")

    if not reports_df.empty:
        # Table view
        st.dataframe(reports_df[["id", "date", "phone", "state", "crop", "issue", "channel", "status"]], use_container_width=True)

        st.subheader("✍️ Select Report to Review & Respond")
        
        pending_reports = st.session_state.problem_reports
        report_options = {f"ID #{r['id']} - {r['crop']} ({r['issue']}) [{r['status']}]": r for r in pending_reports}
        
        selected_key = st.selectbox("Choose a Problem Report:", list(report_options.keys()))
        selected_report = report_options[selected_key]

        col_detail, col_reply = st.columns([1, 1])

        with col_detail:
            st.markdown(f"""
            <div style="background:#eef6f0; padding:15px; border-radius:8px; border:1px solid #c8e0d0;">
                <h4>Report Details (ID #{selected_report['id']})</h4>
                <p><b>Farmer Phone:</b> {selected_report['phone']}</p>
                <p><b>State / Area:</b> {selected_report['state']}</p>
                <p><b>Crop:</b> {selected_report['crop']}</p>
                <p><b>Reported Issue:</b> {selected_report['issue']}</p>
                <p><b>Channel:</b> {selected_report['channel']}</p>
                <p><b>Submitted Date:</b> {selected_report['date']}</p>
                <p><b>Current Status:</b> <code>{selected_report['status']}</code></p>
            </div>
            """, unsafe_allow_html=True)

            if selected_report["expert_reply"]:
                st.success(f"**Existing Expert Advice:** {selected_report['expert_reply']}")

        with col_reply:
            with st.form(key="expert_reply_form"):
                reply_text = st.text_area("Type Expert Advisory Response (will be sent to farmer via SMS):", value=selected_report["expert_reply"], height=120)
                btn_send_reply = st.form_submit_button("Dispatch Advisory Reply (SMS)", type="primary")

                if btn_send_reply and reply_text:
                    # Update report record
                    for r in st.session_state.problem_reports:
                        if r["id"] == selected_report["id"]:
                            r["expert_reply"] = reply_text
                            r["status"] = "Answered"
                            break
                    st.success(f"Advisory reply dispatched to {selected_report['phone']} via SMS!")
                    st.rerun()
    else:
        st.info("No problem reports submitted yet.")


# ------------------------------------------------------------------------------
# VIEW 4: MARKET PRICES & PRODUCE LISTINGS
# ------------------------------------------------------------------------------
elif app_mode == "📊 Market Prices & Produce Listings":
    st.title("📊 Produce Listings & Commodity Market Prices")

    tab_prices, tab_listings = st.tabs(["💰 Market Benchmark Prices", "🌽 Farmer Produce Listings for Sale"])

    # --- TAB A: MARKET PRICES ---
    with tab_prices:
        st.subheader("Daily Local Market Benchmark Prices")
        prices_df = pd.DataFrame(st.session_state.market_prices)
        st.dataframe(prices_df, use_container_width=True)

        st.markdown("---")
        st.subheader("➕ Add / Update Sample Market Price (Ops Utility)")
        with st.form(key="add_price_form"):
            c1, c2, c3, c4 = st.columns(4)
            p_crop = c1.selectbox("Crop:", ["Maize", "Rice", "Cassava", "Yam", "Vegetables"])
            p_market = c2.text_input("Market Name:", value="Oja Oba, Oshogbo")
            p_state = c3.selectbox("State:", ["Osun", "Oyo", "Lagos", "Kano", "Ogun"])
            p_price = c4.text_input("Price Quote:", value="₦35,000 / 50kg bag")
            
            btn_add_p = st.form_submit_button("Publish Market Price", type="primary")
            if btn_add_p:
                st.session_state.market_prices.append({
                    "crop": p_crop,
                    "market": p_market,
                    "state": p_state,
                    "price": p_price,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"Published price update for {p_crop} at {p_market}!")
                st.rerun()

    # --- TAB B: PRODUCE LISTINGS ---
    with tab_listings:
        st.subheader("Active Produce Listed by Farmers for Buyers")
        listings_df = pd.DataFrame(st.session_state.produce_listings)
        st.dataframe(listings_df, use_container_width=True)

        st.markdown("---")
        st.subheader("➕ Test Listing Produce (Ops / Buyer Simulator)")
        with st.form(key="add_listing_form"):
            c1, c2, c3 = st.columns(3)
            l_crop = c1.selectbox("Crop:", ["Maize", "Rice", "Cassava", "Yam", "Vegetables"])
            l_qty = c2.text_input("Quantity:", value="15 Bags")
            l_loc = c3.text_input("Location:", value="Ede, Osun State")
            
            btn_add_l = st.form_submit_button("Submit Produce Listing", type="primary")
            if btn_add_l:
                new_id = len(st.session_state.produce_listings) + 201
                st.session_state.produce_listings.append({
                    "id": new_id,
                    "phone": st.session_state.farmer_profile["phone"],
                    "crop": l_crop,
                    "quantity": l_qty,
                    "location": l_loc,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "consent_shared": True
                })
                st.success(f"Listed {l_qty} of {l_crop}!")
                st.rerun()


# ------------------------------------------------------------------------------
# VIEW 5: PROBLEM TRACKING & ANALYTICS
# ------------------------------------------------------------------------------
elif app_mode == "📈 Problem Tracking & Analytics":
    st.title("📈 Problem Tracking & Mapped Insights")
    st.markdown("Monitors regional pest, disease, and soil problem distributions to enable targeted agricultural interventions.")

    reports_df = pd.DataFrame(st.session_state.problem_reports)

    if not reports_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Problem Distribution by Crop")
            crop_counts = reports_df["crop"].value_counts().reset_index()
            crop_counts.columns = ["Crop", "Report Count"]
            st.bar_chart(crop_counts.set_index("Crop"))

        with col2:
            st.subheader("Problem Distribution by Issue Type")
            issue_counts = reports_df["issue"].value_counts().reset_index()
            issue_counts.columns = ["Issue Type", "Report Count"]
            st.bar_chart(issue_counts.set_index("Issue Type"))

        st.markdown("---")
        st.subheader("📍 Problem Summary by State / Region")
        summary_table = reports_df.groupby(["state", "crop", "issue"]).size().reset_index(name="Incident Count")
        st.dataframe(summary_table, use_container_width=True)
    else:
        st.info("No data available yet for analytics.")
