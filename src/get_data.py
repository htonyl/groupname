import os, requests, time, json

HKSTP_SCMP_KEY = os.environ['HKSTP_SCMP_KEY']
URL = 'https://datastudio-api.hkstp.org:443/scmparticlessample/v1.0/datastore_search?resource_id=0e27027d-ef86-4d03-ba99-3bb0fafec3f9'

fname = 'data/scmp2017_data.json'
def request_data():
    headers = {
            'Authorization': 'Bearer ' + HKSTP_SCMP_KEY, 
            'Accept': 'application/json'
            }
    
    res = requests.get(URL, headers=headers, verify=False)
    data = res.json()
    
    results = data['result']['records']
    offset = 0
    while data['result']['_links']['next']:
        offset = len(results)
        
        print('Fetched {} records...'.format(offset))
        res = requests.get(URL + '&offset='+str(offset), headers=headers, verify=False)
        if res.status_code == 429:
            print('Status_code=429: sleep for 5 sec')
            time.sleep(5)
            continue
    
        data = res.json()
        records = data['result']['records']
        if len(records) == 0:
            print('Fetch done! Total: {} records.'.format(len(records)))
        results += records
    
    with open(fname, 'w', encoding='utf8') as fp:
        print('Dumping data to {}...'.format(fname))
#        json.dump({'results': results}, fp)
    
    return results

def read_data():
    with open(fname, 'r') as fp:
        data = json.load(fp)
    return data['results']

if not os.path.isfile(fname):
    print('Requesting data from HKSTP datastudio')
    results = request_data()
else:
    print('Reading data from {}'.format(fname))
    results = read_data() 

