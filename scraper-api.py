import httpx
from pprint import pprint

api_ROOT ='https://keler.hu/OData.svc/'
# https://www.keler.hu/OData.svc/Root/KelerData/ISIN/items/HU999999?
def fetch_isin_groups():
    r = httpx.get(api_ROOT + '/Root/KelerData/ISIN/items?$select=ISINData', follow_redirects=True)
    if r.status_code == 200:
        data = r.json()
        isin_urls = [ x['__metadata']['uri'] for x in data.get('d', {}).get('results', [])]
        return isin_urls
    else:
        print(f"Error fetching ISIN groups: {r.status_code}")
        return []
    
if __name__ == "__main__":
    isin_groups = fetch_isin_groups()
    if isin_groups:
        pprint(isin_groups)
    else:
        print("No ISIN groups found or an error occurred.")