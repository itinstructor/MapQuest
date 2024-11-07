"""
    Name: map_viewer.py
    Author:
    Created:
    Purpose: Modern MapQuest GUI shows map of location using CustomTkinter
    15,000 requests per month
"""
from base64 import b64decode
import customtkinter as ctk
from tkinter import messagebox
from PIL import ImageTk
from tktooltip import ToolTip
from map_service import MapService
from telescope_ico import icon_16, icon_32
from spin_box import Spinbox


class MapViewer:
    """
    A modern GUI application for viewing maps using the MapQuest API.
    Built with CustomTkinter for a contemporary look and feel.
    """

    def __init__(self):
        """Initialize the MapViewer application."""
        # Set the appearance mode and default color theme
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        # Create the main window
        self.root = ctk.CTk()
        self.root.title("MapQuest Map Viewer")

        # Set the window icon
        small_icon = ImageTk.PhotoImage(data=b64decode(icon_16))
        large_icon = ImageTk.PhotoImage(data=b64decode(icon_32))
        self.root.iconphoto(False, large_icon, small_icon)

        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # Initialize the MapService instance
        self.map_service = MapService()

        # Default settings
        self.zoom = 14
        self.resolution = ctk.StringVar(value="1024x768")
        self.map_type = ctk.StringVar(value="map")

        # Configure initial map dimensions
        self.update_dimensions()

        # Setup the UI
        self.setup_ui()

    def update_dimensions(self):
        """Update the map dimensions based on selected resolution."""
        width, height = self.resolution.get().lower().split('x')
        self.width = int(width)
        self.height = int(height)
        self.map_service.width = self.width
        self.map_service.height = self.height

    def setup_ui(self):
        """Set up the main user interface components."""
        # Main container frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create top frame for search and location info
        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top_frame.grid_columnconfigure(0, weight=3)
        top_frame.grid_columnconfigure(1, weight=2)

        # Setup components
        self.setup_input_frame(top_frame)
        self.setup_geo_frame(top_frame)

        # Map display label
        self.map_label = ctk.CTkLabel(main_frame, text="")
        self.map_label.grid(row=1, column=0, padx=10, pady=10)

        # Load initial map
        self.update_map()

    def setup_input_frame(self, parent):
        """Set up the search and control inputs frame."""
        # Create frame for search controls
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Search section title
        ctk.CTkLabel(input_frame, text="Search", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(10, 5), sticky="w", padx=10)

        # Location search
        ctk.CTkLabel(input_frame, text="Location:").grid(
            row=1, column=0, sticky="w", padx=10)
        self.location_entry = ctk.CTkEntry(input_frame, width=300)
        self.location_entry.grid(row=1, column=1, padx=5, sticky="ew")
        self.location_entry.insert(0, "615 Mountain View Ave Scottsbluff NE")

        # Search button
        search_button = ctk.CTkButton(
            input_frame, text="Search", command=self.update_map)
        search_button.grid(row=1, column=2, padx=10)

        # Zoom control
        ctk.CTkLabel(input_frame, text="Zoom (1-20):").grid(
            row=2, column=0, sticky="w", padx=10, pady=10)
        self.zoom_var = ctk.StringVar(value=str(self.zoom))

        self.zoom_spinbox = Spinbox(
            input_frame,
            width=150,
            step_size=1,
            from_=1,
            to=20
        )
        self.zoom_spinbox.set(self.zoom_var.get())
        self.zoom_spinbox.grid(row=2, column=1, sticky="w", padx=5)

        # Map type and resolution sections
        self.setup_map_type_frame(input_frame)
        self.setup_resolution_frame(input_frame)

        # Bind keys
        self.root.bind('<Return>', lambda e: self.update_map())
        self.root.bind('<KP_Enter>', lambda e: self.update_map())
        self.root.bind("<Escape>", lambda e: self.quit())

    def setup_map_type_frame(self, parent):
        """Set up the map type selection frame."""
        map_type_frame = ctk.CTkFrame(parent)
        map_type_frame.grid(row=3, column=0, columnspan=3,
                            sticky="ew", pady=10, padx=10)

        ctk.CTkLabel(map_type_frame, text="Map Type", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=5, pady=5, sticky="w")

        map_types = [
            ("Map", "map", "Standard street map"),
            ("Hybrid", "hyb", "Satellite with labels"),
            ("Satellite", "sat", "Aerial imagery"),
            ("Light", "light", "Light themed map"),
            ("Dark", "dark", "Dark themed map")
        ]

        for i, (text, value, desc) in enumerate(map_types):
            rb = ctk.CTkRadioButton(
                map_type_frame,
                text=text,
                value=value,
                variable=self.map_type,
                command=self.update_map
            )
            rb.grid(row=1, column=i, padx=10, pady=5)
            ToolTip(rb, msg=desc, delay=1.0)

    def setup_resolution_frame(self, parent):
        """Set up the resolution selection frame."""
        resolution_frame = ctk.CTkFrame(parent)
        resolution_frame.grid(row=4, column=0, columnspan=3,
                              sticky="ew", pady=10, padx=10)

        ctk.CTkLabel(resolution_frame, text="Resolution", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=5, pady=5, sticky="w")

        resolutions = [
            ("640x480", "VGA"),
            ("800x600", "SVGA"),
            ("1024x768", "XGA"),
            ("1280x800", "WXGA"),
            ("1920x1080", "Full HD")
        ]

        for i, (value, desc) in enumerate(resolutions):
            rb = ctk.CTkRadioButton(
                resolution_frame,
                text=value,
                value=value,
                variable=self.resolution,
                command=self.on_resolution_change
            )
            rb.grid(row=1, column=i, padx=10, pady=5)
            ToolTip(rb, msg=desc, delay=1.0)

    def setup_geo_frame(self, parent):
        """Set up the location information frame."""
        self.geo_frame = ctk.CTkFrame(parent)
        self.geo_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(self.geo_frame, text="Location Information",
                     font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(10, 5), sticky="w", padx=10)

        # Create labels with modern styling
        self.lat_label = ctk.CTkLabel(self.geo_frame, text="Latitude: ")
        self.lat_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.lon_label = ctk.CTkLabel(self.geo_frame, text="Longitude: ")
        self.lon_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.street_label = ctk.CTkLabel(self.geo_frame, text="Street: ")
        self.street_label.grid(
            row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.city_label = ctk.CTkLabel(self.geo_frame, text="City: ")
        self.city_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.state_label = ctk.CTkLabel(self.geo_frame, text="State: ")
        self.state_label.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        self.postal_label = ctk.CTkLabel(self.geo_frame, text="Postal Code: ")
        self.postal_label.grid(
            row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    def on_resolution_change(self):
        """Handle resolution change events."""
        self.update_dimensions()
        self.update_map()

    def update_location_info(self, location_data):
        """Update the location information labels."""
        self.lat_label.configure(
            text=f"Latitude: {location_data['latitude']:.6f}")
        self.lon_label.configure(
            text=f"Longitude: {location_data['longitude']:.6f}")
        self.street_label.configure(text=f"Street: {location_data['street']}")
        self.city_label.configure(text=f"City: {location_data['city']}")
        self.state_label.configure(text=f"State: {location_data['state']}")
        self.postal_label.configure(
            text=f"Postal Code: {location_data['postal_code']}")

    def update_map(self, *args):
        """Update the map display based on current settings."""
        location = self.location_entry.get()

        if not location:
            messagebox.showwarning("Warning", "Please enter a location")
            return

        try:
            image, location_data = self.map_service.get_static_map(
                location,
                int(self.zoom_spinbox.get()),
                self.map_type.get()
            )

            photo = ImageTk.PhotoImage(image)
            self.map_label.configure(image=photo)
            self.map_label.image = photo

            self.update_location_info(location_data)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def quit(self, *args):
        """Exit the application."""
        self.root.destroy()


def main():
    """Initialize and run the application."""
    app = MapViewer()
    app.root.mainloop()


if __name__ == "__main__":
    main()
