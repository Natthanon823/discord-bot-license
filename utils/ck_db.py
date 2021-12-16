import pymongo
import json
import datetime
import config


_dbHost = pymongo.MongoClient("mongodb://localhost:27017/")
_dbName = _dbHost[config._databaseName]


def _addLicense(_guildID, get_license, get_licenseTIME, get_roleID, get_addid):
    _ck = _dbName[_guildID]
    _ck.insert_one({
        "license": get_license,
        "addID": get_addid,
        "roleID": get_roleID,
        "licenseTIME": get_licenseTIME,
        "redeemID": None,
        "redeemTIME": None,
        "reedemTIMEst": None,
        "expireTIME": None,
        "expireTIMEst": None,
        "isUse": False,
        "isTime": False}
    )


def _removeLicense(_guildID, get_license):
    _ck = _dbName[_guildID]
    _ckT1 = _ck.find({ "license": get_license })
    try:
        if _ckT1[0]["isUse"] == True:
            return "THIS KEY HAS BEEN USED CAN'T DELETE"
        _ck.delete_one(_ckT1[0])
        return "SUCCESS"
    except:
        return "INVAILD LICENSE"


def _redeemLicense(_guildID, get_license, get_redeemid):
    _ck = _dbName[_guildID]
    _ckT1 = _ck.find({ "license": get_license })
    try:
        if _ckT1[0]["isUse"] == True:
            return "USED",
    except:
        return "INVAILD",
    a = datetime.datetime.now() + datetime.timedelta(hours= int(_ckT1[0]["licenseTIME"]))
    _ck.update_one({
        "license": get_license},
            { "$set": {
        "redeemID": get_redeemid,
        "redeemTIME": str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        "reedemTIMEst": str(datetime.datetime.timestamp(datetime.datetime.now())),
        "expireTIME": str(a.strftime("%d/%m/%Y %H:%M:%S")),
        "expireTIMEst": str(datetime.datetime.timestamp(a)),
        "isUse": True,
        "isTime": True}
        }   
    )
    return "SUCCESS", _ckT1[0]["licenseTIME"], _ckT1[0]["roleID"]



def _checkLicenseActive(_guildID):
    _ck = _dbName[_guildID]
    _ckT1 = _ck.find({ "isTime": True})
    for i in _ckT1:
        if datetime.datetime.now().timestamp() > float(i["expireTIMEst"]):
            _ck.update_one(i, { "$set": { "isTime": False}})
            return str("EXPIRE"), _guildID, i["redeemID"], i["roleID"], i["license"]
        else:
            return "NONE", 
    return "NONE",