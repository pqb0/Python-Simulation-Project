# Python and c++ Simulation-Project

My portfolio includes 7 simulations I created based on physics explorations of interest.
Since I am taking IB Physics, many interesting topics have captivated my attention and I wanted to explore them with greater depth.
It was a matter of interest  which led to the development of my first project which was a planetary system with a center star.
The idea was simple but it implied combining my coding abilities with my knowledge of circular motion, gravitational forces and vector maths. 

I continued to develop my abilities and put into work a simulation for simple harmonic motion, exhibiting a pendulum in motion. It traces the path taken by the pendulum and can have mass, size, and length of rod. Furthermore I tried to study how a double pendulum works. looked at how Lagrangian mechanics is used to analyse the system, and made a simplified expression, to find angles for the pendulum.

Just recently I had to use matplotlib to solve a system of nonlinear ODEs to describe the populations of a preyand a predator in a controlled system. I designed a simple animation to compare the system with actual population statistics. This began as a method to study ODEs and familiarise myself with the coding conventions and understand the process of organising the information and graphing it.

Furthermore I used the same concept to study the double pendulum to solve the Lagrangian equations of motion to find expressions for the angles to the normal of each pendulum. The process involved deriving expressions for Kinetic and Potential energy in terms of the rod position and then using the Lagrangian to solve for the angles 1 and 2 in terms of time. However, I reduced the equation to suit a more convenient and controlled system where I could also hold each individual pendulum.

I make the projects because it first helped me get my mind off things, it distracted me from other important tasks and it also allowed me to grow more in the way I understand the topics I study at school. As a gamer, it also allowed me to explore a part of gaming I never thought of. Being able to visually describe my ideas based on mathematical intricateness really suited my personal interests. Initially I always thought coding would eventually come to my life, considering my curiosity for maths and sciences; it always seemed sequential when trying to operate numerically when doing an investigation. As a way to extend my limitations and capabilities, I try to keep looking for harder challenges and innovative techniques to keep outperforming myself every time: As a scientist, a mathematician and now a newborn programmer. 

For my simulations, I used Python as the programming language thanks to the programming course I took at UC Berkeley. I was presented with the idea of simulating my own physical world using the pygame module, and it is the one I have mainly used for the projects. I used VS Codium as my source-code editor because of its simple and user-friendly overlay which allowed me to get going quickly. Since I only began coding a few months ago, I had to develop my knowledge through other means because the college program was over. I began exploring different sources such as videos, discord servers, stack exchange and even decided to get Brilliant to help familiarize myself with the basics on algorithms and Python essentials. After a while it only felt natural that I should begin my own projects and so I started to create. Finally I share my project ideas with friends from the Berkeley course to help each improve.

Furthermore I extended my codign language by learning c++ because of the limitations on my computer and its inability to process python effectively. I downloaded the Raylib package for c++ and started to code similar simulations with more optimized quality. Furthermore I was able to extend to 3rd dimen sional projects as seen in my last project available.

 Python Projects:

 Single_Pendulum and Double_Pendulum: Using the mouse one can grab either of the pendulums and move it around and then let go.

 Orbits_star:   The simulation includes a star in the middle, and a controllable camera using WASD keys. Using the Down and Up arrow keys, one can zoom in and Out while there are no balls present. If the spacebar is pressed, a ball will spawn at the cursors position,  with its orbital velocity, to have a perfect orbit. If the C key is used, all the balls will disappear. If the 0 key is held down, the mass of the star will become 0, neglecting the effect of gravity. If the G key is pressed, the Gravitational field will increase drastically to suck all balls into the center, this can result in very nice patterns. Finally, the balls can be held by clicking the mouse button. If the ball is being held, Using the T  and Y key, one can increase and decrease the selected ball's size respectively. Finally if the ball is then let go it will lose its orbit velocity and will just oscillate back and forth.

Solar_System:   The simulation is a small depiction of our Solar system. It is inaccurate to relative size and distance but it helps to map all the planets and their relative moons with respect to the sun.

simulator: The code is based on a source code for javascript known as Particle Life Simulator, which uses attractive and repulsive forces to update different particle types using relations between the types. If the space bar is pressed, random particles spawn around the cursor. If the C key is pressed, all particles will dissapear. Using different combinations of relations and particle numbers, one can simulate very particular movements which may seem unpredictable or rather simple. The relation function takes in 2 particle and relates one to the other, either by attractive force or repulsive force by a factor between 0 and 1. Additionally it takes a maximum distance for the effect of the relation between particles.

Spaceship_Planets:    The SpaceshipCamara and Spaceship simulations inside the tests folder were the starting foundations for the SpaceshipPlanet simulation. The Simulation uses a spaceship to navigate around a small solar system consisting of 2 planets. One can fly around the sun and reach the other planets which are further away by using the propulsion provided by the space bar. Furthermore one can tilt the spaceship using the A and D Keys to change the direction of thrust.

Stream:      This simulation is rather simple. I was playing with projectiles and I decide to make a stream of particles which would shoot at my cursor when pressing Spacebar. I added a resistive force to slow down the particles and if the 0 button is held, then a boundary circle is inserted to delimit the movement of the particles. The circle provides energy to the particles with every collision, so the velocity of the particles  increases until breaking the simulation and creating a col spiral effect. While spawning new particles, the older particles will slowly get smaller until dissapearing. Furthermore, the particles can be all deleted at once using the C key.

C++ Projects (The c++ projects are in a second folder under the name "cppProjects"):

Planetary_simulation: It is a simulation in 3d of orbital gravitational motion using newtons gravitational force applying a frictive force and with different functionalities for different keys: The space button generates new balls/planets, The M button while pressed allows planets to merge, the C button clears all the planets, The "0" key disables gravitational fields and the G key strengthens the gravitational field strength.
