import os,sys,lxml.etree

def damuku_parser(origin_xml):
    ret = []
    html = lxml.etree.HTML(origin_xml)
    for item in html.xpath('//d'):
        description = item.xpath('./@p')[0].split(',')
        ret.append( [ float(description[0]),int(description[1]),int(description[3]),description[6],item.text ] )
    return ret