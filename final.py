import requests
import helper

def get_asset_ids(domain_id):
    """"
    This function returns a list of asset ids for a given domain id 
        Parameters:
            domain_id (str): Domain ID from Collibra    
        Returns:
            ids (list): List of asset IDs from the domain
    """""
    url = config['specifications']['url'] + 'assets'

    headers = {
        "Accept": config['user']['accept'],
        "Authorization": config['user']['authorization']
    }

    querystring = {
        "domainId": domain_id,
        "typeIds": config['specifications']['asset_type_ids']
    }

    response = requests.get(url, headers=headers, params=querystring)

    ids = []
    for i in range(len(response.json()['results'])):
        ids.append(response.json()['results'][i]['id'])

    return ids

def get_names(ids):
    """"
        This function returns a list of attributes ("Actual Asset Name")
        from a list of asset IDs
            Parameters:
                ids (list): List of asset IDs    
            Returns:
                attributes (list): List of asset names 
    """""
    attributes = []
    for j in range(len(ids)):
        url = "https://uclahealth-dev.collibra.com/rest/2.0/attributes"
        querystring = {
            "assetId": ids[j],
            "typeIds": ["fdd5c0f3-9357-4706-9d87-03885153e68a",
                        ]
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic SGFubmFoQVBJOlVudDBsZCEhQ2hhbmNl"
        }
        response2 = requests.get(url, headers=headers, params=querystring)
        # Create a list of DM asset names
        attributes.append(response2.json())
    return attributes

def get_logic(ids):
    """"
        This function returns a list of the transformation logic code from the 
        Clinical Data Mart assets
            Parameters:
                ids (list): List of asset IDs    
            Returns:
                attributes (list): List of transformation logic
    """""
    attributes = []
    for j in range(len(ids)):
        url = "https://uclahealth-dev.collibra.com/rest/2.0/attributes"
        querystring = {
            "assetId": ids[j],
            "typeIds": ["00000000-0000-0000-0000-000000000249"
                        ]
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Basic SGFubmFoQVBJOlVudDBsZCEhQ2hhbmNl"
        }
        response2 = requests.get(url, headers=headers, params=querystring)
        # Create a list of transformation logic
        attributes.append(response2.json())
    return attributes

def post_logic():
    """"
        This function uses the POST function to update the transformation logic
        of the Discovery assets with code from the Clinical Data Mart assets if 
        the names of the assets match (ie. when the Discovery asset is missing
        the transformation logic)
    """""
    # Getting asset IDs for the Clinical Data Mart and Discovery domains
    clinical_assets = get_asset_ids("7f0c695e-8577-433d-a3a5-753456ed71ca")
    discovery_assets = get_asset_ids("4710521c-32c0-429f-acad-c180866955a7")

    # Getting asset names and transformation logic from the Clinical Data Mart domain
    # and the asset names from the Discovery Data Mart for comparison
    clinical_names = get_names(clinical_assets)
    trans_logic = get_logic(clinical_assets)
    discovery_names = get_names(discovery_assets)

    for k in range(len(clinical_names)):
        for q in range(len(discovery_names)):
            # Checking that the current asset is not empty
            if clinical_names[k]['total'] != 0:
                # Checking that the two asset names are the same
                if clinical_names[k]['results'][0]['value'].lower() == discovery_names[q]['results'][0]['value'].lower():
                    url = "https://uclahealth-dev.collibra.com/rest/2.0/attributes"

                    headers = {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": "Basic SGFubmFoQVBJOlVudDBsZCEhQ2hhbmNl"
                     }

                    payload = {
                        # posting to the DISCOVERY asset
                        "assetId": discovery_assets[q],
                        "typeId": "00000000-0000-0000-0000-000000000249",
                        "value": trans_logic[k]['results'][0]['value']
                    }

                    response4 = requests.post(url, json=payload, headers=headers)
                    print(response4.status_code)
                    print(response4.json()['results'][0]['value'] + '' + clinical_names[q])



