#!/opt/tufin/securitysuite/ps/python/bin/python3
import argparse
import logging
import shlex
import sys
import urllib.request
import re

sys.path.append('/opt/tufin/securitysuite/ps/lib')

from Secure_Common.Logging.Logger import setup_loggers
from Secure_Common.Logging.Defines import COMMON_LOGGER_NAME
from Secure_Track.XML_Objects.REST import zones
from Secure_Common.REST_Functions.Config import Secure_Config_Parser
from Secure_Track.Helpers import Secure_Track_Helper


conf = Secure_Config_Parser()
logger = logging.getLogger(COMMON_LOGGER_NAME)
st_helper = Secure_Track_Helper.from_secure_config_parser(conf)

zonenname = input("Bitte gewünschten Zonennnamen eingeben: ")
print('The Zonenname ist', zonenname)

neue_zone = zones.Zone(zone_id=None, name=zonenname, comment="New API Zone")

new_zone = st_helper.post_zone(neue_zone)

print(new_zone) # output = zonen id

 # test

liste = zones.Zone_Entries_List

block_liste = ("https://lists.blocklist.de/lists/imap.txt")

for line in urllib.request.urlopen(block_liste):

    if re.search(':' , str(line)):

        pass


    else:

        new_entry = zones.Zone_Entry(item_id=1, zone_id=new_zone, ip=line.decode('utf-8').strip(), comment="API Import",
                                     netmask="255.255.255.255", _=liste)
        add_entry = st_helper.post_zone_entry(new_zone, new_entry)



print("Fertig!")