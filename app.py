import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import json
import os

# ========== КЛАСС ИНФОРМАЦИОННОГО АГЕНТСТВА ==========
class InfoAgency:
    def __init__(self):
        self.companies = []

    def add_company(self, name, country, city, address, phones, activity, products, email="", website=""):
        company = {
            "id": len(self.companies) + 1,
            "name": name,
            "country": country,
            "city": city,
            "address": address,
            "phones": phones,
            "email": email,
            "website": website,
            "activity": activity,
            "products": products,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.companies.append(company)
        return True

    def find_by_country(self, country):
        return [c for c in self.companies if c["country"].lower() == country.lower()]

    def find_by_city(self, city):
        return [c for c in self.companies if c["city"].lower() == city.lower()]
    
    def find_by_name(self, name):
        return [c for c in self.companies if name.lower() in c["name"].lower()]
    
    def find_by_activity(self, activity):
        return [c for c in self.companies if activity.lower() in c["activity"].lower()]

    def get_statistics(self):
        if not self.companies:
            return {"total": 0, "countries": [], "cities": [], "activities": []}
        countries = list(set(c["country"] for c in self.companies))
        cities = list(set(c["city"] for c in self.companies))
        activities = list(set(c["activity"] for c in self.companies if c["activity"]))
        return {
            "total": len(self.companies),
            "countries": countries,
            "cities": cities,
            "activities": activities
        }
    
    def quarterly_bulletin(self, quarter):
        return {
            "quarter": quarter,
            "date": datetime.now().strftime("%d.%m.%Y"),
            "total": len(self.companies),
            "companies": self.companies
        }

# ========== СИСТЕМА АВТОРИЗАЦИИ ==========
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_users():
    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "Администратор"
            },
            "user": {
                "password": hash_password("user123"),
                "role": "user",
                "name": "Пользователь"
            }
        }

def check_auth(username, password):
    if username in st.session_state.users:
        if st.session_state.users[username]["password"] == hash_password(password):
            return True
    return False

