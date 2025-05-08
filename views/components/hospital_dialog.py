from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem, MDList
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
import math

class HospitalDialog:
    def __init__(self, location_service, language):
        self.location_service = location_service
        self.language = language
        self.dialog = None

    def show_dialog(self):
        user_location = self.location_service.get_user_location()  # returns (lat, lon)
        hospitals = self.get_all_hospitals()

        nearby = self.filter_nearby_hospitals(hospitals, user_location, max_distance_km=50)

        layout = BoxLayout(orientation='vertical')
        scroll = MDScrollView()
        list_view = MDList()

        for hospital in nearby:
            list_view.add_widget(
                OneLineListItem(text=f"{hospital['name']} ({hospital['distance']:.1f} km)")
            )

        scroll.add_widget(list_view)
        layout.add_widget(scroll)

        self.dialog = MDDialog(
            title="Nearby Hospitals",
            type="custom",
            content_cls=layout,
            size_hint=(0.9, 0.8),
            buttons=[
                MDFlatButton(text="Close", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def get_all_hospitals(self):
        # Replace with real data source
        return [
            {"name": "Queen Elizabeth Central Hospital", "lat": -15.8013, "lon": 35.0396},
            {"name": "Zomba Central Hospital", "lat": -15.3925, "lon": 35.3334},
            {"name": "Lilongwe Central Hospital", "lat": -13.9833, "lon": 33.7833},
        ]

    def filter_nearby_hospitals(self, hospitals, user_location, max_distance_km=50):
        nearby = []
        for h in hospitals:
            dist = self.haversine(user_location[1], user_location[0], h["lon"], h["lat"])
            if dist <= max_distance_km:
                h["distance"] = dist
                nearby.append(h)
        nearby.sort(key=lambda x: x["distance"])
        return nearby

    def haversine(self, lon1, lat1, lon2, lat2):
        R = 6371  # Earth radius in km
        dlon = math.radians(lon2 - lon1)
        dlat = math.radians(lat2 - lat1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
