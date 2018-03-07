# excel_processing - cherrypy-redis-application

A application that can be used for excel processing and storing it in redis db into proper data structure.A cherrypy script that is used to fetch data from redis and render it on view.

## About

This is especially designed for people who have an understanding of Python but are new to web development in particular. It can be difficult to decide on components and frameworks so that you can get down to coding. This example uses [cherrypy](http://www.cherrypy.org/) for the webserver, [mako](http://www.makotemplates.org/) for html rendering.

## Setting up locally

Make sure you have [Python](https://www.python.org/) , [pip](https://pip.pypa.io/en/stable/installing/) and [Redis](https://redis.io/)installed.

```bash
git clone https://github.com/amigokarthik/excel_processing.git
cd excel_processing
pip install -r requirements.txt
python storage.py
python index.py
```

The webserver should now be running on http://localhost:5050. Editing cherrypy.py will cause cherrypy to reload itself.

