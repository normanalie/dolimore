from odf.opendocument import load
from odf import text, draw, teletype, style, element
from odf.element import Node

#infile = 'contrat.odt'
#outfile = 'contrat{}.odt'.format(2)
#dict = {"#object_number": "0001", "#quote_number": "1010", "#show_name": "Jason Mist DUO", "#show_conditions": "min. 15000 personnes", "#technical_contact": "Norman ALIÉ (06 74 87 22 12)", "#show_date": "25/12/2021", "#price_excl": "42.00", "#taxes": "0.69", "#price_incl": "42.69", "#price_letter": "Universal Answer € and Nice cts", "#date": "01/01/1980"}


class Contract():
    pass


def nodeReplaceText(node, dic, depth=1):
    if node and node.nodeType == Node.TEXT_NODE:
        for k, v in dic.items():
            if node.data.find(k) != -1:
                node.data = node.data.replace(k, v)
                
    while(node and node.childNodes != 0 and depth<=100):
        for child in node.childNodes:
            return nodeReplaceText(child, dic, depth+1)
        return 0
    return 0


def generate(infile, dic, outfile):
    doc = load(infile)
    for item in doc.getElementsByType(text.P):
        for child in item.childNodes:
            nodeReplaceText(child, dic)
            
    doc.save(outfile)
    return 0
