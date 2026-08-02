from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(
    title="Daily Assistant API",
    description="Advanced weather, daily clothing, and targeted workout assistant for developers.",
    version="1.0.0"
)

# API'nin döneceği veri modelini tanımlıyoruz
class WorkoutRecommendation(BaseModel):
    focus: str
    energy_level: str
    routine: str
    set_formation: str
    motivation: str

class AssistantAdvice(BaseModel):
    clothing: str
    workout_recommendation: WorkoutRecommendation

class WeatherData(BaseModel):
    condition: str
    temperature_c: float

class DailyAssistantResponse(BaseModel):
    location: str
    weather: WeatherData
    assistant_advice: AssistantAdvice

@app.get("/api/v1/assistant", response_model=DailyAssistantResponse)
def get_daily_advice(location: str):
    # Şimdilik sıcaklığı dinamik olarak simüle ediyoruz
    temp = round(random.uniform(10.0, 35.0), 1)
    
    # Hava durumuna göre asistanın karar mekanizması
    if temp < 15:
        condition = "Soğuk ve Rüzgarlı"
        clothing = "Hava oldukça serin. Katmanlı giyinmeyi ve yanına rüzgar geçirmez bir ceket almayı unutma."
        energy = "Düşük/Orta"
        set_form = "3 Set: 12-12-12 tekrar. Eklemleri ısıtmak için hafif kilo, kontrollü form."
    elif temp < 25:
        condition = "Ilık ve Bulutlu"
        clothing = "Hava tam kararında. Üzerine bir tişört ve ince bir kapşonlu alarak çıkabilirsin."
        energy = "Orta/Yüksek"
        set_form = "4 Set: 12-10-10-8 tekrar. Son sette tükenişe git."
    else:
        condition = "Sıcak ve Güneşli"
        clothing = "Bugün hava oldukça sıcak. İnce, nefes alabilen pamuklu kumaşlar tercih etmelisin."
        energy = "Yüksek"
        set_form = "4 Set: 15-12-10-8 tekrar (Piramit). Her set sonu 3 saniye negatif (eksantrik) tutuş."

    return DailyAssistantResponse(
        location=location,
        weather=WeatherData(
            condition=condition,
            temperature_c=temp
        ),
        assistant_advice=AssistantAdvice(
            clothing=clothing,
            workout_recommendation=WorkoutRecommendation(
                focus="Omuz Gelişimi (Side Deltoids)",
                energy_level=energy,
                routine="Lateral Raise Odaklı Hipertrofi",
                set_formation=set_form,
                motivation="Hava şartlarına göre optimize edilmiş lateral raise formasyonun hazır. Omuzları büyütme vakti!"
            )
        )
    )