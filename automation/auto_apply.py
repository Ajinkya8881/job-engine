import json
import time
import os
import sys

# Add path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from config import JOBS_DB_FILE, RESUME_DATA

def auto_apply():
    options = EdgeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True) 
    options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    
    try:
        driver = webdriver.Edge(options=options)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("\n🚀 TOTAL-ASSIST ACTIVE!")
    print("1. Filling Location: Hyderabad, Telangana.")
    print("2. Watching all tabs for the GREEN BUTTON.")
    print("------------------------------------------------------------")

    try: driver.get("http://localhost:5000")
    except: driver.get("https://www.google.com")

    while True:
        try:
            handles = driver.window_handles
            for h in reversed(handles):
                try:
                    driver.switch_to.window(h)
                    # Force inject button on every visible tab
                    if driver.execute_script("return document.visibilityState === 'visible'"):
                        inject_omni_assistant(driver)
                        
                        # Resume Auto-Attach (Aggressive)
                        file_inps = driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                        for f in file_inps:
                            if not f.get_attribute("value"):
                                driver.execute_script("arguments[0].style.display = 'block'; arguments[0].style.visibility = 'visible';", f)
                                f.send_keys(RESUME_DATA["resume_path"])
                                break
                        break # Done with active tab
                except: continue
            time.sleep(2) 
        except: time.sleep(2)

def inject_omni_assistant(driver):
    js_data = json.dumps(RESUME_DATA)
    js_script = f"""
    (function() {{
        if (document.getElementById('job-assistant-ui')) return;
        const div = document.createElement('div');
        div.id = 'job-assistant-ui';
        div.style = 'position:fixed; top:10px; left:50%; transform:translateX(-50%); z-index:999999; background:#10b981; color:white; padding:12px 30px; border-radius:50px; box-shadow:0 10px 25px rgba(0,0,0,0.4); font-family:sans-serif; cursor:pointer; font-weight:bold; border:3px solid white; font-size:18px;';
        div.innerHTML = '⚡ CLICK TO AUTO-FILL BASICS';
        div.onclick = function() {{
            const data = {js_data};
            const location = "Hyderabad, Telangana, India";
            
            function fillForm(doc) {{
                doc.querySelectorAll('input, textarea').forEach(inp => {{
                    let label = (inp.labels?.[0]?.innerText || inp.placeholder || inp.name || inp.id || "").toLowerCase();
                    let val = "";
                    if(label.includes('first name')) val = data.first_name;
                    else if(label.includes('last name')) val = data.last_name;
                    else if(label.includes('email')) val = data.email;
                    else if(label.includes('phone') || label.includes('mobile')) val = data.phone;
                    else if(label.includes('linkedin')) val = data.linkedin;
                    else if(label.includes('github')) val = data.github;
                    else if(label.includes('city') || label.includes('location') || label.includes('address')) val = location;
                    else if(label.includes('name') && !val) val = data.first_name + " " + data.last_name;

                    if(val && inp.type !== 'file') {{
                        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        if(setter) setter.call(inp, val); else inp.value = val;
                        inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }});
            }}
            fillForm(document);
            document.querySelectorAll('iframe').forEach(frame => {{
                try {{ fillForm(frame.contentDocument || frame.contentWindow.document); }} catch(e) {{}}
            }});
            this.innerHTML = '✅ BASICS FILLED!';
            this.style.background = '#059669';
            setTimeout(() => {{ this.innerHTML = '⚡ CLICK TO AUTO-FILL BASICS'; this.style.background = '#10b981'; }}, 2000);
        }};
        document.body.appendChild(div);
    }})();
    """
    try: driver.execute_script(js_script)
    except: pass

if __name__ == "__main__":
    auto_apply()
