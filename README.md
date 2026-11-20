# Agrobuild-mvp
**Agrobuild** — An offline USSD ; SMS agricultural platform connecting rural smallholder farmers in Nigeria to expert advice, live market prices, and direct buyers without internet dependency. Submitted for the USPF Changemaker Challenge 2026.
# 🌾 Agrobuild — Mobile Agricultural Platform for Rural Farmers

&gt; **USPF Changemaker Challenge 2026 Entry**  
&gt; *Connecting rural smallholder farmers in Nigeria to agricultural experts, live market prices, and direct produce buyers using basic mobile phones (USSD &amp; SMS) without internet dependency.*

---

## 📌 Project Overview

**Agrobuild** is an offline-first agricultural connectivity platform designed to empower rural smallholder farmers in Nigeria who lack smartphones or internet access. By leveraging standard feature phone communication protocols—primarily **USSD (`*XXX#`)** and **SMS commands**—Agrobuild delivers three vital services directly to the farm gate:

1. **Expert Advisory:** Instant reporting of crop pests, diseases, and soil issues to agricultural specialists via a centralized advisory engine.
2. **Commodity Price Transparency:** Access to daily market price benchmarks across local and regional markets.
3. **Direct Buyer Marketplace:** Simple produce listing to connect smallholder producers directly with commercial off-takers and buyers.

The project is currently preparing for an initial pilot rollout targeting **100 smallholder farmers in Osun State, Nigeria**, operating under strict compliance with the **Nigeria Data Protection Act (NDPA 2023)**.

---

## 🚀 Interactive MVP Prototype

This repository contains an interactive **Streamlit Minimum Viable Product (MVP)** that simulates the complete Agrobuild ecosystem end-to-end:

* **`app-v2.py` (Recommended)**: Ultra-modern, high-impact demonstration UI featuring an OLED USSD smartphone simulator with clickable keypad, 1-click test preset triggers, SMS chat gateway, and an integrated Expert Operations &amp; Analytics Portal.
* **`app.py`**: Clean, functional baseline prototype implementation.

### Key Features Implemented

* **📟 USSD Channel Simulator (`*XXX#`)**: Multi-step menu system supporting:  
  * `1. Report farm problem` (Crop -&gt; Issue selection -&gt; Expert queuing)
  * `2. Market prices` (Local commodity price lookups)
  * `3. Sell my produce` (Quantity &amp; location collection for buyer matching)
  * `4. Farming tips` (Agronomic advice by crop)
  * `5. Language` (Language preference selection)
  * `0. Back / Main Menu` navigation and session resets.
* **💬 SMS Command Gateway**: Parsing engine for SMS text commands:  
  * `PROBLEM
