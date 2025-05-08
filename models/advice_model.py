class PregnancyAdvice:
    @staticmethod
    def get_weekly_advice(week, language="en"):
        tips_en = {
            1: "Start prenatal vitamins (folic acid). Avoid alcohol and smoking.",
            2: "Ovulation occurs. Track basal body temperature if planning conception.",
            3: "Fertilization happens. Maintain a healthy diet.",
            4: "Implantation occurs. Some spotting is normal. Stay hydrated and rest.",
            5: "Hormones rise. Early pregnancy symptoms like fatigue and nausea may begin.",
            6: "Schedule first prenatal visit. Confirm pregnancy and check overall health.",
            7: "Morning sickness peaks. Eat small, frequent meals. Ginger may help.",
            8: "Embryo development accelerates. Ensure adequate protein intake.",
            9: "Maintain blood sugar stability. Consume fiber-rich foods and hydrate well.",
            10: "Avoid high-risk foods such as unpasteurized dairy and raw seafood.",
            11: "Start Kegel exercises to strengthen pelvic muscles for labor.",
            12: "First trimester ends. Nausea may decrease. Schedule a prenatal visit.",
            13: "Boost iron intake. Red meat, spinach, and legumes help prevent anemia.",
            14: "Start light prenatal exercises such as walking or yoga.",
            15: "Baby kicks soon! Note movement patterns and stay hydrated.",
            16: "Stretch regularly to reduce backaches as belly grows.",
            17: "Maintain oral health. Pregnancy hormones can affect gums.",
            18: "Heartburn might begin. Avoid spicy, acidic foods and eat smaller meals.",
            19: "Increase protein and calcium intake for baby's bone development.",
            20: "Anatomy scan time! You might learn the baby's gender.",
            21: "Monitor weight gain. Balance diet with healthy fats, fiber, and protein.",
            22: "Improve sleep with pregnancy pillows and sleep on your left side.",
            23: "Start thinking about childbirth classes. Preparation builds confidence.",
            24: "Swelling may occur. Stay hydrated and elevate feet.",
            25: "Boost omega-3 intake to support baby’s brain development.",
            26: "Glucose screening test time! Monitor for gestational diabetes risks.",
            27: "Second trimester ends. Energy levels might drop slightly.",
            28: "Third trimester begins. Watch for gestational diabetes symptoms.",
            29: "Monitor baby’s movements. Kick counts help assess health.",
            30: "Support digestion. Constipation is common—eat fiber-rich foods.",
            31: "Increase hydration for swelling relief and amniotic fluid levels.",
            32: "Prepare for birth. Learn breathing techniques for labor.",
            33: "Watch for Braxton Hicks contractions. Practice contractions begin.",
            34: "Pelvic pain may increase. Gentle stretching and warm baths can help.",
            35: "Plan maternity leave and organize home and work tasks.",
            36: "Baby drops lower. Pack your hospital bag!",
            37: "Labor signs may appear—watch for contractions and water breaking.",
            38: "Increase rest. Fatigue peaks, prioritize comfort and naps.",
            39: "Final prenatal visit. Doctor checks cervical dilation and baby’s position.",
            40: "Past due? Discuss induction options with your doctor."
        }

        tips_ny = {
            1: "Yambitsani mankhwala a pakati (folic acid). Pewani chakumwa ndi kuyaka fodya.",
            2: "Ovulation imachitika. Yang'anani kutentha kwa thupi ngati mukufuna kubadwa.",
            3: "Kusakaniza kwa maji amuna ndi akazi kumachitika. Khalani ndi chakudya chabwino.",
            4: "Kudzikika kwa mwana kumachitika. Kuona magazi pang'ono ndi kosayenera kudabwitsa. Khalani ndi madzi ndi kupumula.",
            5: "Mahomoni amakwera. Zizindikiro za pakati monga kuuma ndi kusanza zingayambe.",
            6: "Konzani kuyamba kuchipatala. Tsimikizirani kuti mwabala ndi kuyang'aniritsa thanzi lanu.",
            7: "Kusanza kwa m'mawa kumakwera. Idyani pang'ono pang'ono. Ginger ingathandize.",
            8: "Kukula kwa mwana kumachuluka. Onetsetsani kuti mumadya zakudya zokwanira.",
            9: "Sungani sukulu ya magazi. Idyani zakudya zokhala ndi fiber ndi kumwa madzi.",
            10: "Pewani zakudya zowopsa monga mkaka wosafirika ndi nsomba zosapika.",
            11: "Yambitsani ma exercise a Kegel kuimitsa misipa ya m'mimba.",
            12: "Gawo loyamba latha. Kusanza kungachepe. Konzani kuchipatala.",
            13: "Onjezerani zakudya zokhala ndi iron monga nyama, mfutso ndi nyemba.",
            14: "Yambitsani ma exercise a pakati monga kuyenda kapena yoga.",
            15: "Mwana azamba kukankha! Yang'anani momwe amanyamuka ndi kumwa madzi.",
            16: "Pitirizani kutambasula kuti muchepetse kuwawa mwala.",
            17: "Sungani thanzi la m'kamwa. Mahomoni a pakati amatha kusokoneza magazi.",
            18: "Kuwawa kwa khosi kungayambe. Pewani zakudya zotentha ndi zowawa.",
            19: "Onjezerani protein ndi calcium pakukula mwana.",
            20: "Nthawi ya ultrasound! Mungadziwe za mmwamba wa mwana.",
            21: "Yang'anani kulemera. Idyani zakudya zabwino.",
            22: "Konzerani maganizo a kulala pogwiritsa ntchito miphamanda ya pakati.",
            23: "Yambani kuganiza za maphunziro obadwitsa.",
            24: "Kuzizira kungayambe. Mwani madzi ndi kupitiriza kutulutsa miyendo.",
            25: "Onjezerani omega-3 pakukula bwino mwana.",
            26: "Nthawi ya kuyesa sukulu! Yang'anani za matenda a sukulu.",
            27: "Gawo lachiwiri latha. Mphamvu zitha kuchepa.",
            28: "Gawo lachitatu layamba. Yang'anani zizindikiro za matenda a sukulu.",
            29: "Yang'anani momwe mwana akunyamuka.",
            30: "Thandizani digestion. Idyani zakudya zokhala ndi fiber.",
            31: "Mwani madzi kwambiri kuti muchepetse kuzizira.",
            32: "Konzekerani kubadwa. Phunzirani njira zopuma.",
            33: "Yang'anani ma contractions a Braxton Hicks.",
            34: "Kuwawa m'mimba kungawonjezeke. Tambasulani bwino.",
            35: "Konzani nthawi yomwe mungasiye ntchito.",
            36: "Mwana watsika pansi. Konzani m'bag yanu!",
            37: "Zizindikiro za kubadwa zingayambe - yang'anani ma contractions.",
            38: "Pumulani kwambiri. Mphamvu zatha.",
            39: "Kupita koyamba kuchipatala. Dokotala ayang'ane.",
            40: "Mwapita tsiku? Lankhulani ndi dokotala."
        }

        default_tip_en = "No health tip available for this week. Please consult your doctor."
        default_tip_ny = "Palibe malangizo aumoyo pa sabata imeneyi. Funsani dokotala."

        return tips_ny.get(week, default_tip_ny) if language == "ny" else tips_en.get(week, default_tip_en)

    @staticmethod
    def get_symptom_advice(symptom, language="en"):
        advice_en = {
            "Nausea/Vomiting": "Eat small, frequent meals. Try ginger tea.",
            "Back Pain": "Use a pregnancy pillow. Do gentle stretches.",
            "Headache": "Rest in a dark room. Stay hydrated.",
            "Swelling": "Elevate feet. Reduce salt intake.",
            "Bleeding": "CALL DOCTOR IMMEDIATELY. Could indicate emergency.",
            "Fatigue": "Nap when possible. Iron-rich foods may help."
        }
        advice_ny = {
            "Nausea/Vomiting": "Idyani pang'ono pang'ono. Yesetsani kumwa tiyi wa ginger.",
            "Back Pain": "Gwiritsani ntchito mpando wapakati. Tambasulani bwino.",
            "Headache": "Pumulani mumtima. Imwani madzi ochuluka.",
            "Swelling": "imikani miyendo. Chepetsani mchere.",
            "Bleeding": "ITANANI DOKOTALA MWACHANGU. Zitha kukhala zowopsa.",
            "Fatigue": "Gonani nthawi zonse zomwe mungathe. Zakudya zokhala ndi iron zingathandize."
        }

        return advice_ny.get(symptom, "") if language == "ny" else advice_en.get(symptom, "")