import sys
sys.path.append('../')
from helper.helper import LibMS

dbname = "LibMS"

@LibMS
def addData(cursor):
    # TODO: add data in database