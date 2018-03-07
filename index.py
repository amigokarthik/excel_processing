import redis, os
import cherrypy
from operator import itemgetter
from mako.template import Template
import datetime
from datetime import date, timedelta

r = redis.StrictRedis(host="localhost", port=6379, db=0)

# obtaining date of equity copy to display
e_date = date.today() - timedelta(1)
u_date = e_date.strftime('%y%m%d')
dd = datetime.datetime.strptime(u_date,'%y%m%d')
year = str(dd.year)[2:]
str_month = str(dd.month)
if len(str_month) < 2:
    str_month = '0' + str_month
str_day = str(dd.day)
if len(str_day) < 2:
    str_day = '0' + str_day

dd = str_day + "/" + str_month + "/" + year

class Index(object):

    # route to index page
    @cherrypy.expose
    def index(self):
        keys = r.keys('[0-9]-*')
        l1 = []
        for key in keys:
            l1.append(r.hgetall(key))
        sorted_l1 = sorted(l1, key=itemgetter('SC_CODE'))
        index = Template(filename='index.html').render(list=sorted_l1,dd = dd)
        return index

    # route to search action page
    @cherrypy.expose
    def action(self,search):
        regex = '*' + search.upper() + '*'
        keys = r.keys(regex)
        l1 = []
        for key in keys:
                l1.append(r.hgetall(key))
        sorted_l1 = sorted(l1, key=itemgetter('SC_CODE'))
        search = Template(filename='search.html').render(list=sorted_l1,dd = dd)
        return search

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 5050})
    cherrypy.quickstart(Index())
