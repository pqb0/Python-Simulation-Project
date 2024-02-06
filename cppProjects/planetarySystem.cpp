#include "f_planetarySystem.hpp"
#include "raylib.h"
#include <vector>



std::vector<Ball> createBalls(Color color, int amount, float size)
{   
   

    std::vector<Ball> balls;

    for (int i = 0; i < amount; i++)
    {
        Ball ball;
        ball.position = {(float)GetRandomValue(-4 + ball.radius, 4 - ball.radius), (float)GetRandomValue(0,  6 - ball.radius),
                         (float)GetRandomValue(-4 + ball.radius, 4 - ball.radius) };
        ball.velocity = {0,0,0};
        ball.radius = size;
        ball.color = color;
        ball.mass = 5;

        balls.push_back(ball);
        
    }

    return balls;
}

int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 450;

  
   



    float cube1[6] = {0, 2, 0, 8, 8, 8};

    InitWindow(screenWidth, screenHeight, "3D Simulation");
    std::vector<Ball> balls = createBalls(BLUE, 10,0.1);

    Camera camera = InitCamera();


    SetTargetFPS(60);

    while (!WindowShouldClose())
    {


        // Clearing Ball list
        if (IsKeyDown(KEY_C))
        {
           balls.clear();
        }
    

        UpdateCamera(&camera, CAMERA_ORBITAL);
        // Draw
        BeginDrawing();
        ClearBackground(RAYWHITE);

        BeginMode3D(camera);

     
        generateBalls(balls);
        for (Ball  &ball1 : balls){

     
          UpdatePosition(&ball1, balls);
          DrawBall(ball1);
        }

        UpdateAcceleration(balls);
        

        
        DrawContainer(cube1);
       

        // Draw your 3D objects here

        EndMode3D();

        EndDrawing();
    }

    CloseWindow();

    return 0;
}
