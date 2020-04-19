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
from svg import SVGTab
from substrates import SubstrateTab
import debug
from pathlib import Path
#from debug import debug_view
import platform
from hublib.ui import PathSelector

hublib_flag = False


# join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"


# create the tabs, but don't display yet
about_tab = AboutTab()
svg = SVGTab()
sub = SubstrateTab()

nanoHUB_flag = False
if( 'HOME' in os.environ.keys() ):
    nanoHUB_flag = "home/nanohub" in os.environ['HOME']

def read_config_cb(_b):
    # with debug_view:
    #     print("read_config_cb", read_config.value)

    if read_config.value is None:  #occurs when a Run just finishes and we update pulldown with the new cache dir??
        # with debug_view:
        #     print("NOTE: read_config_cb(): No read_config.value. Returning!")
        return

    if os.path.isdir(read_config.value):
        is_dir = True
        config_file = os.path.join(read_config.value, 'config.xml')
    else:
        is_dir = False
        config_file = read_config.value

    if Path(config_file).is_file():
        # with debug_view:
        #     print("read_config_cb:  calling fill_gui_params with ",config_file)
        fill_gui_params(config_file)  #should verify file exists!
    else:
        # with debug_view:
        #     print("read_config_cb: ",config_file, " does not exist.")
        return
    
    # update visualization tabs
    if is_dir:
        svg.update(read_config.value)
        sub.update(read_config.value)
    else:  # may want to distinguish "DEFAULT" from other saved .xml config files
        # FIXME: really need a call to clear the visualizations
        svg.update('')
        sub.update('')

def outcb(s):
    # This is called when new output is received.
    # Only update file list for certain messages: 
    if "simulat" in s:
        # New Data. update visualizations
        svg.update('')
        sub.update('')
    return s

#----------------------------------------------

tab_height = 'auto'
#tab_height = '900px'
tab_layout = widgets.Layout(width='auto',height=tab_height, overflow_y='scroll',)   # border='2px solid black',
#tab_layout = widgets.Layout(width='auto',height=tab_height,)   # border='2px solid black',
titles = ['About', 'Out: Cell Plots', 'Out: Substrate Plots']
tabs = widgets.Tab(children=[about_tab.tab, svg.tab, sub.tab],
                   _titles={i: t for i, t in enumerate(titles)},
                   layout=tab_layout)

homedir = os.getcwd()

tool_title = widgets.Label(r'\(\textbf{PhysiCellVis}\)')

def get_vis_dir():
    home_dir = os.path.expanduser('~')
    dir_dict = {home_dir : home_dir}
    return dir_dict

def vis_dir_cb(s):
    return

vis_dir_select = widgets.Dropdown(
    description='Data dir',
    options=get_vis_dir(),
    tooltip='directory with PhysiCell output',
)
vis_dir_select.style = {'description_width': '%sch' % str(len(vis_dir_select.description) + 1)}
vis_dir_select.observe(vis_dir_cb, names='value') 


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
    top_row = widgets.HBox(children=[tool_title, vis_dir_select])
    # top_row = widgets.HBox(children=[tool_title, path_sel.w])
#    gui = widgets.VBox(children=[top_row, tabs, run_button.w], layout=gui_layout)
    gui = widgets.VBox(children=[top_row, tabs], layout=gui_layout)

#fill_gui_params(read_config.options['DEFAULT'])

# pass in (relative) directory where output data is located
#output_dir = "tmpdir"
output_dir = path_sel.value
#p = PathSelector('/data', select_file=False)

svg.update(output_dir)
sub.update_dropdown_fields("data")
sub.update(output_dir)
