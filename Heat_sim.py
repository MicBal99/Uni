import numpy as np
import matplotlib.pyplot as plt

alpha = 0.025
length = 1.0
time = 7
nodes = 60
specific_heat = 1000
density = 1.2

dx = dy = length / (nodes - 1)
dt = min(dx**2 / (4 * alpha), dy**2 / (4 * alpha))
t_nodes = int(time / dt) + 1

u = np.ones((nodes, nodes)) * 20
total_energy = 0

wall_thickness = 3
walls = [
    (slice(int(0.25 * (nodes - 1)) - wall_thickness // 2, int(0.25 * (nodes - 1)) + wall_thickness // 2),
     slice(0, int(0.31 * (nodes - 1)))),

    (slice(int(0.6 * (nodes - 1)) - wall_thickness // 2, int(0.6 * (nodes - 1)) + wall_thickness // 2),
     slice(int(0.5 * (nodes - 1)), nodes)),

    (slice(int(0.4 * (nodes - 1)), nodes),
     slice(int(0.3 * (nodes - 1)) - wall_thickness // 2, int(0.3 * (nodes - 1)) + wall_thickness // 2))
]

windows = [
    (0, slice(int(0.47 * (nodes - 1)), int(0.8 * (nodes - 1)))),
    (slice(int(0.67 * (nodes - 1)), int(0.95 * (nodes - 1))), nodes - 1)
]

external_walls = [
    (slice(0, 1), slice(0, nodes)),
    (slice(nodes - 1, nodes), slice(0, nodes)),
    (slice(0, nodes), slice(0, 1)),
    (slice(0, nodes), slice(nodes - 1, nodes))
]

heater_temp = 50
heaters = [
    (slice(4, 6), slice(int(0.50 * (nodes -1)), int(0.8 * (nodes - 1)))),
    (slice(int(0.6 * (nodes - 1)), int(0.8 * (nodes - 1))), slice(1, 4))
]

def calculate_heater_energy(u_old, u_new, heaters_active):
    if not heaters_active:
        return 0

    energy = 0
    cell_volume = (dx * dy * 0.1)

    for heater in heaters:
        delta_T = np.mean(u_new[heater] - u_old[heater])
        mass = cell_volume * density * np.prod([s.stop - s.start for s in heater])
        energy += mass * specific_heat * max(0, delta_T)

    return energy

heaters_on = True

for win in windows:
    u[win] = -10

for heat in heaters:
    u[heat] = heater_temp

plt.ion()
fig, ax = plt.subplots()
cmap = ax.imshow(u, cmap='jet', origin='lower', extent=[0, 1, 0, 1])
plt.colorbar(cmap, label='Temperatura [°C]')
plt.title('Rozkład temperatury')

for wall in walls:
    rect = plt.Rectangle(
        (wall[1].start / (nodes - 1), wall[0].start / (nodes - 1)),
        (wall[1].stop - wall[1].start) / (nodes - 1),
        (wall[0].stop - wall[0].start) / (nodes - 1),
        color='gray',
        alpha=0.9
    )
    ax.add_patch(rect)

for wall in external_walls:
    ax.plot([wall[1].start / (nodes - 1), wall[1].stop / (nodes - 1)],
            [wall[0].start / (nodes - 1), wall[0].start / (nodes - 1)], color='black', lw=2)
    ax.plot([wall[1].start / (nodes - 1), wall[1].stop / (nodes - 1)],
            [wall[0].stop / (nodes - 1), wall[0].stop / (nodes - 1)], color='black', lw=2)
    ax.plot([wall[1].start / (nodes - 1), wall[1].start / (nodes - 1)],
            [wall[0].start / (nodes - 1), wall[0].stop / (nodes - 1)], color='black', lw=2)
    ax.plot([wall[1].stop / (nodes - 1), wall[1].stop / (nodes - 1)],
            [wall[0].start / (nodes - 1), wall[0].stop / (nodes - 1)], color='black', lw=2)

def calculate_average_temp(temp_array, exclude_heaters=False):
    mask = np.ones_like(temp_array, dtype=bool)

    for wall in walls + external_walls:
        mask[wall] = False

    for win in windows:
        mask[win] = False

    if exclude_heaters:
        for heat in heaters:
            mask[heat] = False

    return np.mean(temp_array[mask])

def update_plot():
    cmap.set_data(u)
    plt.pause(0.01)

time_points = []
avg_temp_points = []
energy_points = []

t = 0
while t < time:
    w = np.copy(u)
    for i in range(1, nodes - 1):
        for j in range(1, nodes - 1):
            if not any((i in range(wall[0].start, wall[0].stop) and
                       j in range(wall[1].start, wall[1].stop)) for wall in walls + external_walls) and w[i, j] != -10:
                dd_ux = (w[i - 1, j] - 2 * w[i, j] + w[i + 1, j]) / dx**2
                dd_uy = (w[i, j - 1] - 2 * w[i, j] + w[i, j + 1]) / dy**2
                u[i, j] = w[i, j] + dt * alpha * (dd_ux + dd_uy)

    for wall in external_walls:
        if wall[0].start == 0:
            u[0, :] = u[1, :]
        elif wall[0].start == nodes - 1:
            u[-1, :] = u[-2, :]
        if wall[1].start == 0:
            u[:, 0] = u[:, 1]
        elif wall[1].start == nodes - 1:
            u[:, -1] = u[:, -2]

    for wall in walls:
        for i in range(wall[0].start, wall[0].stop):
            for j in range(wall[1].start, wall[1].stop):
                neighbors = []
                if i > 0 and not (i - 1 in range(wall[0].start, wall[0].stop) and j in range(wall[1].start, wall[1].stop)):
                    neighbors.append(u[i - 1, j])
                if i < nodes - 1 and not (i + 1 in range(wall[0].start, wall[0].stop) and j in range(wall[1].start, wall[1].stop)):
                    neighbors.append(u[i + 1, j])
                if j > 0 and not (i in range(wall[0].start, wall[0].stop) and j - 1 in range(wall[1].start, wall[1].stop)):
                    neighbors.append(u[i, j - 1])
                if j < nodes - 1 and not (i in range(wall[0].start, wall[0].stop) and j + 1 in range(wall[1].start, wall[1].stop)):
                    neighbors.append(u[i, j + 1])
                if neighbors:
                    u[i, j] = np.mean(neighbors)

    for win in windows:
        u[win] = -10

    avg_temp = calculate_average_temp(u, exclude_heaters=True)
    time_points.append(t)
    avg_temp_points.append(avg_temp)

    if avg_temp > 21 and heaters_on:
        heaters_on = False
    elif avg_temp < 19 and not heaters_on:
        heaters_on = True

    u_before_heaters = np.copy(u)

    for heat in heaters:
        if heaters_on:
            u[heat] = heater_temp
        else:
            for i in range(heat[0].start, heat[0].stop):
                for j in range(heat[1].start, heat[1].stop):
                    u[i, j] = np.mean([u[i-1, j], u[i+1, j], u[i, j-1], u[i, j+1]])

    energy = calculate_heater_energy(u_before_heaters, u, heaters_on)
    total_energy += energy
    energy_points.append(total_energy)

    print(f"Średnia temperatura: {avg_temp:.2f}°C | Grzejniki: {'ON' if heaters_on else 'OFF'} | Całkowita energia: {total_energy:.2f} J")

    t += dt
    update_plot()

plt.ioff()

plt.figure()
plt.plot(time_points, avg_temp_points, label='Średnia temperatura')
plt.xlabel('Czas')
plt.ylabel('Temperatura [°C]')
plt.title('Średnia temperatura w pomieszczeniu w czasie')
plt.legend()
plt.grid()

plt.figure()
plt.plot(time_points, energy_points, label='Zużyta energia', color='orange')
plt.xlabel('Czas')
plt.ylabel('Energia')
plt.title('Zużycie energii w czasie')
plt.legend()
plt.grid()

plt.show()