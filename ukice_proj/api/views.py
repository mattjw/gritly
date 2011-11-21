# http://127.0.0.1:8000/api/accidents_in_rect?ne=52.012788283447016,-1.8865173453125408&sw=51.95756835101524,-2.468304454687541&Weather_Conditions=1&Road_Surface_Conditions=4,1
#

# Weather Conds:
#1	Fine no high winds
#2	Raining no high winds
#3	Snowing no high winds
#4	Fine + high winds
#5	Raining + high winds
#6	Snowing + high winds
#7	Fog or mist
#8	Other
#9	Unknown
#-1	Data missing or out of range

# Road Surf Conds:
#1	Dry
#2	Wet or damp
#3	Snow
#4	Frost or ice
#5	Flood over 3cm. deep
#6	Oil or diesel
#7	Mud
#-1	Data missing or out of range

# just (snow, frost or ice) on road
# http://127.0.0.1:8000/api/accidents_in_rect?ne=52.012788283447016,-1.8865173453125408&sw=51.95756835101524,-2.468304454687541&Road_Surface_Conditions=3,4
#
# for a lot of cardiff...
# http://127.0.0.1:8000/api/accidents_in_rect?ne=52.012788283447016,-1.8865173453125408&sw=50.95756835101524,-4.468304454687541&Road_Surface_Conditions=3,4


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from django import forms
import models 
import json

from datetime import datetime 

import sqlite3

from django.conf import settings
from tweet_grabber import getTweets, getTweetsLocation


# Create your views here.

def _parse_param_as_ints_list( params, pname ):
    lst_str = params[pname]
    parts = lst_str.split(",")
    try:
        return [ int(x.strip()) for x in parts ]
    except Exception:
        return None

def accidents_in_rect( request ):
    """
    """
    
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest( "GET calls only" )
    
    params = request.GET
    
    req_params = ["ne","sw"]
    for req_param in req_params:
        if req_param not in params:
            return HttpResponseBadRequest( "missing param: %s" %(req_param) )
    
    #
    # Lat longs
    ne = params['ne']
    try:
        ne_lat,ne_long = [ float(x.strip()) for x in ne.split(',')]
    except Exception:
        return HttpResponseBadRequest( "failed to parse %s" % (ne) )
    
    sw = params['sw']
    try:
        sw_lat,sw_long = [ float(x.strip()) for x in sw.split(',')]
    except Exception:
        return HttpResponseBadRequest( "failed to parse %s" % (sw) )
    
    
    #
    # Optionals
    weather_conds = None
    pname = "Weather_Conditions"
    if pname in params:
        weather_conds = _parse_param_as_ints_list( params, pname )
        if weather_conds is None:
            return HttpResponseBadRequest( "failed to parse %s" % (pname) )
            
    road_surf_conds = None
    pname = "Road_Surface_Conditions"
    if pname in params:
        road_surf_conds = _parse_param_as_ints_list( params, pname )
        if road_surf_conds is None:
            return HttpResponseBadRequest( "failed to parse %s" % (pname) )
    
    #
    # Build query
    qry = "SELECT * FROM accidents "
    
    qry += " WHERE "
    qry += " %s <= latitude " % sw_lat
    qry += " AND "
    qry += " latitude <= %s " % ne_lat

    qry += " AND "
    qry += " %s <= longitude " % sw_long
    qry += " AND "
    qry += " longitude <= %s " % ne_long 
    #sw_lat <= p_lat <= ne_lat
    #sw_long <= p_long <= ne_long
    
    
    if weather_conds is not None:        
        lst_str = "("
        lst_str += ''.join( [ str(x)+"," for x in weather_conds] ).rstrip(',') 
        lst_str += ")"
        
        qry += " AND Weather_Conditions IN " + lst_str
        
        
    if road_surf_conds is not None:
        lst_str = "("
        lst_str += ''.join( [ str(x)+"," for x in road_surf_conds] ).rstrip(',')
        lst_str += ")"
        
        qry += " AND Road_Surface_Conditions IN " + lst_str
    
    #
    # Query and parse
    conn = sqlite3.connect(settings.PROJ_PATH+'/datasets_db.db')  #~
    conn.row_factory = sqlite3.Row
    rset = conn.execute(qry)
    results = rset.fetchall()
    dicts = [ dict(res) for res in results ]
    json_str = json.dumps(dicts)
    
    conn.close()

    return HttpResponse( json_str )
    
    
def freezetweets_national( request ):
    """
    """
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest( "GET calls only" )
        
    #
    # 
    try:
        json_str = getTweets( settings.TWITTER_HASHTAG )
        return HttpResponse( json_str )
    except Exception:
        return HttpResponseBadRequest( "Something went wrong. Blame Greenwood." )
    
    
    

def freezetweets_near( request ):
    """
    """
  
    #
    # Prelim
    if request.method != 'GET':
        return HttpResponseBadRequest( "GET calls only" )
    
    params = request.GET
    
    req_params = ["loc"]
    for req_param in req_params:
        if req_param not in params:
            return HttpResponseBadRequest( "missing param: %s" %(req_param) )
    
    #
    # Grab params
    loc = params['loc']
    try:
        llat,llong = [ float(x.strip()) for x in loc.split(',')]
    except Exception:
        return HttpResponseBadRequest( "failed to parse %s" % (loc) )
    
    #
    # 
    try:
        json_str = getTweetsLocation( settings.TWITTER_HASHTAG, llat, llong, "5mi" )
        return HttpResponse( json_str )
    except Exception:
        return HttpResponseBadRequest( "Something went wrong. Blame Greenwood." )
    
    
    
    
    
    
    
    
    
    