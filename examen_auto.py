import requests
from ncclient import manager
import urllib3
import json
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


HOST = 'devnetsandboxiosxec8k.cisco.com'
USER = 'christian.hermoza.t'
PASS = 'NW-m2RqeL1_9'
INTERFACE = 'GigabitEthernet2'
NETCONF_PORT = 830
RESTCONF_PORT = 443

def audit_netconf():

    netconf_filter = f"""
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>{INTERFACE}</name>
        </interface>
      </interfaces>
    """

    try:

        with manager.connect(
            host=HOST,
            port=NETCONF_PORT,
            username=USER,
            password=PASS,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
   
            response = m.get_config(source='running', filter=('subtree', netconf_filter))
            print("conexion lograda")
            print("xml logrado")
            print(response.data_xml)
            
    except Exception as e:
        print(f"error {e}")

def configure_restconf():


    url = f"https://{HOST}:{RESTCONF_PORT}/restconf/data/ietf-interfaces:interfaces/interface={INTERFACE}"


    headers = {
        'Content-Type': 'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }

    payload = {
        "ietf-interfaces:interface": {
            "name": INTERFACE,
            "description": "ENLACE_CRITICO_EXAMEN_AUTO",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": True
        }
    }

    try:
        response = requests.patch(
            url,
            auth=(USER, PASS),
            headers=headers,
            data=json.dumps(payload),
            verify=False,
            timeout=30
        )
        
        print(f" Código de estado HTTP: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print("correcto")
        else:
            print(f"fallo: {response.text}")
            response.raise_for_status() 

    except requests.exceptions.RequestException as e:
        print(f"error conexion: {e}")
    except Exception as e:
        print(f"erro inesperado: {e}")

if __name__ == "__main__":
    audit_netconf()
    configure_restconf()
