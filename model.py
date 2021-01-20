# %%
import numpy as np
from logbin import logbin
# %%
def propagate_avalanche(start):
    involved_sites = 0
    current_energy = 0
    for i in range(start, L):
        # print('i \t', i)
        if i == 0 and z_i[i] > z_i_th[i]:
            involved_sites += 1
            current_energy += z_i[i] - 1
            z_i[i] -= 2
            z_i[i+1] += 1
            h_i[i+1] += 1
        elif i == L - 1 and z_i[i] > z_i_th[i]:
            involved_sites += 1
            current_energy += z_i[i] - 1
            z_i[i] -= 1
            z_i[i-1] += 1
        elif z_i[i] > z_i_th[i]:
            involved_sites += 1
            current_energy += z_i[i] - 1
            z_i[i] -= 2
            z_i[i+1] += 1
            z_i[i-1] += 1
            h_i[i+1] += 1
        else:
            # can we skip the rest of the sites since they will have no change from previous checks?
            break
        # remove one from current height and move it to the next
        h_i[i] -= 1
        # h_i[i+1] += 1

        z_i_th[i] = int(np.random.random() > p) + 1

    if involved_sites == 0 :
        print(i, start)
    return i, involved_sites, current_energy
# %% 
# If sites are critical return 1
def test_gradients():
    for zi, zt in zip(z_i, z_i_th):
        if zi > zt: 
            print('Gradient inaccuracy!')
            return 1
        else:
            return 0
# %%
L = 16

z_i_th = np.random.randint(1,3,L)
z_i = np.zeros(L)
h_i = np.zeros(L)

p = 0.5

h0 = []
avalanche_count = 0
avalanche_sizes = []
inaccuracies = 0

avalanche_energies = []

iterations = 20000
for gen in range(iterations):
    # start at first site 
    site = 0
    # add a grain to it
    z_i[0] += 1
    h_i[0] += 1
    # direction is forward
    direction = 1
    # start a loop for checking for critical sites
    current_avalanche_size = 0
    current_avalanche_energy = 0
    while True:
        # When we return to the initial site, all sites should be resolved
        if site == -1:
            break
        # is site is critical, do an avalanche
        if z_i[site] > z_i_th[site]:
            site, size, energy = propagate_avalanche(site)
            current_avalanche_size += size
            current_avalanche_energy += energy
            # after an avalanche is performed, go back and check if any consecutive avalanches need to be triggered
            direction = -1
        else:
            # move one step in current direction
            site += direction
        # if we reach the last site, go back to check for criticality
        if site == L - 1:
            direction = -1
    # keep track of height of first site
    h0.append(h_i[0])
    avalanche_sizes.append(current_avalanche_size)
    avalanche_energies.append(current_avalanche_energy)
    if current_avalanche_size > 0:
        avalanche_count += 1

    # ERROR CHECK
    # if there are any sites with a z larger than the max threshold, it must be critical. If this is the case not all sites have been resolved and an error has occurred. 
    deviation = np.where(z_i > 2)
    if len(deviation[0]) > 0:
        print('ERROR IN THRESHOLDS!', deviation[0])
    
    inaccuracies += test_gradients()

if inaccuracies > 0: print('Finished with errors')
else: print('Finished without errors')
# %%
import matplotlib.pyplot as plt
# %%
plt.plot(h0)
# plt.plot([0,1000],[26.5,26.5])
print(np.average(h0[400:]) )# 3000 for L=32; 400 for L = 16
# %%
plt.bar(np.arange(1, 1 + L), h_i)
# %%
avalanche_sizes_np = np.array(avalanche_sizes[1000:])
avalanche_set_s = set(avalanche_sizes_np)
av_pdf_s = []
no_avs = len(avalanche_sizes_np)
for av_size in set(avalanche_sizes_np):
    larger_or_equal = len(np.where(avalanche_sizes_np >= av_size)[0])
    equal = len(np.where(avalanche_sizes_np == av_size)[0])
    frac = equal/no_avs
    av_pdf_s.append(frac)
    # print(av_size, '\t', frac)
# %% 
avalanche_energies_no0 = [e for e in avalanche_energies if e != 0]
avalanche_energies_np = np.array(avalanche_energies_no0[1000:])
avalanche_set_e = set(avalanche_energies_np)
av_pdf_e = []
no_avs = len(avalanche_energies_np)
for av_energy in avalanche_set_e:
    larger_or_equal = len(np.where(avalanche_energies_np >= av_energy)[0])
    equal = len(np.where(avalanche_energies_np == av_energy)[0])
    equal_de = len(np.where(avalanche_energies_np == av_energy)[0])
    frac = larger_or_equal/no_avs
    av_pdf_e.append(frac)
    # print(av_size, '\t', frac)
# %%
# plt.plot(list(avalanche_set_s), av_pdf_s)
plt.plot(list(avalanche_set_e), av_pdf_e)
plt.xscale('log')
plt.yscale('log')
plt.xlim((400,1000))
# %%
# %%
avalanche_energy_lb = logbin(avalanche_energies_no0, scale=1.01)
plt.plot(avalanche_energy_lb[0], avalanche_energy_lb[1])
plt.xscale('log')
plt.yscale('log')
# %%
