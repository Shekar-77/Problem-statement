import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

def api_web_call(url,**kwargs):
    BRIGHT_API_KEY=os.getenv("BRIGHT_API_KEY")
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {BRIGHT_API_KEY}',
    }

    try:
        response=requests.post(url,headers=headers,**kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed:{e}")
        return None
    except Exception as e:
        print(f"Unkown error occured:{e}")
        return None

def serp_search(question,model="google"):
    if model=="google":
        base_url="https://www.google.com/search"
    elif model=="bing":
        base_url="https://www.bing.com/search"
    else:
        raise ValueError(f"Unkown engine:{model}")
    payload={
        "zone":"serp_api1",
        "url":f"{base_url}?q={quote_plus(question)}&brd_json=1",
        "format":"raw"
    }
    url='https://api.brightdata.com/request'
    full_response=api_web_call(url,json=payload)
    if not full_response:
        return None
    
    extracted_data={
        "knowledge":full_response.get("knowledge",{}), #Knowledge supports dictionary
        "organic":full_response.get("organic",[])   #Organic supports list
    } 
    return extracted_data
