__author__ = 'David'
from xml.dom.minidom import parse
import xml.dom.minidom
from xml.etree.ElementTree import ElementTree as ET
from geopy.distance import vincenty as vincent
class Search_Query:
    def __init__(self,product_node,radius,price_range,output_length):
        self.product_node = product_node
        self.radius = radius
        self.price_range = price_range
        self.output_length = output_length

#Example used as template
#DOMTree = xml.dom.minidom.parse("Stores.xml")
collection = ET()
root = collection.parse("Stores.xml")
product_node = root[0][0][0] # <PRODUCT PRICE="1" NAME="black chair" GEOID="125665" URL="http://www.buyme.com/product=125665"></PRODUCT>
radius = 500
store_location = "(41.49008, -71.312796)"
product_section = "Bed"
price_range = 50
output_length = 3

#Returns co-ords
def getCoords(co_ord):
    co_ord_list = co_ord.split(",")
    x = float(co_ord_list[0][1:])
    y = float(co_ord_list[1][:-1])
    return [x,y]

"""Filters the stores by location"""
def filterLocation():
    for store in root.findall("STORE"):
        dist = vincent(getCoords(store.get("LOCATION")),getCoords(store_location)).meters
        if (dist > radius):
            root.remove(store)
    return root

"""Removes products from stores with unmatching sections"""
def filterSection():
#    sections = root.findall("*/SECTION")
    for sections in root:
        for section in sections:
            if (section.get("NAME") != product_section):
                sections.remove(section)
    return root

def main():
    filterLocation()
    subcollection = ET(filterSection())
    subcollection.write('newStores.xml', xml_declaration=True)



