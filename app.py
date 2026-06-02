import streamlit as st
import pandas as pd
import math

# Класс информационного агентства (из вашей практической)
class InfoAgency:
    def __init__(self):
        self.companies = []

    def add_company(self, name, country, city, address, phones, activity, products):
        company = {
            "name": name,
            "country": country,
            "city": city,
            "address": address,
            "phones": phones,
            "activity": activity,
            "products": products
        }
        self.companies.append(company)
        return True

    def find_by_country(self, country):
        result = [c for c in self.companies if c["country"].lower() == country.lower()]
        return result

    def find_by_city(self, city):
        result = [c for c in self.companies if c["city"].lower() == city.lower()]
        return result

    def quarterly_bulletin(self, quarter):
        return {
            "quarter": quarter,
            "total_organizations": len(self.companies),
            "companies": self.companies
        }

# Функция определения типа треугольника (из практической)
def triangle_type_and_area(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "Ошибка: стороны должны быть положительными", None
    if a + b <= c or a + c <= b or b + c <= a:
        return "Ошибка: треугольник с такими сторонами не существует", None
    if a == b == c:
        triangle_type = "Равносторонний"
    elif a == b or a == c or b == c:
        triangle_type = "Равнобедренный"
    else:
        triangle_type = "Разносторонний"
    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return triangle_type, area

# Инициализация сессии
if "agency" not in st.session_state:
    st.session_state.agency = InfoAgency()
    # Добавляем тестовые данные
    st.session_state.agency.add_company(
        "ООО ТехноСервис", "Россия", "Москва",
        "ул. Тверская, 10", "+7(495)123-45-67",
        "IT-услуги", "Разработка ПО"
    )
    st.session_state.agency.add_company(
        "БелИнфо", "Беларусь", "Минск",
        "пр. Независимости, 15", "+375(17)234-56-78",
        "Информационные услуги", "Новости, аналитика"
    )

# Навигация
st.set_page_config(page_title="Информационное агентство", page_icon="📰", layout="wide")

st.title("📰 Информационное агентство")
st.markdown("---")

# Боковое меню
menu = st.sidebar.radio(
    "Навигация",
    ["🏢 Организации", "➕ Добавить организацию", "🔍 Поиск", "📊 Бюллетень", "📐 Калькулятор треугольника", "🐛 Отладка модуля"]
)

# 1. Список организаций
if menu == "🏢 Организации":
    st.header("Список организаций")
    if len(st.session_state.agency.companies) == 0:
        st.info("Нет добавленных организаций")
    else:
        df = pd.DataFrame(st.session_state.agency.companies)
        st.dataframe(df, use_container_width=True)

# 2. Добавление организации
elif menu == "➕ Добавить организацию":
    st.header("Добавить новую организацию")
    with st.form("add_company_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Название*")
            country = st.text_input("Страна*")
            city = st.text_input("Город*")
            address = st.text_input("Адрес")
        with col2:
            phones = st.text_input("Телефоны")
            activity = st.text_input("Деятельность")
            products = st.text_input("Товары/услуги")
        submitted = st.form_submit_button("Добавить организацию")
        if submitted:
            if name and country and city:
                st.session_state.agency.add_company(name, country, city, address, phones, activity, products)
                st.success(f"Организация '{name}' успешно добавлена!")
                st.rerun()
            else:
                st.error("Название, страна и город обязательны для заполнения")

# 3. Поиск
elif menu == "🔍 Поиск":
    st.header("Поиск организаций")
    search_by = st.radio("Искать по:", ["Страна", "Город"])
    if search_by == "Страна":
        country = st.text_input("Введите страну")
        if st.button("Найти"):
            results = st.session_state.agency.find_by_country(country)
            if results:
                st.success(f"Найдено {len(results)} организаций")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Ничего не найдено")
    else:
        city = st.text_input("Введите город")
        if st.button("Найти"):
            results = st.session_state.agency.find_by_city(city)
            if results:
                st.success(f"Найдено {len(results)} организаций")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Ничего не найдено")

# 4. Бюллетень
elif menu == "📊 Бюллетень":
    st.header("Квартальный бюллетень")
    quarter = st.slider("Выберите квартал", 1, 4, 1)
    if st.button("Сформировать бюллетень"):
        bulletin = st.session_state.agency.quarterly_bulletin(quarter)
        st.subheader(f"📋 Бюллетень за {quarter}-й квартал")
        st.metric("Всего организаций", bulletin["total_organizations"])
        if bulletin["companies"]:
            st.write("### Список организаций:")
            for c in bulletin["companies"]:
                st.write(f"• **{c['name']}** ({c['country']}, {c['city']}) — {c['activity']}")

# 5. Калькулятор треугольника (из практической)
elif menu == "📐 Калькулятор треугольника":
    st.header("Определение вида треугольника и площади")
    st.markdown("Введите длины сторон треугольника:")
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Сторона A", min_value=0.0, step=0.1, format="%.1f")
    with col2:
        b = st.number_input("Сторона B", min_value=0.0, step=0.1, format="%.1f")
    with col3:
        c = st.number_input("Сторона C", min_value=0.0, step=0.1, format="%.1f")
    if st.button("Рассчитать"):
        result, area = triangle_type_and_area(a, b, c)
        if area is not None:
            st.success(f"**Тип треугольника:** {result}")
            st.success(f"**Площадь:** {area:.2f} кв. ед.")
        else:
            st.error(result)

# 6. Отладка модуля
elif menu == "🐛 Отладка модуля":
    st.header("Отладка программного модуля")
    st.markdown("### Точки останова и отладка (визуализация)")
    
    st.code("""
    # Точка останова установлена на agency.add_company(...)
    def main():
        agency = InfoAgency()
        # >>> ТОЧКА ОСТАНОВА ЗДЕСЬ (F9) <<<
        agency.add_company(
            "ООО ТехноСервис", "Россия", "Москва",
            "ул. Тверская, 10", "+7(495)123-45-67",
            "IT-услуги", "Разработка ПО"
        )
        print(agency.find_by_country("Россия"))
        print(agency.quarterly_bulletin(1))
    """, language="python")
    
    st.markdown("---")
    st.subheader("Текущее состояние данных (отладка)")
    
    if st.button("Показать содержимое self.companies"):
        st.write("### Содержимое st.session_state.agency.companies:")
        for i, company in enumerate(st.session_state.agency.companies):
            st.json(company)
    
    st.markdown("---")
    st.info("""
    **Процесс отладки:**
    - Точка останова устанавливается на agency.add_company(...)
    - Пошаговое выполнение позволяет проверить заполнение полей
    - При ошибке деления на ноль или обращения к пустому списку отладчик укажет строку
    - Окно локальных переменных показывает содержимое self.companies
    """)

st.sidebar.markdown("---")
st.sidebar.caption(f"Всего организаций в базе: {len(st.session_state.agency.companies)}")