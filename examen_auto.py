import sys
from ncclient import manager
import requests
import urllib3

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration Variables ---
HOST = "sandbox-iosxe-latest-1.cisco.com"
USER = "developer"
PASS = "C1sco12345"
INTERFACE = "GigabitEthernet2"

def run_netconf():
    """
    Connects via NETCONF (port 830) and retrieves configuration for the target interface.
    """
    print(f"\n--- NETCONF: Retrieving configuration for {INTERFACE} ---")
    try:
        # Construct the XML filter for the specific interface using IETF model
        # Note: Depending on the device capabilities, this might need adjustment (e.g., to Cisco-IOS-XE-native)
        netconf_filter = f"""
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{INTERFACE}</name>
            </interface>
        </interfaces>
        """

        with manager.connect(host=HOST, port=830, username=USER, password=PASS,
                             hostkey_verify=False, look_for_keys=False, allow_agent=False) as m:

            response = m.get_config(source='running', filter=netconf_filter)
            print("NETCONF Response (XML):")
            print(response.xml)

    except Exception as e:
        print(f"NETCONF Error: {e}")

def run_restconf():
    """
    Connects via RESTCONF (port 443) and updates the interface description.
    """
    print(f"\n--- RESTCONF: Updating description for {INTERFACE} ---")

    url = f"https://{HOST}/restconf/data/ietf-interfaces:interfaces/interface={INTERFACE}"

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }

    payload = {
        "ietf-interfaces:interface": {
            "name": INTERFACE,
            "description": "ENLACE_CRITICO_EXAMEN_AUTO"
        }
    }

    try:
        # Using PATCH to update only the description
        response = requests.patch(url, auth=(USER, PASS), json=payload, headers=headers, verify=False, timeout=10)

        print(f"HTTP Status Code: {response.status_code}")

        if response.status_code in [200, 204]:
            print("Success: Interface description updated.")
        else:
            print(f"Failed to update. Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"RESTCONF HTTP Error: {e}")
    except Exception as e:
        print(f"RESTCONF Error: {e}")

if __name__ == "__main__":
    print(f"Targeting Host: {HOST}")
    run_netconf()
    run_restconf()
