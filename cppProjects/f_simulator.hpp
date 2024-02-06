#include "raylib.h"
#include <vector>
#include <cmath>

const float screenWidth = 1200;
const float screenHeight = 650;







struct particle_struc
{
    Vector2 position;
    Vector2 velocity;
    float radius;
    Color color;
    int mass;
};

inline
void updateCam(Camera2D &camera, std::vector<float> &offset_velocity) {
    if (IsKeyDown(KEY_W)) offset_velocity[1] += 0.2f;  // Move up
    if (IsKeyDown(KEY_S)) offset_velocity[1] -= 0.2f;  // Move down
    if (IsKeyDown(KEY_A)) offset_velocity[0] += 0.2f;  // Move left
    if (IsKeyDown(KEY_D)) offset_velocity[0] -= 0.2f;  // Move right

    camera.offset.x += offset_velocity[0];
    camera.offset.y += offset_velocity[1];

    // Apply damping to smooth camera movement
    offset_velocity[0] *= 0.95;
    offset_velocity[1] *= 0.95;
}






inline
double forceMagnitudeUpdate(float distance, particle_struc particle1, particle_struc otherParticle, int maxDistance, float Gstrength)
 {
    if (distance > particle1.radius + otherParticle.radius && distance < maxDistance)
                {
                // Calculate gravitational force
                float forceMagnitude = Gstrength * otherParticle.mass / (distance * distance);

                return forceMagnitude;
                } else { return 0; }
 }  

inline
void updateParticles(std::vector<particle_struc> &particles1, std::vector<particle_struc> &particles2, float Gstrength, int maxDistance)
{
    for (particle_struc &particle1 : particles1)
    {
        // Update particle position and handle screen edges
        particle1.position.x += particle1.velocity.x;
        particle1.position.y += particle1.velocity.y; 

        //particle1.velocity.x *= 0.999;
       // particle1.velocity.y *= 0.999;


        if (particle1.position.x < particle1.radius || particle1.position.x > screenWidth - particle1.radius)
        {
            particle1.velocity.x *= - 0.9;
        }

        if (particle1.position.y < particle1.radius || particle1.position.y > screenHeight - particle1.radius)
        {
            particle1.velocity.y *= - 0.9;
        }

        for(particle_struc &otherParticle : particles2)
            { 

            // Calculate gravitational force if within range
            float dx = otherParticle.position.x - particle1.position.x;
            float dy = otherParticle.position.y - particle1.position.y;

            // Distance and Angle
            float distance = sqrt(dx * dx + dy * dy);
            float angle = atan2(dy, dx);
            float forceMagnitude = forceMagnitudeUpdate(distance,  particle1,  otherParticle,  maxDistance,  Gstrength);
                // Calculate direction of the force
            float accelerationX = forceMagnitude * cos(angle) ;
            float accelerationY = forceMagnitude * sin(angle) ;

            particle1.velocity.x += accelerationX;
            particle1.velocity.y += accelerationY;
            }
    }
}

inline
void mergeParticles(std::vector<particle_struc> &particles)
{
    for (size_t i = 0; i < particles.size(); ++i)
    {
        for (size_t j = i + 1; j < particles.size(); ++j)
        {
            float dx = particles[j].position.x - particles[i].position.x;
            float dy = particles[j].position.y - particles[i].position.y;
            float distance = sqrt(dx * dx + dy * dy);

                        if (distance < particles[i].radius + particles[j].radius - 4)
            {
                // Compare masses to determine which particle is larger
                if (particles[i].mass > particles[j].mass)
                {
                    // Update velocity with a weighted average
                    particles[i].velocity = {
                        (particles[i].velocity.x * particles[i].mass + particles[j].velocity.x * particles[j].mass) /
                        (particles[i].mass + particles[j].mass),
                        (particles[i].velocity.y * particles[i].mass + particles[j].velocity.y * particles[j].mass) /
                        (particles[i].mass + particles[j].mass)
                    };

                    // Increase the radius of the larger particle

                    while (particles[i].radius < particles[i].radius + particles[j].radius / 3) {
                    particles[i].radius += 1;
                    break;
                    }

                    // Increase mass
                    particles[i].mass += particles[j].mass;

                    // Erase the smaller particle
                    particles.erase(particles.begin() + j);
                }
                else
                {
                    // Update velocity with a weighted average
                    particles[j].velocity = {
                        (particles[j].velocity.x * particles[j].mass + particles[i].velocity.x * particles[i].mass) /
                        (particles[j].mass + particles[i].mass),
                        (particles[j].velocity.y * particles[j].mass + particles[i].velocity.y * particles[i].mass) /
                        (particles[j].mass + particles[i].mass)
                    };

                    while (particles[j].radius < particles[i].radius + particles[j].radius / 3) {
                    particles[j].radius += 1;
                    break;
                    }
                    

                    // Increase mass
                    particles[j].mass += particles[i].mass;

                    // Erase the smaller particle
                    particles.erase(particles.begin() + i);
                }
            }
        }
    }
}

inline
void drawParticles(std::vector<particle_struc> particles)
{
    for ( particle_struc &particle : particles)
    {
        DrawCircleV(particle.position, particle.radius, particle.color);
    }
}


inline
void generateParticles(std::vector<particle_struc> &particles)
{   bool generating = false;
    Vector2 mouse_coords = GetMousePosition();

    // Generating condition
    if (IsKeyDown(KEY_SPACE))
        {
        generating = true;
        }
    if (IsKeyUp(KEY_SPACE))
        {
        generating = false;
        }

    if (generating)
       
            {
                particle_struc particle;

                particle.position = {(float)GetRandomValue(-150, 150) + mouse_coords.x, (float)GetRandomValue(-150, 150 ) + mouse_coords.y};
                particle.velocity = {0, 0};
                particle.radius = 3;
                particle.color = particles[1].color;
                particle.mass = 4;

                particles.push_back(particle);
            }


        




}


inline
void InelasticCollision(particle_struc &obj1, particle_struc &obj2) {
    float v1x = obj1.velocity.x;
    float v1y = obj1.velocity.y;
    float m1 = obj1.mass;

    float v2x = obj2.velocity.x;
    float v2y = obj2.velocity.y;
    float m2 = obj2.mass;

    // Calculate final velocity after inelastic collision
    float v_final_x = (m1 * v1x + m2 * v2x) / (m1 + m2);
    float v_final_y = (m1 * v1y + m2 * v2y) / (m1 + m2);

    // Update both objects with the final velocity
    obj1.velocity.x = v_final_x;
    obj1.velocity.y = v_final_y;

    obj2.velocity.x = v_final_x;
    obj2.velocity.y = v_final_y;
}

inline
void collisionUpdate(std::vector<particle_struc> particles1, std::vector<particle_struc> particles2 )
        {
        for (int i = 0; i < particles1.size(); i++)
            {
            for (int j = 0; j < particles1.size(); j++)
                {
                InelasticCollision(particles1[i], particles2[j]);
                }
            }
        }