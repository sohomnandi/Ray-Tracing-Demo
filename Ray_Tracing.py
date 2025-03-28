# pylint: disable=no-member

import pygame     # Import libraries
import numpy as np
import math

# Initialize the game engine

pygame.init() 

# SECTION A: Definition of objects and properties
# -------------------------------------------------------------

# Define Screen Size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Tracing Demo")

# Get a clock
clock = pygame.time.Clock()
FPS = 60    # Set the FPS Accordingly

# Define Colors (RGB Values)
BG_COLOR = (0, 0, 0)
LIGHT_RAY_COLOR = (255, 220, 100)
SPHERE_COLOR = (100, 200, 255)
LIGHT_COLOR = (255, 255, 150)

# Define Sphere Parameters
sphere_center = np.array([400.0, 300.0])
sphere_radius = 50.0
move_speed = 5
velocity = np.array([5.0, 5.0])  # Ball velocity

# Define Light Source Parameters
light_position = np.array([150.0, 100.0])
light_radius = 8

# Define Rays Parameters
num_rays = 1000
ray_width = 1

# SECTION B: Math Formalizations and Ray Tracing Implementations
# -------------------------------------------------------------

# Function to calculate the intersection of a ray with a sphere
def ray_circle_intersection(L, D, C, r):
    """
    Compute intersection between ray (L + t*D) and circle (center of circle C, radius of circle r).
    Returns the smallest positive t if an intersection occurs, else None.
    L is the Origin point of the ray, D is the Direction vector of the ray.
    """
    # Compute the distance from the ray origin to the sphere center
    OC = L - C              # Vector from the ray origin to the sphere's center

    # Bringing all into a Quadratic equation form
    # a, b, c are the terms of the quadratic equation

    a = np.dot(D, D)            # As D is a unit vector, a = 1 and is normalized to
    b = 2.0 * np.dot(OC, D)     # b = 2 * (OC . D)
    c = np.dot(OC, OC) - r**2   # c = (OC . OC) - r^2

    # Compute discriminant
    discriminant = b**2 - 4.0*a*c
    if discriminant < 0:
        return None
    
    # Compute the smallest positive t
    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2 * a)      # 1st Root
    t2 = (-b + sqrt_disc) / (2 * a)      # 2nd Root
    t = None

    if t1 > 1e-3 and t2 > 1e-3:
        t = min(t1, t2)
    elif t1 > 1e-3:
        t = t1
    elif t2 > 1e-3:
        t = t2
    return t
    

# Function to calculate the intersection of a ray with the screen boundary
def ray_screen_boundary(L, D):
    """
    Find t such that L + t*D lies on one of the screen boundaries.
    Checks intersections with x=0, x=WIDTH, y=0, and y=HEIGHT,
    then returns the smallest positive t.
    """
    ts = []

    # Vertical boundaries
    if D[0] != 0:
        t_left = (0 - L[0]) / D[0]
        t_right = (WIDTH - L[0]) / D[0]
        if t_left > 0:
            ts.append(t_left)
        if t_right > 0:
            ts.append(t_right)

    # Horizontal boundaries
    if D[1] != 0:
        t_top = (0 - L[1]) / D[1]
        t_bottom = (HEIGHT - L[1]) / D[1]
        if t_top > 0:
            ts.append(t_top)
        if t_bottom > 0:
            ts.append(t_bottom)
    return min(ts) if ts else None


# SECTION C: Ray Tracing and Rendering for a Scene View
# -------------------------------------------------------------

def draw_scene():
    # Clear the screen
    screen.fill(BG_COLOR)

    # Draw many light rays emanating from the light source
    for i in range(num_rays):
        angle = 2 * math.pi * i / num_rays
        D = np.array([math.cos(angle), math.sin(angle)]) # Normalize Direction Vector

        # Determine where this ray would end at the screen boundary.
        t_bound = ray_screen_boundary(light_position, D)
        end_point = light_position + t_bound * D if t_bound is not None else light_position

        # Check for an intersection with the sphere
        t_int = ray_circle_intersection(light_position, D, sphere_center, sphere_radius)
        if t_int is not None and t_int < t_bound:
            end_point = light_position + t_int * D
        
        # Draw the ray from the light source to the end point.
        pygame.draw.line(screen, LIGHT_RAY_COLOR, light_position.astype(int), end_point.astype(int), ray_width)

    # Draw the sphere (Which blocks the rays).
    pygame.draw.circle(screen, SPHERE_COLOR, sphere_center.astype(int), int(sphere_radius))

    # Only draw the light source it its circle is not overlapped by the sphere.
    # Check if the distance between centers is greater that the sum of radii.
    if np.linalg.norm(sphere_center - light_position) > (sphere_radius + light_radius):
        pygame.draw.circle(screen, LIGHT_COLOR, light_position.astype(int), light_radius)

    pygame.display.flip()


# SECTION D: Main Loop
# -------------------------------------------------------------

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control movement using arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        velocity = np.array([-5.0, 0.0])
    elif keys[pygame.K_RIGHT]:
        velocity = np.array([5.0, 0.0])
    elif keys[pygame.K_UP]:
        velocity = np.array([0.0, -5.0])
    elif keys[pygame.K_DOWN]:
        velocity = np.array([0.0, 5.0])
    else:
        velocity = np.array([0.0, 0.0])  # Stop movement when no key is pressed

    # Move sphere based on velocity
    sphere_center += velocity

    # Prevent the ball from going past the edges
    if sphere_center[0] - sphere_radius <= 0:
        sphere_center[0] = sphere_radius
    elif sphere_center[0] + sphere_radius >= WIDTH:
        sphere_center[0] = WIDTH - sphere_radius

    if sphere_center[1] - sphere_radius <= 0:
        sphere_center[1] = sphere_radius
    elif sphere_center[1] + sphere_radius >= HEIGHT:
        sphere_center[1] = HEIGHT - sphere_radius

    draw_scene()    # Draw the scene

pygame.quit()       # Exit the program

