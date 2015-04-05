__author__ = 'David'
from xml.dom.minidom import parse
import xml.dom.minidom
import Queue
from xml.etree.ElementTree import ElementTree as ET
from geopy.distance import vincenty as vincent

collection = ET()
root = collection.parse("Stores.xml")


""" Example Input:
product_node = root[0][0][0] # <PRODUCT PRICE="1" NAME="black chair" GEOID="125665" URL="http://www.buyme.com/product=125665"></PRODUCT>
radius = 500
store_location = "(41.49008, -71.312796)"
product_section = "Bed"
price_range = 50
output_length = 3"""


class Search_Query:
    #Last 2 can be automated using product_node.
    def __init__(self):
        #self,product_node,radius,price_range,output_length,store_location,product_section):
        self.store_location = "(41.49008, -71.312796)"
        self.product_section = "Bed"
        self.product_node = root[0][0][0]
        self.radius = 500
        self.price_range = 50
        self.output_length = 4

    """Returns the complete filtered search-result in terms of an XML-Document"""
    def buildXML(self):
        global root
        list = self.request()
        for store in root:
            for category in store:
                for product in category:
                    if not(product in list):
                        category.remove(product)
        root = ET(root)
        root.write("SearchResults.xml", xml_declaration=True)


    """This should in theory be the only public method. Updates and returns search-results in a list of XML-Elements"""
    def request(self):
        self.filterLocation()
        self.filterSection()
        self.filterPriceRange()
        return self.getSearchResults()

    #Returns co-ords
    def getCoords(self, co_ord):
        co_ord_list = co_ord.split(",")
        x = float(co_ord_list[0][1:])
        y = float(co_ord_list[1][:-1])
        return [x,y]

    """Filters the stores by location"""
    def filterLocation(self):
        for store in root.findall("STORE"):
            dist = vincent(self.getCoords(store.get("LOCATION")),self.getCoords(self.store_location)).meters
            if (dist > self.radius):
                root.remove(store)
        return root

    """Removes products from stores with unmatching sections"""
    def filterSection(self):
        for sections in root:
            for section in sections:
                if (section.get("NAME") != self.product_section):
                    sections.remove(section)
        return root
    """Removes products that do not satify price-range criteria"""
    def filterPriceRange(self):
        #q = Queue.PriorityQueue(output_length)
        product_price = float(self.product_node.get("PRICE"))
        for store in root:
            for section in store:
                productNo = len(section)
                i = 0
                while(i<productNo):
                    price_temp = float(section[i].get("PRICE"))
                    print(price_temp)
                    print("i: "+ str(i)+" number of products-1: "+str(productNo))
                    if (product_price+self.price_range < price_temp or product_price-self.price_range > price_temp):
                        print("Deleted product with price above: ")
                        #print(price_temp)
                        section.remove(section[i])
                        productNo-=1
                        i-=1
                    i+=1
        return root

    def getAllProducts(self):
        list_xml =[]
        for store in root:
            for section in store:
                for product in section:
                    tuple = (product,float(product.get("PRICE")))  #[price,xml-product]
                    list_xml.append(tuple)
        return list_xml

    """Outputs a list of XML-Nodes that satisfy search criteria"""
    def getSearchResults(self):
        products = []
        list_xml  = self.getAllProducts()
        list_sorted =sorted(list_xml,key=lambda x: x[1], reverse=False)
        for i in range(len(list_sorted)):
            if i < self.output_length:
                products.append(list_sorted[i][0])
        return products