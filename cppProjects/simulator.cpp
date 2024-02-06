#include "f_simulator.hpp"

std::vector<particle_struc> createParticles(Color color, int amount, int size)
{   
   

    std::vector<particle_struc> particles;

    for (int i = 0; i < amount; i++)
    {
        particle_struc particle;
        particle.position = {(float)GetRandomValue(10, screenWidth - 10), (float)GetRandomValue(10, screenHeight - 10)};
        particle.velocity = {0, 0};
        particle.radius = size;
        particle.color = color;
        particle.mass = 2;

        particles.push_back(particle);
        
    }

    return particles;
}

int main()
{
    Vector2 center {screenWidth / 2, screenHeight / 2};


    Camera2D camera = {0};
    std::vector<float> offset_velocity = {0,0};

    camera.offset = (Vector2){ 0, 0 };  // Initial position
    camera.target = (Vector2){ 0, 0 };  // Point the camera towards
    camera.rotation = 0.0f;            // Initial rotation
    camera.zoom = 1.0f;


   
    std::vector<particle_struc> blueParticles = createParticles(BLUE, 10, 3);
    std::vector<particle_struc> redParticles = createParticles(RED, 5, 4);
    std::vector<particle_struc> whiteParticles = createParticles(WHITE, 2, 3);

    std::vector<std::vector<particle_struc>> setOfAllParticles {blueParticles, redParticles};



    // Initialization
    InitWindow(screenWidth, screenHeight, "Simulation");
    

    
    // Main game loop
    while (!WindowShouldClose())
    {

        updateCam(camera , offset_velocity);       
        
        ClearBackground(BLACK);
        BeginDrawing();
       
       
        BeginMode2D(camera);


    updateParticles(whiteParticles, whiteParticles, 0.1, 50);

    drawParticles(blueParticles);
    drawParticles(whiteParticles);


            


        EndMode2D();
        EndDrawing();
    }
    // De-Initialization
    CloseWindow();
    return 0;
}
