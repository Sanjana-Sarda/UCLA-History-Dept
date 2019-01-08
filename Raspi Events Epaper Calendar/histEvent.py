from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests, sys, webbrowser, bs4

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
CAL_ID = <HEH_HIDE>

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    #Retrieve event names and dates from Hist website
    res = requests.get ('http://www.history.ucla.edu/events')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features="html5lib")
    event_names = soup.select('div[class*=events-title] a span')
    event_dates = soup.select('div[class*=events-date] span[class*=date-display-single]')
    event_time = ''
    event_time = soup.select('div[class*=events-time] span[class*=date-display-single]') 
    a = 0 
    for ev in event_names:
        ev = str(ev).replace('<span>', '').replace('</span>', '')
        event_names[a] = ev
        a = a+1
    a = 0 
    for ev in event_dates:
        ev1 = event_time[a]
        date = str(ev).split()
        month_name = (date[2])[0:3]
        month_day = date[3].replace('</span>', '')
        month_number = datetime.datetime.strptime(month_name, '%b').month
        ev = '2019-'+str(month_number)+'-'+month_day
        #event_dates[a] = ev
        #print (ev)
        time = list(filter(str.isdigit, str(ev1)))
        hr = time[0]
        if ((hr=='1')and(time[1] != '0')):
            hr = hr +time[1]
        else:
            hr = int(time[0])+12
        ev1 = str(hr)+':00:00.00'
        fin = ev+'T'+ev1
        event_dates[a]=fin
        print (fin)
        a = a+1
    

    # Call the Calendar API
    a = 0;
    for x in event_names:
        event = {
          'summary': x,
          'start': {
            'dateTime': event_dates[a],
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': event_dates[a],
            'timeZone': 'America/Los_Angeles',
          },
        }
        a = a+1
        event = service.events().insert(calendarId=CAL_ID, body=event).execute()
        print ('Event created: %s..' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
