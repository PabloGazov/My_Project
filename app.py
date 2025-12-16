import streamlit as st
from abc import ABC, abstractmethod

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Италия": ["София", "Скопие", "Рим", "Милано"],
    "България → Франция": ["София", "Будапеща", "Виена", "Париж"]
}

city_info = {
    "София": {"hotel": 70, "food": 20, "sight": "Александър Невски", "tour": 15},
    "Белград": {"hotel": 65, "food": 22, "sight": "Калемегдан", "tour": 18},
    "Виена": {"hotel": 90, "food": 30, "sight": "Шьонбрун", "tour": 25},
    "Мюнхен": {"hotel": 95, "food": 28, "sight": "Мариенплац", "tour": 22},
    "Скопие": {"hotel": 60, "food": 18, "sight": "Старият базар", "tour": 14},
    "Рим": {"hotel": 100, "food": 35, "sight": "Колизеумът", "tour": 30},
    "Милано": {"hotel": 95, "food": 32, "sight": "Катедралата Дуомо", "tour": 26},
    "Будапеща": {"hotel": 75, "food": 24, "sight": "Парламентът", "tour": 20},
    "Париж": {"hotel": 110, "food": 40, "sight": "Айфеловата кула", "tour": 35}
}

DISTANCE_BETWEEN_CITIES = 300
INSURANCE_PER_DAY = 8

# ================== OOP ==================

class Transport(ABC):
    def __init__(self, price_per_km):
        self.price_per_km = price_per_km

    @abstractmethod
    def name(self):
        pass

    def travel_cost(self, distance):
        return distance * self.price_per_km


class Car(Transport):
    def __init__(self):
        super().__init__(0.25)

    def name(self):
        return "🚗 Кола"


class Train(Transport):
    def __init__(self):
        super().__init__(0.18)

    def name(self):
        return "🚆 Влак"


class Plane(Transport):
    def __init__(self):
        super().__init__(0.45)

    def name(self):
        return "✈️ Самолет"

# ================== UI ==================

st.title("🌍 Разширен туристически планер")

route_choice = st.selectbox("Маршрут:", list(routes.keys()))
transport_choice = st.selectbox("Превоз:", ["Кола", "Влак", "Самолет"])
trip_type = st.selectbox("Тип пътуване:", ["Бюджетно", "Стандартно", "Луксозно"])
season = st.selectbox("Сезон:", ["Пролет", "Лято", "Зима"])

days = st.slider("Общо дни:", 2, 14, 7)
budget = st.number_input("Бюджет (лв):", 300, 8000, 2000)

guided_tours = st.checkbox("🎟️ Организирани турове")
insurance = st.checkbox("🛡️ Пътническа застраховка")

# ================== MULTIPLIERS ==================

trip_multipliers = {
    "Бюджетно": (0.8, 0.8),
    "Стандартно": (1.0, 1.0),
    "Луксозно": (1.3, 1.4)
}

season_multiplier = {
    "Пролет": 1.0,
    "Лято": 1.2,
    "Зима": 0.9
}

hotel_mult, food_mult = trip_multipliers[trip_type]
season_mult = season_multiplier[season]

# ================== ACTION ==================

if st.button("Планирай 🧭"):
    cities = routes[route_choice]
    days_per_city = days // len(cities)
    remaining_days = days % len(cities)

    transport = {"Кола": Car(), "Влак": Train(), "Самолет": Plane()}[transport_choice]

    total_cost = 0

    st.subheader("🏙️ Детайли по градове")

    for index, city in enumerate(cities):
        stay_days = days_per_city + (1 if index == len(cities) - 1 else 0) + remaining_days
        info = city_info[city]

        hotel_cost = info["hotel"] * hotel_mult * season_mult * stay_days
        food_cost = info["food"] * food_mult * season_mult * stay_days
        tour_cost = info["tour"] * stay_days if guided_tours else 0

        city_total = hotel_cost + food_cost + tour_cost
        total_cost += city_total

        st.markdown(f"### 📍 {city} ({stay_days} дни)")
        st.write(f"🏨 Хотел: {hotel_cost:.2f} лв")
        st.write(f"🍽️ Храна: {food_cost:.2f} лв")
        if guided_tours:
            st.write(f"🎟️ Турове: {tour_cost:.2f} лв")
        st.write(f"➡️ Общо за града: **{city_total:.2f} лв**")

    distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(distance)
    total_cost += transport_cost

    if insurance:
        insurance_cost = INSURANCE_PER_DAY * days
        total_cost += insurance_cost
        st.write(f"🛡️ Застраховка: {insurance_cost:.2f} лв")

    st.subheader("📊 Обобщение")
    st.write(f"Маршрут: {route_choice}")
    st.write(f"Превоз: {transport.name()}")
    st.write(f"Тип пътуване: {trip_type}")
    st.write(f"Сезон: {season}")
    st.write(f"🚗 Транспорт: {transport_cost:.2f} лв")

    st.markdown("---")
    st.write(f"## 💰 Крайна сума: **{total_cost:.2f} лв**")

    if total_cost <= budget:
        st.success("✅ Бюджетът е достатъчен!")
    else:
        st.error("❌ Бюджетът не достига.")
