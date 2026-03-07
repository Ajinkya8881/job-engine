import requests
import re
from config import GREENHOUSE_COMPANIES_FILE, LEVER_COMPANIES_FILE, YC_COMPANIES_FILE

def discover_greenhouse_companies():
    # Adding even MORE Indian tech hubs
    known_companies = [
        "airbnb", "twitch", "stripe", "uber", "doordash", "dropbox", "instacart",
        "robinhood", "coinbase", "affirm", "block", "pinterest", "reddit",
        "gitlab", "hashicorp", "datadog", "confluent", "twilio", "okta", "plaid",
        "zomato", "swiggy", "razorpay", "cred", "meesho", "ola", "unacademy", 
        "dream11", "urbancompany", "lenskart", "nykaa", "zepto", "upstox", "myntra",
        "flipkart", "blinkit", "yatra", "makemytrip", "tata1mg", "healthians",
        "swiggy", "dunzo", "gojek", "paytm", "phonepe", "zestmoney", "bharatpe",
        "fampay", "jupiter", "fi", "niyo", "onecard", "jar", "slice", "uni"
    ]
    
    current = set()
    try:
        with open(GREENHOUSE_COMPANIES_FILE, 'r') as f:
            current = set(f.read().splitlines())
    except: pass
    for c in known_companies: current.add(c)
    with open(GREENHOUSE_COMPANIES_FILE, 'w') as f:
        for c in sorted(current): f.write(c + "\n")

def discover_lever_companies():
    known_companies = [
        "netflix", "atlassian", "shipt", "udemy", "coursehero", "palantir",
        "figma", "notion", "airtable", "webflow", "benchling", "bolt",
        "postman", "khatabook", "groww", "paytm", "phonepe", "games24x7",
        "bigbasket", "curefit", "mpl", "simpl", "spinny", "slice", "jupiter",
        "jar", "coinswitch", "wazirx", "urbanic", "mobiqwik", "freecharge"
    ]
    current = set()
    try:
        with open(LEVER_COMPANIES_FILE, 'r') as f:
            current = set(f.read().splitlines())
    except: pass
    for c in known_companies: current.add(c)
    with open(LEVER_COMPANIES_FILE, 'w') as f:
        for c in sorted(current): f.write(c + "\n")

def discover_yc_companies():
    yc_companies = [
        "brex", "faire", "deel", "ramp", "gitlab", "coinbase", "stripe", "airbnb",
        "doordash", "instacart", "cruise", "pagerduty", "dropbox", "razorpay", 
        "meesho", "clevertap", "fampay", "orangehealth", "vahan", "atlys", "magicpin"
    ]
    current = set()
    try:
        with open(YC_COMPANIES_FILE, 'r') as f:
            current = set(f.read().splitlines())
    except: pass
    for c in yc_companies: current.add(c)
    with open(YC_COMPANIES_FILE, 'w') as f:
        for c in sorted(current): f.write(c + "\n")

def run_discovery():
    print("Massive Indian Ecosystem Expansion...")
    discover_greenhouse_companies()
    discover_lever_companies()
    discover_yc_companies()
    print("Expansion complete.")
