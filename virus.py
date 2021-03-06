
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 11:39:18 2018

@author: hsauro
"""

import tellurium as te
import roadrunner
import pylab


r = te.loada("""
         J1:  -> rcDNA;       k1*cccDNA
        rcDNA -> cccDNA;      k2*rcDNA
         J3:  -> envelope;    k3*cccDNA   
       cccDNA -> ;            k4*cccDNA
     envelope -> ;            k5*envelope
   rcDNA + envelope -> virus; k6*rcDNA*envelope

k1 = 1; k2 = 0.025;
k3 = 1000; k4 = 0.25
k5 = 2; k6 = 7.5E-6

cccDNA = 1; rcDNA = 0; envelope = 0
""")

md = r.simulate (0, 200, 100, ['time', 'rcDNA'])

r.seed = 124
for i in range(10):
    r.reset()
    m = r.gillespie (0, 200, 100, ['time', 'rcDNA'])
    pylab.plot(m['time'], m['rcDNA'], linewidth=4, alpha=0.4)
pylab.plot (md['time'], md['rcDNA'], color='red')
pylab.show()

