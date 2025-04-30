import http.client
import json
import csv
def order_array_by_id(array):
    """
    Sorts an array of dictionaries by the 'id' key.
    """
    return sorted(array, key=lambda x: int(x['ID']))

def get_keler_data(top=100, skip=0):
    """
    Fetches data from the KELER website using HTTP GET request.
    """
    conn = http.client.HTTPSConnection('www.keler.hu')
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8,hu-HU;q=0.7,hu;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.keler.hu/isin/',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': 'ASP.NET_SessionId=apbbnf422pr0pxufnrtsecfp; .ASPXANONYMOUS=TDChNg_w2wEkAAAAYTRmMjY3YzctNDMwMC00NTM2LTgxZTYtNWY3NTM2Yzk4MDhiGB47FQNcTXhjcy2HiIvsHFKNA8uqeavuOKGloyS-JmQ1',
    }
    conn.request('GET', f"/isin.mvc/getitems?filterItems=&top={top}&skip={skip}", headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return json.loads(data)

if __name__ == "__main__":
    page_size = 100
    csv_headers = []
    records = []
    print("Fetching data from KELER...")
    print("Querying CSV headers...")
    data = get_keler_data(1,0)
    record_count = data['Count']
    if data and 'Nodes' in data:
        csv_headers = data['Nodes'][0].keys()
    else:
        print(data)
        print("No data found or invalid response.")
        exit(1)
    print("CSV headers fetched successfully.")
    print("Record count:", record_count)
    for i in range(0, record_count, page_size):
        print(f"Fetching records {i} to {i + page_size}...")
        data = get_keler_data(page_size, i)
        if data and 'Nodes' in data:
            for record in data['Nodes']:
                records.append(record)
                pass
        else:
            print("No data found or invalid response.")
            break
    ordered_records = order_array_by_id(records)
    csv.writer(open('isin_data.csv', 'w', newline='', encoding='utf-8')).writerow(csv_headers)
    with open('isin_data.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        for record in ordered_records:
            writer.writerow(record)
    print("Data fetching completed. Records saved to keler_data.csv.")
    print("Total records fetched:", len(ordered_records))
    print("CSV file created successfully.")
    with open("hungary_isin.json", "w", encoding="utf-8") as f:
        json.dump({
            "data": ordered_records,
            "count": len(ordered_records)
        }, f, ensure_ascii=False)
