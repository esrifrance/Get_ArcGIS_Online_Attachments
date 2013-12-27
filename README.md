About this script:
==================

This Python script (Get_ArcGIS_Online_Attachments.py) allow you to download attachments from an ArcGIS Online hosted feature fervice. Then these attachments could be easily associated to a feature class of your Geodatabase.

How to use:
===========

You will need to provide your ArcGIS Online account information, the url of the feature service containing attachments   and a key field. All attachments are stored in a folder and a csv file is created with the file local paths associated to key field from the attribute table. 

If you have exported your hosted feature service as a feature class in a Geodatabase (Personnal, File, Workgroup or Enterprise), this csv file can be used with the ArcGIS tool "Add Attachments" to include all attachements in this feature class.

Notes:
=====

This script doesn't require any ArcGIS Python libraries but it can be combined to arcpy instructions to automate
workflow of importing attachments into a Geodatabase Feature Class.

This script need to have the module "Requests" installed on you machine.
You will find more details about this module here: http://docs.python-requests.org/en/latest/



