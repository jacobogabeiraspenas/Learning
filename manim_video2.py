%%manim -qm --disable_caching TerrainSurfaceZoom
from manim import *
import numpy as np
import requests
from io import BytesIO
from PIL import Image


# Download the image from the URL
url = "https://github.com/jacobogabeiraspenas/Learning/blob/master/terrain.png?raw=true"
response = requests.get(url)
image = Image.open(BytesIO(response.content))
# Save the image temporarily
image.save("grenoble_map_temp.png")



# Load the terrain data
url = "https://raw.githubusercontent.com/jacobogabeiraspenas/Learning/master/hgt200.npy"
data = np.load(BytesIO(requests.get(url).content))
# Scale 1:2000
start1, stop1 = 52,172
start1, stop1 = 0,-1
nth = 20
terrain_data7 = (data[0,start1:stop1,start1:stop1][::nth, ::nth]) / 2000  # Extract a 10x10 section for context
# Set up x and y coordinates for the whole 10x10 grid
# Scale 1:2000
x_coords7 = np.linspace(-terrain_data7.shape[1]/2, terrain_data7.shape[1]/2, terrain_data7.shape[1])*nth / 10
y_coords7 = np.linspace(-terrain_data7.shape[0]/2, terrain_data7.shape[0]/2, terrain_data7.shape[0])*nth / 10

height_middle_unit = terrain_data7[int(terrain_data7.shape[0]/2),int(terrain_data7.shape[1]/2)]
terrain_data7 = terrain_data7 - height_middle_unit 


# Increase resolution
nth = 10
terrain_data4 = (data[0,start1:stop1,start1:stop1][::nth, ::nth]) / 2000  # Extract a 10x10 section for context
# Set up x and y coordinates for the whole 10x10 grid
# Scale 1:2000
x_coords4 = np.linspace(-terrain_data4.shape[1]/2, terrain_data4.shape[1]/2, terrain_data4.shape[1])*nth / 10
y_coords4 = np.linspace(-terrain_data4.shape[0]/2, terrain_data4.shape[0]/2, terrain_data4.shape[0])*nth / 10

height_middle_unit4 = terrain_data4[int(terrain_data4.shape[0]/2),int(terrain_data4.shape[1]/2)]
terrain_data4 = terrain_data4 - height_middle_unit4 

# All resolution
nth = 1
terrain_data1 = (data[0,start1:stop1,start1:stop1][::nth, ::nth]) / 2000  # Extract a 10x10 section for context
# Set up x and y coordinates for the whole 10x10 grid
# Scale 1:2000
x_coords1 = np.linspace(-terrain_data1.shape[1]/2, terrain_data1.shape[1]/2, terrain_data1.shape[1])*nth / 10
y_coords1 = np.linspace(-terrain_data1.shape[0]/2, terrain_data1.shape[0]/2, terrain_data1.shape[0])*nth / 10

height_middle_unit = terrain_data1[int(terrain_data1.shape[0]/2),int(terrain_data1.shape[1]/2)]
terrain_data1 = terrain_data1 - height_middle_unit 


# Load the terrain data
url = "https://raw.githubusercontent.com/jacobogabeiraspenas/Learning/master/hgt111.npy"
data = np.load(BytesIO(requests.get(url).content))
# Scale 1:2000
start2, stop2 = 142,262
start2, stop2 = 0,-1
start2, stop2 = 20,-21
nth = 1
terrain_data111 = (data[0,start2:stop2,start2:stop2][::nth, ::nth]) / 2000  # Extract a 10x10 section for context
# Set up x and y coordinates for the whole 10x10 grid
# Scale 1:2000
x_coords_111 = np.linspace(-terrain_data111.shape[1]/2, terrain_data111.shape[1]/2, terrain_data111.shape[1])*nth / 18
y_coords_111 = np.linspace(-terrain_data111.shape[0]/2, terrain_data111.shape[0]/2, terrain_data111.shape[0])*nth / 18

