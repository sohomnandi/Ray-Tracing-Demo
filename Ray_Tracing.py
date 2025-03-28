# pylint: disable=no-member

import pygame     # Import libraries
import numpy as np
import math
import sys, os

# Function to handle resource paths in executable mode
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temporary folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Initialize the game engine

pygame.init() 

# SECTION A: Definition of objects and properties
# -------------------------------------------------------------

# Define Screen Size
WIDTH, HEIGHT = 900, 800
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
move_speed = 7.0

# Define Light Source Parameters
light_position = np.array([150.0, 100.0])
light_radius = 8
light_move_speed = 7.0

# Define Rays Parameters
num_rays = 1000
ray_width = 1

# Load Icon
ICON_PATH = resource_path("lightning.ico")
icon = pygame.image.load(ICON_PATH)
icon = pygame.transform.scale(icon, (60, 60))  # Increase icon size
pygame.display.set_icon(icon)

# UI Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ray Tracing Simulator")
clock = pygame.time.Clock()
FPS = 60
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 130, 180)
ERROR_COLOR = (255, 69, 0)  # Error text color

# Fonts
title_font = pygame.font.SysFont("Arial", 48)
label_font = pygame.font.SysFont("Arial", 24)
input_font = pygame.font.SysFont("Arial", 20)

# Default Parameters
params = {
    "FPS": 60,
    "Sphere Radius": 50,
    "Sphere Speed": 7,
    "Light Radius": 8,
    "Light Speed": 7,
    "Number of Rays": 1000,
    "Ray Width": 1
}
input_boxes = []  # For dynamic inputs
active_input = None
input_texts = {key: str(value) for key, value in params.items()}
error_message = ""

# Utility Function
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Main UI Loop
def show_ui():
    global active_input, input_texts, error_message
    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_text("RAY TRACING SIMULATOR", title_font, TEXT_COLOR, 120, 40)
        screen.blit(icon, (50, 20))  # Adjusted icon position

        # Display input fields
        y_offset = 150
        input_boxes.clear()  # Clear previous boxes
        for i, (label, value) in enumerate(params.items()):
            draw_text(label + ":", label_font, TEXT_COLOR, 150, y_offset + 40 * i)
            rect = pygame.Rect(350, y_offset + 40 * i, 200, 30)
            pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=5)
            color = TEXT_COLOR if active_input != label else (0, 255, 0)
            draw_text(input_texts[label], input_font, color, 360, y_offset + 40 * i)
            input_boxes.append((label, rect))

        # Instructions
        draw_text("Controls: Arrow Keys to Move Sphere, WASD to Move Light", input_font, TEXT_COLOR, 120, y_offset + 40 * len(params) + 20)

        # Display error message if present
        if error_message:
            draw_text(error_message, input_font, ERROR_COLOR, 150, y_offset + 40 * len(params) + 50)

        # Draw Start Simulation Button
        start_button = pygame.Rect(300, y_offset + 40 * len(params) + 100, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, start_button, border_radius=5)
        draw_text("Start Simulation", label_font, TEXT_COLOR, 310, y_offset + 40 * len(params) + 110)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    try:
                        params.update({k: (int(v) if v.replace('.','',1).isdigit() else float(v)) for k, v in input_texts.items()})
                        error_message = ""
                        running = False  # Proceed to simulation
                    except ValueError:
                        error_message = "Invalid input detected! Ensure all values are numeric."
                for label, rect in input_boxes:
                    if rect.collidepoint(event.pos):
                        active_input = label
            if event.type == pygame.KEYDOWN and active_input is not None:
                if event.key == pygame.K_RETURN:
                    try:
                        params.update({k: (int(v) if v.replace('.','',1).isdigit() else float(v)) for k, v in input_texts.items()})
                        error_message = ""
                        running = False  # Proceed to simulation
                    except ValueError:
                        error_message = "Invalid input detected! Ensure all values are numeric."
                elif event.key == pygame.K_BACKSPACE:
                    input_texts[active_input] = input_texts[active_input][:-1]
                else:
                    input_texts[active_input] += event.unicode

        pygame.display.flip()
        clock.tick(FPS)

# Call UI First
show_ui()

# Map Parameters to Variables
FPS = params["FPS"]
sphere_radius = params["Sphere Radius"]
move_speed = params["Sphere Speed"]
light_radius = params["Light Radius"]
light_move_speed = params["Light Speed"]
num_rays = params["Number of Rays"]
ray_width = params["Ray Width"]

print("Proceeding to Simulation...")

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

    for i in range(num_rays):
        angle = 2 * math.pi * i / num_rays
        D = np.array([math.cos(angle), math.sin(angle)])  # Direction vector

        # Compute boundary intersection safely
        t_bound = ray_screen_boundary(light_position, D)
        if t_bound is None or not np.isfinite(t_bound) or t_bound <= 0:
            continue

        # Compute sphere intersection safely
        t_int = ray_circle_intersection(light_position, D, sphere_center, sphere_radius)

        # Determine the final intersection point
        t_final = t_int if t_int is not None and 0 < t_int < t_bound else t_bound

        # Ensure t_final is valid
        if not np.isfinite(t_final) or t_final <= 0:
            continue

        # Calculate end point
        end_point = light_position + t_final * D

        # Clamp end_point to stay within screen boundaries
        end_point = np.clip(end_point, [0, 0], [WIDTH, HEIGHT])

        # Draw the ray
        start_pos = tuple(light_position.astype(int))
        end_pos = tuple(end_point.astype(int))
        pygame.draw.line(screen, LIGHT_RAY_COLOR, start_pos, end_pos, ray_width)

    # Draw the sphere
    pygame.draw.circle(screen, SPHERE_COLOR, tuple(sphere_center.astype(int)), int(sphere_radius))

    # Draw the light source if not overlapping
    if np.linalg.norm(sphere_center - light_position) > (sphere_radius + light_radius):
        pygame.draw.circle(screen, LIGHT_COLOR, tuple(light_position.astype(int)), light_radius)

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
        velocity = np.array([-move_speed, 0.0])
    elif keys[pygame.K_RIGHT]:
        velocity = np.array([move_speed, 0.0])
    elif keys[pygame.K_UP]:
        velocity = np.array([0.0, -move_speed])
    elif keys[pygame.K_DOWN]:
        velocity = np.array([0.0, move_speed])
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

    # Control movement using WASD for the light source
    # We check if moving will keep the light within the boundaries.
    if keys[pygame.K_a] and (light_position[0] - light_move_speed >= 0):
        light_position[0] -= light_move_speed
    if keys[pygame.K_d] and (light_position[0] + light_move_speed <= WIDTH):
        light_position[0] += light_move_speed
    if keys[pygame.K_w] and (light_position[1] - light_move_speed >= 0):
        light_position[1] -= light_move_speed
    if keys[pygame.K_s] and (light_position[1] + light_move_speed <= HEIGHT):
        light_position[1] += light_move_speed

    draw_scene()    # Draw the scene

pygame.quit()       # Exit the program

