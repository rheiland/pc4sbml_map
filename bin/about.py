from ipywidgets import Output
from IPython.display import display, HTML

class AboutTab(object):

    def __init__(self):
#        self.tab = Output(layout={'height': '600px'})
#        self.tab = Output(layout={'height': '500px'})
#        self.tab = Output()
        self.tab = Output(layout={'height': 'auto'})
        self.tab.append_display_data(HTML(filename='doc/about.html'))
        
