# Author: Juan Jiménez, flybd5@gmail.com
# Copyright 2020 by Juan Jiménez
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Sample Python code to illustrate seeding Python's random number generator
# with the datasum of the latest image of the sun from one of sources 8-17 on the
# Helioviewer API (SDO AIA instrument sources).

import requests, json, random
import xml.etree.ElementTree as ET
from datetime import datetime

# Init image checksum value to default of zero
datasum = 0
# Generate a pseudorandom image source from 8 to 17 for AIA images
theSource = random.randint(8,17)
print("Using source: "+str(theSource))
# convert now to date/time string in Zulu time
dtnow = datetime.utcnow()
datetimestring = dtnow.strftime("%Y-%m-%dT%H:%M:%SZ")
# create HTTP response object url to the Helioviewer API to get latest image
resp = requests.get('https://api.helioviewer.org/v2/getClosestImage/?date='+datetimestring+'&sourceId='+str(theSource))
if resp.status_code != 200:
    print("Unable to connect to Helioviewer API.")
else:
    # parse the returned json and get the id
    resp_dict = json.loads(resp.text)
    id = resp_dict["id"]
    if id is None:
        print("Image not found.")
    else:
        print("Requesting FITS data for image ID: "+str(id))
        # create HTTP response object for json FITS data of latest image
        resp = requests.get('https://api.helioviewer.org/v2/getJP2Header/?id='+str(id))
        if resp.status_code != 200:
            print("Unable to get FITS JSON data for image id:"+id+" from Helioviewer API.")
        else:
            # create element tree object
            tree = ET.fromstring(resp.text)
            # go find the datasum
            datasum = tree.findtext('.//DATASUM')
            if datasum is None:
                print("Image has no datasum attribute, or attribute empty.")
                datasum = 0
            else:
                print("The image datasum is: "+str(datasum))

# seed the random number generator with timestamp + datasum
# and print some random numbers. if no image checksum was found
# always default to the current timestamp
theStamp = datetime.utcnow().timestamp()
theSeed = int(theStamp) + int(datasum)
print("Calculated seed: "+str(theSeed))
random.seed(theSeed)
print("10 sample random numbers...")
for i in range(0,10):
    print(i+1,random.randint(0,100000000),sep='\t')
