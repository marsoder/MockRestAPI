
import requests 

def app_is_running():
    try:
        r = requests.get("http://localhost:5000")
        return True
    except requests.exceptions.ConnectionError:
        return False
        
        
