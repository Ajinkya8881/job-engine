import json
import time
import os
import sys

# Add path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from config import RESUME_DATA

def get_driver():
    # Try Edge then Chrome
    try:
        options = EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("detach", True) 
        options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        return webdriver.Edge(options=options)
    except:
        try:
            options = ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("detach", True)
            return webdriver.Chrome(options=options)
        except Exception as e:
            print(f"Failed to initialize driver: {e}")
            return None

def auto_apply():
    driver = get_driver()
    if not driver:
        print("Could not start browser. Ensure Edge or Chrome is installed.")
        return

    print("\n🚀 JOB ASSISTANT ACTIVE!")
    print(f"Profile: {RESUME_DATA['first_name']} {RESUME_DATA['last_name']}")
    print("Navigating to dashboard...")
    
    try: driver.get("http://localhost:5000")
    except: print("Dashboard not running on localhost:5000")

    print("--- INSTRUCTIONS ---")
    print("1. Open job links from the dashboard.")
    print("2. The '⚡ CLICK TO AUTO-FILL' button will appear on job pages.")
    print("3. Click it to fill Name, Email, Phone, LinkedIn, and Resume.")
    print("--------------------")

    while True:
        try:
            handles = driver.window_handles
            for h in reversed(handles):
                try:
                    driver.switch_to.window(h)
                    # Force inject button on every visible tab
                    if driver.execute_script("return document.readyState === 'complete'"):
                        inject_omni_assistant(driver)
                except: continue
            time.sleep(2) 
        except: time.sleep(2)

def inject_omni_assistant(driver):
    js_data = json.dumps(RESUME_DATA)
    js_script = f"""
    (function() {{
        if (document.getElementById('job-assistant-ui')) return;
        
        // Detect ATS
        let ats = 'generic';
        if (window.location.href.includes('greenhouse.io')) ats = 'greenhouse';
        if (window.location.href.includes('lever.co')) ats = 'lever';
        
        const div = document.createElement('div');
        div.id = 'job-assistant-ui';
        div.style = 'position:fixed; bottom:20px; right:20px; z-index:999999; background:#2563eb; color:white; padding:15px 25px; border-radius:12px; box-shadow:0 4px 20px rgba(0,0,0,0.3); font-family:sans-serif; cursor:pointer; font-weight:bold; border:2px solid white; font-size:16px; transition: transform 0.2s;';
        div.innerHTML = '⚡ AUTO-FILL (' + ats.toUpperCase() + ')';
        div.onmouseover = () => div.style.transform = 'scale(1.05)';
        div.onmouseout = () => div.style.transform = 'scale(1)';
        
        div.onclick = function() {{
            const data = {js_data};
            const location = "Hyderabad, Telangana, India";
            
            function setVal(input, val) {{
                if (!input) return;
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                if(setter) setter.call(input, val); else input.value = val;
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                input.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            }}

            function fillForm(doc) {{
                // 1. Text Inputs
                doc.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"], textarea').forEach(inp => {{
                    let label = (inp.labels?.[0]?.innerText || inp.placeholder || inp.name || inp.id || "").toLowerCase();
                    let val = "";
                    
                    if(label.includes('first') && label.includes('name')) val = data.first_name;
                    else if(label.includes('last') && label.includes('name')) val = data.last_name;
                    else if(label.includes('full name') || label.includes('name')) val = data.first_name + " " + data.last_name;
                    else if(label.includes('email')) val = data.email;
                    else if(label.includes('phone') || label.includes('mobile')) val = data.phone;
                    else if(label.includes('linkedin')) val = data.linkedin;
                    else if(label.includes('github')) val = data.github;
                    else if(label.includes('portfolio') || label.includes('website')) val = data.portfolio;
                    else if(label.includes('city') || label.includes('location')) val = location;
                    else if(label.includes('gender')) val = data.gender;
                    
                    if(val) {{
                        setVal(inp, val);
                        inp.style.backgroundColor = '#dcfce7'; // Light green highlight
                    }}
                }});

                // 2. Selects (Gender, Race, Auth) - Basic heuristic
                doc.querySelectorAll('select').forEach(sel => {{
                    let label = (sel.labels?.[0]?.innerText || sel.name || "").toLowerCase();
                    if(label.includes('gender')) {{
                        Array.from(sel.options).forEach(opt => {{ if(opt.text.includes(data.gender)) sel.value = opt.value; }});
                    }}
                }});
            }}
            
            fillForm(document);
            // Handle iframes (common in some ATS)
            document.querySelectorAll('iframe').forEach(frame => {{
                try {{ fillForm(frame.contentDocument || frame.contentWindow.document); }} catch(e) {{}}
            }});
            
            this.innerHTML = '✅ FILLED!';
            this.style.background = '#059669';
            setTimeout(() => {{ this.innerHTML = '⚡ AUTO-FILL (' + ats.toUpperCase() + ')'; this.style.background = '#2563eb'; }}, 3000);
        }};
        document.body.appendChild(div);
    }})();
    """
    try: driver.execute_script(js_script)
    except: pass

if __name__ == "__main__":
    auto_apply()
