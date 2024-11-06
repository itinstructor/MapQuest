"""
    Name: mapquest_gui.py
    Author:
    Created:
    Purpose: MapQuest GUI shows map of location
    15,000 requests per month
"""
from tkinter import *
from tkinter.ttk import *
import webbrowser
import requests
from api_key import API_KEY, GEOCODE_ENDPOINT
from PIL import ImageTk, Image
from io import BytesIO

# Set this to False to only display the joke
IS_DEBUGGING = True


class MapQuestGui:

    def __init__(self):
        """Initialize program"""
        self._mapquest_data = {}
        self.window = Tk()
        self.window.title("MapQuest App")
        self.window.iconbitmap("telescope.ico")
        self.window.geometry("450x300")
        self.window.config(padx=10, pady=10)

        self.create_widgets()
        mainloop()

# ------------------------- GET GEOCODE ---------------------------------- #
    def get_geocode(self):
        """Find the location of an address"""
        self.location = self.entry_location.get()
        params = {
            "key": API_KEY,
            "location": self.location,
            "maxResults": 1,
            "thumbMaps": True
        }
        # Use the requests.get() function with the parameter of the url
        # Get and store in the data attribute
        response = requests.get(
            GEOCODE_ENDPOINT,
            params=params,
        )

        # If the status_code is 200, successful connection and data
        if (response.status_code == 200):

            # Convert JSON data into Python dictionary with key value pairs
            self._mapquest_data = response.json()

            # Used to debug process
            if (IS_DEBUGGING):

                # Display the status code
                print(
                    f'\nStatus code: {response.status_code} \n')

                # Display the raw JSON data from API
                # print('Raw data from mapquest:')
                # print(response.text)

                # Display the Python dictionary
                print('\nJSON data converted to a Python dictionary:')
                print(self._mapquest_data)

        else:
            print('API unavailable')

# ------------------------ GET DICTIONARIES ------------------------------ #
    def get_dictionaries(self):
        """Get mapquest dictionary"""
        # locations dictionary
        self._locations = self._mapquest_data["results"][0]["locations"][0]

# ------------------------- GET URL -------------------------------------- #
    def get_url(self):
        """Open default webbrowser from url"""
        webbrowser.open_new_tab(self._mapquest_data["url"])

# ------------------------- GET MAP IMAGE -------------------------------- #
    def get_map_image(self):
        """Get Map image"""
        # Get Map image url from request data
        image_url = self._locations["mapUrl"]

        # Get the image data from the url
        map_photo_data = requests.get(image_url)

        # Get the image data as a bytes object
        image_data = map_photo_data.content

        # Load image data from bytes object to image
        map_image = ImageTk.PhotoImage(Image.open(BytesIO(image_data)))

        # Create a label to show the image
        self.image_panel.configure(image=map_image)

        # Assign image to label
        self.image_panel.image = map_image

# ------------------------- DISPLAY GEOCODE ------------------------------ #
    def display_geocode(self, *args):
        """ Get individual items from dictionaries """
        self.get_geocode()
        self.get_dictionaries()
        # self.get_map_image()

        # Get latitude and longitude
        self._latitude = self._locations["latLng"]["lat"]
        self._longitude = self._locations["latLng"]["lng"]

        self._street = self._locations["street"]
        self._city = self._locations["adminArea5"]
        self._state = self._locations["adminArea3"]
        self._zipcode = self._locations["postalCode"]

        self.lbl_display_latitude.config(text=self._latitude)
        self.lbl_display_longitude.config(text=self._longitude)
        self.lbl_display_street.config(text=self._street)
        self.lbl_display_city.config(text=self._city)
        self.lbl_display_state.config(text=self._state)
        self.lbl_display_zipcode.config(text=self._zipcode)

# ------------------------- CREATE WIDGETS ------------------------------- #
    def create_widgets(self):
        """Create and place GUI widgets"""
        # Create frames
        self.entry_frame = LabelFrame(self.window, text="Enter Location")
        self.display_frame = LabelFrame(self.window, text="Location")

        # Fill the frame to the width of the window
        self.entry_frame.pack(fill=X)
        self.display_frame.pack(fill=X)
        # Keep the frame size regardless of the widget sizes
        self.entry_frame.pack_propagate(False)
        self.display_frame.pack_propagate(False)

        self.entry_location = Entry(self.entry_frame, width=40)
        self.entry_location.insert(
            END, string="615 Mountain View, Scottsbluff, NE, US")
        # Select all text in entry
        self.entry_location.selection_range(0, END)
        self.entry_location.focus_set()

        self.image_panel = Label(self.display_frame)

        self.lbl_latitude = Label(
            self.display_frame, text="Lat:", justify='right')
        self.lbl_display_latitude = Label(self.display_frame, justify='left')
        self.lbl_longitude = Label(
            self.display_frame, text="Lng:", justify='right')
        self.lbl_display_longitude = Label(self.display_frame, justify='left')

        self.lbl_display_street = Label(self.display_frame, )
        self.lbl_display_city = Label(self.display_frame, )
        self.lbl_display_state = Label(self.display_frame, )
        self.lbl_display_zipcode = Label(self.display_frame, )

        self.btn_geocode = Button(
            self.entry_frame,
            text="Get Geocode",
            command=self.display_geocode
        )

        # Enter key will activate the get_apod method
        self.window.bind('<Return>', self.display_geocode)

        # Place Widgets
        self.entry_location.grid(row=1, column=1, columnspan=2, sticky=W)
        self.btn_geocode.grid(row=1, column=3)

        # Place image label
        self.image_panel.grid(row=2, column=2, columnspan=2, rowspan=8)

        self.lbl_latitude.grid(row=2, column=0, sticky=E)
        self.lbl_display_latitude.grid(row=2, column=1, sticky=W)
        self.lbl_longitude.grid(row=3, column=0, sticky=E)
        self.lbl_display_longitude.grid(row=3, column=1, sticky=W)
        self.lbl_display_street.grid(row=4, column=1, sticky=W)
        self.lbl_display_city.grid(row=5, column=1, sticky=W)
        self.lbl_display_state.grid(row=6, column=1, sticky=W)
        self.lbl_display_zipcode.grid(row=7, column=1, sticky=W)

        self.entry_frame.pack_configure(padx=5, pady=5)
        self.display_frame.pack_configure(padx=5, pady=5)
        # Set padding for all widgets
        for child in self.entry_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        for child in self.display_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)


# Create program object
if __name__ == '__main__':
    mapquest_gui = MapQuestGui()
