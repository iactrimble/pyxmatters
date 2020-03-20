# standard python modules
import logging
import urllib.parse
import json

# # local module
from .api import xMattersAPI


class xMattersLibraries(object):

    # constructor
    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger(__name__)

    def getLibraries(self, id, filter='', retry=0):

        defName = "getLibraries "

        try:
            self.log.debug(defName + "Getting Libraries for Plan: " + id)
            url = "/api/xm/1/plans/" + urllib.parse.quote(id, safe='') + "/shared-libraries" + filter

            response = self.request.get(url)

            if xMattersAPI.statusCodeSuccess(response.status_code):
                jsonStr = response.json()
                self.log.debug(defName + json.dumps(jsonStr))
                self.log.debug(defName + "Retrieved libraries" + str(response.content))
            elif response.status_code == 404:
                self.log.debug(defName + "The plan could not be found: " + id)
                jsonStr = None
            elif xMattersAPI.tooManyRequests(response.status_code):
                self.log.error(defName + "Status Code: "+str(response.status_code)+". Too many requests.")
                if retry < 3:
                    retry = retry+1
                    self.log.error(defName + "Retrying, retry count: " + str(retry))
                    return self.getPlan(id, filter, retry)
            else:
                self.log.debug(defName + "Error occurred while retrieving Plan: " + id + " Response: " + str(response.content))
                jsonStr = None
        except Exception as e:
            self.log.error(defName + "Unexpected exception:" + str(e))
            jsonStr = None

        self.log.debug(defName + "Returning response: " + str(jsonStr))

        return jsonStr
