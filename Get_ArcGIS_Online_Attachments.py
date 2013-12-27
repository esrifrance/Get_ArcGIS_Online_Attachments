#-------------------------------------------------------------------------------
# Name:
# Purpose:     This script downloads attachment files of an ArcGIS hosted Feature
#   		   Service and lists these files in a csv file with a key field so that
#              you can use the "Add Attachment" Tool in ArcGIS Desktop.
#
# Authors:      Christophe Tourret - Gaëtan Lavenu
#
# Created:     26/12/2013
# Copyright:   (c) Esri France - 2013
# Licence:     This script is free, it can be used and modified at your convenience
# Comments:    This script uses the "Requests" Python library, check yau installed
#              on you machine befor executing the script.
#              More info here: http://docs.python-requests.org/en/latest/user/install/
#-------------------------------------------------------------------------------

import requests, os, sys

# ArcGIS Online url to get token
agol_url = 'https://www.arcgis.com/sharing/rest/generateToken'

# Your ArcGIS Online account username
agol_user = 'xxxx'

# Your ArcGIS Online account password
agol_password = 'xxxx'

# The Feature Service ypu want to download attachements from
service = 'http://services2.arcgis.com/xxxxxxxx/arcgis/rest/services/xxxxx/FeatureServer/0'

# A field contaning unique values that will be use to join attachements to features
field_name = "ObjectId"

# Path to the folder where the script will export the attachment files.
# This folder must already exists
outDir = r"C:\AGOL_Attachments\Attachment_Files"

# The name of the CSV file to export
outFicName = "Attachments" + ".csv"

field_name = field_name.upper()
out_csv_file = os.path.join(outDir,outFicName)



params = {'username': agol_user,'password': agol_password, 'f': 'pjson', 'client': 'referer','referer':'arcgis.com'}
token_reponse = requests.post(agol_url,data=params)
token = token_reponse.json()['token']


params = {'f': 'json','token': token}
headers = {'referer': 'www.arcgis.com'}
query_reponse = requests.get(service,data=params,headers=headers)



if not query_reponse.json()['hasAttachments']:
    print "This Feature Service doesn't contain any attachment - Aborded"
    quit()



for field in query_reponse.json()['fields']:
    if field['name'].upper() == field_name:
        break
    else:
        print 'Can\'t find the field ' + field_name + ' - Aborded'
        quit()



objectIDField = query_reponse.json()['objectIdField']

query_url = service + '/query'
params = {'where': '1=1','outfields': field_name+','+objectIDField,'f': 'json','token': token}
headers = {'referer': 'www.arcgis.com'}

print "Querying the Feature Service..."

features = requests.get(query_url,data=params,headers=headers).json()['features']

nbAtt = 0
nbFeat = 0


listeAtt = open(out_csv_file, "w")
listeAtt.write(field_name + "," + "File_Path")


for feature in features:

    query_url = service + '/' + str(feature['attributes'][objectIDField]) + '/attachments'
    params = {'f': 'json','token': token}
    headers = {'referer': 'www.arcgis.com'}
    attachments = requests.get(query_url,data=params,headers=headers).json()['attachmentInfos']

    if len(attachments) > 0:
        nbFeat = nbFeat + 1



    for attachment in attachments:

        nbAtt = nbAtt + 1
        print "    Exporting attachment " + str(attachment['id']) + "  of feature " + str(feature['attributes'][field_name])
        query_url = service + '/' + str(feature['attributes'][objectIDField]) + '/attachments/' + str(attachment['id'])
        params = {'token': token}
        headers = {'referer': 'www.arcgis.com'}

        FileContent = requests.get(query_url,data=params,headers=headers).content
        FilePath = os.path.join(outDir,str(attachment['parentID'])+'_'+str(attachment['id'])+attachment['name'])
        ExportFile = open(FilePath, "wb")
        ExportFile.write(FileContent)
        ExportFile.close()

        listeAtt.write(str(feature['attributes'][field_name]) + "," + FilePath + os.linesep)

        print "        Writing file " + str(attachment['parentID'])+'_'+str(attachment['id'])+'_'+attachment['name']


listeAtt.close()

print "Export succeded for " + str(nbAtt) + " attachments of " + str(nbFeat) + " features"

