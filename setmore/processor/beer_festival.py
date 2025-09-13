"""Module for processing booking data from SetMore."""

from typing import ClassVar

import pandas as pd


class SetMoreBeerFestivalProcessor:
    """A class for processing event booking data, specifically for festival or bar events.

    This class handles reading, formatting, and analyzing booking data including
    customer information, bar preferences, and shirt size summaries.

    Attributes:
        BAR_ORDER (Dict[str, int]): Mapping of bar types to their display order priority.
    """

    BAR_ORDER: ClassVar[dict] = {
        "Beer": 0,
        "Cider": 1,
        "Gin": 3,
        "Ticket": 2,
    }

    def __init__(self, file_path: str) -> None:
        """Initialize the processor with optional file path."""
        self._file_path = file_path
        self._raw_data = self.read_data()
        self._data = self.format_data()

    @property
    def data(self) -> pd.DataFrame:
        """Get the formatted booking data."""
        return self._data

    def read_data(self) -> pd.DataFrame:
        """Read booking data from a CSV file."""
        return pd.read_csv(self._file_path)

    def format_data(self) -> pd.DataFrame:
        """Clean and format the booking data for analysis."""
        # Filter for confirmed bookings only
        data = self._raw_data[self._raw_data["Status"] == "Confirmed"]

        # Create _timestamp from appointment date and time
        data["_timestamp"] = pd.to_datetime(data["Appointment date"])
        data["time_s"] = data["Appointment time"].str.split(" - ").str[0]
        data["_timestamp_s_time"] = pd.to_datetime(data["time_s"], format="%I:%M %p")
        data["_timestamp"] = pd.to_datetime(data["_timestamp"].dt.date.astype(str) + " " + data["_timestamp_s_time"].dt.time.astype(str))

        # Define columns to remove
        columns_to_drop = [
            "Appointment date",
            "Appointment time",
            "time_s",
            "_timestamp_s_time",
            "Status",
            "Cost",
            "Team member",
            "Country code",
            "Phone",
            "Email",
            "Label",
            "Comments",
            "Booking ID",
            "Booked via",
            "Booked on",
            "Address",
            "City",
            "State",
            "Country",
            "Zipcode / Postal code",
        ]

        # Drop unnecessary columns and rename for clarity
        data = data.drop(columns=columns_to_drop, errors="ignore")
        return data.rename(columns={"Customer name": "Name", "Service/class/event": "Bar preference", "Fest shirt size": "Shirt size"})

    def shirt_size_summary(self) -> pd.Series:
        """Generate a summary of shirt size counts."""
        if self._raw_data is None:
            return pd.Series()

        shirt_sizes = self._raw_data["Fest shirt size"]
        return shirt_sizes.value_counts()

    def bars(self) -> pd.DataFrame:
        """Process bar preference data and organize by _timestamp and preference type."""
        if self._data is None:
            return pd.DataFrame()

        # Subsetted data for the bbq only
        data_bars = self._data[~self._data["Bar preference"].isin(["BBQ", "bbq"])]

        # Group by _timestamp and bar preference, collecting names into lists
        grouped_data = data_bars.groupby(["_timestamp", "Bar preference"])["Name"].agg(list).reset_index()

        # Add ordering column based on BAR_ORDER mapping
        grouped_data["order"] = grouped_data["Bar preference"].map(self.BAR_ORDER)

        # Sort by _timestamp and bar preference order
        grouped_data = grouped_data.sort_values(["_timestamp", "order"]).drop(columns=["order"]).reset_index(drop=True)

        # Create pivot table with bar preferences as columns
        pivoted_data = (
            grouped_data.pivot_table(index="_timestamp", columns="Bar preference", values="Name", aggfunc=list).fillna("").reset_index()
        )
        pivoted_data["Timestamp"] = pivoted_data["_timestamp"].dt.strftime("%H:%M")

        exploded_data = pivoted_data.explode(list(self.BAR_ORDER.keys()))

        for col in self.BAR_ORDER:
            if col in exploded_data:
                if exploded_data[col].apply(lambda x: isinstance(x, list)).any():
                    exploded_data[col] = exploded_data[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else str(x))
                else:
                    exploded_data[col] = exploded_data[col].astype(str)

        return exploded_data

    def bbq(self) -> pd.DataFrame:
        """Process bar preference data and organize by _timestamp and preference type."""
        if self._data is None:
            return pd.DataFrame()

        # Subsetted data for the bbq only
        data_bbq = self._data[self._data["Bar preference"].isin(["BBQ", "bbq"])]

        # Group by _timestamp and bar preference, collecting names into lists
        grouped_data = data_bbq.groupby(["_timestamp"])["Name"].agg(list).reset_index()

        # Sort by _timestamp and bar preference order
        grouped_data = grouped_data.sort_values(["_timestamp"]).reset_index(drop=True)

        # Create pivot table with bar preferences as columns
        grouped_data["Timestamp"] = grouped_data["_timestamp"].dt.strftime("%H:%M")

        return grouped_data
