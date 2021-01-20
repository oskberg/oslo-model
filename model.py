# %%
import numpy as np
# %%
def propagate_avalanche(i):
    for i in range(i, L):
        # print('i \t', i)
        if i == 0 and z_i[i] > z_i_th[i]:
            z_i[i] -= 2
            z_i[i+1] += 1
            h_i[i+1] += 1
        elif i == L - 1 and z_i[i] > z_i_th[i]:
            z_i[i] -= 1
            z_i[i-1] += 1
        elif z_i[i] > z_i_th[i]:
            z_i[i] -= 2
            z_i[i+1] += 1
            z_i[i-1] += 1
            h_i[i+1] += 1
        else:
            break
        # remove one from current height and move it to the next
        h_i[i] -= 1
        # h_i[i+1] += 1

        z_i_th[i] = int(np.random.random() > p) + 1
    return i
# %%
L = 5

z_i_th = np.random.randint(1,3,L)
z_i = np.zeros(L)
h_i = np.zeros(L)

p = 0.5

iterations = 30
for gen in range(iterations):
    site = 0
    z_i[0] += 1
    h_i[0] += 1
    print(gen, h_i, ' ->  ', end='')
    # It's impossible to have a double avalanche?
    direction = 1
    while True:
        if site == -1:
            break
        # print('site \t', site)
        if z_i[site] > z_i_th[site]:
            # if site == 0 and direction == -1:
            #     print('!!!')
            site = propagate_avalanche(site)
            direction = -1
        else:
            site += direction
            # break?
        if site == L - 1:
            direction = -1
    print(h_i)
    deviation = np.where(z_i > 2)
    if len(deviation[0]) > 0:
        print(deviation[0])

# %%
