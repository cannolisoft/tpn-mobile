import logging
import os

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import models

class OfficesHandler(webapp.RequestHandler):

    def getOffice(self, officeid):
        office = models.Office.get_by_id(int(officeid))

        template_values = {
            'office': office
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/office.html')
        self.response.out.write(template.render(path, template_values))

    def getOffices(self):
        offices = memcache.get('offices')
        if not offices:
            offices_query = models.Office.all().order('name')
            offices = offices_query.fetch(100)
            memcache.add('offices', offices)
        else:
            logging.info('cache hit offices')

        template_values = {
            'offices': offices
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/offices.html')
        self.response.out.write(template.render(path, template_values))


    def get(self, officeid):
        if officeid:
            return self.getOffice(officeid)
        else:
            return self.getOffices()


class DocHandler(webapp.RequestHandler):
    def getDoc(self, docid):
        doc = models.Doc.get_by_id(int(docid))

        template_values = {
            'doc': doc
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/doc.html')
        self.response.out.write(template.render(path, template_values))


    def getDocs(self):
        docs = memcache.get('docs')
        if not docs:
            docs_query = models.Doc.all().order('name')
            docs = docs_query.fetch(100)
            memcache.add('docs', docs)
        else:
            logging.info('cache hit docs')

        template_values = {
            'docs': docs
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/docs.html')
        self.response.out.write(template.render(path, template_values))

    def get(self, docid):
        if docid:
            return self.getDoc(docid)
        else:
            return self.getDocs()


application = webapp.WSGIApplication(
                [
                    ('/office/(.*)', OfficesHandler),
                    ('/physician/(.*)', DocHandler)
                ],
                 debug=True)

def main():
        run_wsgi_app(application)

if __name__ == "__main__":
        main()
