from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Daily Assistant API",
    description="Advanced weather, daily clothing, and targeted workout assistant for developers.",
    version="1.0.0"
)

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
    # 1. Adım: Şehir isminden Enlem ve Boylam bulma (Geocoding)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=tr&format=json"
    geo_response = requests.get(geo_url).json()
    
    # Şehir bulunamazsa 404 hatası döndür
    if "results" not in geo_response:
        raise HTTPException(status_code=404, detail="Şehir bulunamadı. Lütfen geçerli bir şehir girin.")
        
    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]
    city_name = geo_response["results"][0]["name"] 
    
    # 2. Adım: Bulunan koordinatlara göre anlık sıcaklığı çekme
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}¤t_weather=true"
    weather_response = requests.get(weather_url).json()
    
    # Gerçek sıcaklık verisini alıyoruz
    temp = weather_response["current_weather"]["temperature"]
    
    # Hava durumuna göre asistanın dinamik karar mekanizması
    if temp < 15:
        condition = "Soğuk"
        clothing = "Hava oldukça serin. Katmanlı giyinmeyi ve yanına rüzgar geçirmez bir ceket almayı unutma."
        energy = "Düşük/Orta"
        set_form = "3 Set: 12-12-12 tekrar. Eklemleri ısıtmak için hafif kilo, kontrollü form."
    elif temp < 25:
        condition = "Ilık"
        clothing = "Hava tam kararında. Üzerine bir tişört ve ince bir kapşonlu alarak çıkabilirsin."
        energy = "Orta/Yüksek"
        set_form = "4 Set: 12-10-10-8 tekrar. Son sette tükenişe git."
    else:
        condition = "Sıcak"
        clothing = "Bugün hava oldukça sıcak. İnce, nefes alabilen pamuklu kumaşlar tercih etmelisin."
        energy = "Yüksek"
        set_form = "4 Set: 15-12-10-8 tekrar (Piramit). Her set sonu 3 saniye negatif (eksantrik) tutuş."

    return DailyAssistantResponse(
        location=city_name,
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