from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask, jsonify
from app_1 import app1
from app_2 import app2
#from app_3 import app as app3
from flask import Flask
#from nomar import app9
from app_5 import app5
from app_6 import app6
from app_7 import app7
from app_8 import app8
from clu import appc
from sameday import appsd
from main import appt
from antiguedad import appa
from traspasos import apptr
from pkt import appkt
from stock import appst

#unused base app
base_app = Flask(__name__)

app = DispatcherMiddleware(base_app, {
    '/app1': app1.server,
    '/app2':  app2.server,
    #'/dashboard':  app3.server,
    #'/nomarcaciones':app9.server,
    '/app5':app5.server,
    '/app6':app6.server,
    '/app7':app7.server,
    '/app8':app8.server,
    '/clu':appc.server,
    '/sameday':appsd.server,
    '/main':appt.server,
    '/antiguedad':appa.server,
    '/traspasos':apptr.server,
    '/pkt':appkt.server,
    '/stock':appst.server

   
   
})

