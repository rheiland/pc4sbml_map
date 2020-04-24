import sys
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html

print('argc=',len(sys.argv))
print(sys.argv)
fname = sys.argv[1]
try:
    tree = ET.parse(fname)
    xml_root = tree.getroot()
except:
    print("Cannot open ",fname," to read SBML info.")
    sys.exit(-1)

# uep = xml_root.find(".//sbml//model//listOfSpecies")
uep = xml_root.find(".//listOfSpecies")
print('listOfSpecies uep=',uep)
# sbml_list = ['----- species -----']
sbml_list = []
if uep:
    sbml_list.append('----- species -----')
    for var in uep.findall('species'):
        menv_name = var.attrib['id']
        sbml_list.append(menv_name)
    # print(var.attrib['name'])
    # self.physicell_vars.options.
    # tmp = list(self.physicell_vars.options)
    # tmp.append(var.attrib['name'])
    # self.physicell_vars.options = tuple(tmp)
    # print(var.text)

uep = xml_root.find(".//listOfParameters")
if uep:
    sbml_list.append('----- parameters -----')
    for var in uep.findall('parameter'):
        # print('--- found param')
        if (not 'constant' in var.attrib.keys()) or (var.attrib['constant'] == 'false'):
            param_name = var.attrib['id']
            sbml_list.append(param_name)

# uep = xml_root.find(".//cell_population")
# uep = xml_root.find(".//labels")
# for var in uep.findall('label'):
#     cd_name = var.text
#     sbml_list.append(cd_name)

#self.sbml_vars.options = tuple(sbml_list)
sbml_vars = tuple(sbml_list)
print(sbml_vars)