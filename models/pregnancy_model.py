from datetime import datetime, timedelta


class PregnancyCalculator:
    @staticmethod
    def calculate_due_date(lmp_date):
        return lmp_date + timedelta(days=280)

    @staticmethod
    def get_current_week(lmp_date):
        return (datetime.today() - lmp_date).days // 7

    @staticmethod
    def get_health_tip(week, language):
        tips_en = {
            1: "Start prenatal vitamins (folic acid). Avoid alcohol and smoking.",
            # ... rest of the English tips
        }

        tips_ny = {
            1: "Yambitsani mankhwala a pakati (folic acid). Pewani chakumwa ndi kuyaka fodya.",
            # ... rest of the Chichewa tips
        }

        default_tip_en = "No health tip available for this week. Please consult your doctor."
        default_tip_ny = "Palibe malangizo aumoyo pa sabata imeneyi. Funsani dokotala."

        return tips_ny.get(week, default_tip_ny) if language == "ny" else tips_en.get(week, default_tip_en)