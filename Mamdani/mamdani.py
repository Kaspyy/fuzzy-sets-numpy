#YOUR CODE HERE
import numpy as np
import matplotlib.pyplot as plt
# pomocnicza funkcja do rysowania zbiorów rozmytych
def plot_fuzzyset(ax, fuzzy_set, x, *args, **kwargs):
    y = np.array([fuzzy_set(e) for e in x])
    ax.plot(x, y,  *args, **kwargs)
    ax.set_ylim(-0.1, 1.1)
    ax.legend()

from fuzzython.fsets.triangular import Triangular
from fuzzython.fsets.trapezoid import Trapezoid
from fuzzython.variable import Variable
from fuzzython.adjective import Adjective

s_low = Triangular((9.9,0), (10,1), (50,0))
s_average = Triangular((10,0), (50,1), (90,0))
s_high = Triangular((50,0), (120,1), (150,0))
s_veryhigh = Triangular((120,0), (200, 1), (200.1,0))
a_s_low = Adjective('s_low', s_low)
a_s_average = Adjective('s_average', s_average)
a_s_high = Adjective('s_high', s_high)
a_s_veryhigh = Adjective('s_veryhigh', s_veryhigh)
speed = Variable('speed', 'km/h', a_s_low, a_s_average, a_s_high, a_s_veryhigh)

v_verypoor = Triangular((0.04,0), (0.05,1), (1.5,0))
v_average = Triangular((0.05,0), (2.5,1), (3,0))
v_good = Triangular((2.5,0), (4,1), (4.1,0))
a_v_verypoor = Adjective('a_v_verypoor', v_verypoor)
a_v_average = Adjective('a_v_average', v_average)
a_v_good = Adjective('a_v_good', v_good)
visibility = Variable('visibility', 'km', a_v_verypoor, a_v_average, a_v_good)


a_verylow = Triangular((-0.1, 0), (0.0, 1), (0.3, 0))
a_low = Triangular((0.0,0), (0.3, 1), (0.55,0))
a_medium = Triangular((0.3,0), (0.55,1), (0.7,0))
a_high = Triangular((0.55,0), (1,1), (1.1,0))
a_a_verylow = Adjective('a_a_verylow', a_verylow)
a_a_low = Adjective('a_a_low', a_low)
a_a_medium = Adjective('a_a_medium', a_medium)
a_a_high = Adjective('a_a_high', a_high)
accident = Variable('accident', '%', a_a_verylow, a_a_low, a_a_medium, a_a_high, defuzzification='COG', default=0)


x = np.linspace(10,200,1000)
x2 = np.linspace(0.05,4,1000)
x3 = np.linspace(0,1,1000)
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,8))
((ax1), (ax2), (ax3)) = axs
plot_fuzzyset(ax1, s_low, x, 'b', label='s_low')
plot_fuzzyset(ax1, s_average, x, 'g', label='s_average')
plot_fuzzyset(ax1, s_high, x, 'r', label='s_high')
plot_fuzzyset(ax1, s_veryhigh, x, 'y', label='s_veryhigh')
plot_fuzzyset(ax2, v_verypoor, x2, 'b', label='v_verypoor')
plot_fuzzyset(ax2, v_average, x2, 'g', label='v_average')
plot_fuzzyset(ax2, v_good, x2, 'r', label='v_good')
plot_fuzzyset(ax3, a_verylow, x3, 'b', label='a_verylow')
plot_fuzzyset(ax3, a_low, x3, 'g', label='a_low')
plot_fuzzyset(ax3, a_medium, x3, 'r', label='a_medium')
plot_fuzzyset(ax3, a_high, x3, 'y', label='a_high')
plt.show()


from fuzzython.ruleblock import RuleBlock

scope = locals()

rule1 = 'if speed is a_s_veryhigh and visibility is a_v_verypoor then accident is a_a_high'
rule2 = 'if speed is a_s_veryhigh and visibility is a_v_average then accident is a_a_medium'
rule3 = 'if speed is a_s_veryhigh and visibility is a_v_good then accident is a_a_low'
rule4 = 'if speed is a_s_high or visibility is a_v_verypoor then accident is a_a_high'
rule5 = 'if speed is a_s_high or visibility is a_v_average then accident is a_a_medium'
rule6 = 'if speed is a_s_high or visibility is a_v_good then accident is a_a_low'
rule7 = 'if speed is a_s_average or visibility is a_v_verypoor then accident is a_a_medium'
rule8 = 'if speed is a_s_average or visibility is a_v_average then accident is a_a_low'
rule9 = 'if speed is a_s_average or visibility is a_v_good then accident is a_a_verylow'
rule10 = 'if speed is a_s_low and visibility is a_v_good then accident is a_a_verylow'
rule11 = 'if speed is a_s_low and visibility is a_v_average then accident is a_a_low'
rule12 = 'if speed is a_s_low and visibility is a_v_verypoor then accident is a_a_medium'



block = RuleBlock('rb_mamdani', operators=('MIN','MAX','ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, scope=scope)


from fuzzython.systems.mamdani import MamdaniSystem

mamdani = MamdaniSystem('mamdani_model', block)


inputs = {'speed': 10, 'visibility': 4} #tak naprawdę to można podać liczby rzeczywiste od 0 do 10

res = mamdani.compute(inputs)

res

from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampled1 = np.linspace(10, 200, 20)
sampled2 = np.linspace(0.05, 4, 20)
x, y = np.meshgrid(sampled1, sampled2)
z = np.zeros((len(sampled1),len(sampled2)))

for i in range(len(sampled1)):
    for j in range(len(sampled2)):
        inputs = {'speed': x[i, j], 'visibility': y[i, j]}
        res = mamdani.compute(inputs)
        z[i, j] = res['rb_mamdani']['accident']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset= -1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset= 11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset= 11, cmap='viridis', alpha=0.5)
ax.set_xlabel('speed')
ax.set_ylabel('visibility')
ax.set_zlabel('accident')
ax.view_init(30, 200)
