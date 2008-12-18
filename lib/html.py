#!/usr/bin/env python

"""html.py - html helper functions"""

from BeautifulSoup import BeautifulSoup

_entities = {
    "quot": 34, "amp": 38, "lt": 60, "gt": 62, "euro": 128,
    "sbquo": 130, "fnof": 131, "bdquo": 132, "hellip": 133, "dagger": 134, "Dagger": 135, "circ": 136, "permil": 137,
    "Scaron": 138, "lsaquo": 139, "OElig": 140, "lsquo": 145, "rsquo": 146, "ldquo": 147, "rdquo": 148, "bull": 149,
    "ndash": 150, "mdash": 151, "tilde": 152, "trade": 153, "scaron": 154, "rsaquo": 155, "oelig": 156, "Yuml": 159,
    "nbsp": 160, "iexcl": 161, "cent": 162, "pound": 163, "curren": 164, "yen": 165, "brvbar": 166, "sect": 167,
    "uml": 168, "copy": 169, "ordf": 170, "laquo": 171, "not": 172, "shy": 173, "reg": 174, "macr": 175,
    "deg": 176, "plusmn": 177, "sup2": 178, "sup3": 179, "acute": 180, "micro": 181, "para": 182, "middot": 183,
    "cedil": 184, "sup1": 185, "ordm": 186, "raquo": 187, "frac14": 188, "frac12": 189, "frac34": 190, "iquest": 191,
    "Agrave": 192, "Aacute": 193, "Acirc": 194, "Atilde": 195, "Auml": 196, "Aring": 197, "AElig": 198, "Ccedil": 199,
    "Egrave": 200, "Eacute": 201, "Ecirc": 202, "Euml": 203, "Igrave": 204, "Iacute": 205, "Icirc": 206, "Iuml": 207,
    "ETH": 208, "Ntilde": 209, "Ograve": 210, "Oacute": 211, "Ocirc": 212, "Otilde": 213, "Ouml": 214, "times": 215,
    "Oslash": 216, "Ugrave": 217, "Uacute": 218, "Ucirc": 219, "Uuml": 220, "Yacute": 221, "THORN": 222, "szlig": 223,
    "agrave": 224, "aacute": 225, "acirc": 226, "atilde": 227, "auml": 228, "aring": 229, "aelig": 230, "ccedil": 231,
    "egrave": 232, "eacute": 233, "ecirc": 234, "euml": 235, "igrave": 236, "iacute": 237, "icirc": 238, "iuml": 239,
    "eth": 240, "ntilde": 241, "ograve": 242, "oacute": 243, "ocirc": 244, "otilde": 245, "ouml": 246, "divide": 247,
    "oslash": 248, "ugrave": 249, "uacute": 250,"ucirc": 251, "uuml": 252, "yacute": 253, "thorn": 254, "yuml": 255
}
for i in range(1, 256):
    _entities["#%s" % i] = i

def encode(html):
    """encodes html entities"""

    html = html.replace("&", "&amp;")
    for entity in _entities:
        if not entity.startswith("#") and entity != "amp":
            html = html.replace(chr(_entities[entity]), "&%s;" % entity)
    return html

def decode(html):
    """decodes html entities"""

    for entity in _entities:
        html = html.replace("&%s;" % entity, chr(_entities[entity]))
    return html

def strip(html):
    """strips out html tags"""

    html = decode(str(html))
    while "<" in html and html.find(">", html.find("<")) > html.find("<"):
        html = "%s%s" % (html[:html.find("<")], html[html.find(">", html.find("<")) + 1:])
    html = " ".join([part for part in html.split(" ") if part])
    return html

def parse(html):
    """BeautifulSoup wrapper"""

    return BeautifulSoup(html)

def colourise(lst, colours):
    """returns list coloured in html"""

    i = 0
    coloured = []
    for item in lst:
        if item in colours:
            colour = item
        else:
            colour = colours[i]
        coloured.append("<font color=\"%s\"><b>%s</b></font>" % (colour, item))
        i += 1
        if i == len(colours):
            i = 0
    return coloured

def borderise(lists, colours):
    """returns lists in coloured borders"""

    longest = max([len(lst) for lst in lists])
    bordered = []
    for lst in lists:
        for i in range(len(lst) - 1, longest):
            lst.append("&nbsp;")
        bordered.append("<font style=\"" \
                        "display:block;" \
                        "float:left;" \
                        "white-space:nowrap;" \
                        "border:5px solid;" \
                        "-moz-border-radius:9px;" \
                        "padding:20px;" \
                        "margin:5px;" \
                        "\"><b>%s</b></font>" % "<br>".join(lst))
    return colourise(bordered, colours)
