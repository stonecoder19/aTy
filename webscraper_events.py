import requests
from bs4 import BeautifulSoup


class WebScraper():

    def __init__(self):
    	pass

    def parse_events(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        event_titles = soup.find_all(
            'div', class_='views-field views-field-title')
        event_dates = soup.find_all(
            'div', class_='views-field views-field-field-event-datetime')
        event_summaries = soup.find_all(
            'div', class_='views-field views-field-body')

        titles = []
        dates = []
        summaries = []

        for event in event_titles:
            span = list(event.children)[1]
            a = list(span.children)[0]
            text = a.text
            titles.append(text)

        for event_date in event_dates:
            div = list(event_date.children)[1]
            span = list(div.children)[0]
            date_span = list(span.children)[0]
            try:
                dates.append(date_span.text)
            except AttributeError:
                dates.append(date_span)

        for summary in event_summaries:
            span = list(summary.children)[1]
            try:
                summaries.append(str(list(span.children)[0].text))
            except AttributeError:
                summaries.append(str(list(span.children)[0]))

        events = []
        for i in range(0, len(summaries)):
            event = Event(titles[i], dates[i], summaries[i])
            events.append(event)

        return events


class Event:

    def __init__(self, title, date, summary):
        self.title = title
        self.date = date
        self.summary = summary

    def print_event(self):
        return "Title: " + str(self.title) + " Date: " + \
            str(self.date) + " Summary: " + str(self.summary)


if __name__ == "__main__":
   
    web_scrapper = WebScraper()
    events = web_scrapper.parse_events("http://pripsjamaica.com/events/list/8/parties")
    print(events)
