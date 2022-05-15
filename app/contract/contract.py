from datetime import datetime
from os import path, remove

from odf.opendocument import load
from odf import text, draw, teletype, style, element
from odf.element import Node

#infile = 'contrat.odt'
#outfile = 'contrat{}.odt'.format(2)
#dict = {"#object_number": "0001", "#quote_number": "1010", "#show_name": "Jason Mist DUO", "#show_conditions": "min. 15000 personnes", "#technical_contact": "Norman ALIÉ (06 74 87 22 12)", "#show_date": "25/12/2021", "#price_excl": "42.00", "#taxes": "0.69", "#price_incl": "42.69", "#price_letter": "Universal Answer € and Nice cts", "#date": "01/01/1980"}


class Contract():
    @classmethod
    def generate(cls, infile, datas_dic):
        """
        Generate a contract file from an input file (.odt).
        Look for datas_dic.keys and replace them by datas_dic.value
        Return the ouput file path
        """
        if not path.exists(infile):
            return 1

        doc = load(infile)
        outfile = path.join(path.dirname(infile), f'contract-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.odt' )
        for item in doc.getElementsByType(text.P):
            for child in item.childNodes:
                nodeReplaceText(child, datas_dic)
                
        doc.save(outfile)
        return outfile

    @classmethod
    def delete(cls, file):
        if path.exists(file):
            remove(file)
            return 0
        else:
            return 1

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

