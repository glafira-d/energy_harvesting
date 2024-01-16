# Electromagnetic energy harvesting device simulation
## Purpose
The script in this project simulates the behavior of an electromagnetic energy harvesting (EH) device. The device is an electromechanical mass-spring-damper system. The mass (magnet) is connected to a base through a spring and damper. The base undergoes simple harmonic motion, causing excitation forces on the mass. Additionally, an electrical circuit is involved, where the coil resistance, load resistance, and the rate of change of magnetic flux with respect to displacement are considered. 

The power output and net mass displacement are calculated, which can be used in **_sizing and performance evaluation of a theoretical EH device._** 

The script and commentary for this project are an adaptation of my MSc research thesis "Energy harvesting for aircraft fuel system level-sensing applications", in which I assessed the feasibility of an electromagnetic EH device as a power source for a typical fuel level sensor in aircraft fuel tanks. Please contact me if you have any questions or would like to cite in your work at glafira.d@gmail.com

## Background
### Equation of motion
Energy harvesting is “the conversion of ambient energy present in the environment into electrical energy” (Kazmierski and Beeby, 2011). Interest in the development of EH technologies is often accredited to the rise of demand for wireless electronic systems, where it is widely regarded as a solution for replacing finite energy sources, i.e. batteries (Bai et al., 2018; O'Mathuna et al., 2007; Anton and Sodano, 2007).

Electromagnetic EH is based on Faraday’s law, where the induction of a current, and subsequently electromotive force, occurs as a result of the mechanical motion of a magnet relative to a stationary coil, or the coil relative to a stationary magnet, which causes a change in magnetic flux. The amount of output electrical energy depends on the length of the coil, i.e. the number of turns, as well as the strength of the magnetic field, and the velocity of the coil’s movement in the magnetic field (Spies, Pollak and Mateu, 2015; Rastegar and Dhadwal, 2017).

Figure 1 is a schematic representation of a common electromagnetic-based transduction system, where one can observe the two characteristic components: magnet and conductor (i.e. coil). In this case, the conductor is stationary, and the magnet is positioned inside it and moves relative to the coil in order to induce an electromotive force. 

<img height="150" src="img/Screenshot 2024-01-11 at 16.48.57.png"/>

*Figure 1: Schematic of an electromagnetic induction transducer (Rastegar and Dhadwal, 2017).*

Electromagnetic transducers are commonly modelled as spring-mass-damper systems, which is an approach that largely rests on the fundamental work of Williams and Yates (1996). The spring-mass-damper model is used to describe the mechanical element of the energy harvester. The electrical element is modelled as an additional damping term. Therefore, the governing differential equation of motion of the resulting linear single degree-of-freedom system is:

<img height="30" src="img/Screenshot 2024-01-11 at 17.35.15.png"/>

where m is the mass, g is the gravity, c is damping, k is the spring stiffness, and Fe is the force on the mass due to the electromagnetic coupling; z(t) is the relative displacement and is defined as z=x-y, where x is the displacement of the mass and y is the base displacement; ce is the additional damping term defining the electrical component of the harvester. 

<img height="150" src="img/Screenshot 2024-01-11 at 18.15.47.png" />

*Figure 2: Schematic of electromagnetic generator device – adapted from (Hadas et al., 2008)*

Figure 2 shows the model parameters and the respective components of the generator they are associated with. RL is the load resistance, RC – coil resistance, Ф – magnetic flux through a fixed coil of inductance L. Hence, the left-hand side of the schematic is the electrical circuit, featuring a fixed coil, connected to the mechanical spring-mass-damper system, the relative motion of which results in a magnetic flux to be generated, that in turn induces a current in the circuit by the effect of Faraday’s law (Hadas et al., 2008).  

The right-hand side of the equation of motion is the force that excites the system, where the base displacement is a result of that. The base displacement is defined as:

<img height="30" src="img/Screenshot 2024-01-12 at 00.18.32.png"/>

where Y0 is the amplitude of base excitation, omega is the frequency of forced excitation, and t is the time. It follows that the excitation force is sinusoidal and is defined as:

<img height="30" src="img/Screenshot 2024-01-12 at 00.20.59.png"/>

It is important to define the resonant (natural) frequency of the energy harvester. This is different from the frequency of base excitation, and is defined as:

<img height="50" src="img/Screenshot 2024-01-12 at 00.21.58.png"/>

Evaluating the performance of the system is done via solution of the equation of motion, i.e. via finding the **_resulting relative displacement of the mass, and, consequently, the power output generated._**

To find the power output we use Faraday's law, which states that the induced electromotive force (emf) is equal to the rate of change of magnetic flux:

<img height="60" src="img/Screenshot 2024-01-16 at 20.39.13.png"/>

where z_dot is the velocity of the oscillating magnet. 

Equating the power originating in the mechanical (left-hand side) and electrical (right-hand side) components:

<img height="40" src="img/Screenshot 2024-01-16 at 20.41.14.png"/>

where i is the current present in the coil. Then, the two equations can be manipulated to obtain the expression for Fe:

<img height="60" src="img/Screenshot 2024-01-16 at 20.43.03.png"/>

From Kirchoff's voltage rule:

<img height="40" src="img/Screenshot 2024-01-16 at 20.44.12.png"/>

The inductance, L is negligible in low frequency scenarios. Re-writing using expression for Fe:

<img height="40" src="img/Screenshot 2024-01-16 at 20.47.43.png"/>

Current (i) term cancels out, and electrical force is then equal to: 

<img height="50" src="img/Screenshot 2024-01-16 at 20.53.28.png"/>

where alpha = dФ/dz. Therefore, substituting the resulting expression for Fe, electrical power can be found:

<img height="50" src="img/Screenshot 2024-01-16 at 20.55.45.png"/>

From this, the electrical power supplied to the load is given by:

<img height="50" src="img/Screenshot 2024-01-16 at 20.58.17.png"/>

Since electrical damping is given by:

<img height="50" src="img/Screenshot 2024-01-16 at 20.58.49.png"/>

The expression for P_load becomes (Green et al., 2012):

<img height="50" src="img/Screenshot 2024-01-16 at 20.59.32.png"/>

### Numerical solution
To solve for displacement we use 4th order Runge-Kutta (RK4) numerical integration method. To find the power output we also need to find the velocity of the magnet. 

The 4th order Runge-Kutta technique is an approximation method for solving ordinary differential equations (ODEs), especially useful for dynamic systems analysis. Other lower-order numerical integration methods exist, such as the Euler’s method and the 2nd order Runge-Kutta method. However, the lower-order techniques are known to produce a higher degree of error. Moreover, RK4 has the additional benefit of higher computational stability, which becomes important when more complicated systems are considered (Beamer, 2013; Suli and Mayers, 2003).

For a general differential equation of the form

<img height="30" src="img/Screenshot 2024-01-16 at 21.12.26.png"/>

RK4 requires the following:

<img height="100" src="img/Screenshot 2024-01-16 at 21.13.10.png"/>

where p terms define the increments used for the estimation, h is the step size, and i = 0, 1, 2, 3,..., so that y_0 = y(t=0) = 0 and t_(i+1) = t_i + h.

The solution for y is then estimated as (Beamer, 2013):

<img height="50" src="img/Screenshot 2024-01-16 at 21.17.43.png"/>

In order to apply RK4 to the second-order equation of motion of the spring-mass-damper system, we transform it into a system of first-order ODEs. In order to do that, the variables are redefined using a new variable u as follows:

<img height="60" src="img/Screenshot 2024-01-16 at 21.21.32.png"/>

where F has been defined to equal the right-hand side of the equation.

Substituting this into the equation of motion:

<img height="40" src="img/Screenshot 2024-01-16 at 21.24.44.png"/>

After re-arranging for u_dot, two first-order ODEs with two variables are obtained:

<img height="70" src="img/Screenshot 2024-01-16 at 21.26.21.png"/>

This can be evaluated as a system of equations by applying RK4 separately to each. Hence, the solution will take the following form:

<img height="300" src="img/Screenshot 2024-01-16 at 21.27.58.png"/>

which is also for i = 0, 1, 2, 3,..., with initial conditions:

<img height="60" src="img/Screenshot 2024-01-16 at 21.29.25.png"/>

As the next step, the power output generated is calculated, according to theory outlined earlier, using the result for velocity of the displaced magnet.

## How to use
The script in this project is a simulation tool, which uses parameters of an electromagnetic EH device as inputs, and outputs displacement of the magnet, maximum power and RMS power. 

To run the script, enter numerical values for parameters, where object of class EnergyHarvester is created as follows:

    system = EnergyHarvester(m=0.41, w=11.99, c=0.1, rl=0.5, rc=0.5, alpha=0.1992, y_0=0.01)

The main parameters to change are: magnet mass (m) and the natural resonant frequency of the harvester (w). 

Maximum power is generated by an energy harvester when excited by vibrations of equal frequency to the natural frequency of the device itself (Kazmierski and Beeby, 2011). Therefore, w is equal to the frequency of ambient vibration that is expected to excite the EH device.

In this case Load resistance, Coil resistance, Rate of change of magnetic flux are literature values from (Green et al., 2013). Damping was chosen based on two values found in literature. Two experimental values for damping are given in (Banerjee, 2016) for a model that does not incorporate friction (which is reflective of the current model): c = 0.116 Ns/m and c = 0.079 Ns/m. Therefore, a value of 0.1 Ns/m is considered reasonable.

The script also allows to specify the desired number of time steps to run the simulation for (n_steps). 

The tool prints the input parameters and the simulation results, as well as shows plots of displacement and power output for the number of time steps specified, which look like:  

<img height="300" src="img/Screenshot 2024-01-16 at 22.28.45.png"/>

## Dependencies
Python 3.11

## References
Anton, S.R. and Sodano, H.A. 2007, "A review of power harvesting using piezoelectric materials (2003-2006)", Smart Materials and Structures, vol. 16, no. 3, pp. R1-R21.

Bai, Y., Jantunen, H. and Juuti, J. 2018, "Energy harvesting research: The road from single source to multisource", Advanced Materials, vol. 30, no. 34.

Beamer, K. (2013). Runge-Kutta - Numerical Solutions of Differential Equations. [ebook] Available at: http://www.ujfi.fei.stuba.sk/fyzika-ballo/Runge-Kutta.pdf.

Green, P., Worden, K., Atallah, K. and Sims, N. (2012). The benefits of Duffing-type nonlineari- ties and electrical optimisation of a mono-stable energy harvester under white Gaussian excitations. Journal of Sound and Vibration, 331(20), pp.4504-4517.

Hadas, Z., Zouhar, J., Singule, V. & Ondrusek, C. 2008, "Design of energy harvesting generator base on rapid prototyping parts", 2008 13th International Power Electronics and Motion Control Conference, EPE-PEMC 2008, September 1, 2008 - September 3IEEE Computer Society, Poznan, Poland, 2008, pp. 1665.

Kazmierski, T. and Beeby, S. (2011). Energy harvesting systems. Springer.

O'Mathuna, C.O., O’Donnell, T., Martinez-Catala, R., Rohan, J. & O’Flynn, B. 2008, "Energy scavenging for long-term deployable wireless sensor networks", Talanta, vol. 75, no. 3, pp. 613-623.

Rastegar, J. and Dhadwal, H. (2017). Energy harvesting for low-power autonomous devices and systems. Washington: SPIE Press. 

Spies, P., Pollak, M. & Mateu, L. 2015, Handbook of energy harvesting power supplies and applications, Pan Stanford Publishing Pte. Ltd.

Suli, E. and Mayers, D. (2003). An introduction to numerical analysis. Cambridge University Press.


