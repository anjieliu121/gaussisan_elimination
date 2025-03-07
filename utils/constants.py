import numpy as np
########################################################################################################################
#                                           Global Constants                                                           #
########################################################################################################################
k_start, k_end = 1, 12
L = 120                     # unit: in
S = 1000                    # unit: lb
E = 3.0e7                   # unit: lb/(in^2)
I = 625                     # unit: in^4
q = 100 / 12                # unit: lb/in
e = np.exp(1)               # e^1
########################################################################################################################
#                                           true solution                                                              #
########################################################################################################################
a = np.sqrt(S / (E*I))
b = -q / (2*S)
c = -(q*E*I) / (S**2)
c_temp = c / (e**(-a*L)-e**(a*L))
c1 = (1 - e**(-a*L)) * c_temp
c2 = (e**(a*L) - 1)  * c_temp
########################################################################################################################
#                                           approximate solution                                                       #
########################################################################################################################
Q = S / (E * I)
R = q / (2 * E * I)
r = lambda x: R * x * (x - L)



