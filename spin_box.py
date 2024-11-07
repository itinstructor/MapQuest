import customtkinter as ct
from typing import Union, Callable


class Spinbox(ct.CTkFrame):
    """
    A custom spinbox widget that inherits from CTkFrame.
    Provides a numeric input field with increment/decrement buttons.
    """

    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 from_: Union[int, float] = None,  # New parameter
                 to: Union[int, float] = None,     # New parameter
                 **kwargs):
        """
        Initialize the Spinbox widget.
        Args:
            width: Width of the spinbox in pixels
            height: Height of the spinbox in pixels
            step_size: Amount to increment/decrement when buttons are pressed
            command: Optional callback function to execute on value change
            from_: Minimum allowed value (inclusive)
            to: Maximum allowed value (inclusive)
        """
        super().__init__(*args, width=width, height=height, **kwargs)
        self.step_size = step_size
        self.command = command
        self._value = 0.0

        # Store min/max values
        self.from_ = float('-inf') if from_ is None else float(from_)
        self.to = float('inf') if to is None else float(to)

        # Validate min/max values
        if self.from_ > self.to:
            raise ValueError(
                "'from_' value must be less than or equal to 'to' value")

        # Set the frame's background color based on light/dark mode
        self.configure(fg_color=("gray78", "gray28"))

        # Configure grid weights: buttons don't expand, but entry does
        self.grid_columnconfigure((0, 2), weight=0)  # buttons
        self.grid_columnconfigure(1, weight=1)  # entry

        # Create the subtract (-) button
        self.subtract_button = ct.CTkButton(
            self, text="-",
            width=height-6,
            height=height-6,
            command=self.subtract_button_callback
        )
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        # Create the display label
        self.entry = ct.CTkLabel(
            self,
            width=width-(2*height),
            height=height-6
        )
        self.entry.grid(row=0, column=1, columnspan=1,
                        padx=3, pady=3, sticky="ew")

        # Create the add (+) button
        self.add_button = ct.CTkButton(self, text="+",
                                       width=height-6,
                                       height=height-6,
                                       command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # Initialize with default value (respecting min/max)
        self.set(max(min(0.0, self.to), self.from_))

        # Update button states
        self._update_button_states()

    def _update_button_states(self):
        """
        Update the state of increment/decrement buttons based on current value
        and min/max limits.
        """
        # Disable subtract button if at or below minimum
        self.subtract_button.configure(
            state="normal" if self._value > self.from_ else "disabled"
        )

        # Disable add button if at or above maximum
        self.add_button.configure(
            state="normal" if self._value < self.to else "disabled"
        )

    def add_button_callback(self):
        """
        Handler for the add (+) button click.
        Increments the current value by step_size if within bounds.
        """
        if self.command is not None:
            self.command()

        new_value = min(self._value + self.step_size, self.to)
        if new_value != self._value:
            self._value = new_value
            self.entry.configure(text=f"{self._value}")
            self._update_button_states()

    def subtract_button_callback(self):
        """
        Handler for the subtract (-) button click.
        Decrements the current value by step_size if within bounds.
        """
        if self.command is not None:
            self.command()

        new_value = max(self._value - self.step_size, self.from_)
        if new_value != self._value:
            self._value = new_value
            self.entry.configure(text=f"{self._value}")
            self._update_button_states()

    def get(self) -> float:
        """
        Get the current value of the spinbox.
        Returns:
            float: Current value
        """
        return self._value

    def set(self, value: float):
        """
        Set the spinbox to a specific value within the allowed range.
        Args:
            value: The new value to display
        Raises:
            ValueError: If value cannot be converted to float or is outside allowed range
        """
        try:
            new_value = float(value)
            if new_value < self.from_ or new_value > self.to:
                raise ValueError(
                    f"Value must be between {self.from_} and {self.to}"
                )
            self._value = new_value
            self.entry.configure(text=f"{self._value}")
            self._update_button_states()
        except (ValueError, TypeError) as e:
            raise ValueError(
                "Value must be a number within the allowed range") from e

    def get_range(self) -> tuple[float, float]:
        """
        Get the allowed range of values.
        Returns:
            tuple[float, float]: (minimum value, maximum value)
        """
        return (self.from_, self.to)


def main():
    """
    Example usage of the Spinbox widget with value restrictions.
    Creates a window with a spinbox, sets its value, and prints it.
    """
    app = ct.CTk()

    # Create a spinbox with value restrictions (0 to 100)
    spinbox_1 = Spinbox(
        app,
        width=150,
        step_size=3,
        from_=0,    # Minimum value
        to=100      # Maximum value
    )
    spinbox_1.pack(padx=20, pady=20)

    # Set initial value
    spinbox_1.set(35)
    print(f"Current value: {spinbox_1.get()}")
    print(f"Allowed range: {spinbox_1.get_range()}")

    app.mainloop()


if __name__ == "__main__":
    main()
