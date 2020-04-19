import tellurium as te
te.setDefaultPlottingEngine('matplotlib')

vm = te.loada("""
     V' = -r_u*V;
     U' = r_u*V - r_p*U;
     R' = r_p*U - lambda_r*R;
     P' = r_s*R - r_a*P - lambda_p*P;
     A' = r_a*P;
     
     V = 0.1;  U = 0.1;  R = 0.1; P = 0.1; A = 0.1;

     r_u = 0.1;  r_p = 0.2; lambda_r = 0.1; r_s = 0.3; r_a = 0.4; lambda_p = 0.1;
""")
result = vm.simulate (0, 20, 1000, ['time', 'V', 'U', 'R', 'P', 'A'])
vm.plot()
