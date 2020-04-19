import ipywidgets as widgets
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
import os
import glob
import shutil
import math
import datetime
import tempfile
from about import AboutTab
#from config import ConfigTab
#from user_params import UserTab
from sbml_map import SBMLTab
from pathlib import Path
#from debug import debug_view
import platform
from hublib.ui import PathSelector

hublib_flag = False

# create the tabs, but don't display yet
about_tab = AboutTab()
mapping_tab = SBMLTab()

nanoHUB_flag = False
if( 'HOME' in os.environ.keys() ):
    nanoHUB_flag = "home/nanohub" in os.environ['HOME']
#----------------------------------------------

tab_height = 'auto'
#tab_height = '900px'
tab_layout = widgets.Layout(width='auto',height=tab_height, overflow_y='scroll',)   # border='2px solid black',
#tab_layout = widgets.Layout(width='auto',height=tab_height,)   # border='2px solid black',
#titles = ['About', 'Out: Cell Plots', 'Out: Substrate Plots']
titles = ['About', 'PhysiCell-SBML mapping']
#tabs = widgets.Tab(children=[about_tab.tab, svg.tab, sub.tab],
tabs = widgets.Tab(children=[about_tab.tab, mapping_tab.tab],
                   _titles={i: t for i, t in enumerate(titles)},
                   layout=tab_layout)

homedir = os.getcwd()

tool_title = widgets.Label(r'\(\textbf{PhysiCell-SBML map}\)')

def get_sbml_dir():
    home_dir = os.path.expanduser('~')
    dir_dict = {home_dir : home_dir}
    return dir_dict

def sbml_dir_cb(s):
    return

sbml_dir_select = widgets.Dropdown(
    description='Data dir',
    options=get_sbml_dir(),
    tooltip='directory with PhysiCell output',
)
sbml_dir_select.style = {'description_width': '%sch' % str(len(sbml_dir_select.description) + 1)}
sbml_dir_select.observe(sbml_dir_cb, names='value') 


gui_height = '900px'
gui_layout = widgets.Layout(width='auto',height=gui_height, overflow_y='scroll',)   # border='2px solid black',
path_sel = PathSelector('.', select_file=True)
if nanoHUB_flag:
    # define this, but don't use (yet)
    remote_cb = widgets.Checkbox(indent=False, value=False, description='Submit as Batch Job to Clusters/Grid')

    # top_row = widgets.HBox(children=[read_config, tool_title])
    # top_row = widgets.HBox(children=[tool_title, path_sel])
    top_row = widgets.HBox(children=[tool_title])
#    gui = widgets.VBox(children=[top_row, tabs, run_button.w])
    gui = widgets.VBox(children=[top_row, tabs])
else:
    top_row = widgets.HBox(children=[tool_title, sbml_dir_select])
    # top_row = widgets.HBox(children=[tool_title, path_sel.w])
#    gui = widgets.VBox(children=[top_row, tabs, run_button.w], layout=gui_layout)
    gui = widgets.VBox(children=[top_row, tabs], layout=gui_layout)

#fill_gui_params(read_config.options['DEFAULT'])

# pass in (relative) directory where output data is located
#output_dir = "tmpdir"
output_dir = path_sel.value
#p = PathSelector('/data', select_file=False)

#svg.update(output_dir)
#sub.update_dropdown_fields("data")
#sub.update(output_dir)

    # Populate the GUI widgets with values from the XML
mapping_tab.fill_physicell_table()
mapping_tab.fill_sbml_table()
