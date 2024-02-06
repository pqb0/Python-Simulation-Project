#include "raylib.h"
#include <vector>
#include <cmath>



inline
Camera InitCamera(){
    Camera mycamera = { 0 };
    mycamera.position = (Vector3){ 10.0f, 10.0f, 10.0f };
    mycamera.target = (Vector3){ 0.0f, 0.0f, 0.0f };
    mycamera.up = (Vector3){ 0.0f, 1.0f, 0.0f };
    mycamera.fovy = 45.0f;

    return mycamera;
}

inline
void DrawContainer(float cube[6]){

    DrawCubeWires( {cube[0], cube[1], cube[2]} ,cube[3] , cube[4], cube[5] , BLACK);
}

struct Ball{

    Vector3 position;
    Vector3 velocity;
    float radius;
    int mass;
    Color color;
};

inline
void DrawBall(Ball ball1){

    DrawSphere(ball1.position,  ball1.radius,  ball1.color);


}

inline
void CollisionUpdate(Ball *ball1){
     if (ball1 -> position.y  < -2 + ball1 -> radius) {
        ball1 -> position.y += 0.1;
        ball1 ->  velocity.y *= -0.95;

    }else if (ball1 -> position.y > 6 - ball1 -> radius) {
        ball1 -> position.y += -0.1;
        ball1 -> velocity.y *= -0.95;
    }

    if (ball1 -> position.z > 4 - ball1->radius  ){
        ball1 -> position.z -= 0.1;
        ball1 -> velocity.z *= -1;

    } else if (ball1 -> position.z < - 4 + ball1->radius){
        ball1 -> position.z += 0.1;
        ball1 -> velocity.z *= -1;
    }

     if (ball1 -> position.x > 4 - ball1->radius  ){
        ball1-> position.x -= 0.1;
        ball1 -> velocity.x *= -1;

    } else if (ball1 -> position.x < - 4 + ball1->radius){
        ball1-> position.x += 0.1;
        ball1 -> velocity.x *= -1;
    }

}




inline
float forceMagnitudeUpdate(float distance, Ball ball1, Ball ball2, float Gstrength, float maxDistance)
 {
    if (distance > 3*(ball1.radius + ball2.radius) and distance < maxDistance)
                {
                // Calculate gravitational force
                float forceMagnitude = Gstrength * ball2.mass / (distance * distance);

                return forceMagnitude;
                } else { return 0; }
 }  


inline void UpdateAcceleration(std::vector<Ball> &balls)
 {
    float G = 0.3f; // Gravitational constant

    // gravitational strength condition
        bool mega_Gstrength = false;
    if (IsKeyDown(KEY_G))
        {
        G = 3.0f;
        }
    if (IsKeyUp(KEY_G))
        {
        G = 0.3f;
        }
    if (IsKeyDown(KEY_ZERO))
        {
        G = 0;
        }
    if (IsKeyUp(KEY_ZERO))
        {
        G = 0.3f;
        }


    // merging condition
        bool merging = false;
    if (IsKeyDown(KEY_M))
        {
        merging = true;
        }
    if (IsKeyUp(KEY_M))
        {
        merging = false;
        }

    for (int i = 0; i < balls.size(); i++) {
        Ball &ball1 = balls[i];

        for (int j = 0; j < balls.size(); j++) {
            if (i != j) { // Skip self-interaction
                Ball &ball2 = balls[j];

                // Calculate distance and direction between ball1 and ball2
                float dx = ball2.position.x - ball1.position.x;
                float dy = ball2.position.y - ball1.position.y;
                float dz = ball2.position.z - ball1.position.z;

                float distance = sqrt(dx * dx + dy * dy + dz * dz);

                    float maxDistance = 8.0 / balls.size() ;
                    float forceMagnitude = forceMagnitudeUpdate(distance , ball1, ball2, G, maxDistance + 2);
                    // Calculate acceleration components
                    float accelerationX = forceMagnitude * dx / distance ;
                    float accelerationY = forceMagnitude * dy / distance ;
                    float accelerationZ = forceMagnitude * dz / distance ;
                    // Update ball1's velocity (acceleration vector)
                    ball1.velocity.x += accelerationX * 0.8;
                    ball1.velocity.y += accelerationY * 0.8;
                    ball1.velocity.z += accelerationZ * 0.8;

                    if (distance < maxDistance - ball1.radius and distance > 4 * (ball1.radius + ball2.radius)){
                    ball1.velocity.x *= 0.9;
                    ball1.velocity.y *= 0.9;
                    ball1.velocity.z *= 0.9;
                    }
                if (merging){

                    if (distance < ball1.radius + ball2.radius)
            {
                // Compare masses to determine which particle is larger
                if (ball1.mass > ball2.mass)
                {
                    // Update velocity with a weighted average
                    ball1.velocity = {
                        (ball1.velocity.x * ball1.mass + ball2.velocity.x * ball2.mass) /
                        (ball1.mass + ball2.mass),
                        (ball1.velocity.y * ball1.mass + ball2.velocity.y * ball2.mass) /
                        (ball1.mass + ball2.mass)
                    };

                    // Increase the radius of the larger particle

                    while (ball1.radius < ball1.radius + ball2.radius / 3) {
                    ball1.radius += 0.1;
                    break;
                    }

                    // Increase mass
                    ball1.mass += ball2.mass;

                    // Erase the smaller particle
                    balls.erase(balls.begin() + j);
                }
                else
                {
                    // Update velocity with a weighted average
                    ball2.velocity = {
                        (ball2.velocity.x * ball2.mass + ball1.velocity.x * ball1.mass) /
                        (ball2.mass + ball1.mass),
                        (ball2.velocity.y * ball2.mass + ball1.velocity.y * ball1.mass) /
                        (ball2.mass + ball1.mass)
                    };

                    while (ball2.radius < ball1.radius + ball2.radius / 3) {
                    ball2.radius += 0.1;
                    break;
                    }
                    

                    // Increase mass
                    ball2.mass += ball1.mass;

                    // Erase the smaller particle
                    balls.erase(balls.begin() + i);
                }
                
            }
            }
        }
    }
}
 }

inline 
void UpdatePosition(Ball *ball1, std::vector<Ball> &balls){

    float delta = GetFrameTime();
    ball1 -> position.x += ball1 -> velocity.x * delta;
    ball1 -> position.y += ball1 -> velocity.y * delta;
    ball1 -> position.z += ball1 -> velocity.z * delta;

   
    CollisionUpdate(ball1);

   

    
}

inline
void generateBalls(std::vector<Ball> &balls)
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
                Ball ball;

                ball.position = {(float)GetRandomValue(-4 + ball.radius, 4 - ball.radius), (float)GetRandomValue(0,  6 - ball.radius),
                                 (float)GetRandomValue(-4 + ball.radius, 4 - ball.radius) };               
                ball.velocity = {0, 0};
                ball.radius = 0.1;
                ball.color = balls[0].color;
                ball.mass = 5;


                balls.push_back(ball);
            }


}
