import requests


def fetch_ticketmaster_events(api_key, keyword):
    """Fetch raw concert events from the Ticketmaster Discovery API for a given artist keyword."""

    payload = {'keyword': keyword,'size': '10', 'apikey': api_key}
    r = requests.get("https://app.ticketmaster.com/discovery/v2/events.json", params=payload, timeout= 10)

    if (r.status_code == 200):
        data= r.json()

        # Ticketmaster omits the '_embedded' key completely when 0 events are found
        if ("_embedded" in data.keys()):

            events=data.get("_embedded").get("events")
            return events
        
        else:
            print(f"NO EVENTS {keyword}")
            return []

    else:
        print(f"CALL ERROR CODE | {r.status_code}")
        return []

def transform_events(events):
    """Transform raw Ticketmaster event objects into a list of clean dictionaries.
    Keys per dictionary: 'event_id', 'name', 'city', 'sales_start_datetime', 'date', 'url'.
    """
    cleaned_events= []

    for event in events:
        event_id= event.get('id')
        name= event.get('name')

        # Venues is a nested list inside '_embedded'; safely check it is non-empty before indexing [0]
        venues=(event.get('_embedded') or  {}).get('venues') or []
        if venues != []:
            city= (venues[0].get('city', {}) or {}).get('name')
        else:
            city= None

        sales_start_datetime= ((event.get('sales') or {}).get('public') or {}).get('startDateTime')
        date= ((event.get('dates') or {}).get('start') or {}).get('localDate')
        url= event.get('url')

        cleaned_event= {'event_id': event_id, 'name': name, 'city': city, 'sales_start_datetime': sales_start_datetime, 'date':date, 'url':url}

        cleaned_events.append(cleaned_event)

    return cleaned_events