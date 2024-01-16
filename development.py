import numpy as np
import matplotlib.pyplot as plt
import math

# Model parameters
g = 9.81  # Gravitational constant
m = 0.41  # Mass (kg)
w = 11.99  # Wing oscillation frequency (rad/s)
f = w / 2 / np.pi  # Wing oscillation frequency (Hz)
k = w ** 2 * m  # Spring stiffness (N/m)
c = 0.1  # Net damping (Ns/m)

print('Model parameters:')
print('Excitation frequency is =', f, 'Hz')
print('Mass of magnet is =', m, 'kg')
print('Spring stiffness is =', k, 'N/m')
print('Damping is =', c, 'Ns/m')

# Electrical model parameters
rl = 0.5  # Load resistance (Ohm)
rc = 0.5  # Coil resistance (Ohm)
alpha = 0.1992  # Rate of change of magnetic flux with respect to displacement = dphi/dz = Wb/m

print('Electrical model parameters:')
print('Load resistance is =', rl, 'Ohm')
print('Coil resistance is =', rc, 'Ohm')
print('Rate of change of magnetic flux with respect to displacement is =', alpha, 'Wb/m')

# Find electrical damping term
ce = (alpha ** 2) * (1 / (rl + rc))
print('Electrical damping is =', ce, 'Ns/m')

# Find time step for simulation
wn = np.sqrt(k / m)  # rad/s
fn = wn / 2 / np.pi  # Hz
h = 1 / fn / 20

print('Natural frequency = ', fn, 'Hz')
print('Setting time step equal to ', h, 's')


# Methods
def f1(z, u, t, F):
    return u


def f2(z, u, t, F):
    return (m ** (-1)) * (F - (c + ce) * u - k * z)


n = 1000
t = np.zeros(n)  # Time vector
x = np.zeros(n)  # Mass displacement
u = np.zeros(n)  # Velocity for RK4 (z_dot = u)
y = np.zeros(n)  # Base displacement
ydot = np.zeros(n)  # Base velocity
ydotdot = np.zeros(n)  # Base acceleration
P = np.zeros(n)  # Electrical power to the load

# Set initial conditions for simple harmonic motion
y[0] = 0
ydot[0] = 0
ydotdot[0] = 0
y_0 = 0.01  # Amplitude of base vibration is 0.01m

# Simple harmonic motion loop
for i in range(0, n - 1):
    y[i + 1] = y_0 * np.cos(w * i * h)
    ydot[i + 1] = -w * y_0 * np.sin(w * i * h)
    ydotdot[i + 1] = (-w ** 2) * y_0 * np.cos(w * i * h)
    t[i + 1] = t[i] + h

F = - m * g - m * ydotdot  # Excitation force
z = x - y  # Net displacement between moving mass and base
z[0] = 0  # Set initial conditions

# Main loop
for i in range(0, n - 1):
    k1 = f1(z[i], u[i], t[i], F[i])
    m1 = f2(z[i], u[i], t[i], F[i])
    k2 = f1(z[i] + 0.5 * h * k1, u[i] + 0.5 * h * m1, t[i] + 0.5 * h, F[i] + 0.5 * h)
    m2 = f2(z[i] + 0.5 * h * k1, u[i] + 0.5 * h * m1, t[i] + 0.5 * h, F[i] + 0.5 * h)
    k3 = f1(z[i] + 0.5 * h * k2, u[i] + 0.5 * h * m2, t[i] + 0.5 * h, F[i] + 0.5 * h)
    m3 = f2(z[i] + 0.5 * h * k2, u[i] + 0.5 * h * m2, t[i] + 0.5 * h, F[i] + 0.5 * h)
    k4 = f1(z[i] + h * k3, u[i] + h * m3, t[i] + h, F[i] + h)
    m4 = f2(z[i] + h * k3, u[i] + h * m3, t[i] + h, F[i] + h)
    z[i + 1] = z[i] + ((h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
    u[i + 1] = u[i] + ((h / 6) * (m1 + 2 * m2 + 2 * m3 + m4))
    P[i + 1] = (rl * ce * u[i + 1] ** 2) / (rl + rc)
    t[i + 1] = t[i] + h

# Finding max power output
P_set = P[102:]  # Take power values settled after 10 sec
P_max = max(P_set)
print('Simulation results:')
print('Maximum power output is = ', P_max, 'W')

# Finding RMS power output
rms = np.sqrt(np.mean(P ** 2))
print('RMS power output is =', rms, 'W')

# Finding max displacement of mass
z_set = z[102:]  # Take displacement values settled after 10 sec
z_max_set = max(z_set)
print('Maximum displacement (after 10 sec) is = ', z_max_set, 'm')
z_max = max(z)  # Finding actual max displacement
print('Maximum displacement is = ', z_max, 'm')

# Plot results
plt.figure(1)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.5)
plt.subplot(211)
plt.plot(t, P)
plt.title('(a) Electrical power output (W)', fontsize=20)
plt.xlabel('Time (s)', fontsize=16)
plt.ylabel('Power (W)', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.subplot(212)
plt.plot(t, z)
plt.title('(b) Net mass displacement (m)', fontsize=20)
plt.xlabel('Time (s)', fontsize=16)
plt.ylabel('Net displacement (m)', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
# Show graphics
plt.show()
