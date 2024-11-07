"""
    Name: map_viewer.py
    Author:
    Created:
    Purpose: MapQuest GUI shows map of location
    15,000 requests per month
"""
from base64 import b64decode
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk
# pip install tkinter-tooltip
from tktooltip import ToolTip
from map_service import MapService
from telescope_ico import icon_16, icon_32


class MapViewer:
    """
    A GUI application for viewing maps using the MapQuest API.
    Provides an interface for searching locations and 
    displaying maps with various options.
    The layout is organized with location details to the right of the 
    search area, includes controls for map type and resolution selection.
    """

    def __init__(self, root):
        """
        Initialize the MapViewer application.

        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("MapQuest Map Viewer")
        
        # Set the window and task bar icon
        small_icon = tk.PhotoImage(data=b64decode(icon_16))
        large_icon = tk.PhotoImage(data=b64decode(icon_32))
        self.root.iconphoto(False, large_icon, small_icon)

        # The WM_DELETE_WINDOW protocol is used to handle what happens
        # when the user clicks the close button of a window.
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Initialize the MapService instance
        self.map_service = MapService()

        # Default map settings
        # Default zoom level
        self.zoom = 14

        # Default resolution
        self.resolution = tk.StringVar(value="1024x768")

        # Default map type
        self.map_type = tk.StringVar(value="map")

        # Configure initial map dimensions based on default resolution
        self.update_dimensions()

        self.setup_ui()

# ---------------------------- UPDATE DIMENSIONS ------------------------- #
    def update_dimensions(self):
        """
        Update the map dimensions based on the selected resolution.
        Parses the resolution string and updates width and height accordingly.
        """
        # Parse the the current resolution string to extract width and height
        width, height = self.resolution.get().lower().split('x')
        self.width = int(width)
        self.height = int(height)

        # Update the MapService instance dimensions
        self.map_service.width = self.width
        self.map_service.height = self.height

# ----------------------------- SETUP UI --------------------------------- #
    def setup_ui(self):
        """
        Set up the main user interface components.
        Uses a two-column layout with controls on the left 
        and location details on the right.
        """
        # Main container frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create top frame for search and location info
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        # Configure column weights for proper spacing
        top_frame.columnconfigure(0, weight=3)  # Search section
        top_frame.columnconfigure(1, weight=2)  # Location info section

        # Set up the UI components in their new positions
        self.setup_input_frame(top_frame)
        self.setup_geo_frame(top_frame)

        # Create the label that will display the map below both frames
        self.map_label = ttk.Label(main_frame)
        self.map_label.grid(row=1, column=0, padx=10, pady=10)

        # Load the initial map
        self.update_map()

# ---------------------------- SETUP INPUT FRAME ------------------------- #
    def setup_input_frame(self, parent):
        """
        Set up the frame containing the search inputs and controls.

        Args:
            parent: Parent widget to contain this frame
        """
        # Create labeled frame for search controls
        input_frame = ttk.LabelFrame(parent, text="Search", padding="5")
        input_frame.grid(row=0, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Location search section
        ttk.Label(input_frame, text="Location:").grid(
            row=0, column=0, sticky=tk.W)
        self.location_entry = ttk.Entry(input_frame, width=40)
        self.location_entry.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        # Default location
        self.location_entry.insert(
            0,
            "615 Mountain View Ave Scottsbluff NE"
        )

        # Search button
        search_button = ttk.Button(
            input_frame, text="Search", command=self.update_map)
        search_button.grid(row=0, column=2, padx=(5, 0))

        # Zoom level control
        ttk.Label(input_frame, text="Zoom (1-20):").grid(
            row=1, column=0, sticky=tk.W)

        # StringVar to hold the zoom level
        self.zoom_var = tk.StringVar(value=str(self.zoom))

        zoom_spinbox = ttk.Spinbox(
            input_frame,
            from_=1,
            to=20,
            textvariable=self.zoom_var,
            width=5
        )
        zoom_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Set up the map type and resolution selection frames
        self.setup_map_type_frame(input_frame)
        self.setup_resolution_frame(input_frame)

        # Bind Enter key to search function
        self.root.bind('<Return>', self.update_map)
        self.root.bind('<KP_Enter>', self.update_map)
        self.root.bind("<Escape>", self.quit)

# -------------------------- SETUP MAP TYPE FRAME ------------------------ #
    def setup_map_type_frame(self, parent):
        """
        Set up the frame containing map type radio buttons.

        Args:
            parent: Parent widget to contain this frame
        """
        map_type_frame = ttk.LabelFrame(parent, text="Map Type", padding="3")
        map_type_frame.grid(row=2, column=0, columnspan=3,
                            sticky=(tk.W, tk.E), pady=5)

        # Define available map types with their descriptions
        map_types = [
            ("Map", "map", "Standard street map"),
            ("Hybrid", "hyb", "Satellite with labels"),
            ("Satellite", "sat", "Aerial imagery"),
            ("Light", "light", "Light themed map"),
            ("Dark", "dark", "Dark themed map")
        ]

        # Create radio buttons for each map type in a single row
        for i, (text, value, desc) in enumerate(map_types):
            rb = ttk.Radiobutton(
                map_type_frame,
                text=text,
                value=value,
                variable=self.map_type,
                command=self.update_map
            )
            rb.grid(row=0, column=i, padx=3, pady=2)

            # Apply ToolTip directly
            ToolTip(rb, msg=desc, delay=1.0)

# ----------------------- SETUP RESOLUTION FRAME ------------------------- #
    def setup_resolution_frame(self, parent):
        """
        Set up the frame containing resolution radio buttons.

        Args:
            parent: Parent widget to contain this frame
        """
        resolution_frame = ttk.LabelFrame(
            parent, text="Resolution", padding="3")
        resolution_frame.grid(row=3, column=0, columnspan=3,
                              sticky=(tk.W, tk.E), pady=5)

        # Define available resolutions with their descriptions
        resolutions = [
            ("640x480", "VGA"),
            ("800x600", "SVGA"),
            ("1024x768", "XGA"),
            ("1280x800", "WXGA"),
            ("1920x1080", "Full HD")
        ]

        # Create radio buttons for each resolution in a grid layout
        # Each resolution is a tuple of (value, description)
        # The value is the resolution string, and the description is the tooltip
        # The resolution string is in the format "width x height"
        # The tooltip is a description of the resolution
        for i, (value, desc) in enumerate(resolutions):
            rb = ttk.Radiobutton(
                resolution_frame,
                text=value,
                value=value,
                variable=self.resolution,
                command=self.on_resolution_change
            )
            rb.grid(row=0, column=i, padx=3, pady=2)

            # Apply resolution ToolTip directly
            ToolTip(rb, msg=desc,  delay=1.0)

# --------------------------- SETUP GEO FRAME ---------------------------- #
    def setup_geo_frame(self, parent):
        """
        Set up the frame displaying location information.
        Now positioned to the right of the search controls.

        Args:
            parent: Parent widget to contain this frame
        """
        self.geo_frame = ttk.LabelFrame(
            parent, text="Location Information", padding="5")
        self.geo_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create a 3x2 grid for location information
        for i in range(3):
            self.geo_frame.columnconfigure(i, weight=1)

        # Create and position all location information labels
        self.lat_label = ttk.Label(self.geo_frame, text="Latitude: ")
        self.lat_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)

        self.lon_label = ttk.Label(self.geo_frame, text="Longitude: ")
        self.lon_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        self.street_label = ttk.Label(self.geo_frame, text="Street: ")
        self.street_label.grid(
            row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

        self.city_label = ttk.Label(self.geo_frame, text="City: ")
        self.city_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)

        self.state_label = ttk.Label(self.geo_frame, text="State: ")
        self.state_label.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        self.postal_label = ttk.Label(self.geo_frame, text="Postal Code: ")
        self.postal_label.grid(
            row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=2)

# ---------------------- ON RESOLUTION CHANGE ---------------------------- #
    def on_resolution_change(self):
        """
        Handle resolution change events.
        Updates the map dimensions and refreshes the display.
        """
        self.update_dimensions()
        self.update_map()

# ------------------------ UPDATE LOCATION INFO -------------------------- #
    def update_location_info(self, location_data):
        """
        Update the location information labels with new data.

        Args:
            location_data (dict): Dictionary containing location information
        """
        # Update all location information labels with formatted data
        self.lat_label.config(
            text=f"Latitude: {location_data['latitude']:.6f}")
        self.lon_label.config(
            text=f"Longitude: {location_data['longitude']:.6f}")
        self.street_label.config(text=f"Street: {location_data['street']}")
        self.city_label.config(text=f"City: {location_data['city']}")
        self.state_label.config(text=f"State: {location_data['state']}")
        self.postal_label.config(text=f"Postal Code: {
                                 location_data['postal_code']}")

# ---------------------------- UPDATE MAP -------------------------------- #
    def update_map(self):
        """
        Update the map display based on current settings.
        Retrieves new map image and location data from the MapService.
        Handles errors and displays appropriate messages to the user.
        """
        # Get the location from the entry field
        location = self.location_entry.get()

        # Check if the location is empty
        if not location:
            messagebox.showwarning("Warning", "Please enter a location")
            return

        try:
            # Get new map image and location data from the service
            image, location_data = self.map_service.get_static_map(
                location,
                self.zoom_var.get(),
                self.map_type.get()
            )

            # Update the map display
            photo = ImageTk.PhotoImage(image)
            self.map_label.configure(image=photo)
            
            # Keep a reference to prevent garbage collection
            self.map_label.image = photo

            # Update the location information display
            self.update_location_info(location_data)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quit(self):
        self.root.destroy()


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = MapViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
