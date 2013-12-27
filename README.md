How to use this script
=============================

This Python script (Get_ArcGIS_Online_Attachments.py) allow you to download attachment from an ArcGIS Online hosted feature fervice. 

All attachments are stored in a folder and a csv file is created with the file local paths associated to key field 
from the attribute table. 

If you have exported your hosted feature service as a feature class in a Geodatabase (Personnal, File, Workgroup or Enterprise), this csv file can be used with the ArcGIS tool "Add Attachments" to include all attachements in this feature class.

Note:
=====

This script doesn't require any ArcGIS Python libraries but it can be combined to arcpy instructions to automate
workflow of importing attachments into a Geodatabase Feature Class.

This script need to have the module "Requests" installed on you machine.
You will find more details about this module here: http://docs.python-requests.org/en/latest/

