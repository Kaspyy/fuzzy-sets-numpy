# YOUR CODE HERE

y_low = Triangular((0.9,0), (5,1), (10,0))
y_average = Triangular((1,0), (10,1), (20,0))
y_high = Triangular((10,0), (15, 1), (20.1,0))
a_y_low = Adjective('y_low', y_low)
a_y_average = Adjective('y_average', y_average)
a_y_high = Adjective('y_high', y_high)
price_yesterday = Variable('price_yesterday', 'zł', a_y_low, a_y_average, a_y_high)

t_low = Triangular((0.9,0), (5,1), (10,0))
t_average = Triangular((1,0), (10,1), (20,0))
t_high = Triangular((10,0), (15, 1), (20.1,0))
a_t_low = Adjective('a_t_low', t_low)
a_t_average = Adjective('a_t_average', t_average)
a_t_high = Adjective('a_t_high', t_high)
price_today = Variable('price_today', 'zł', a_t_low, a_t_average, a_t_high)


tm_low = Triangular((0.9,0), (5,1), (10,0))
tm_average = Triangular((1,0), (10,1), (20,0))
tm_high = Triangular((10,0), (15, 1), (20.1,0))
a_tm_low = Adjective('a_tm_low', tm_low)
a_tm_average = Adjective('a_tm_average', tm_average)
a_tm_high = Adjective('a_tm_high', tm_high)
price_tomorrow = Variable('price_tomorrow', 'zł', a_tm_low, a_tm_average, a_tm_high, defuzzification='COG', default=0)

x = np.linspace(1,20,1000)
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,8))
((ax1), (ax2), (ax3)) = axs
plot_fuzzyset(ax1, y_low, x, 'b', label='y_low')
plot_fuzzyset(ax1, y_average, x, 'g', label='y_average')
plot_fuzzyset(ax1, y_high, x, 'r', label='y_high')
plot_fuzzyset(ax2, t_low, x, 'b', label='t_low')
plot_fuzzyset(ax2, t_average, x, 'g', label='t_average')
plot_fuzzyset(ax2, t_high, x, 'r', label='t_high')
plot_fuzzyset(ax3, tm_low, x, 'b', label='tm_low')
plot_fuzzyset(ax3, tm_average, x, 'g', label='tm_average')
plot_fuzzyset(ax3, tm_high, x, 'r', label='tm_high')
plt.show()

rule13 = 'if price_yesterday is a_y_low and price_today is a_t_low then z = price_yesterday*0.5 + price_today*0.5'
rule14 = 'if price_yesterday is a_y_average and price_today is a_t_average then z = price_today*0.7 + 5'
rule15 = 'if price_yesterday is a_y_high and price_today is a_t_high then z = price_yesterday*0.4+ price_today*0.6 + 15'


block = RuleBlock('rb_takagi', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule13, rule14, rule15, scope=scope)

from fuzzython.systems.sugeno import SugenoSystem

sugeno = SugenoSystem('model_takagi', block)

inputs = {'price_yesterday': 10, 'price_today': 2}
res = sugeno.compute(inputs)
res

from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampled = np.linspace(0, 10, 20)
x, y = np.meshgrid(sampled, sampled)
z = np.zeros((len(sampled),len(sampled)))

for i in range(len(sampled)):
    for j in range(len(sampled)):
        inputs = {'price_yesterday': x[i, j], 'price_today': y[i, j]}
        res = sugeno.compute(inputs)
        z[i, j] = res['rb_takagi']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset= -1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset= 11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset= 11, cmap='viridis', alpha=0.5)
ax.set_xlabel('price_yesterday')
ax.set_ylabel('price_today')
ax.set_zlabel('price_tomorrow')
ax.view_init(30, 200)