from kivy import platform
from kivy.logger import Logger
from math import radians, sin, cos, sqrt, atan2

import requests
import json

# Default coordinates for Blantyre (fallback if GPS fails)
DEFAULT_LAT = -15.7861
DEFAULT_LON = 35.0058

# Sample hospital data for Malawi
MALAWI_HOSPITALS = [
    {"name": "Queen Elizabeth Central Hospital", "city": "Blantyre", "lat": -15.7861, "lon": 35.0058},
    {"name": "Kamuzu Central Hospital", "city": "Lilongwe", "lat": -13.9833, "lon": 33.7833},
    {"name": "Mzuzu Central Hospital", "city": "Mzuzu", "lat": -11.4583, "lon": 34.0156},
    # Add more hospitals as needed
]

class LocationService:
    def __init__(self):
        # Initialize with default location (Blantyre)
        self.current_location = (DEFAULT_LAT, DEFAULT_LON)
        self.gps_enabled = False

    def start_gps(self):
        """Start GPS service and request permissions (Android)."""
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            request_permissions([Permission.ACCESS_FINE_LOCATION])

        if platform in ('android', 'ios'):
            from plyer import gps
            try:
                gps.configure(on_location=self.on_location)
                gps.start()
                self.gps_enabled = True
                Logger.info("GPS started successfully")
                return True
            except Exception as e:
                Logger.error(f"GPS Error: {str(e)}")
                self.gps_enabled = False
                return False
        else:
            # For desktop testing - use default location
            Logger.info("Running on desktop, using default location")
            self.on_location(lat=DEFAULT_LAT, lon=DEFAULT_LON)
            return True

    def stop_gps(self):
        """Stop GPS updates."""
        if platform in ('android', 'ios'):
            from plyer import gps
            gps.stop()
            self.gps_enabled = False

    def on_location(self, **kwargs):
        """Callback when GPS updates location."""
        lat = kwargs.get('lat', DEFAULT_LAT)
        lon = kwargs.get('lon', DEFAULT_LON)
        self.current_location = (lat, lon)
        Logger.info(f"Location updated: {self.current_location}")

    def get_user_location(self):
        """Returns current (lat, lon) or None if unavailable."""
        return self.current_location

    def get_nearby_hospitals(self, max_distance_km=50):
        if not self.current_location:
            Logger.error("Location not available!")  # Debug log
            return [], "Location not available"

        Logger.info(f"Filtering hospitals near: {self.current_location}")  # Debug log
        hospitals, error = [], None

        for hospital in MALAWI_HOSPITALS:
            distance = self._calculate_distance(
                self.current_location[0], self.current_location[1],
                hospital['lat'], hospital['lon']
            )
            if distance <= max_distance_km:
                hospital['distance'] = round(distance, 1)
                hospitals.append(hospital)
                Logger.info(f"Added hospital: {hospital['name']} ({distance} km)")  # Debug log

        hospitals.sort(key=lambda x: x['distance'])
        Logger.info(f"Found {len(hospitals)} hospitals")  # Debug log
        return hospitals, error


    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formula (distance in km)."""
        R = 6371.0  # Earth radius in km
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c