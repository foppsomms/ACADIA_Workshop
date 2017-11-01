import Rhino as rh
import rhinoscriptsyntax as rs
import scriptcontext as sc
import json

#Reference Network Linework from Rhino
lines = rs.GetObjects(message="Select Network Lines", filter = 4)
newDict = {}

#Create Dictionary
for id in enumerate(lines):
    keys = ["speed","type"]
    newDict[("line" + str(id[0]))] = {}
    
    for i in keys:
        val = rs.GetUserText(id[1], i)
        newDict[("line" + str(id[0]))][i] = val
        
    pt = rs.CurvePoints(id[1])
    for k in enumerate(pt):
        newDict[("line" + str(id[0]))]["pt"+(str(k[0]))]= tuple(k[1])

#Write JSON
filePath = rs.OpenFileName()
with open(filePath, 'w') as file:
    json.dump(newDict, file)