height_middle_unit = terrain_data111[int(terrain_data111.shape[0]/2),int(terrain_data111.shape[1]/2)]
terrain_data111 = terrain_data111 - height_middle_unit 

# Load the terrain data
url = "https://raw.githubusercontent.com/jacobogabeiraspenas/Learning/master/hgt111_42.npy"
data = np.load(BytesIO(requests.get(url).content))
# Scale 1:2000
nth = 1
terrain_data111s = (data[0,start2:stop2,start2:stop2][::nth, ::nth]) / 2000  # Extract a 10x10 section for context
terrain_data111s = terrain_data111s - height_middle_unit


# Define the Terrain Plot class
class TerrainSurfaceZoom(ThreeDScene):
    def construct(self):

        # Load the image in Manim
        background_image = ImageMobject("grenoble_map_temp.png")
        # Scale and position the image as needed
        background_image.move_to([0, 0, 0])
        background_image.set_width(22.5)
        background_image.set_height(22.5)
        # Add the image to the scene
        self.add(background_image)
        
        # Set initial camera orientation
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=0.5)
        self.wait(2)

        # Define color gradient range
        min_height, max_height = np.min(terrain_data7), np.max(terrain_data7)
        
        # Helper function to map height to color
        def height_to_color(height):
            alpha = (height - 0) / (4)  # normalize height
            return interpolate_color(BLUE, YELLOW, alpha)  # interpolates between BLUE (low) and YELLOW (high)


        color_matrix = np.array([
            [0.2, 0.2, 0.6, 1.0],
            [0.05359477, 0.49281046, 0.89281046, 1.0],
            [0.0, 0.73921569, 0.58235294, 1.0],
            [0.33333333, 0.86666667, 0.46666667, 1.0],
            [0.77254902, 0.9545098, 0.5545098, 1.0],
            [0.88627451, 0.85443137, 0.53858824, 1.0],
            [0.66666667, 0.57333333, 0.42, 1.0],
            [0.56078431, 0.43780392, 0.41145098, 1.0],
            [0.78039216, 0.71890196, 0.70572549, 1.0],
            [1.0, 1.0, 1.0, 1.0]
        ])
        
        # Function to map height to color using the custom colormap
        def height_to_color(height):
            alpha = (height - min_height) / (max_height - min_height)  # Normalize height
            index = int(alpha * (len(color_matrix) - 1))  # Map alpha to an index in the color matrix
            index = np.clip(index, 0, len(color_matrix) - 1)  # Ensure index is within bounds
            rgb = color_matrix[index][:3]  # Get the RGB values, ignoring alpha
            return rgb_to_color(rgb)  # Convert RGB to a Manim color


        # Generate the terrain surface using vertices from terrain data
        surface_mesh7 = VGroup()
        for i in range(len(y_coords7) - 1):
            for j in range(len(x_coords7) - 1):
                # Define vertices of each small quad
                p1 = np.array([x_coords7[j], y_coords7[i], terrain_data7[i, j]])
                p2 = np.array([x_coords7[j+1], y_coords7[i], terrain_data7[i, j+1]])
                p3 = np.array([x_coords7[j+1], y_coords7[i+1], terrain_data7[i+1, j+1]])
                p4 = np.array([x_coords7[j], y_coords7[i+1], terrain_data7[i+1, j]])

                # Calculate the average height for color interpolation
                avg_height = (terrain_data7[i, j] + terrain_data7[i, j+1] + terrain_data7[i+1, j+1] + terrain_data7[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad as a Polygon and add to surface mesh
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0.8, color=color)
                surface_mesh7.add(quad)

        # Display the full terrain initially
        self.play(Create(surface_mesh7),FadeOut(background_image),run_time=2)
        self.move_camera(phi=60 * DEGREES, theta=-120 * DEGREES, zoom=1, run_time=2)
        
        # Perform a full 360-degree loop around the Z-axis
        #self.move_camera(phi=60 * DEGREES, theta=390 * DEGREES, run_time=4)
        self.wait(2)

        # Increase resolution
        
        # # Zoom in to the central 2x2 grid
        # self.move_camera(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=1, run_time=2)
        # self.move_camera(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=6, run_time=2)
        # self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, zoom=20, run_time=2)
        # self.wait(2)

        # Generate the terrain surface using vertices from terrain data
        surface_mesh4 = VGroup()
        for i in range(len(y_coords4) - 1):
            for j in range(len(x_coords4) - 1):
                # Define vertices of each small quad
                p1 = np.array([x_coords4[j], y_coords4[i], terrain_data4[i, j]])
                p2 = np.array([x_coords4[j+1], y_coords4[i], terrain_data4[i, j+1]])
                p3 = np.array([x_coords4[j+1], y_coords4[i+1], terrain_data4[i+1, j+1]])
                p4 = np.array([x_coords4[j], y_coords4[i+1], terrain_data4[i+1, j]])

                # Calculate the average height for color interpolation
                avg_height = (terrain_data4[i, j] + terrain_data4[i, j+1] + terrain_data4[i+1, j+1] + terrain_data4[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad as a Polygon and add to surface mesh
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0.8, color=color)
                surface_mesh4.add(quad)

        # Display the full terrain initially
        self.play(Create(surface_mesh4),FadeOut(surface_mesh7),run_time=2)
        

        # self.move_camera(zoom=2, run_time=2)
        self.move_camera(phi=75 * DEGREES, theta=-120 * DEGREES, frame_center=[0, 3, 1] ,zoom=1.5, run_time=2)

        # Generate the terrain surface using vertices from terrain data
        surface_mesh1 = VGroup()
        for i in range(len(y_coords1) - 1):
            for j in range(len(x_coords1) - 1):
                # Define vertices of each small quad
                p1 = np.array([x_coords1[j], y_coords1[i], terrain_data1[i, j]])
                p2 = np.array([x_coords1[j+1], y_coords1[i], terrain_data1[i, j+1]])
                p3 = np.array([x_coords1[j+1], y_coords1[i+1], terrain_data1[i+1, j+1]])
                p4 = np.array([x_coords1[j], y_coords1[i+1], terrain_data1[i+1, j]])

                # Calculate the average height for color interpolation
                avg_height = (terrain_data1[i, j] + terrain_data1[i, j+1] + terrain_data1[i+1, j+1] + terrain_data1[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad as a Polygon and add to surface mesh
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0.8, color=color)
                surface_mesh1.add(quad)

        # Display the full terrain initially
        self.play(Create(surface_mesh1),FadeOut(surface_mesh4),run_time=2)

        
        # Generate the terrain surface using vertices from terrain data
        surface_mesh_111 = VGroup()
        for i in range(len(y_coords_111) - 1):
            for j in range(len(x_coords_111) - 1):
                # Define vertices of each small quad
                p1 = np.array([x_coords_111[j], y_coords_111[i], terrain_data111[i, j]])
                p2 = np.array([x_coords_111[j+1], y_coords_111[i], terrain_data111[i, j+1]])
                p3 = np.array([x_coords_111[j+1], y_coords_111[i+1], terrain_data111[i+1, j+1]])
                p4 = np.array([x_coords_111[j], y_coords_111[i+1], terrain_data111[i+1, j]])

                # Calculate the average height for color interpolation
                avg_height = (terrain_data111[i, j] + terrain_data111[i, j+1] + terrain_data111[i+1, j+1] + terrain_data111[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad as a Polygon and add to surface mesh
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0.8, color=color)
                surface_mesh_111.add(quad)

        # Display the full terrain initially
        self.play(Create(surface_mesh_111),FadeOut(surface_mesh1),run_time=2)


        # Generate the terrain surface using vertices from terrain data
        surface_mesh_111s = VGroup()
        for i in range(len(y_coords_111) - 1):
            for j in range(len(x_coords_111) - 1):
                # Define vertices of each small quad
                p1 = np.array([x_coords_111[j], y_coords_111[i], terrain_data111s[i, j]])
                p2 = np.array([x_coords_111[j+1], y_coords_111[i], terrain_data111s[i, j+1]])
                p3 = np.array([x_coords_111[j+1], y_coords_111[i+1], terrain_data111s[i+1, j+1]])
                p4 = np.array([x_coords_111[j], y_coords_111[i+1], terrain_data111s[i+1, j]])

                # Calculate the average height for color interpolation
                avg_height = (terrain_data111s[i, j] + terrain_data111s[i, j+1] + terrain_data111s[i+1, j+1] + terrain_data111s[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad as a Polygon and add to surface mesh
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0.8, color=color)
                surface_mesh_111s.add(quad)

        # Display the full terrain initially
        # self.play(Create(surface_mesh_111s),FadeOut(surface_mesh_111),run_time=2)
        self.play(Transform(surface_mesh_111, surface_mesh_111s),run_time=2)
        self.wait(2)

        self.play(Create(surface_mesh1), FadeOut(surface_mesh_111s),run_time=2)
        self.wait(2)
                
        # Perform a full 360-degree loop around the Z-axis
        
        self.move_camera(phi=60 * DEGREES, frame_center=[0, 0, 0] ,zoom=2, run_time=2)
        self.move_camera(phi=60 * DEGREES, theta=360 * DEGREES, run_time=6) ##########
        self.wait(2)

        # Define the center 2x2 grid section for final zoomed-in view
        center_surface = VGroup()
        for i in range(int(terrain_data1.shape[1]/2)-1, int(terrain_data1.shape[1]/2)):
            for j in range(int(terrain_data1.shape[0]/2)-1, int(terrain_data1.shape[0]/2)):
                # Define vertices for the 2x2 center grid
                p1 = np.array([x_coords1[j], y_coords1[i], terrain_data1[i, j]])
                p2 = np.array([x_coords1[j+1], y_coords1[i], terrain_data1[i, j+1]])
                p3 = np.array([x_coords1[j+1], y_coords1[i+1], terrain_data1[i+1, j+1]])
                p4 = np.array([x_coords1[j], y_coords1[i+1], terrain_data1[i+1, j]])

                # Get color for center grid cells
                avg_height = (terrain_data1[i, j] + terrain_data1[i, j+1] + terrain_data1[i+1, j+1] + terrain_data1[i+1, j]) / 4
                color = height_to_color(avg_height)

                # Create the quad and add to center surface
                quad = Polygon(p1, p2, p3, p4, fill_opacity=0, color=color)
                center_surface.add(quad)

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, zoom=20, run_time=2)
        
        # Fade out the full terrain except for the center 2x2 grid
        self.play(FadeOut(surface_mesh1), FadeIn(center_surface))
        self.wait(2)

        #Final zoom in on the center grid
        # self.wait(2)

        # Extrude the center square into a cube by creating vertical edges
        height = 0.1  # Set height for extrusion to create a 3D effect
        extruded_cube = VGroup()
        for quad in center_surface:
            vertices = quad.get_vertices()
            for vertex in vertices:
                # Create a vertical line (extrusion) from each vertex
                top_vertex = vertex + np.array([0, 0, height])  # Offset along the z-axis
                edge = Line(vertex, top_vertex, color=color, stroke_opacity=0.6)
                extruded_cube.add(edge)
        
            # Create a top face for the extruded shape
            top_face = Polygon(
                *[v + np.array([0, 0, height]) for v in vertices],
                fill_opacity=0,
                color=color,
            )
            extruded_cube.add(top_face)
        
        # Add extruded cube to the scene
        self.play(Create(extruded_cube))
        self.wait(2)

        # Present where the variables are staggered in the extruded cube
        # Define colors for each variable to distinguish them
        mass_color = BLUE_B
        u_color = GREEN
        v_color = RED
        w_color = ORANGE
        
        # Display the staggered variables step-by-step
        # Step 1: Show the mass point at the center of the base
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=20, run_time=2)
        radi = 0.01
        mass_point = Dot3D(point=center_surface.get_center() + np.array([0, 0, height/2]), color=mass_color, radius=radi)
        mass_label = Text("Mass", color=mass_color).scale(0.03).next_to(mass_point, UP, buff=0.02)
        self.play(FadeIn(mass_point), Write(mass_label))
        self.wait(1)
        
        # Step 2: Show U-grid points on the left and right faces of the base
        u_left = Dot3D(point=center_surface.get_center() + np.array([-0.05, 0, height/2]), color=u_color, radius=radi)
        u_right = Dot3D(point=center_surface.get_center() + np.array([0.05, 0, height/2]), color=u_color, radius=radi)
        u_label = Text("U-grid", color=u_color).scale(0.03).next_to(u_right, RIGHT, buff=0.02)
        self.play(FadeIn(u_left), FadeIn(u_right), Write(u_label))
        self.wait(1)
        
        # Step 3: Show V-grid points on the front and back faces of the base
        v_front = Dot3D(point=center_surface.get_center() + np.array([0, -0.05, height/2]), color=v_color, radius=radi)
        v_back = Dot3D(point=center_surface.get_center() + np.array([0, 0.05, height/2]), color=v_color, radius=radi)
        v_label = Text("V-grid", color=v_color).scale(0.03).next_to(v_back, LEFT, buff=0.02)
        self.play(FadeIn(v_front), FadeIn(v_back), Write(v_label))
        self.wait(1)

        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, zoom=20, run_time=2)
        # Step 4: Show W-grid points at the top and bottom center of the cube
        w_top = Dot3D(point=center_surface.get_center() + np.array([0, 0, height]), color=w_color, radius=radi)
        w_bottom = Dot3D(point=center_surface.get_center(), color=w_color, radius=radi)
        w_label = Text("W-grid", color=w_color).scale(0.03).next_to(w_top, UP, buff=0.02)
        self.play(FadeIn(w_top), FadeIn(w_bottom), Write(w_label))
        self.wait(2)

        # Group all elements into a single VGroup
        all_elements = VGroup(
            mass_point, mass_label,
            u_left, u_right, u_label,
            v_front, v_back, v_label,
            w_top, w_bottom, w_label
        )
        
        # Fade out all elements at once
        self.play(FadeOut(all_elements))
        self.wait(1)
                
        # Rotate camera to view the placement of staggered variables from different angles
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, zoom=40, run_time=2)
        self.wait(1)

        # Measure and display the side length of the cube
        side_length = 0.1  # Actual size of the cube in scene coordinates
        measurement_line = Line(p1, p2, color=WHITE)
        measurement_label = Text("200 m", color=WHITE).scale(0.03).next_to(measurement_line, DOWN, buff=0.05)

        # Show the measurement line and label
        self.play(Create(measurement_line), FadeIn(measurement_label))
        self.wait(1)

        # Fade out the measurement line and label
        self.play(FadeOut(measurement_line), FadeOut(measurement_label))
        self.wait(1)

                # Create a regular grid of small prisms (buildings) at ground level
        num_buildings = 5  # Number of buildings along one side of the grid
        building_spacing = 0.022  # Distance between buildings
        max_building_height = 0.05  # Max height for buildings

        # Define the group to hold building prisms
        building_prisms = VGroup()
        
        for i in range(num_buildings):
            for j in range(num_buildings):
                # Calculate position for each building at ground level
                x_pos = (0.5 + i - num_buildings / 2) * building_spacing
                y_pos = (0.5 + j - num_buildings / 2) * building_spacing
                building_height = np.random.uniform(0.01, max_building_height)  # Random height

                # Create the building prism at minimal height, then target the final height
                building_prism = Prism(
                    dimensions=[building_spacing * 0.6, building_spacing * 0.8, 0.001],  # Start with zero height
                    fill_opacity=0.6,
                    color=BLUE_D,
                ).shift([x_pos, y_pos, building_height/2])  # Positioned at ground level
                
                # Save the target height for extrusion
                building_prism.target_height = building_height
                building_prisms.add(building_prism)

        # Add the building grid at ground level
        self.play(Create(building_prisms))

        # Animate extrusion of all buildings at once
        self.play(
            *[building.animate.scale([1, 1, building.target_height / 0.001]) for building in building_prisms],
            run_time=1.5
        )

        self.wait(2)

        self.move_camera(phi=45 * DEGREES, theta=-120 * DEGREES, zoom=40, run_time=2)

        # Step 1: Calculate the mean height of the current buildings for the canyon height
        mean_building_height = np.mean([building.height for building in building_prisms])

        # Step 2: Define the dimensions and positions of the canyon buildings
        canyon_width = building_spacing   # Width of the canyon
        canyon_depth = num_buildings * building_spacing  # Depth of the canyon (along y-axis)
        
        # Define parameters for canyon buildings
        num_canyon_buildings = 5  # Number of tall buildings
        canyon_width = building_spacing / 2  # Width of each canyon
        building_width = (num_buildings * building_spacing - (num_canyon_buildings - 1) * canyon_width) / num_canyon_buildings
        canyon_height = mean_building_height  # Set the canyon building height to the mean of smaller buildings
        
        # Calculate the mean height of the current buildings to use as the canyon height
        mean_building_height = np.mean([building.target_height for building in building_prisms])
        
        # Define dimensions and positions for four canyon buildings
        num_canyon_buildings = 3
        canyon_spacing = building_spacing*0.8  # Spacing between canyon buildings
        building_width = (num_buildings * building_spacing - (num_canyon_buildings - 1) * canyon_spacing) / num_canyon_buildings
        canyon_height = mean_building_height*0.8  # Set the canyon building height to the mean height of smaller buildings
        
        # Create four canyon buildings positioned to form canyons in between
        canyon_buildings = VGroup()
        for i in range(num_canyon_buildings):
            x_position = - (num_buildings * building_spacing) / 2 + i * (building_width + canyon_spacing) + building_width / 2
            canyon_building = Prism(
                dimensions=[building_width, num_buildings * building_spacing, canyon_height],
                color=BLUE_D,
                fill_opacity=0.6
            ).shift([x_position, 0,canyon_height / 2])
            canyon_buildings.add(canyon_building)
        
        # Perform the transformation of all small buildings into the four canyon buildings
        self.play(
            *[Transform(building, canyon_buildings[i % num_canyon_buildings]) for i, building in enumerate(building_prisms)],
            run_time=2
        )
        
        

        # self.wait(5)


        # # # Define wind arrows (vectors) flowing through the cube
        # # num_arrows = 10  # Number of arrows representing the wind
        # # arrow_spacing = 0.04  # Distance between each arrow path along the x-axis
        # # wind_color = BLUE_C
        # # arrow_length = 0.05
        # # wind_speed = 0.1  # Speed of arrow movement

        # # wind_arrows = VGroup()  # Group to hold all wind arrows

        # # for i in range(num_arrows):
        # #     # Calculate the starting position for each arrow at one side of the cube
        # #     x_start = -0.1  # Start at the left side of the cube
        # #     y_pos = (i - num_arrows / 2) * arrow_spacing  # Position arrows in the y-axis
        # #     z_pos = 0.03  # Position arrows slightly above ground level

        # #     # Create an arrow at the starting position
        # #     wind_arrow = Arrow3D(
        # #         start=[x_start, y_pos, z_pos],
        # #         end=[x_start + arrow_length, y_pos, z_pos],
        # #         color=wind_color,
        # #         stroke_width=2
        # #     )

        # #     wind_arrows.add(wind_arrow)

        # # # Add all arrows to the scene
        # # self.add(wind_arrows)

        # # # Animate the arrows moving across the cube to simulate wind blowing
        # # for wind_arrow in wind_arrows:
        # #     self.play(wind_arrow.animate.shift([0.2, 0, 0]), run_time=wind_speed, rate_func=linear)

        # # self.wait(1)

        # # # Fade out the wind arrows
        # # self.play(FadeOut(wind_arrows))
        


