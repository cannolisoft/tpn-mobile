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
        offices_html = memcache.get('offices html')
        if not offices_html:
            offices = models.Office.all().order('name')
            template_values = {
                'offices': offices
            }

            path = os.path.join(os.path.dirname(__file__), 'templates/offices.html')
            offices_html = template.render(path, template_values)

            memcache.add('offices html', offices_html)

        self.response.out.write(offices_html)


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
        docs_html = memcache.get('docs html')
        if not docs_html:
            docs = models.Doc.all().order('name')
            template_values = {
                'docs': docs
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/docs.html')
            docs_html = template.render(path, template_values)

            memcache.add('docs html', docs_html)

        self.response.out.write(docs_html)

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
