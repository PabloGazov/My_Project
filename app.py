import streamlit as st
from abc import ABC, abstractmethod

# ================== DATA ==================

routes = {
    "България → Германия": ["София", "Белград", "Виена", "Мюнхен"]
}

city_info = {
    "София": {
        "hotel": ("Hotel Sofia Center", 70),
        "food": ("Традиционна българска кухня", 20),
        "sight": "Катедралата Александър Невски",
        "tour": 15
    },
    "Белград": {
        "hotel": ("Belgrade Inn", 65),
        "food": ("Сръбска скара", 22),
        "sight": "Калемегдан",
        "tour": 18
    },
    "Виена": {
        "hotel": ("Vienna City Hotel", 90),
        "food": ("Виенски шницел", 30),
        "sight": "Дворецът Шьонбрун",
        "tour": 25
    },
    "Мюнхен": {
        "hotel": ("Munich Central Hotel", 95),
        "food": ("Немска кухня", 28),
        "sight": "Мариенплац",
        "tour": 22
    }
}

DISTANCE_BETWEEN_CITIES = 300 # км

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

st.title("🌍 Интерактивен туристически планер")

route_choice = st.selectbox("Избери маршрут:", list(routes.keys()))

transport_choice = st.selectbox(
    "Превозно средство:",
    ["Кола", "Влак", "Самолет"]
)

trip_type = st.selectbox(
    "Тип пътуване:",
    ["Бюджетно", "Стандартно", "Луксозно"]
)

days = st.slider("Брой дни за пътуването:", 1, 10, 4)
budget = st.number_input("Твоят бюджет (лв):", 300, 5000, 1500)

guided_tours = st.checkbox("🎟️ Включи организирани турове")

# ================== MULTIPLIERS ==================

if trip_type == "Бюджетно":
    hotel_multiplier = 0.8
    food_multiplier = 0.8
elif trip_type == "Луксозно":
    hotel_multiplier = 1.3
    food_multiplier = 1.4
else:
    hotel_multiplier = 1.0
    food_multiplier = 1.0

# ================== ACTION ==================

if st.button("Планирай пътуването 🧭"):
    cities = routes[route_choice]

    if transport_choice == "Кола":
        transport = Car()
    elif transport_choice == "Влак":
        transport = Train()
    else:
        transport = Plane()

    st.subheader("🗺️ Маршрут")
    st.write(" ➡️ ".join(cities))

    total_food_cost = 0
    total_hotel_cost = 0
    total_tour_cost = 0

    st.subheader("🏙️ Спирки и разходи")

    for city in cities:
        info = city_info[city]

        hotel_cost = info["hotel"][1] * hotel_multiplier * days
        food_cost = info["food"][1] * food_multiplier * days
        tour_cost = info["tour"] * days if guided_tours else 0

        st.markdown(f"### 📍 {city}")
        st.write(f"🏨 Хотел: {hotel_cost:.2f} лв")
        st.write(f"🍽️ Храна: {food_cost:.2f} лв")
        st.write(f"🏛️ Забележителност: {info['sight']}")

        if guided_tours:
            st.write(f"🎟️ Турове: {tour_cost:.2f} лв")

        total_hotel_cost += hotel_cost
        total_food_cost += food_cost
        total_tour_cost += tour_cost

    total_distance = DISTANCE_BETWEEN_CITIES * (len(cities) - 1)
    transport_cost = transport.travel_cost(total_distance)

    total_cost = (
        transport_cost
        + total_food_cost
        + total_hotel_cost
        + total_tour_cost
    )

    st.subheader("💰 Обща сума")
    st.write(f"{transport.name()} – транспорт: {transport_cost:.2f} лв")
    st.write(f"🍽️ Храна: {total_food_cost:.2f} лв")
    st.write(f"🏨 Хотели: {total_hotel_cost:.2f} лв")

    if guided_tours:
        st.write(f"🎟️ Турове: {total_tour_cost:.2f} лв")

    st.markdown("---")
    st.write(f"## 💵 Общ бюджет: **{total_cost:.2f} лв**")

    if total_cost <= budget:
        st.success("✅ Бюджетът е достатъчен! Приятно пътуване ✨")
    else:
        st.error("❌ Бюджетът не достига. Опитай друг тип пътуване или по-малко дни.")
