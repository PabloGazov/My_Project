import streamlit as st
from abc import ABC, abstractmethod
import pandas as pd

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"],
    "България → Италия": ["София", "Скопие", "Рим", "Милано"],
    "България → Франция": ["София", "Будапеща", "Виена", "Париж"]
}

city_info = {
    "София": {"hotel": 70, "food": 20, "tour": 15},
    "Белград": {"hotel": 65, "food": 22, "tour": 18},
    "Виена": {"hotel": 90, "food": 30, "tour": 25},
    "Мюнхен": {"hotel": 95, "food": 28, "tour": 22},
    "Скопие": {"hotel": 60, "food": 18, "tour": 14},
    "Рим": {"hotel": 100, "food": 35, "tour": 30},
    "Милано": {"hotel": 95, "food": 32, "tour": 26},
    "Будапеща": {"hotel": 75, "food": 24, "tour": 20},
    "Париж": {"hotel": 110, "food": 40, "tour": 35}
}

DISTANCE_BETWEEN_CITIES = 300
INSURANCE_PER_DAY = 8

# ================== STRATEGY PATTERN ==================

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_hotel(self, base_price, days):
        pass

    @abstractmethod
    def calculate_food(self, base_price, days):
        pass


class BudgetStrategy(PricingStrategy):
    def calculate_hotel(self, base_price, days):
        return base_price * 0.8 * days

    def calculate_food(self, base_price, days):
        return base_price * 0.8 * days


class StandardStrategy(PricingStrategy):
    def calculate_hotel(self, base_price, days):
        return base_price * days

    def calculate_food(self, base_price, days):
        return base_price * days


class LuxuryStrategy(PricingStrategy):
    def calculate_hotel(self, base_price, days):
        return base_price * 1.3 * days

    def calculate_food(self, base_price, days):
        return base_price * 1.4 * days

# ================== TRANSPORT ==================

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

st.title("🌍 Международен туристически планер")

route_choice = st.selectbox("Маршрут:", list(routes.keys()))
transport_choice = st.selectbox("Превоз:", ["Кола", "Влак", "Самолет"])
pricing_choice = st.selectbox("Тип пътуване:", ["Бюджетно", "Стандартно", "Луксозно"])

days = st.slider("Общо дни:", 3, 15, 7)
budget = st.number_input("Бюджет (лв):", 500, 9000, 2500)

guided_tours = st.checkbox("🎟️ Организирани турове")
insurance = st.checkbox("🛡️ Пътническа застраховка")

# ================== STRATEGY SELECTION ==================

pricing_strategy = {
    "Бюджетно": BudgetStrategy(),
    "Стандартно": StandardStrategy(),
    "Луксозно": LuxuryStrategy()
}[pricing_choice]

# ================== ACTION ==================

if st.button("Планирай 🧭"):
    cities = routes[route_choice]
    days_per_city = days // len(cities)

    transport = {
        "Кола": Car(),
        "Влак": Train(),
        "Самолет": Plane()
    }[transport_choice]

    total_hotel = total_food = total_tour = 0
    city_costs = {}

    for city in cities:
        info = city_info[city]

        hotel_cost = pricing_strategy.calculate_hotel(info["hotel"], days_per_city)
        food_cost = pricing_strategy.calculate_food(info["food"], days_per_city)
        tour_cost = info["tour"] * days_per_city if guided_tours else 0

        city_total = hotel_cost + food_cost + tour_cost
        city_costs[city] = city_total

        total_hotel += hotel_cost
        total_food += food_cost
        total_tour += tour_cost

    distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(distance)

    insurance_cost = INSURANCE_PER_DAY * days if insurance else 0

    total_cost = (
        total_hotel +
        total_food +
        total_tour +
        transport_cost +
        insurance_cost
    )

    # ================== CHARTS ==================

    st.subheader("📊 Разходи по категории")
    category_df = pd.DataFrame({
        "Цена (лв)": [
            total_hotel,
            total_food,
            total_tour,
            transport_cost,
            insurance_cost
        ]
    }, index=["Хотели", "Храна", "Турове", "Транспорт", "Застраховка"])

    st.bar_chart(category_df)

    st.subheader("🏙️ Разходи по градове")
    city_df = pd.DataFrame.from_dict(
        city_costs,
        orient="index",
        columns=["Цена (лв)"]
    )

    st.bar_chart(city_df)

    # ================== FINAL ==================

    st.markdown("---")
    st.write(f"## 💰 Обща сума: **{total_cost:.2f} лв**")

    if total_cost <= budget:
        st.success("✅ Бюджетът е достатъчен!")
    else:
        st.error("❌ Бюджетът не достига.")