def login():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
            st.markdown("<h2 style='text-align:center'>📰 Информационное агентство</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#666'>Вход в систему</p>", unsafe_allow_html=True)
            
            username = st.text_input("👤 Имя пользователя", key="login_username")
            password = st.text_input("🔒 Пароль", type="password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚪 Войти", use_container_width=True):
                    if check_auth(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_name = st.session_state.users[username]["name"]
                        st.session_state.user_role = st.session_state.users[username]["role"]
                        st.rerun()
                    else:
                        st.error("❌ Неверное имя пользователя или пароль")
            with col2:
                st.markdown("<p style='font-size:12px; color:#999; margin-top:10px'><br>demo: admin/admin123 или user/user123</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    for key in ["logged_in", "username", "user_name", "user_role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ========== КРАСИВЫЙ CSS ==========
def apply_css():
    st.markdown("""
    <style>
    /* Основные цвета */
    :root {
        --primary: #667eea;
        --primary-dark: #5a67d8;
        --secondary: #f093fb;
        --success: #48bb78;
        --warning: #ed8936;
        --danger: #f56565;
        --dark: #2d3748;
        --light: #f7fafc;
    }
    
    /* Шапка */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Карточки */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        transition: transform 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-label {
        color: #718096;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Кнопки */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    /* Боковое меню */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    /* Таблицы */
    .dataframe {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px;
    }
    
    /* Формы */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Алерты */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* Футер */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
        color: #718096;
        font-size: 0.8rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)

# ========== ОСНОВНЫЕ СТРАНИЦЫ ==========
def page_dashboard():
    stats = st.session_state.agency.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total']}</div>
            <div class="stat-label">📋 Организаций</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(stats['countries'])}</div>
            <div class="stat-label">🌍 Стран</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(stats['cities'])}</div>
            <div class="stat-label">🏙️ Городов</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(stats['activities'])}</div>
            <div class="stat-label">📊 Сфер деятельности</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if stats['total'] > 0:
        st.subheader("📋 Последние добавленные организации")
        df = pd.DataFrame(st.session_state.agency.companies[-5:])
        df_display = df[["name", "country", "city", "activity"]]
        df_display.columns = ["Название", "Страна", "Город", "Деятельность"]
        st.dataframe(df_display, use_container_width=True)

def page_add_company():
    st.markdown("## ➕ Добавление новой организации")
    st.markdown("Заполните информацию о компании или агентстве")
    
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("🏢 Название организации *", placeholder="ООО Пример")
            country = st.text_input("🌍 Страна *", placeholder="Россия")
            city = st.text_input("🏙️ Город *", placeholder="Москва")
            address = st.text_input("📍 Адрес", placeholder="ул. Примерная, д. 1")
        with col2:
            phones = st.text_input("📞 Телефоны", placeholder="+7 (123) 456-78-90")
            email = st.text_input("✉️ Email", placeholder="info@example.com")
            website = st.text_input("🌐 Сайт", placeholder="www.example.com")
            activity = st.text_input("⚙️ Деятельность", placeholder="IT-услуги, консалтинг...")
        products = st.text_area("📦 Товары/услуги", placeholder="Перечислите основные товары или услуги")
        
        st.markdown("* — обязательные поля")
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            submitted = st.form_submit_button("✅ Добавить организацию", use_container_width=True)
        
        if submitted:
            if name and country and city:
                st.session_state.agency.add_company(name, country, city, address, phones, activity, products, email, website)
                st.success(f"🎉 Организация **{name}** успешно добавлена!")
                st.balloons()
            else:
                st.error("❌ Пожалуйста, заполните обязательные поля: Название, Страна, Город")

def page_search():
    st.markdown("## 🔍 Поиск организаций")
    
    search_type = st.radio(
        "Искать по:",
        ["🌍 Страна", "🏙️ Город", "🏢 Название", "⚙️ Деятельность"],
        horizontal=True
    )
    
    search_map = {
        "🌍 Страна": ("country", "Введите название страны", st.session_state.agency.find_by_country),
        "🏙️ Город": ("city", "Введите название города", st.session_state.agency.find_by_city),
        "🏢 Название": ("name", "Введите название организации", st.session_state.agency.find_by_name),
        "⚙️ Деятельность": ("activity", "Введите вид деятельности", st.session_state.agency.find_by_activity)
    }
    
    key, placeholder, search_func = search_map[search_type]
    query = st.text_input(placeholder, key="search_query")
    
    if query:
        results = search_func(query)
        if results:
            st.success(f"🔎 Найдено **{len(results)}** организаций")
            df = pd.DataFrame(results)
            display_cols = ["name", "country", "city", "phones", "activity"]
            df_display = df[[c for c in display_cols if c in df.columns]]
            df_display.columns = ["Название", "Страна", "Город", "Телефоны", "Деятельность"]
            st.dataframe(df_display, use_container_width=True)
            
            with st.expander("📋 Подробная информация"):
                for r in results:
                    st.markdown(f"""
                    ---
                    **🏢 {r['name']}**  
                    📍 {r['country']}, {r['city']}, {r['address']}  
                    📞 {r['phones']} | ✉️ {r.get('email', '—')} | 🌐 {r.get('website', '—')}  
                    ⚙️ *{r['activity']}*  
                    📦 {r['products']}
                    """)
        else:
            st.warning("😕 Ничего не найдено. Попробуйте изменить поисковый запрос.")

def page_bulletin():
    st.markdown("## 📊 Квартальный бюллетень")
    
    col1, col2 = st.columns([1,2])
    with col1:
        quarter = st.selectbox("Выберите квартал", [1, 2, 3, 4], format_func=lambda x: f"{x}-й квартал")
        if st.button("📄 Сформировать бюллетень", use_container_width=True):
            bulletin = st.session_state.agency.quarterly_bulletin(quarter)
            st.session_state.bulletin_data = bulletin
    
    if "bulletin_data" in st.session_state:
        b = st.session_state.bulletin_data
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); padding: 1.5rem; border-radius: 15px; margin: 1rem 0">
            <h3 style="margin:0">📋 ИНФОРМАЦИОННЫЙ БЮЛЛЕТЕНЬ</h3>
            <p style="color:#666">за {b['quarter']}-й квартал {b['date']}</p>
            <hr>
            <p><strong>Всего организаций в базе:</strong> {b['total']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if b['companies']:
            st.subheader("Список организаций")
            for c in b['companies']:
                with st.expander(f"🏢 {c['name']} — {c['country']}, {c['city']}"):
                    st.markdown(f"""
                    - **📍 Адрес:** {c['address']}
                    - **📞 Контакты:** {c['phones']}
                    - **⚙️ Деятельность:** {c['activity']}
                    - **📦 Товары/услуги:** {c['products']}
                    - **📅 Добавлена:** {c['created_at']}
                    """)

def page_companies_list():
    st.markdown("## 🏢 Все организации")
    
    if st.session_state.agency.companies:
        df = pd.DataFrame(st.session_state.agency.companies)
        display_cols = ["name", "country", "city", "phones", "email", "activity"]
        df_display = df[[c for c in display_cols if c in df.columns]]
        df_display.columns = ["Название", "Страна", "Город", "Телефоны", "Email", "Деятельность"]
        st.dataframe(df_display, use_container_width=True)
        
        # Экспорт
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Скачать список (CSV)",
            data=csv,
            file_name=f"organizations_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("📭 Нет добавленных организаций. Перейдите в раздел '➕ Добавить организацию'")

def page_profile():
    st.markdown("## 👤 Мой профиль")
    
    col1, col2 = st.columns([1,2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
    with col2:
        st.markdown(f"""
        <div style="margin-top: 1rem">
            <p><strong>Имя пользователя:</strong> {st.session_state.username}</p>
            <p><strong>Роль:</strong> {st.session_state.user_role}</p>
            <p><strong>Имя:</strong> {st.session_state.user_name}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🚪 Выйти из системы"):
        logout()

def page_about():
    st.markdown("## 📰 Об информационной системе")
    st.markdown("""
    ### Информационное агентство — система управления организациями
    
    **Возможности системы:**
    - 📝 Добавление и хранение информации об организациях
    - 🔍 Поиск по странам, городам, названиям и видам деятельности
    - 📊 Формирование квартальных бюллетеней
    - 📥 Экспорт данных в CSV
    - 👥 Система авторизации пользователей
    
    **Технологии:**
    - Python + Streamlit
    - Современный адаптивный дизайн
    - Хранение данных в сессии
    
    **Демо-доступ:**
    - Администратор: `admin` / `admin123`
    - Пользователь: `user` / `user123`
    """)

# ========== ГЛАВНАЯ ФУНКЦИЯ ==========
def main():
    apply_css()
    
    # Инициализация
    init_users()
    
    if "agency" not in st.session_state:
        st.session_state.agency = InfoAgency()
        # Тестовые данные
        if not st.session_state.agency.companies:
            st.session_state.agency.add_company(
                "ТАСС", "Россия", "Москва",
                "Тверской бульвар, 2", "+7 (495) 123-45-67",
                "Информационное агентство", "Новости, репортажи, аналитика",
                "info@tass.ru", "www.tass.ru"
            )
            st.session_state.agency.add_company(
                "Рейтер", "Великобритания", "Лондон",
                "Canary Wharf, 5", "+44 20 1234 5678",
                "Новостное агентство", "Финансовые новости, медиа",
                "info@reuters.com", "www.reuters.com"
            )
            st.session_state.agency.add_company(
                "БелТА", "Беларусь", "Минск",
                "пр. Независимости, 45", "+375 (17) 234-56-78",
                "Информационное агентство", "Новости Беларуси и мира",
                "info@belta.by", "www.belta.by"
            )
    
    # Проверка авторизации
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login()
        return
    
    # ШАПКА
    st.markdown(f"""
    <div class="main-header">
        <h1>📰 Информационное агентство</h1>
        <p>Единая база организаций и компаний</p>
        <p style="font-size:0.8rem; margin-top:1rem">👋 Добро пожаловать, {st.session_state.user_name}!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # БОКОВОЕ МЕНЮ
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.markdown(f"### {st.session_state.user_name}")
        st.markdown(f"<small>@{st.session_state.username}</small>", unsafe_allow_html=True)
        st.markdown("---")
        
        menu_options = {
            "🏠 Дашборд": page_dashboard,
            "➕ Добавить организацию": page_add_company,
            "🔍 Поиск": page_search,
            "📊 Бюллетень": page_bulletin,
            "🏢 Список организаций": page_companies_list,
            "👤 Мой профиль": page_profile,
            "ℹ️ О системе": page_about
        }
        
        choice = st.radio("Меню", list(menu_options.keys()))
        st.markdown("---")
        
        # Статистика в сайдбаре
        stats = st.session_state.agency.get_statistics()
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 0.8rem; margin-top: 1rem">
            <p style="font-size:0.8rem; margin:0">📊 Всего: {stats['total']}</p>
            <p style="font-size:0.8rem; margin:0">🌍 Стран: {len(stats['countries'])}</p>
            <p style="font-size:0.8rem; margin:0">🏙️ Городов: {len(stats['cities'])}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ОТОБРАЖЕНИЕ ВЫБРАННОЙ СТРАНИЦЫ
    menu_options[choice]()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Информационное агентство",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    main()