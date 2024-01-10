import numpy as np
import matplotlib.pyplot as plt


class EnergyHarvester:
    def __init__(self, m, w, c, rl, rc, alpha, y_0):
        self.g, self.h = 9.81, None
        self.m, self.w, self.c, self.rl, self.rc, self.alpha, self.y_0 = m, w, c, rl, rc, alpha, y_0

    def print_model_parameters(self):
        print('Model parameters:')
        print('Mass of magnet is =', self.m, 'kg')
        print('Spring stiffness is =', self.spring_stiffness(), 'N/m')
        print('Damping is =', self.c, 'Ns/m')
        print('Load resistance is =', self.rl, 'Ohm')
        print('Coil resistance is =', self.rc, 'Ohm')
        print('Rate of change of magnetic flux with respect to displacement is =', self.alpha, 'Wb/m')

    def spring_stiffness(self):
        return self.w ** 2 * self.m

    def electrical_damping(self):
        return self.alpha ** 2 / (self.rl + self.rc)

    def time_step(self):
        k = self.spring_stiffness()
        fn = np.sqrt(k / self.m) / (2 * np.pi)
        self.h = 1 / fn / 20
        print('Natural frequency = ', fn, 'Hz')
        print('Setting time step equal to ', self.h, 's')

    def simple_harmonic_motion(self, n):
        t = np.zeros(n)
        y = np.zeros(n)
        ydot = np.zeros(n)
        ydotdot = np.zeros(n)

        for i in range(n - 1):
            t[i + 1] = t[i] + self.h
            y[i + 1] = self.y_0 * np.cos(self.w * i * self.h)
            ydot[i + 1] = -self.w * self.y_0 * np.sin(self.w * i * self.h)
            ydotdot[i + 1] = -self.w ** 2 * self.y_0 * np.cos(self.w * i * self.h)

        return t, y, ydot, ydotdot

    def excitation_force(self, ydotdot):
        return -self.m * self.g - self.m * ydotdot

    def net_displacement(self, x, y):
        return x - y

    def run_simulation(self, n):
        t, y, ydot, ydotdot = self.simple_harmonic_motion(n)
        F = self.excitation_force(ydotdot)
        z = np.zeros(n)

        for i in range(n - 1):
            k1, m1 = self.f1(z[i], ydot[i], t[i], F[i]), self.f2(z[i], ydot[i], t[i], F[i])
            k2, m2 = self.f1(z[i] + 0.5 * self.h * k1, ydot[i] + 0.5 * self.h * m1, t[i] + 0.5 * self.h,
                             F[i] + 0.5 * self.h), self.f2(z[i] + 0.5 * self.h * k1, ydot[i] + 0.5 * self.h * m1,
                                                           t[i] + 0.5 * self.h, F[i] + 0.5 * self.h)
            k3, m3 = self.f1(z[i] + 0.5 * self.h * k2, ydot[i] + 0.5 * self.h * m2, t[i] + 0.5 * self.h,
                             F[i] + 0.5 * self.h), self.f2(z[i] + 0.5 * self.h * k2, ydot[i] + 0.5 * self.h * m2,
                                                           t[i] + 0.5 * self.h, F[i] + 0.5 * self.h)
            k4, m4 = self.f1(z[i] + self.h * k3, ydot[i] + self.h * m3, t[i] + self.h, F[i] + self.h), \
                     self.f2(z[i] + self.h * k3, ydot[i] + self.h * m3, t[i] + self.h, F[i] + self.h)

            z[i + 1] = z[i] + ((self.h / 6) * (k1 + 2 * k2 + 2 * k3 + k4))
            ydot[i + 1] = ydot[i] + ((self.h / 6) * (m1 + 2 * m2 + 2 * m3 + m4))

        P = self.calculate_power_output(ydot)
        return t, P, z

    def calculate_power_output(self, ydot):
        ce = self.electrical_damping()
        return (self.rl * ce * ydot ** 2) / (self.rl + self.rc)

    def f1(self, z, u, t, F):
        return u

    def f2(self, z, u, t, F):
        k, ce = self.spring_stiffness(), self.electrical_damping()
        return (self.m ** (-1)) * (F - (self.c + ce) * u - k * z)

    def analyse_results(self, t, P, z):
        P_set = P[102:]
        P_max = max(P_set)
        print('Simulation results:')
        print('Maximum power output is = ', P_max, 'W')

        rms = np.sqrt(np.mean(P ** 2))
        print('RMS power output is =', rms, 'W')

        z_set = z[102:]
        print('Maximum displacement (after 10 sec) is = ', max(z_set), 'm')
        print('Maximum displacement is = ', max(z), 'm')
        self.plot_results(t, P, z)

    def plot_results(self, t, P, z):
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

        plt.show()


if __name__ == "__main__":
    system = EnergyHarvester(m=0.41, w=11.99, c=0.1, rl=0.5, rc=0.5, alpha=0.1992, y_0=0.01)
    system.print_model_parameters()
    system.electrical_damping()
    system.time_step()
    n_steps = 1000
    t, P, z = system.run_simulation(n_steps)
    system.analyse_results(t, P, z)
