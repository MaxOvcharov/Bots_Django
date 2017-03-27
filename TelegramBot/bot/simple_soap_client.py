# -*- coding: utf-8 -*-

from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.signature import Signature

from TelegramBot.settings import KEY_FILENAME, CERT_FILENAME

session = Session()
session.verify = False
transport = Transport(session=session)
r = session.get('https://37.230.149.6:10004/emias-soap-service/PGUServicesInfo2?wsdl',
                cert=(CERT_FILENAME, KEY_FILENAME))
client = Client('https://37.230.149.6:10004/emias-soap-service/PGUServicesInfo2?wsdl',
                wsse=Signature(KEY_FILENAME, CERT_FILENAME), transport=transport)

#client.wsdl.dump()
print "#######"*12

http_get = client.bind('PGUServicesInfoV1ImplService', 'PGUServicesV1ImplPort')
print http_get.getAllLpusInfo(returnBranches=True, externalSystemId='MPGU')

