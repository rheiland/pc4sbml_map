from ipywidgets import Select, Button, Textarea, HBox, VBox, Layout, Box
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

        gen_button_layout ={'width':'20%'}
        self.generate= Button(
            description='Generate', #style={'description_width': 'initial'},
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Generate code to map two quantities.',
            disabled=False,
            layout=gen_button_layout
            # layout=Layout(width='490px')
        )
        empty_btn = Button(disabled=True,layout=Layout(width='270px'))
        empty_btn.style.button_color = 'white'

        box_layout = Layout(display='flex', flex_flow='row', align_items='stretch', width='700px')
        row1 = [empty_btn, self.generate]
        box1 = Box(children=row1, layout=box_layout)

        self.code = Textarea(
            value='code goes here...',
            placeholder='placeholder',
            description='Code:',
            disabled=False,
            layout=Layout(width='700px', height='300px')
        )

        def generate_code_cb(b):
            # validate selections as valid
            self.code.value = "// " + str(self.physicell_vars.value) + " --> " + str(self.sbml_vars.value)
            self.code.value += "\n..."
            str1 = """
    static int idx_sbml_oxygen = 3;
    static int idx_substrate_oxygen = microenvironment.find_density_index( "oxygen" ); 

    int index_voxel = microenvironment.nearest_voxel_index(pCell->position);
    double oxy_val = microenvironment(vi)[idx_substrate_oxygen];

    rrc::RRVectorPtr vptr;
    rrc::RRCDataPtr result;  // start time, end time, and number of points
    vptr = rrc::getFloatingSpeciesConcentrations(pCell->phenotype.molecular.model_rr);
    """
            self.code.value += str1
            self.code.value += "\n..."
            self.code.value += "\n// " + str(self.sbml_vars.value) + " --> " + str(self.physicell_vars.value)
            str2 = """
    static int idx_sbml_oxygen = 3;
    static int idx_substrate_oxygen = microenvironment.find_density_index( "oxygen" ); 

    int index_voxel = microenvironment.nearest_voxel_index(pCell->position);
    double oxy_val = microenvironment(vi)[idx_substrate_oxygen];

    rrc::RRVectorPtr vptr;
    rrc::RRCDataPtr result;  // start time, end time, and number of points
    vptr = rrc::getFloatingSpeciesConcentrations(pCell->phenotype.molecular.model_rr);

    """
            self.code.value += str2
            self.code.value += "\n..."

        self.generate.on_click(generate_code_cb)


        map_tables = HBox([self.physicell_vars, self.sbml_vars, ])

        # self.tab = VBox([map_tables, self.generate, self.code])  
        self.tab = VBox([map_tables, box1, self.code])  
                         
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
        fname = os.path.join(".","data","virus_odes.xml")
        fname = os.path.join(".","data","stacey_model1.xml")
        try:
            tree = ET.parse(fname)
            xml_root = tree.getroot()
        except:
            print("Cannot open ",fname," to read SBML info.")
            return

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

        self.sbml_vars.options = tuple(sbml_list)
        # os.system('dir(var)')
        