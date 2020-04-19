from ipywidgets import Select, HBox, VBox
import os
import xml.etree.ElementTree as ET
# from IPython.display import display, HTML

class SBMLTab(object):

    def __init__(self):

        self.physicell_vars = Select(
            # options=['--- microenv ---','--- cell var ---'],
            options=[],
        #     value='OSX',
            rows=10,
            description='PhysiCell:',
            disabled=False
        )
        self.sbml_vars = Select(
            options=[],
        #     value='OSX',
            rows=10,
            description='SBML:',
            disabled=False
        )

        map_tables = HBox([self.physicell_vars, self.sbml_vars, ])

        self.tab = VBox([map_tables,])  
                         
    #----------------------------------------
    # def fill_physicell_table(self, xml_root):
    def fill_physicell_table(self):
        fname = os.path.join(".","data","initial_covid19.xml")
        # fname = os.path.join("..","data","initial_covid19.xml")
        try:
            # fname = os.path.join(self.output_dir, "initial.xml")
            tree = ET.parse(fname)
            xml_root = tree.getroot()
        except:
            print("Cannot open ",fname," to read info, e.g., names of substrate fields.")
            return

        uep = xml_root.find(".//microenvironment//variables")
        p_list = ['----- microenv -----']
        for var in uep.findall('variable'):
            menv_name = var.attrib['name']
            p_list.append(menv_name)
            # print(var.attrib['name'])
            # self.physicell_vars.options.
            # tmp = list(self.physicell_vars.options)
            # tmp.append(var.attrib['name'])
            # self.physicell_vars.options = tuple(tmp)
            # print(var.text)
        p_list.append('----- cell data -----')

        uep = xml_root.find(".//cell_population")
        uep = xml_root.find(".//labels")
        for var in uep.findall('label'):
            cd_name = var.text
            p_list.append(cd_name)
        self.physicell_vars.options = tuple(p_list)
        # os.system('dir(var)')
        
    #----------------------------------------
    def fill_sbml_table(self):
        fname = os.path.join(".","data","Toy_Model_for_PhysiCell.xml")
        try:
            tree = ET.parse(fname)
            xml_root = tree.getroot()
        except:
            print("Cannot open ",fname," to read SBML info.")
            return

        # uep = xml_root.find(".//sbml//model//listOfSpecies")
        uep = xml_root.find(".//listOfSpecies")
        print('listOfSpecies uep=',uep)
        sbml_list = ['----- species -----']
        for var in uep.findall('species'):
            menv_name = var.attrib['id']
            sbml_list.append(menv_name)
            # print(var.attrib['name'])
            # self.physicell_vars.options.
            # tmp = list(self.physicell_vars.options)
            # tmp.append(var.attrib['name'])
            # self.physicell_vars.options = tuple(tmp)
            # print(var.text)
        sbml_list.append('----- rates -----')

        # uep = xml_root.find(".//cell_population")
        # uep = xml_root.find(".//labels")
        # for var in uep.findall('label'):
        #     cd_name = var.text
        #     sbml_list.append(cd_name)

        self.sbml_vars.options = tuple(sbml_list)
        # os.system('dir(var)')
        