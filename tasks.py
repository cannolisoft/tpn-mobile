import logging

from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import models
import scrapemark

LIST_URL = "http://tpnmd.com/body.cfm?id=12&action=list"

class SyncHandler(webapp.RequestHandler):
    def get(self):
    #todo: maybe status on last sync?
        logging.debug('SyncHandler.get')
        self.post()

    def post(self):
        logging.debug('SyncHandler.post')
        scrape = scrapemark.scrape("""
                    {* <tr class='metalist'><td><a href='{{[details]}}'></a></td></tr> *}
                """, url=LIST_URL)

        for detailurl in scrape['details']:
            taskqueue.add(url='/tasks/item', params={'url': detailurl})

        self.redirect('/')

class ItemHandler(webapp.RequestHandler):
    def post(self):
        logging.debug('ItemHandler.post')
        url = self.request.get('url')

        detail = scrapemark.scrape("""
                        {* <tr><td><font>{{ name }}</font></td></tr>  *}
                        {* <tr><th>Specialty</th><td>{{ specialty }}</td></tr>  *}
                        {* <tr><th>Facility</th><td>{{ facility }}</td></tr>  *}
                        {* <tr><th>Address</th><td>{{ address|html }}</td></tr>  *}
                        {* <tr><th>Phone</th><td>{{ phone }}</td></tr>  *}
                        {* <tr><th>Certification</th><td>{{ certification }}</td></tr>  *}
                        {* <tr><th>Medical School</th><td>{{ school }}</td></tr>  *}
                        {* <tr><th>Residency</th><td>{{ residence }}</td></tr>  *}
                        {* <tr><th>Gender</th><td>{{ gender }}</td></tr>  *}
                        """, url=url)

        address = detail['address'].replace('<br>','\n').replace('\t','').replace('\r','').replace('\n\n','\n')
        office = models.Office.getOrCreate(detail['facility'], address, detail['phone'])

        detail['specialties'] = [i.strip() for i in detail['specialty'].split(';')]
        doc = models.Doc(**detail)
        doc.office = office
        doc.put()

logging.debug('root')
application = webapp.WSGIApplication([
                    ('/tasks/sync', SyncHandler),
                    ('/tasks/item', ItemHandler)],
                 debug=True)

def main():
        logging.debug('main')
        run_wsgi_app(application)

if __name__ == "__main__":
        main()
