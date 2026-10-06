import json
import math
import os
import calendar
import shutil
import threading
import time
import sys
import uuid
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import webbrowser
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from urllib.request import Request, urlopen

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.figure import Figure

APP_DIR = os.path.dirname(
    sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
)
DATA_FILE = os.path.join(APP_DIR, "data.json")
SETTINGS_FILE = os.path.join(APP_DIR, "settings.json")
APP_RESOURCE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
APP_ICON_FILE = os.path.join(APP_RESOURCE_DIR, "budget-tracker.ico")
RATES_URL = "https://open.er-api.com/v6/latest/USD"
RATES_PROVIDER_URL = "https://www.exchangerate-api.com/"
CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "JPY": "Japanese Yen",
    "INR": "Indian Rupee",
    "RUB": "Russian Ruble",
    "TRY": "Turkish Lira"
}
CURRENCY_SYMBOLS = {
    "USD": "$", "EUR": "€", "GBP": "£", "CAD": "CA$",
    "AUD": "A$", "JPY": "¥", "INR": "₹", "RUB": "₽", "TRY": "₺"
}
LANGUAGES = {
    "en": "English", "es": "Español", "ru": "Русский",
    "tr": "Türkçe", "ja": "日本語", "hi": "हिन्दी"
}
LANGUAGE_CURRENCIES = {
    "en": "USD", "es": "EUR", "ru": "RUB",
    "tr": "TRY", "ja": "JPY", "hi": "INR"
}
CURRENCY_NAMES = {
    "en": CURRENCIES,
    "es": {
        "USD": "Dólar estadounidense", "EUR": "Euro", "GBP": "Libra esterlina",
        "CAD": "Dólar canadiense", "AUD": "Dólar australiano", "JPY": "Yen japonés",
        "INR": "Rupia india", "RUB": "Rublo ruso", "TRY": "Lira turca"
    },
    "ru": {
        "USD": "Доллар США", "EUR": "Евро", "GBP": "Британский фунт",
        "CAD": "Канадский доллар", "AUD": "Австралийский доллар", "JPY": "Японская иена",
        "INR": "Индийская рупия", "RUB": "Российский рубль", "TRY": "Турецкая лира"
    },
    "tr": {
        "USD": "ABD doları", "EUR": "Euro", "GBP": "İngiliz sterlini",
        "CAD": "Kanada doları", "AUD": "Avustralya doları", "JPY": "Japon yeni",
        "INR": "Hindistan rupisi", "RUB": "Rus rublesi", "TRY": "Türk lirası"
    },
    "ja": {
        "USD": "米ドル", "EUR": "ユーロ", "GBP": "英ポンド",
        "CAD": "カナダドル", "AUD": "オーストラリアドル", "JPY": "日本円",
        "INR": "インドルピー", "RUB": "ロシアルーブル", "TRY": "トルコリラ"
    },
    "hi": {
        "USD": "अमेरिकी डॉलर", "EUR": "यूरो", "GBP": "ब्रिटिश पाउंड",
        "CAD": "कनाडाई डॉलर", "AUD": "ऑस्ट्रेलियाई डॉलर", "JPY": "जापानी येन",
        "INR": "भारतीय रुपया", "RUB": "रूसी रूबल", "TRY": "तुर्की लीरा"
    }
}


def set_app_icon(window):
    if os.path.exists(APP_ICON_FILE):
        try:
            window.iconbitmap(APP_ICON_FILE)
        except tk.TclError:
            pass


TEXT = {
    "en": {
        "welcome": "Welcome to Budget Tracker",
        "window_title": "Personal Budget Tracker",
        "setup_description": "Choose your language and currency to get started.",
        "language": "Language",
        "currency": "Currency",
        "continue": "Continue",
        "settings": "Settings",
        "theme": "Theme",
        "light": "Light",
        "dark": "Dark",
        "reset_data": "Reset data",
        "change_language": "Change language",
        "change_currency": "Change currency",
        "overview": "Overview",
        "subtitle": "A clear view of what comes in and goes out",
        "add_tab": "Add transaction",
        "history_tab": "History",
        "total_income": "Total income",
        "total_expense": "Total expenses",
        "net_balance": "Net balance",
        "spending_insights": "Spending insights",
        "chart": "Chart",
        "period": "Period",
        "chart_income_expense": "Income vs expenses",
        "chart_monthly_cash": "Monthly cash flow",
        "chart_category_bar": "Spending by category",
        "chart_category_pie": "Category share",
        "chart_monthly_bars": "Monthly comparison",
        "chart_balance": "Cumulative balance",
        "all_time": "All time",
        "last_30_days": "Last 30 days",
        "last_90_days": "Last 90 days",
        "last_6_months": "Last 6 months",
        "last_12_months": "Last 12 months",
        "this_year": "This year",
        "income": "Income",
        "expense": "Expense",
        "expenses": "Expenses",
        "amount": "Amount",
        "record_transaction": "Record a transaction",
        "transaction_description": "Enter an amount and category to update your totals.",
        "type": "Type",
        "category": "Category",
        "category_examples": "Examples: salary, food, rent",
        "add_transaction": "Add transaction",
        "transactions": "Transactions",
        "date": "Date",
        "rename_category": "Rename expense category",
        "invalid_amount": "Invalid amount",
        "amount_positive": "Enter an amount greater than zero.",
        "missing_category": "Missing category",
        "enter_category": "Enter a category for this transaction.",
        "no_transactions": "No transactions for this period",
        "no_dated_transactions": "No dated transactions for this period",
        "no_expenses": "No expenses for this period",
        "no_categories": "No categories",
        "add_expense_first": "Add an expense before renaming a category.",
        "rename_title": "Rename expense category",
        "current_category": "Current category",
        "new_category": "New category name",
        "missing_name": "Missing name",
        "enter_new_name": "Enter a new category name.",
        "cancel": "Cancel",
        "rename": "Rename",
        "reset_title": "Reset budget data",
        "reset_warning": "This permanently deletes all income and expense records. Continue?",
        "previous_year": "Previous year",
        "edit_transaction": "Edit transaction",
        "delete_transaction": "Delete transaction",
        "confirm_delete": "Delete this transaction permanently?",
        "search": "Search",
        "all_types": "All types",
        "all_categories": "All categories",
        "from_date": "From YYYY-MM-DD",
        "to_date": "To YYYY-MM-DD",
        "apply_filters": "Apply",
        "export_csv": "Export CSV",
        "no_selection": "Select a transaction first.",
        "saved": "Saved",
        "export_complete": "Transactions exported successfully.",
        "repeat_monthly": "Repeat monthly",
        "plan_tab": "Budgets & advice",
        "budget_title": "Monthly category budgets",
        "manage_budgets": "Manage budgets",
        "delete_budget": "Delete budget",
        "monthly_limit": "Monthly limit",
        "spent": "Spent this month",
        "remaining": "Remaining",
        "guidance_title": "Money guidance",
        "budget_advice": "Use the 50/30/20 guideline as a flexible starting point: up to 50% for needs, 30% for wants (including dining out), and 20% for savings or debt repayment. Groceries and dining out are different; adjust the guide for your income and obligations.",
        "investment_note": "There is no universally suitable stock percentage, such as 25%. Investing depends on your time horizon, emergency savings, debts, and risk tolerance.",
        "over_budget": "Over budget",
        "on_track": "On track",
        "monthly_income": "Income this month",
        "budget_saved": "Save budget",
        "status": "Status",
        "add_income_first": "Add income to calculate your monthly spending ratio.",
        "spending_ratio": "Your expenses are {ratio:.0f}% of this month's income.",
        "spending_over_income": "Expenses are above income. Review flexible spending and recurring bills.",
        "spending_near_limit": "You're using over 80% of income; check upcoming bills before optional spending.",
        "spending_under_limit": "Consider directing some remaining income toward savings or high-interest debt.",
        "delete_recurring_warning": "This transaction repeats monthly. Deleting it will also stop future repeats. Continue?"
    },
    "es": {
        "welcome": "Bienvenido a Budget Tracker",
        "window_title": "Control de presupuesto personal",
        "setup_description": "Elige tu idioma y moneda para comenzar.",
        "language": "Idioma",
        "currency": "Moneda",
        "continue": "Continuar",
        "settings": "Configuración",
        "theme": "Tema",
        "light": "Claro",
        "dark": "Oscuro",
        "reset_data": "Borrar datos",
        "change_language": "Cambiar idioma",
        "change_currency": "Cambiar moneda",
        "overview": "Resumen",
        "subtitle": "Una vista clara de tus ingresos y gastos",
        "add_tab": "Añadir transacción",
        "history_tab": "Historial",
        "total_income": "Ingresos totales",
        "total_expense": "Gastos totales",
        "net_balance": "Saldo neto",
        "spending_insights": "Análisis de gastos",
        "chart": "Gráfico",
        "period": "Período",
        "chart_income_expense": "Ingresos y gastos",
        "chart_monthly_cash": "Flujo mensual",
        "chart_category_bar": "Gastos por categoría",
        "chart_category_pie": "Proporción por categoría",
        "chart_monthly_bars": "Comparación mensual",
        "chart_balance": "Saldo acumulado",
        "all_time": "Todo el período",
        "last_30_days": "Últimos 30 días",
        "last_90_days": "Últimos 90 días",
        "last_6_months": "Últimos 6 meses",
        "last_12_months": "Últimos 12 meses",
        "this_year": "Este año",
        "income": "Ingreso",
        "expense": "Gasto",
        "expenses": "Gastos",
        "amount": "Importe",
        "record_transaction": "Registrar transacción",
        "transaction_description": "Indica el importe y la categoría para actualizar tus totales.",
        "type": "Tipo",
        "category": "Categoría",
        "category_examples": "Ejemplos: salario, comida, alquiler",
        "add_transaction": "Añadir transacción",
        "transactions": "Transacciones",
        "date": "Fecha",
        "rename_category": "Cambiar categoría de gasto",
        "invalid_amount": "Importe no válido",
        "amount_positive": "Introduce un importe mayor que cero.",
        "missing_category": "Falta la categoría",
        "enter_category": "Introduce una categoría para esta transacción.",
        "no_transactions": "No hay transacciones en este período",
        "no_dated_transactions": "No hay transacciones fechadas en este período",
        "no_expenses": "No hay gastos en este período",
        "no_categories": "Sin categorías",
        "add_expense_first": "Añade un gasto antes de cambiar una categoría.",
        "rename_title": "Cambiar categoría de gasto",
        "current_category": "Categoría actual",
        "new_category": "Nombre de la nueva categoría",
        "missing_name": "Falta el nombre",
        "enter_new_name": "Introduce el nombre de la nueva categoría.",
        "cancel": "Cancelar",
        "rename": "Cambiar nombre",
        "reset_title": "Borrar datos del presupuesto",
        "reset_warning": "Se borrarán permanentemente todos los ingresos y gastos. ¿Continuar?",
        "previous_year": "Año anterior"
    },
    "ru": {
        "welcome": "Добро пожаловать в Budget Tracker",
        "window_title": "Личный бюджет",
        "setup_description": "Выберите язык и валюту, чтобы начать.",
        "language": "Язык", "currency": "Валюта", "continue": "Продолжить",
        "settings": "Настройки", "theme": "Тема", "light": "Светлая", "dark": "Тёмная",
        "reset_data": "Сбросить данные", "change_language": "Сменить язык",
        "change_currency": "Сменить валюту", "overview": "Обзор",
        "subtitle": "Доходы и расходы в одном месте", "add_tab": "Добавить операцию",
        "history_tab": "История", "total_income": "Общий доход",
        "total_expense": "Общие расходы", "net_balance": "Итоговый баланс",
        "spending_insights": "Анализ расходов", "chart": "График", "period": "Период",
        "chart_income_expense": "Доходы и расходы", "chart_monthly_cash": "Денежный поток по месяцам",
        "chart_category_bar": "Расходы по категориям", "chart_category_pie": "Доли расходов",
        "chart_monthly_bars": "Сравнение по месяцам", "chart_balance": "Накопительный баланс",
        "all_time": "За всё время", "last_30_days": "Последние 30 дней",
        "last_90_days": "Последние 90 дней", "last_6_months": "Последние 6 месяцев",
        "last_12_months": "Последние 12 месяцев", "this_year": "Этот год",
        "income": "Доход", "expense": "Расход", "expenses": "Расходы",
        "amount": "Сумма", "record_transaction": "Добавить операцию",
        "transaction_description": "Укажите сумму и категорию, чтобы обновить итоги.",
        "type": "Тип", "category": "Категория",
        "category_examples": "Например: зарплата, продукты, аренда",
        "add_transaction": "Добавить операцию", "transactions": "Операции", "date": "Дата",
        "rename_category": "Переименовать категорию расходов", "invalid_amount": "Неверная сумма",
        "amount_positive": "Введите сумму больше нуля.", "missing_category": "Нет категории",
        "enter_category": "Укажите категорию операции.",
        "no_transactions": "За этот период операций нет",
        "no_dated_transactions": "За этот период нет операций с датой",
        "no_expenses": "За этот период расходов нет", "no_categories": "Нет категорий",
        "add_expense_first": "Сначала добавьте расход.", "rename_title": "Переименовать категорию",
        "current_category": "Текущая категория", "new_category": "Новое название категории",
        "missing_name": "Нет названия", "enter_new_name": "Введите новое название категории.",
        "cancel": "Отмена", "rename": "Переименовать", "reset_title": "Сбросить бюджет",
        "reset_warning": "Все доходы и расходы будут удалены. Продолжить?",
        "previous_year": "Прошлый год"
    },
    "tr": {
        "welcome": "Budget Tracker'a hoş geldiniz",
        "window_title": "Kişisel Bütçe Takipçisi",
        "setup_description": "Başlamak için dilinizi ve para biriminizi seçin.",
        "language": "Dil", "currency": "Para birimi", "continue": "Devam et",
        "settings": "Ayarlar", "theme": "Tema", "light": "Açık", "dark": "Koyu",
        "reset_data": "Verileri sıfırla", "change_language": "Dili değiştir",
        "change_currency": "Para birimini değiştir", "overview": "Genel bakış",
        "subtitle": "Gelir ve giderlerinizi bir arada görün", "add_tab": "İşlem ekle",
        "history_tab": "Geçmiş", "total_income": "Toplam gelir",
        "total_expense": "Toplam gider", "net_balance": "Net bakiye",
        "spending_insights": "Harcama analizi", "chart": "Grafik", "period": "Dönem",
        "chart_income_expense": "Gelir ve giderler", "chart_monthly_cash": "Aylık nakit akışı",
        "chart_category_bar": "Kategoriye göre giderler", "chart_category_pie": "Kategori payı",
        "chart_monthly_bars": "Aylık karşılaştırma", "chart_balance": "Birikimli bakiye",
        "all_time": "Tüm zamanlar", "last_30_days": "Son 30 gün",
        "last_90_days": "Son 90 gün", "last_6_months": "Son 6 ay",
        "last_12_months": "Son 12 ay", "this_year": "Bu yıl",
        "income": "Gelir", "expense": "Gider", "expenses": "Giderler",
        "amount": "Tutar", "record_transaction": "İşlem kaydet",
        "transaction_description": "Toplamları güncellemek için tutar ve kategori girin.",
        "type": "Tür", "category": "Kategori", "category_examples": "Örnekler: maaş, yemek, kira",
        "add_transaction": "İşlem ekle", "transactions": "İşlemler", "date": "Tarih",
        "rename_category": "Gider kategorisini yeniden adlandır", "invalid_amount": "Geçersiz tutar",
        "amount_positive": "Sıfırdan büyük bir tutar girin.", "missing_category": "Kategori eksik",
        "enter_category": "Bu işlem için bir kategori girin.",
        "no_transactions": "Bu dönemde işlem yok",
        "no_dated_transactions": "Bu dönemde tarihli işlem yok",
        "no_expenses": "Bu dönemde gider yok", "no_categories": "Kategori bulunamadı",
        "add_expense_first": "Kategori değiştirmeden önce bir gider ekleyin.",
        "rename_title": "Gider kategorisini yeniden adlandır",
        "current_category": "Mevcut kategori", "new_category": "Yeni kategori adı",
        "missing_name": "Ad eksik", "enter_new_name": "Yeni bir kategori adı girin.",
        "cancel": "İptal", "rename": "Yeniden adlandır", "reset_title": "Bütçe verilerini sıfırla",
        "reset_warning": "Tüm gelir ve gider kayıtları kalıcı olarak silinecek. Devam edilsin mi?",
        "previous_year": "Geçen yıl"
    },
    "ja": {
        "welcome": "Budget Trackerへようこそ",
        "window_title": "家計簿",
        "setup_description": "開始するには、言語と通貨を選択してください。",
        "language": "言語", "currency": "通貨", "continue": "続行",
        "settings": "設定", "theme": "テーマ", "light": "ライト", "dark": "ダーク",
        "reset_data": "データをリセット", "change_language": "言語を変更",
        "change_currency": "通貨を変更", "overview": "概要",
        "subtitle": "収入と支出をひと目で確認", "add_tab": "取引を追加",
        "history_tab": "履歴", "total_income": "収入合計",
        "total_expense": "支出合計", "net_balance": "差引残高",
        "spending_insights": "支出分析", "chart": "グラフ", "period": "期間",
        "chart_income_expense": "収入と支出", "chart_monthly_cash": "月ごとの収支推移",
        "chart_category_bar": "カテゴリ別支出", "chart_category_pie": "カテゴリ別割合",
        "chart_monthly_bars": "月ごとの比較", "chart_balance": "累積残高",
        "all_time": "全期間", "last_30_days": "過去30日間",
        "last_90_days": "過去90日間", "last_6_months": "過去6か月",
        "last_12_months": "過去12か月", "this_year": "今年",
        "income": "収入", "expense": "支出", "expenses": "支出",
        "amount": "金額", "record_transaction": "取引を記録",
        "transaction_description": "金額とカテゴリを入力して合計を更新します。",
        "type": "種類", "category": "カテゴリ", "category_examples": "例: 給与、食費、家賃",
        "add_transaction": "取引を追加", "transactions": "取引", "date": "日付",
        "rename_category": "支出カテゴリ名を変更", "invalid_amount": "金額が無効です",
        "amount_positive": "0より大きい金額を入力してください。", "missing_category": "カテゴリが未入力です",
        "enter_category": "取引のカテゴリを入力してください。",
        "no_transactions": "この期間の取引はありません",
        "no_dated_transactions": "この期間に日付付きの取引はありません",
        "no_expenses": "この期間の支出はありません", "no_categories": "カテゴリがありません",
        "add_expense_first": "カテゴリを変更する前に支出を追加してください。",
        "rename_title": "支出カテゴリ名を変更", "current_category": "現在のカテゴリ",
        "new_category": "新しいカテゴリ名", "missing_name": "名前が未入力です",
        "enter_new_name": "新しいカテゴリ名を入力してください。", "cancel": "キャンセル",
        "rename": "変更", "reset_title": "予算データをリセット",
        "reset_warning": "すべての収入と支出の記録が削除されます。続行しますか？",
        "previous_year": "前年"
    },
    "hi": {
        "welcome": "बजट ट्रैकर में आपका स्वागत है",
        "window_title": "व्यक्तिगत बजट ट्रैकर",
        "setup_description": "शुरू करने के लिए भाषा और मुद्रा चुनें।",
        "language": "भाषा", "currency": "मुद्रा", "continue": "जारी रखें",
        "settings": "सेटिंग्स", "theme": "थीम", "light": "लाइट", "dark": "डार्क",
        "reset_data": "डेटा रीसेट करें", "change_language": "भाषा बदलें",
        "change_currency": "मुद्रा बदलें", "overview": "अवलोकन",
        "subtitle": "आय और खर्च का साफ़ विवरण", "add_tab": "लेन-देन जोड़ें",
        "history_tab": "इतिहास", "total_income": "कुल आय",
        "total_expense": "कुल खर्च", "net_balance": "शुद्ध शेष",
        "spending_insights": "खर्च का विश्लेषण", "chart": "चार्ट", "period": "अवधि",
        "chart_income_expense": "आय और खर्च", "chart_monthly_cash": "मासिक नकदी प्रवाह",
        "chart_category_bar": "श्रेणी के अनुसार खर्च", "chart_category_pie": "श्रेणी का हिस्सा",
        "chart_monthly_bars": "मासिक तुलना", "chart_balance": "संचयी शेष",
        "all_time": "पूरी अवधि", "last_30_days": "पिछले 30 दिन",
        "last_90_days": "पिछले 90 दिन", "last_6_months": "पिछले 6 महीने",
        "last_12_months": "पिछले 12 महीने", "this_year": "इस वर्ष",
        "income": "आय", "expense": "खर्च", "expenses": "खर्च",
        "amount": "राशि", "record_transaction": "लेन-देन दर्ज करें",
        "transaction_description": "कुल अपडेट करने के लिए राशि और श्रेणी दर्ज करें।",
        "type": "प्रकार", "category": "श्रेणी", "category_examples": "उदाहरण: वेतन, भोजन, किराया",
        "add_transaction": "लेन-देन जोड़ें", "transactions": "लेन-देन", "date": "तारीख",
        "rename_category": "खर्च की श्रेणी का नाम बदलें", "invalid_amount": "अमान्य राशि",
        "amount_positive": "शून्य से बड़ी राशि दर्ज करें।", "missing_category": "श्रेणी खाली है",
        "enter_category": "इस लेन-देन की श्रेणी दर्ज करें।",
        "no_transactions": "इस अवधि में कोई लेन-देन नहीं",
        "no_dated_transactions": "इस अवधि में तारीख वाला लेन-देन नहीं",
        "no_expenses": "इस अवधि में कोई खर्च नहीं", "no_categories": "कोई श्रेणी नहीं",
        "add_expense_first": "श्रेणी बदलने से पहले खर्च जोड़ें।",
        "rename_title": "खर्च की श्रेणी का नाम बदलें", "current_category": "मौजूदा श्रेणी",
        "new_category": "नई श्रेणी का नाम", "missing_name": "नाम खाली है",
        "enter_new_name": "नई श्रेणी का नाम दर्ज करें।", "cancel": "रद्द करें",
        "rename": "नाम बदलें", "reset_title": "बजट डेटा रीसेट करें",
        "reset_warning": "आय और खर्च के सभी रिकॉर्ड स्थायी रूप से हट जाएंगे। जारी रखें?",
        "previous_year": "पिछला वर्ष"
    }
}
CHART_KEYS = (
    "chart_income_expense", "chart_monthly_cash", "chart_category_bar",
    "chart_category_pie", "chart_monthly_bars", "chart_balance"
)
PERIOD_KEYS = (
    "all_time", "last_30_days", "last_90_days", "last_6_months",
    "last_12_months", "this_year", "previous_year"
)


def currency_option(code, language):
    name = CURRENCY_NAMES.get(language, CURRENCY_NAMES["en"]).get(code, CURRENCIES[code])
    return f"{code} - {name}"


def fetch_exchange_rates():
    request = Request(RATES_URL, headers={"User-Agent": "BudgetTracker/1.0"})
    with urlopen(request, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))
    rates = payload.get("rates", {})
    if payload.get("result") != "success" or not isinstance(rates, dict):
        raise ValueError("The exchange-rate service returned invalid data.")
    valid_rates = {}
    for code in CURRENCIES:
        try:
            rate = float(rates[code])
        except (KeyError, TypeError, ValueError):
            continue
        if math.isfinite(rate) and rate > 0:
            valid_rates[code] = rate
    if "USD" not in valid_rates:
        raise ValueError("The exchange-rate response did not include USD.")
    return valid_rates


def convert_currency_amount(amount, source_currency, target_currency, rates):
    source_rate = Decimal(str(rates[source_currency]))
    target_rate = Decimal(str(rates[target_currency]))
    if not all(rate.is_finite() and rate > 0 for rate in (source_rate, target_rate)):
        raise ValueError("Exchange rates must be positive finite numbers.")
    return Decimal(str(amount)) * target_rate / source_rate


def preferred_font(language):
    return {"ja": "Yu Gothic UI", "hi": "Nirmala UI"}.get(language, "Segoe UI")


def get_total_amount(records):
    total = Decimal(0)
    for item in records:
        if isinstance(item, dict):
            amount = item.get("amount", 0)
        else:
            amount = item
        try:
            total += Decimal(str(amount))
        except (InvalidOperation, TypeError, ValueError):
            continue
    return total


def save_data(incomes, expenses, recurring=None):
    data = {
        "incomes": incomes,
        "expenses": expenses,
        "recurring": recurring or []
    }
    temporary_file = DATA_FILE + ".tmp"
    if os.path.exists(DATA_FILE):
        shutil.copy2(DATA_FILE, DATA_FILE + ".bak")
    try:
        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        os.replace(temporary_file, DATA_FILE)
    finally:
        if os.path.exists(temporary_file):
            os.remove(temporary_file)


def load_data(default_currency="USD"):
    backup_file = DATA_FILE + ".bak"
    if not os.path.exists(DATA_FILE) and not os.path.exists(backup_file):
        return [], [], []

    def read_data(path):
        with open(path, "r", encoding="utf-8-sig") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Budget data must be a JSON object.")
        incomes = data.get("incomes", [])
        expenses = data.get("expenses", [])
        if not isinstance(incomes, list) or not isinstance(expenses, list):
            raise ValueError("Income and expense records must be lists.")
        return data, incomes, expenses

    loaded_from_backup = False
    try:
        data, incomes, expenses = read_data(DATA_FILE)
    except (OSError, ValueError):
        if not os.path.exists(backup_file):
            raise
        data, incomes, expenses = read_data(backup_file)
        loaded_from_backup = True
    if loaded_from_backup:
        shutil.copy2(backup_file, DATA_FILE)
    recurring = data.get("recurring", [])
    if not isinstance(recurring, list):
        recurring = []
    for record in incomes + expenses:
        if isinstance(record, dict):
            record.setdefault("id", uuid.uuid4().hex)
            record.setdefault("currency", default_currency)
    return incomes, expenses, recurring


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8-sig") as file:
            settings = json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError):
        settings = {}
    if not isinstance(settings, dict):
        settings = {}
    theme = settings.get("theme", "light")
    language = settings.get("language", "en")
    language = language if language in LANGUAGES else "en"
    currency = settings.get("currency", LANGUAGE_CURRENCIES[language])
    currency = currency if currency in CURRENCIES else LANGUAGE_CURRENCIES[language]
    exchange_rates = settings.get("exchange_rates", {})
    if not isinstance(exchange_rates, dict):
        exchange_rates = {}
    valid_rates = {}
    for code, rate in exchange_rates.items():
        try:
            numeric_rate = float(rate)
        except (TypeError, ValueError):
            continue
        if code in CURRENCIES and math.isfinite(numeric_rate) and numeric_rate > 0:
            valid_rates[code] = numeric_rate
    return {
        "theme": theme if theme in ("light", "dark") else "light",
        "language": language,
        "currency": currency,
        "currency_customized": settings.get(
            "currency_customized", currency != LANGUAGE_CURRENCIES[language]
        ),
        "exchange_rates": valid_rates,
        "rates_updated_at": settings.get("rates_updated_at", 0),
        "rates_next_update_at": settings.get("rates_next_update_at", 0)
    }


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)


def show_first_run_setup():
    root = tk.Tk()
    set_app_icon(root)
    root.title("Budget Tracker Setup")
    root.geometry("440x330")
    root.resizable(False, False)
    root.configure(bg="#F1F5F3")
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    style.configure("Setup.TFrame", background="#F1F5F3")
    style.configure("SetupTitle.TLabel", background="#F1F5F3", foreground="#142B30",
                    font=(preferred_font("en"), 20, "bold"))
    style.configure("SetupText.TLabel", background="#F1F5F3", foreground="#687E80",
                    font=(preferred_font("en"), 10))
    result = {}
    body = ttk.Frame(root, style="Setup.TFrame", padding=(34, 30))
    body.pack(fill="both", expand=True)
    title_label = ttk.Label(body, text=TEXT["en"]["welcome"], style="SetupTitle.TLabel")
    title_label.pack(anchor="w")
    description_label = ttk.Label(
        body, text=TEXT["en"]["setup_description"], style="SetupText.TLabel"
    )
    description_label.pack(anchor="w", pady=(6, 22))

    language_label = ttk.Label(body, text=TEXT["en"]["language"])
    language_label.pack(anchor="w", pady=(0, 5))
    language_var = tk.StringVar(value="English")
    language_selector = ttk.Combobox(
        body, textvariable=language_var, state="readonly", values=tuple(LANGUAGES.values()),
        width=35
    )
    language_selector.pack(fill="x", pady=(0, 14))
    currency_label_widget = ttk.Label(body, text=TEXT["en"]["currency"])
    currency_label_widget.pack(anchor="w", pady=(0, 5))
    currency_options = tuple(currency_option(code, "en") for code in CURRENCIES)
    currency_var = tk.StringVar(value=currency_option("USD", "en"))
    currency_selector = ttk.Combobox(
        body, textvariable=currency_var, state="readonly", values=currency_options,
        width=35
    )
    currency_selector.pack(fill="x", pady=(0, 22))
    currency_customized = tk.BooleanVar(value=False)

    def select_language_currency(_event=None):
        selected_language = next(
            code for code, name in LANGUAGES.items() if name == language_var.get()
        )
        localized_text = TEXT[selected_language]
        font_family = preferred_font(selected_language)
        root.title(localized_text["welcome"])
        style.configure("TLabel", font=(font_family, 10))
        style.configure("TCombobox", font=(font_family, 10))
        style.configure("SetupTitle.TLabel", font=(font_family, 20, "bold"))
        style.configure("SetupText.TLabel", font=(font_family, 10))
        title_label.configure(text=localized_text["welcome"])
        description_label.configure(text=localized_text["setup_description"])
        language_label.configure(text=localized_text["language"])
        currency_label_widget.configure(text=localized_text["currency"])
        continue_button.configure(text=localized_text["continue"])
        currency_selector.configure(values=tuple(
            currency_option(code, selected_language) for code in CURRENCIES
        ))
        selected_currency = currency_var.get().split(" - ", 1)[0]
        if currency_customized.get():
            currency_var.set(currency_option(selected_currency, selected_language))
            return
        selected_currency = LANGUAGE_CURRENCIES[selected_language]
        currency_var.set(currency_option(selected_currency, selected_language))

    language_selector.bind("<<ComboboxSelected>>", select_language_currency)
    currency_selector.bind(
        "<<ComboboxSelected>>", lambda _event: currency_customized.set(True)
    )

    def finish_setup():
        language = next(code for code, name in LANGUAGES.items() if name == language_var.get())
        currency = currency_var.get().split(" - ", 1)[0]
        result.update({
            "theme": "light", "language": language, "currency": currency,
            "currency_customized": currency_customized.get()
        })
        save_settings(result)
        root.destroy()

    continue_button = ttk.Button(body, text=TEXT["en"]["continue"], command=finish_setup)
    continue_button.pack(anchor="e")
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
    return result or None


class BudgetTrackerApp:
    def __init__(self, root, settings=None):
        self.root = root
        self.preferences = settings or load_settings()
        self.theme = self.preferences["theme"]
        self.language = self.preferences["language"]
        self.currency = self.preferences["currency"]
        self.incomes, self.expenses, self.recurring = load_data(self.currency)
        self.process_recurring_transactions()
        self.chart_font = self.chart_font_for_language()
        self.theme_var = tk.StringVar(value=self.theme)
        self.language_var = tk.StringVar(value=self.language)
        self.currency_var = tk.StringVar(value=self.currency)
        self.chart_key = CHART_KEYS[0]
        self.period_key = PERIOD_KEYS[0]
        self.chart_type = tk.StringVar(value=self.text(self.chart_key))
        self.chart_period = tk.StringVar(value=self.text(self.period_key))

        self.root.title(self.text("window_title"))
        self.root.geometry("1000x720")
        self.root.minsize(820, 600)
        self.set_theme(self.theme, persist=False)
        self.build_window()
        self.refresh()

    def text(self, key):
        return TEXT[self.language].get(key, TEXT["en"].get(key, key))

    def format_amount(self, amount):
        decimals = 0 if self.currency == "JPY" else 2
        quantum = Decimal(1).scaleb(-decimals)
        rounded = Decimal(str(amount)).quantize(quantum, rounding=ROUND_HALF_UP)
        return f"{CURRENCY_SYMBOLS[self.currency]}{rounded:,.{decimals}f}"

    @staticmethod
    def money_string(amount, currency):
        decimals = 0 if currency == "JPY" else 2
        quantum = Decimal(1).scaleb(-decimals)
        rounded = Decimal(str(amount)).quantize(quantum, rounding=ROUND_HALF_UP)
        return format(rounded, "f")

    def display_amount(self, record):
        amount = Decimal(str(record.get("amount", 0)))
        source_currency = record.get("currency", self.currency)
        if source_currency == self.currency:
            return amount
        rates = self.preferences.get("exchange_rates", {})
        return convert_currency_amount(amount, source_currency, self.currency, rates)

    def persist_data(self):
        save_data(self.incomes, self.expenses, self.recurring)

    def chart_font_for_language(self):
        family = preferred_font(self.language)
        try:
            findfont(FontProperties(family=family), fallback_to_default=False)
        except ValueError:
            return "DejaVu Sans"
        return family

    def set_theme(self, theme, persist=True):
        self.theme = theme.lower() if theme.lower() in ("light", "dark") else "light"
        if self.theme == "dark":
            self.background = "#101A20"
            self.surface = "#18262D"
            self.ink = "#EDF4F2"
            self.muted = "#9BAEAD"
            self.green = "#57D6A3"
            self.orange = "#F2A477"
            self.border = "#30434A"
            self.grid = "#25373E"
            self.button_ink = "#10221C"
        else:
            self.background = "#F1F5F3"
            self.surface = "#ffffff"
            self.ink = "#142B30"
            self.muted = "#687E80"
            self.green = "#147D64"
            self.orange = "#CC6541"
            self.border = "#D8E4E1"
            self.grid = "#E8EFED"
            self.button_ink = "#ffffff"
        self.root.configure(bg=self.background)
        self.configure_styles()
        self.theme_var.set(self.theme)
        if persist:
            self.preferences["theme"] = self.theme
            save_settings(self.preferences)
        if hasattr(self, "chart_figure"):
            self.total_income.configure(foreground=self.green)
            self.total_expense.configure(foreground=self.orange)
            self.net_balance.configure(foreground=self.ink)
            self.category_hint.configure(foreground=self.muted)
            self.chart_figure.set_facecolor(self.surface)
            self.chart_canvas.get_tk_widget().configure(background=self.surface)
            self.refresh()

    def change_language(self, language):
        self.language = language if language in LANGUAGES else "en"
        self.root.title(self.text("window_title"))
        self.chart_font = self.chart_font_for_language()
        self.preferences["language"] = self.language
        if not self.preferences.get("currency_customized", False):
            self.currency = LANGUAGE_CURRENCIES[self.language]
            self.preferences["currency"] = self.currency
        save_settings(self.preferences)
        for child in self.root.winfo_children():
            child.destroy()
        self.configure_styles()
        self.theme_var = tk.StringVar(value=self.theme)
        self.language_var = tk.StringVar(value=self.language)
        self.currency_var = tk.StringVar(value=self.currency)
        self.chart_type = tk.StringVar(value=self.text(self.chart_key))
        self.chart_period = tk.StringVar(value=self.text(self.period_key))
        self.build_window()
        self.refresh()

    def change_currency(self, currency):
        target_currency = currency if currency in CURRENCIES else "USD"
        if target_currency == self.currency:
            return
        source_currency = self.currency
        self.currency_change_id = getattr(self, "currency_change_id", 0) + 1
        change_id = self.currency_change_id

        def load_rates():
            try:
                rates = fetch_exchange_rates()
                used_cache = False
                error = None
            except Exception as exception:
                rates = self.preferences.get("exchange_rates", {})
                used_cache = True
                error = exception
                if not all(
                    isinstance(rates.get(code), (int, float)) and rates[code] > 0
                    for code in (source_currency, target_currency)
                ):
                    rates = None
            self.root.after(
                0, lambda: self.finish_currency_change(
                    change_id, source_currency, target_currency, rates, used_cache, error
                )
            )

        threading.Thread(target=load_rates, daemon=True).start()

    def finish_currency_change(
        self, change_id, source_currency, target_currency, rates, used_cache, error
    ):
        if change_id != getattr(self, "currency_change_id", 0):
            return
        if rates is None:
            messagebox.showerror(
                self.text("change_currency"),
                f"Could not load exchange rates: {error}",
                parent=self.root
            )
            self.currency_var.set(self.currency)
            return

        self.currency = target_currency
        self.preferences["currency"] = self.currency
        self.preferences["currency_customized"] = True
        self.preferences["exchange_rates"] = rates
        if not used_cache:
            self.preferences["rates_updated_at"] = time.time()
            self.preferences["rates_next_update_at"] = time.time() + 86400
        self.currency_var.set(self.currency)
        if hasattr(self, "entry_currency_var"):
            self.entry_currency_var.set(self.currency)
        save_settings(self.preferences)
        self.refresh()
        if used_cache:
            messagebox.showwarning(
                self.text("change_currency"),
                f"The exchange-rate service was unavailable. Saved rates were used. ({error})",
                parent=self.root
            )

    def show_settings_menu(self):
        menu = tk.Menu(
            self.root, tearoff=False, background=self.surface, foreground=self.ink,
            activebackground=self.green, activeforeground=self.button_ink,
            borderwidth=1, relief="solid"
        )
        theme_menu = tk.Menu(menu, tearoff=False, background=self.surface, foreground=self.ink,
                             activebackground=self.green, activeforeground=self.button_ink)
        for theme in ("light", "dark"):
            theme_menu.add_radiobutton(
                label=self.text(theme), variable=self.theme_var, value=theme,
                command=lambda selected=theme: self.set_theme(selected)
            )
        menu.add_cascade(label=self.text("theme"), menu=theme_menu)

        language_menu = tk.Menu(menu, tearoff=False, background=self.surface, foreground=self.ink,
                                activebackground=self.green, activeforeground=self.button_ink)
        for code, name in LANGUAGES.items():
            language_menu.add_radiobutton(
                label=name, variable=self.language_var, value=code,
                command=lambda selected=code: self.change_language(selected)
            )
        menu.add_cascade(label=self.text("change_language"), menu=language_menu)

        currency_menu = tk.Menu(menu, tearoff=False, background=self.surface, foreground=self.ink,
                                activebackground=self.green, activeforeground=self.button_ink)
        for code, name in CURRENCIES.items():
            currency_menu.add_radiobutton(
                label=currency_option(code, self.language), variable=self.currency_var, value=code,
                command=lambda selected=code: self.change_currency(selected)
            )
        menu.add_cascade(label=self.text("change_currency"), menu=currency_menu)
        menu.add_separator()
        menu.add_command(label=self.text("reset_data"), command=self.reset_data)
        menu.tk_popup(self.settings_button.winfo_rootx(),
                      self.settings_button.winfo_rooty() + self.settings_button.winfo_height())
        menu.grab_release()

    def configure_styles(self):
        style = ttk.Style(self.root)
        font_family = preferred_font(self.language)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("TLabel", background=self.surface, foreground=self.ink,
                        font=(font_family, 10))
        style.configure("TFrame", background=self.surface)
        style.configure("App.TFrame", background=self.background)
        style.configure("Card.TFrame", background=self.surface, relief="flat", borderwidth=0)
        style.configure("Header.TFrame", background=self.surface)
        style.configure("Title.TLabel", background=self.surface, foreground=self.ink,
                font=(font_family, 23, "bold"))
        style.configure("Subtitle.TLabel", background=self.background, foreground=self.muted,
                        font=(font_family, 10))
        style.configure("HeaderSubtitle.TLabel", background=self.surface, foreground=self.muted,
                font=(font_family, 10))
        style.configure("CardTitle.TLabel", background=self.surface, foreground=self.muted,
                font=(font_family, 9, "bold"))
        style.configure("CardValue.TLabel", background=self.surface, foreground=self.ink,
                font=(font_family, 21, "bold"))
        style.configure("Section.TLabel", background=self.background, foreground=self.ink,
                font=(font_family, 14, "bold"))
        style.configure("TNotebook", background=self.background, borderwidth=0,
                tabmargins=(0, 6, 0, 0))
        style.configure("TNotebook.Tab", padding=(19, 12), font=(font_family, 10, "bold"),
                background=self.background, foreground=self.muted)
        style.map("TNotebook.Tab", background=[("selected", self.surface), ("active", self.grid)],
              foreground=[("selected", self.green), ("!selected", self.muted)])
        style.configure("Treeview", rowheight=36, font=(font_family, 10), borderwidth=0,
                        background=self.surface, fieldbackground=self.surface,
                        foreground=self.ink)
        style.configure("Treeview.Heading", font=(font_family, 10, "bold"),
                background=self.grid, foreground=self.ink, padding=(10, 9), relief="flat")
        style.map("Treeview", background=[("selected", self.green)],
                  foreground=[("selected", self.button_ink)])
        style.configure("TEntry", fieldbackground=self.surface, foreground=self.ink,
                insertcolor=self.ink, padding=(9, 8), borderwidth=1)
        style.configure("TCombobox", fieldbackground=self.surface, foreground=self.ink,
                background=self.grid, arrowcolor=self.ink, padding=(8, 7))
        style.map("TCombobox", fieldbackground=[("readonly", self.surface)],
                  foreground=[("readonly", self.ink)])
        style.configure("Accent.TButton", background=self.green, foreground=self.button_ink,
                        padding=(15, 10), font=(font_family, 10, "bold"), relief="flat")
        style.map("Accent.TButton", background=[("active", self.orange)])
        style.configure("Quiet.TButton", padding=(12, 8), font=(font_family, 10),
                        background=self.surface, foreground=self.ink, relief="flat")
        style.map("Quiet.TButton", background=[("active", self.grid)])
        style.configure("Danger.TButton", foreground=self.orange, padding=(10, 7))

    def build_window(self):
        header = ttk.Frame(self.root, style="Header.TFrame", padding=(30, 20, 30, 15))
        header.pack(fill="x")
        title_area = ttk.Frame(header, style="Header.TFrame")
        title_area.pack(side="left", fill="x", expand=True)
        ttk.Label(title_area, text=self.text("window_title"), style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_area, text=self.text("subtitle"),
                  style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(4, 0))
        self.settings_button = ttk.Button(
            header, text="⚙", width=4, style="Quiet.TButton", command=self.show_settings_menu
        )
        self.settings_button.pack(side="right", anchor="center")
        tk.Frame(self.root, height=3, background=self.green).pack(fill="x")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=30, pady=(9, 26))
        self.overview_page = ttk.Frame(self.notebook, style="App.TFrame", padding=18)
        self.add_page = ttk.Frame(self.notebook, style="App.TFrame", padding=22)
        self.history_page = ttk.Frame(self.notebook, style="App.TFrame", padding=18)
        self.plan_page = ttk.Frame(self.notebook, style="App.TFrame", padding=18)
        self.notebook.add(self.overview_page, text=self.text("overview"))
        self.notebook.add(self.add_page, text=self.text("add_tab"))
        self.notebook.add(self.history_page, text=self.text("history_tab"))
        self.notebook.add(self.plan_page, text=self.text("plan_tab"))

        self.build_overview()
        self.build_add_form()
        self.build_history()
        self.build_plan_page()

    def build_overview(self):
        cards = ttk.Frame(self.overview_page, style="App.TFrame")
        cards.pack(fill="x", pady=(0, 20))
        self.total_income = self.make_stat_card(cards, "total_income", self.green)
        self.total_expense = self.make_stat_card(cards, "total_expense", self.orange)
        self.net_balance = self.make_stat_card(cards, "net_balance", self.ink)

        ttk.Label(self.overview_page, text=self.text("spending_insights"),
                  style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        chart_frame = ttk.Frame(self.overview_page, style="Card.TFrame", padding=12)
        chart_frame.pack(fill="both", expand=True)
        controls = ttk.Frame(chart_frame, style="Card.TFrame")
        controls.pack(fill="x", pady=(0, 4))
        ttk.Label(controls, text=self.text("chart"), style="CardTitle.TLabel").pack(side="left", padx=(4, 8))
        chart_selector = ttk.Combobox(
            controls, textvariable=self.chart_type, state="readonly", width=25,
            values=tuple(self.text(key) for key in CHART_KEYS)
        )
        chart_selector.pack(side="left", padx=(0, 16))
        chart_selector.bind("<<ComboboxSelected>>", self.on_chart_selected)
        ttk.Label(controls, text=self.text("period"), style="CardTitle.TLabel").pack(side="left", padx=(0, 8))
        period_selector = ttk.Combobox(
            controls, textvariable=self.chart_period, state="readonly", width=18,
            values=tuple(self.text(key) for key in PERIOD_KEYS)
        )
        period_selector.pack(side="left")
        period_selector.bind("<<ComboboxSelected>>", self.on_period_selected)

        self.chart_figure = Figure(figsize=(8, 4), dpi=100, facecolor=self.surface)
        self.chart_axes = self.chart_figure.add_subplot(111)
        self.chart_canvas = FigureCanvasTkAgg(self.chart_figure, master=chart_frame)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_chart_selected(self, _event=None):
        selected = self.chart_type.get()
        self.chart_key = next(key for key in CHART_KEYS if self.text(key) == selected)
        self.refresh()

    def on_period_selected(self, _event=None):
        selected = self.chart_period.get()
        self.period_key = next(key for key in PERIOD_KEYS if self.text(key) == selected)
        self.refresh()

    def make_stat_card(self, parent, label, color):
        card = ttk.Frame(parent, style="Card.TFrame", padding=(0, 15, 17, 15))
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        tk.Frame(card, width=4, background=color).pack(side="left", fill="y", padx=(0, 14))
        content = ttk.Frame(card, style="Card.TFrame")
        content.pack(side="left", fill="x", expand=True)
        ttk.Label(content, text=self.text(label), style="CardTitle.TLabel").pack(anchor="w")
        value = ttk.Label(
            content, text=self.format_amount(0), style="CardValue.TLabel", foreground=color
        )
        value.pack(anchor="w", pady=(7, 0))
        return value

    def build_add_form(self):
        ttk.Label(self.add_page, text=self.text("record_transaction"),
                  style="Section.TLabel").pack(anchor="w", pady=(4, 6))
        ttk.Label(self.add_page, text=self.text("transaction_description"),
                  style="Subtitle.TLabel").pack(anchor="w", pady=(0, 24))
        form = ttk.Frame(self.add_page, style="Card.TFrame", padding=22)
        form.pack(fill="x", anchor="n")

        ttk.Label(form, text=self.text("type")).grid(row=0, column=0, sticky="w", pady=(0, 7))
        self.transaction_type = tk.StringVar(value=self.text("expense"))
        ttk.Combobox(form, textvariable=self.transaction_type, state="readonly",
                     values=(self.text("income"), self.text("expense")), width=34).grid(
                         row=1, column=0, sticky="ew", padx=(0, 18), pady=(0, 18))

        ttk.Label(form, text=self.text("amount")).grid(row=0, column=1, sticky="w", pady=(0, 7))
        self.amount_entry = ttk.Entry(form, width=36)
        self.amount_entry.grid(row=1, column=1, sticky="ew", pady=(0, 18))

        ttk.Label(form, text=self.text("currency")).grid(row=2, column=1, sticky="w", pady=(0, 7))
        self.entry_currency_var = tk.StringVar(value=self.currency)
        ttk.Combobox(
            form, textvariable=self.entry_currency_var, state="readonly",
            values=tuple(CURRENCIES), width=12
        ).grid(row=3, column=1, sticky="w", pady=(0, 18))

        ttk.Label(form, text=self.text("category")).grid(row=2, column=0, sticky="w", pady=(0, 7))
        self.category_entry = ttk.Entry(form)
        self.category_entry.grid(row=3, column=0, sticky="ew", padx=(0, 18))
        self.category_hint = ttk.Label(form, text=self.text("category_examples"),
                                       foreground=self.muted)
        self.category_hint.grid(row=4, column=0, sticky="w", pady=(6, 0))
        self.repeat_monthly_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form, text=self.text("repeat_monthly"), variable=self.repeat_monthly_var
        ).grid(row=5, column=0, sticky="w", pady=(12, 0))
        self.add_transaction_button = ttk.Button(
            form, text=self.text("add_transaction"), style="Accent.TButton",
            command=self.add_transaction
        )
        self.add_transaction_button.grid(row=5, column=1, sticky="w", pady=(12, 0))
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)
        self.amount_entry.bind("<Return>", lambda _event: self.add_transaction())
        self.category_entry.bind("<Return>", lambda _event: self.add_transaction())

    def build_history(self):
        toolbar = ttk.Frame(self.history_page, style="App.TFrame")
        toolbar.pack(fill="x", pady=(0, 12))
        ttk.Label(toolbar, text=self.text("transactions"), style="Section.TLabel").pack(side="left")
        ttk.Button(toolbar, text=self.text("export_csv"), style="Quiet.TButton",
                   command=self.export_transactions).pack(side="right", padx=(8, 0))
        ttk.Button(toolbar, text=self.text("delete_transaction"), style="Danger.TButton",
                   command=self.delete_transaction).pack(side="right", padx=(8, 0))
        ttk.Button(toolbar, text=self.text("edit_transaction"), style="Quiet.TButton",
                   command=self.edit_transaction).pack(side="right", padx=(8, 0))
        ttk.Button(toolbar, text=self.text("rename_category"), style="Quiet.TButton",
                   command=self.rename_category).pack(side="right", padx=(8, 0))

        filters = ttk.Frame(self.history_page, style="App.TFrame")
        filters.pack(fill="x", pady=(0, 10))
        self.history_search_var = tk.StringVar()
        search_entry = ttk.Entry(filters, textvariable=self.history_search_var, width=22)
        search_entry.pack(side="left", padx=(0, 8))
        search_entry.bind("<KeyRelease>", lambda _event: self.refresh_history())
        self.history_type_var = tk.StringVar(value=self.text("all_types"))
        self.history_type_filter = ttk.Combobox(
            filters, textvariable=self.history_type_var, state="readonly", width=13,
            values=(self.text("all_types"), self.text("income"), self.text("expense"))
        )
        self.history_type_filter.pack(side="left", padx=(0, 8))
        self.history_type_filter.bind("<<ComboboxSelected>>", lambda _event: self.refresh_history())
        self.history_category_var = tk.StringVar(value=self.text("all_categories"))
        self.history_category_filter = ttk.Combobox(
            filters, textvariable=self.history_category_var, state="readonly", width=18,
            values=(self.text("all_categories"),)
        )
        self.history_category_filter.pack(side="left", padx=(0, 8))
        self.history_category_filter.bind(
            "<<ComboboxSelected>>", lambda _event: self.refresh_history()
        )
        self.history_from_var = tk.StringVar()
        self.history_to_var = tk.StringVar()
        ttk.Entry(filters, textvariable=self.history_from_var, width=17).pack(
            side="left", padx=(0, 6)
        )
        ttk.Entry(filters, textvariable=self.history_to_var, width=17).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(filters, text=self.text("apply_filters"), style="Quiet.TButton",
                   command=self.refresh_history).pack(side="left")

        table_frame = ttk.Frame(self.history_page, style="Card.TFrame", padding=8)
        table_frame.pack(fill="both", expand=True)
        columns = ("date", "type", "category", "amount")
        self.history_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {
            "date": self.text("date"), "type": self.text("type"),
            "category": self.text("category"), "amount": self.text("amount")
        }
        for column, heading in headings.items():
            self.history_table.heading(column, text=heading)
        self.history_table.column("date", width=190, anchor="w")
        self.history_table.column("type", width=105, anchor="w")
        self.history_table.column("category", width=180, anchor="w")
        self.history_table.column("amount", width=130, anchor="e")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_table.yview)
        self.history_table.configure(yscrollcommand=scrollbar.set)
        self.history_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_plan_page(self):
        ttk.Label(self.plan_page, text=self.text("guidance_title"),
                  style="Section.TLabel").pack(anchor="w", pady=(0, 8))
        self.guidance_label = ttk.Label(
            self.plan_page,
            text=f"{self.text('budget_advice')}\n\n{self.text('investment_note')}",
            style="Subtitle.TLabel", justify="left", wraplength=760
        )
        self.guidance_label.pack(fill="x", anchor="w", pady=(0, 18))
        self.monthly_income_label = ttk.Label(self.plan_page, style="Section.TLabel")
        self.monthly_income_label.pack(anchor="w", pady=(0, 12))
        heading = ttk.Frame(self.plan_page, style="App.TFrame")
        heading.pack(fill="x", pady=(0, 8))
        ttk.Label(heading, text=self.text("budget_title"), style="Section.TLabel").pack(side="left")
        ttk.Button(heading, text=self.text("manage_budgets"), style="Quiet.TButton",
                   command=self.manage_budgets).pack(side="right")
        budget_frame = ttk.Frame(self.plan_page, style="Card.TFrame", padding=8)
        budget_frame.pack(fill="both", expand=True)
        columns = ("category", "limit", "spent", "remaining", "status")
        self.budget_table = ttk.Treeview(budget_frame, columns=columns, show="headings")
        heading_keys = {
            "category": "category", "limit": "monthly_limit", "spent": "spent",
            "remaining": "remaining", "status": "status"
        }
        for column, key in heading_keys.items():
            self.budget_table.heading(column, text=self.text(key))
        self.budget_table.column("category", width=200, anchor="w")
        for column in columns[1:]:
            self.budget_table.column(column, width=135, anchor="e")
        self.budget_table.pack(fill="both", expand=True)

    def manage_budgets(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.text("manage_budgets"))
        dialog.transient(self.root)
        dialog.grab_set()
        body = ttk.Frame(dialog, padding=18)
        body.pack(fill="both", expand=True)
        ttk.Label(body, text=self.text("category")).grid(row=0, column=0, sticky="w", pady=5)
        budgets = self.preferences.setdefault("budgets", {})
        categories = sorted({
            str(record.get("category", "General"))
            for record in self.expenses if isinstance(record, dict)
        } | set(budgets), key=str.casefold)
        category_var = tk.StringVar()
        category_entry = ttk.Combobox(body, textvariable=category_var, values=categories, width=30)
        category_entry.grid(row=0, column=1, sticky="ew", padx=(12, 0), pady=5)
        ttk.Label(body, text=self.text("monthly_limit")).grid(row=1, column=0, sticky="w", pady=5)
        amount_var = tk.StringVar()
        amount_entry = ttk.Entry(body, textvariable=amount_var, width=33)
        amount_entry.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=5)

        def load_budget(_event=None):
            budget = budgets.get(category_var.get(), {})
            amount_var.set(str(budget.get("amount", "")) if isinstance(budget, dict) else str(budget))

        category_entry.bind("<<ComboboxSelected>>", load_budget)

        def save_budget():
            category = category_var.get().strip().capitalize()
            try:
                amount = Decimal(amount_var.get().strip())
                if not category or not amount.is_finite() or amount <= 0:
                    raise ValueError
            except (InvalidOperation, ValueError):
                messagebox.showerror(
                    self.text("invalid_amount"), self.text("amount_positive"), parent=dialog
                )
                return
            budgets[category] = {
                "amount": self.money_string(amount, self.currency), "currency": self.currency
            }
            save_settings(self.preferences)
            self.refresh_plan()
            dialog.destroy()

        def delete_budget():
            category = category_var.get().strip().capitalize()
            if category in budgets:
                del budgets[category]
                save_settings(self.preferences)
                self.refresh_plan()
            dialog.destroy()

        buttons = ttk.Frame(body)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text=self.text("delete_budget"), style="Danger.TButton",
                   command=delete_budget).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text=self.text("cancel"), command=dialog.destroy).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(buttons, text=self.text("budget_saved"), style="Accent.TButton",
                   command=save_budget).pack(side="left")
        body.columnconfigure(1, weight=1)
        category_entry.focus_set()

    def refresh_plan(self):
        if not hasattr(self, "budget_table"):
            return
        self.budget_table.delete(*self.budget_table.get_children())
        today = datetime.now().date()
        month_start = today.replace(day=1)
        monthly_income = Decimal(0)
        monthly_spending = {}
        for transaction_type, records in (("Income", self.incomes), ("Expense", self.expenses)):
            for record in records:
                if not isinstance(record, dict):
                    continue
                try:
                    record_date = datetime.fromisoformat(record.get("date", "")).date()
                    amount = self.display_amount(record)
                except (KeyError, TypeError, ValueError):
                    continue
                if not month_start <= record_date <= today:
                    continue
                if transaction_type == "Income":
                    monthly_income += amount
                else:
                    category = str(record.get("category", "General"))
                    monthly_spending[category] = monthly_spending.get(category, Decimal(0)) + amount
        self.monthly_income_label.configure(
            text=f"{self.text('monthly_income')}: {self.format_amount(monthly_income)}"
        )
        total_spending = sum(monthly_spending.values())
        if monthly_income > 0:
            ratio = total_spending / monthly_income * 100
            if ratio > 100:
                recommendation = self.text("spending_over_income")
            elif ratio > 80:
                recommendation = self.text("spending_near_limit")
            else:
                recommendation = self.text("spending_under_limit")
            personalized_guidance = (
                f"{self.text('spending_ratio').format(ratio=ratio)} {recommendation}"
            )
        else:
            personalized_guidance = self.text("add_income_first")
        self.guidance_label.configure(text=(
            f"{self.text('budget_advice')}\n\n{personalized_guidance}\n\n"
            f"{self.text('investment_note')}"
        ))
        budgets = self.preferences.get("budgets", {})
        for category, budget in sorted(budgets.items(), key=lambda item: item[0].casefold()):
            if isinstance(budget, dict):
                amount = budget.get("amount", 0)
                budget_currency = budget.get("currency", self.currency)
            else:
                amount = budget
                budget_currency = self.currency
            try:
                limit = convert_currency_amount(
                        amount, budget_currency, self.currency,
                    self.preferences.get("exchange_rates", {})
                )
            except (KeyError, TypeError, ValueError):
                continue
            spent = monthly_spending.get(category, Decimal(0))
            remaining = limit - spent
            self.budget_table.insert("", "end", iid=category, values=(
                category, self.format_amount(limit), self.format_amount(spent),
                self.format_amount(remaining),
                self.text("over_budget" if remaining < 0 else "on_track")
            ))

    def add_transaction(self):
        if getattr(self, "transaction_pending", False):
            return
        try:
            amount = Decimal(self.amount_entry.get().strip())
            if not amount.is_finite() or amount <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messagebox.showerror(self.text("invalid_amount"), self.text("amount_positive"), parent=self.root)
            self.amount_entry.focus_set()
            return

        category = self.category_entry.get().strip().capitalize()
        if not category:
            messagebox.showerror(self.text("missing_category"), self.text("enter_category"), parent=self.root)
            self.category_entry.focus_set()
            return

        entry_currency = self.entry_currency_var.get()
        if entry_currency not in CURRENCIES:
            entry_currency = self.currency
        if entry_currency == self.currency:
            self.save_transaction(amount, entry_currency, category)
            return

        rates = self.preferences.get("exchange_rates", {})
        rates_are_fresh = self.preferences.get("rates_next_update_at", 0) > time.time()
        if rates_are_fresh:
            try:
                converted_amount = convert_currency_amount(
                    amount, entry_currency, self.currency, rates
                )
            except (KeyError, TypeError, ValueError):
                pass
            else:
                self.save_transaction(
                    converted_amount, entry_currency, category, amount
                )
                return

        self.transaction_pending = True
        self.add_transaction_button.configure(state="disabled")

        def load_rates():
            try:
                fetched_rates = fetch_exchange_rates()
                used_cache = False
                error = None
            except Exception as exception:
                fetched_rates = self.preferences.get("exchange_rates", {})
                used_cache = True
                error = exception
                try:
                    convert_currency_amount(
                        amount, entry_currency, self.currency, fetched_rates
                    )
                except (KeyError, TypeError, ValueError):
                    fetched_rates = None
            self.root.after(
                0, lambda: self.finish_add_transaction(
                    amount, entry_currency, category, fetched_rates, used_cache, error
                )
            )

        threading.Thread(target=load_rates, daemon=True).start()

    def finish_add_transaction(
        self, amount, entry_currency, category, rates, used_cache, error
    ):
        self.transaction_pending = False
        self.add_transaction_button.configure(state="normal")
        if rates is None:
            messagebox.showerror(
                self.text("invalid_amount"),
                f"Could not load exchange rates: {error}",
                parent=self.root
            )
            return
        try:
            converted_amount = convert_currency_amount(
                amount, entry_currency, self.currency, rates
            )
        except (KeyError, TypeError, ValueError) as exception:
            messagebox.showerror(
                self.text("invalid_amount"),
                f"Could not convert {entry_currency} to {self.currency}: {exception}",
                parent=self.root
            )
            return
        if not used_cache:
            self.preferences["exchange_rates"] = rates
            self.preferences["rates_updated_at"] = time.time()
            self.preferences["rates_next_update_at"] = time.time() + 86400
            save_settings(self.preferences)
        self.save_transaction(converted_amount, entry_currency, category, amount)

    def save_transaction(self, amount, entry_currency, category, source_amount=None):
        recorded_amount = amount if source_amount is None else source_amount
        transaction_type = "Income" if self.transaction_type.get() == self.text("income") else "Expense"
        recorded_amount = self.money_string(recorded_amount, entry_currency)
        transaction = {
            "id": uuid.uuid4().hex,
            "amount": recorded_amount,
            "currency": entry_currency,
            "source_amount": recorded_amount,
            "source_currency": entry_currency,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        target = self.incomes if transaction_type == "Income" else self.expenses
        target.append(transaction)
        if self.repeat_monthly_var.get():
            self.recurring.append({
                "id": uuid.uuid4().hex,
                "type": transaction_type,
                "amount": recorded_amount,
                "currency": entry_currency,
                "category": category,
                "next_date": self.next_month_date(datetime.now().date()).isoformat()
            })
            self.repeat_monthly_var.set(False)
        self.persist_data()
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.refresh()

    @staticmethod
    def next_month_date(current_date):
        month_index = current_date.month % 12 + 1
        year = current_date.year + (current_date.month // 12)
        day = min(current_date.day, calendar.monthrange(year, month_index)[1])
        return current_date.replace(year=year, month=month_index, day=day)

    def process_recurring_transactions(self):
        today = datetime.now().date()
        changed = False
        for template in self.recurring:
            if not isinstance(template, dict):
                continue
            try:
                due_date = datetime.strptime(template["next_date"], "%Y-%m-%d").date()
                amount = Decimal(str(template["amount"]))
                transaction_type = template["type"]
                if transaction_type not in ("Income", "Expense") or not amount.is_finite() or amount <= 0:
                    continue
            except (InvalidOperation, KeyError, TypeError, ValueError):
                continue
            catch_up_count = 0
            while due_date <= today and catch_up_count < 600:
                target = self.incomes if transaction_type == "Income" else self.expenses
                target.append({
                    "id": uuid.uuid4().hex,
                    "recurring_id": template.get("id"),
                    "amount": self.money_string(amount, template.get("currency", self.currency)),
                    "currency": template.get("currency", self.currency),
                    "source_amount": self.money_string(amount, template.get("currency", self.currency)),
                    "source_currency": template.get("currency", self.currency),
                    "category": template.get("category", "General"),
                    "date": f"{due_date.isoformat()} 09:00:00"
                })
                due_date = self.next_month_date(due_date)
                catch_up_count += 1
                changed = True
            template["next_date"] = due_date.isoformat()
        if changed:
            self.persist_data()

    def refresh(self):
        income = sum(
            (self.display_amount(item) for item in self.incomes if isinstance(item, dict)),
            Decimal(0)
        )
        expense = sum(
            (self.display_amount(item) for item in self.expenses if isinstance(item, dict)),
            Decimal(0)
        )
        self.total_income.configure(text=self.format_amount(income))
        self.total_expense.configure(text=self.format_amount(expense))
        self.net_balance.configure(text=self.format_amount(income - expense))
        self.refresh_charts(income, expense)
        self.refresh_history()
        self.refresh_plan()

    def refresh_charts(self, income, expense):
        del income, expense
        matplotlib.rcParams["font.family"] = [self.chart_font]
        axes = self.chart_axes
        axes.clear()
        axes.set_facecolor(self.surface)
        axes.tick_params(colors=self.muted)
        axes.grid(axis="y", color=self.grid, linewidth=0.8)
        axes.set_axisbelow(True)
        for spine in axes.spines.values():
            spine.set_color(self.border)

        transactions = self.get_chart_transactions()
        period_suffix = "" if self.period_key == "all_time" else f" · {self.text(self.period_key)}"
        axes.set_title(f"{self.text(self.chart_key)}{period_suffix}", color=self.ink, fontsize=13, pad=14)

        if self.chart_key == "chart_income_expense":
            totals = {"Income": 0.0, "Expense": 0.0}
            for item in transactions:
                totals[item["type"]] += item["amount"]
            values = [max(totals["Income"], 0), max(totals["Expense"], 0)]
            if any(values):
                bars = axes.bar([self.text("income"), self.text("expenses")], values,
                                color=[self.green, self.orange], width=0.52)
                axes.bar_label(bars, labels=[self.format_amount(value) for value in values], padding=5,
                               color=self.ink, fontsize=9)
                axes.set_ylabel(self.text("amount"), color=self.muted)
            else:
                self.show_empty_chart(self.text("no_transactions"))

        elif self.chart_key == "chart_monthly_cash":
            monthly = {}
            for item in transactions:
                if item["date"] is None:
                    continue
                month_key = item["date"].strftime("%Y-%m")
                monthly.setdefault(month_key, {"Income": 0.0, "Expense": 0.0})
                monthly[month_key][item["type"]] += item["amount"]
            months = sorted(monthly)
            if months:
                positions = list(range(len(months)))
                income_values = [monthly[month]["Income"] for month in months]
                expense_values = [monthly[month]["Expense"] for month in months]
                axes.plot(positions, income_values, marker="o", linewidth=2.4,
                          color=self.green, label=self.text("income"))
                axes.plot(positions, expense_values, marker="o", linewidth=2.4,
                          color=self.orange, label=self.text("expenses"))
                axes.set_xticks(positions)
                axes.set_xticklabels([self.format_month(month) for month in months],
                                     rotation=30, ha="right")
                axes.set_ylabel(self.text("amount"), color=self.muted)
                axes.legend(frameon=False, labelcolor=self.ink)
            else:
                self.show_empty_chart(self.text("no_dated_transactions"))

        elif self.chart_key in ("chart_category_bar", "chart_category_pie"):
            categories = {}
            for item in transactions:
                if item["type"] == "Expense":
                    categories[item["category"]] = categories.get(item["category"], 0) + item["amount"]
            positive_categories = {
                name: amount for name, amount in categories.items() if amount > 0
            }
            if not positive_categories:
                self.show_empty_chart(self.text("no_expenses"))
            elif self.chart_key == "chart_category_bar":
                ordered = sorted(positive_categories.items(), key=lambda item: item[1])
                bars = axes.barh([item[0] for item in ordered],
                                 [item[1] for item in ordered], color=self.orange)
                axes.bar_label(bars, labels=[self.format_amount(item[1]) for item in ordered],
                               padding=5, color=self.ink, fontsize=9)
                axes.set_xlabel(self.text("amount"), color=self.muted)
                axes.grid(axis="x", color=self.grid, linewidth=0.8)
                axes.grid(axis="y", visible=False)
            else:
                axes.grid(False)
                wedges, _labels, percentages = axes.pie(
                    list(positive_categories.values()),
                    labels=list(positive_categories.keys()), autopct="%1.0f%%",
                    startangle=140, textprops={"color": self.ink, "fontsize": 9}
                )
                for wedge in wedges:
                    wedge.set_edgecolor(self.surface)
                for percentage in percentages:
                    percentage.set_color(self.ink)

        elif self.chart_key in ("chart_monthly_bars", "chart_balance"):
            dated = [item for item in transactions if item["date"] is not None]
            if self.chart_key == "chart_monthly_bars":
                monthly = {}
                for item in dated:
                    month = item["date"].strftime("%Y-%m")
                    monthly.setdefault(month, {"Income": 0.0, "Expense": 0.0})
                    monthly[month][item["type"]] += item["amount"]
                months = sorted(monthly)
                if months:
                    positions = list(range(len(months)))
                    width = 0.38
                    income_bars = axes.bar(
                        [position - width / 2 for position in positions],
                        [monthly[month]["Income"] for month in months], width,
                        color=self.green, label=self.text("income")
                    )
                    expense_bars = axes.bar(
                        [position + width / 2 for position in positions],
                        [monthly[month]["Expense"] for month in months], width,
                        color=self.orange, label=self.text("expenses")
                    )
                    axes.set_xticks(positions)
                    axes.set_xticklabels([self.format_month(month) for month in months],
                                         rotation=30, ha="right")
                    axes.bar_label(income_bars, labels=[
                        self.format_amount(monthly[month]["Income"]) for month in months
                    ], padding=3, color=self.ink, fontsize=8)
                    axes.bar_label(expense_bars, labels=[
                        self.format_amount(monthly[month]["Expense"]) for month in months
                    ], padding=3, color=self.ink, fontsize=8)
                    axes.set_ylabel(self.text("amount"), color=self.muted)
                    axes.legend(frameon=False, labelcolor=self.ink)
                else:
                    self.show_empty_chart(self.text("no_dated_transactions"))
            elif dated:
                if self.period_key in ("last_30_days", "last_90_days", "last_6_months", "last_12_months"):
                    period_days = {
                        "last_30_days": 30, "last_90_days": 90,
                        "last_6_months": 183, "last_12_months": 365
                    }
                    period_start = datetime.now() - timedelta(days=period_days[self.period_key])
                elif self.period_key == "this_year":
                    period_start = datetime(datetime.now().year, 1, 1)
                elif self.period_key == "previous_year":
                    period_start = datetime(datetime.now().year - 1, 1, 1)
                else:
                    period_start = None
                if period_start is not None:
                    all_dated = [
                        item for item in self.get_chart_transactions(include_outside_period=True)
                        if item["date"] is not None
                    ]
                    opening_balance = sum(
                        item["amount"] if item["type"] == "Income" else -item["amount"]
                        for item in all_dated if item["date"] < period_start
                    )
                else:
                    opening_balance = 0.0
                daily = {}
                for item in dated:
                    day = item["date"].date()
                    daily[day] = daily.get(day, 0.0) + (
                        item["amount"] if item["type"] == "Income" else -item["amount"]
                    )
                dates = sorted(daily)
                balance = opening_balance
                balances = []
                for day in dates:
                    balance += daily[day]
                    balances.append(balance)
                positions = list(range(len(dates)))
                axes.plot(positions, balances, color=self.green, linewidth=2.5, marker="o")
                axes.fill_between(positions, balances, 0, color=self.green, alpha=0.16)
                axes.axhline(0, color=self.muted, linewidth=0.8)
                step = max(1, len(dates) // 8)
                ticks = positions[::step]
                axes.set_xticks(ticks)
                axes.set_xticklabels([self.format_day(dates[index]) for index in ticks],
                                     rotation=30, ha="right")
                axes.set_ylabel(self.text("amount"), color=self.muted)
            else:
                self.show_empty_chart(self.text("no_dated_transactions"))

        self.chart_figure.tight_layout()
        chart_text = [
            axes.title, axes.xaxis.label, axes.yaxis.label,
            *axes.texts, *axes.get_xticklabels(), *axes.get_yticklabels()
        ]
        if axes.get_legend():
            chart_text.extend(axes.get_legend().get_texts())
        for text in chart_text:
            text.set_fontfamily(self.chart_font)
        self.chart_canvas.draw_idle()

    def format_month(self, month):
        date = datetime.strptime(month, "%Y-%m")
        months_by_language = {
            "es": ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"),
            "ru": ("янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"),
            "tr": ("Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"),
            "ja": tuple(f"{number}月" for number in range(1, 13)),
            "hi": ("जन", "फ़र", "मार्च", "अप्रै", "मई", "जून", "जुल", "अग", "सित", "अक्टू", "नव", "दिस")
        }
        months = months_by_language.get(self.language)
        if months:
            return f"{months[date.month - 1]} {date.year}"
        return date.strftime("%b %Y")

    def format_day(self, day):
        month = self.format_month(day.strftime("%Y-%m"))
        if self.language in ("ja",):
            return f"{day.year}年{month.split()[0]}{day.day}日"
        if self.language in ("ru", "es", "tr", "hi"):
            return f"{day.day} {month.split()[0]}"
        return day.strftime("%b %d")

    def get_chart_transactions(self, include_outside_period=False):
        period_days = {"last_30_days": 30, "last_90_days": 90,
                       "last_6_months": 183, "last_12_months": 365}
        days = period_days.get(self.period_key)
        cutoff = datetime.now() - timedelta(days=days) if days else None
        today = datetime.now().date()
        if self.period_key == "this_year":
            start_date = datetime(today.year, 1, 1).date()
            end_date = None
        elif self.period_key == "previous_year":
            start_date = datetime(today.year - 1, 1, 1).date()
            end_date = datetime(today.year, 1, 1).date()
        else:
            start_date = None
            end_date = None
        transactions = []
        for transaction_type, records in (("Income", self.incomes), ("Expense", self.expenses)):
            for record in records:
                if not isinstance(record, dict):
                    continue
                try:
                    amount = float(record.get("amount", 0))
                except (TypeError, ValueError):
                    continue
                try:
                    date = datetime.fromisoformat(record.get("date", ""))
                except (TypeError, ValueError):
                    date = None
                if not include_outside_period and cutoff and (date is None or date < cutoff):
                    continue
                if not include_outside_period and start_date and (date is None or date.date() < start_date):
                    continue
                if not include_outside_period and end_date and (date is None or date.date() >= end_date):
                    continue
                transactions.append({
                    "type": transaction_type,
                    "amount": float(self.display_amount(record)),
                    "category": str(record.get("category", "General")),
                    "date": date
                })
        return transactions

    def show_empty_chart(self, message):
        self.chart_axes.text(0.5, 0.5, message, ha="center", va="center",
                             color=self.muted, transform=self.chart_axes.transAxes)
        self.chart_axes.grid(False)

    def refresh_history(self):
        self.history_table.delete(*self.history_table.get_children())
        all_categories = sorted({
            str(record.get("category", "General"))
            for records in (self.incomes, self.expenses)
            for record in records if isinstance(record, dict)
        }, key=str.casefold)
        category_values = (self.text("all_categories"), *all_categories)
        self.history_category_filter.configure(values=category_values)
        if self.history_category_var.get() not in category_values:
            self.history_category_var.set(self.text("all_categories"))
        start_date = self.parse_filter_date(self.history_from_var.get())
        end_date = self.parse_filter_date(self.history_to_var.get())
        search = self.history_search_var.get().strip().casefold()
        selected_type = self.history_type_var.get()
        selected_category = self.history_category_var.get()
        transactions = []
        for transaction_type, records in (("Income", self.incomes), ("Expense", self.expenses)):
            for record in records:
                if not isinstance(record, dict):
                    continue
                category = str(record.get("category", "General"))
                if selected_type not in (self.text("all_types"), self.text(
                    "income" if transaction_type == "Income" else "expense"
                )):
                    continue
                if selected_category != self.text("all_categories") and category != selected_category:
                    continue
                if search and search not in category.casefold():
                    continue
                try:
                    transaction_date = datetime.fromisoformat(record.get("date", ""))
                except (TypeError, ValueError):
                    transaction_date = None
                if start_date and (transaction_date is None or transaction_date.date() < start_date):
                    continue
                if end_date and (transaction_date is None or transaction_date.date() > end_date):
                    continue
                try:
                    amount = self.display_amount(record)
                except (KeyError, TypeError, ValueError):
                    continue
                transactions.append((
                    record.get("date", "Unknown date"), transaction_type,
                    record.get("category", "General"), amount, record.get("id", "")
                ))

        for date, transaction_type, category, amount, record_id in sorted(transactions, reverse=True):
            self.history_table.insert(
                "", "end", iid=record_id or None, values=(
                    date, self.text("income" if transaction_type == "Income" else "expense"),
                    category, self.format_amount(amount)
                )
            )

    @staticmethod
    def parse_filter_date(value):
        value = value.strip()
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None

    def find_transaction(self, record_id):
        for records in (self.incomes, self.expenses):
            for record in records:
                if isinstance(record, dict) and record.get("id") == record_id:
                    return records, record
        return None, None

    def selected_transaction(self):
        selection = self.history_table.selection()
        if not selection:
            messagebox.showinfo(self.text("transactions"), self.text("no_selection"), parent=self.root)
            return None, None
        return self.find_transaction(selection[0])

    def delete_transaction(self):
        records, record = self.selected_transaction()
        if record is None:
            return
        if not messagebox.askyesno(
            self.text("delete_transaction"), self.text("confirm_delete"),
            icon="warning", parent=self.root
        ):
            return
        records.remove(record)
        recurring_id = record.get("recurring_id")
        if recurring_id:
            self.recurring = [
                template for template in self.recurring
                if not isinstance(template, dict) or template.get("id") != recurring_id
            ]
        self.persist_data()
        self.refresh()

    def edit_transaction(self):
        records, record = self.selected_transaction()
        if record is None:
            return
        is_income = records is self.incomes
        dialog = tk.Toplevel(self.root)
        dialog.title(self.text("edit_transaction"))
        dialog.transient(self.root)
        dialog.grab_set()
        body = ttk.Frame(dialog, padding=18)
        body.pack(fill="both", expand=True)
        fields = {}
        labels = ("type", "amount", "currency", "category", "date")
        values = (
            self.text("income" if is_income else "expense"),
            str(record.get("amount", "")), record.get("currency", self.currency),
            record.get("category", "General"), record.get("date", "")
        )
        for row, (key, value) in enumerate(zip(labels, values)):
            ttk.Label(body, text=self.text(key)).grid(row=row, column=0, sticky="w", pady=5)
            if key == "type":
                field = ttk.Combobox(
                    body, state="readonly", values=(self.text("income"), self.text("expense")),
                    width=30
                )
            elif key == "currency":
                field = ttk.Combobox(body, state="readonly", values=tuple(CURRENCIES), width=30)
            else:
                field = ttk.Entry(body, width=33)
            field.grid(row=row, column=1, sticky="ew", padx=(12, 0), pady=5)
            field.insert(0, value) if isinstance(field, ttk.Entry) else field.set(value)
            fields[key] = field

        def save_edit():
            try:
                amount = Decimal(fields["amount"].get().strip())
                if not amount.is_finite() or amount <= 0:
                    raise ValueError
                edited_date = datetime.fromisoformat(fields["date"].get().strip())
            except (InvalidOperation, ValueError):
                messagebox.showerror(
                    self.text("invalid_amount"), self.text("amount_positive"), parent=dialog
                )
                return
            category = fields["category"].get().strip().capitalize()
            if not category:
                messagebox.showerror(
                    self.text("missing_category"), self.text("enter_category"), parent=dialog
                )
                return
            target_records = self.incomes if fields["type"].get() == self.text("income") else self.expenses
            if target_records is not records:
                records.remove(record)
                target_records.append(record)
            record.update({
                "amount": self.money_string(amount, fields["currency"].get()),
                "currency": fields["currency"].get(),
                "source_amount": self.money_string(amount, fields["currency"].get()),
                "source_currency": fields["currency"].get(),
                "category": category,
                "date": edited_date.strftime("%Y-%m-%d %H:%M:%S")
            })
            self.persist_data()
            self.refresh()
            dialog.destroy()

        buttons = ttk.Frame(body)
        buttons.grid(row=len(labels), column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text=self.text("cancel"), command=dialog.destroy).pack(
            side="left", padx=(0, 8)
        )
        ttk.Button(buttons, text=self.text("saved"), style="Accent.TButton",
                   command=save_edit).pack(side="left")
        body.columnconfigure(1, weight=1)

    def export_transactions(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, defaultextension=".csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
            initialfile="budget-transactions.csv"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(("date", "type", "category", "amount", "currency"))
            for transaction_type, records in (("Income", self.incomes), ("Expense", self.expenses)):
                for record in records:
                    if isinstance(record, dict):
                        writer.writerow((
                            record.get("date", ""), transaction_type,
                            record.get("category", "General"), record.get("amount", ""),
                            record.get("currency", self.currency)
                        ))
        messagebox.showinfo(self.text("export_csv"), self.text("export_complete"), parent=self.root)

    def rename_category(self):
        categories = sorted({
            item.get("category", "General") for item in self.expenses if isinstance(item, dict)
        })
        if not categories:
            messagebox.showinfo(self.text("no_categories"), self.text("add_expense_first"), parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(self.text("rename_title"))
        dialog.transient(self.root)
        dialog.resizable(False, False)
        dialog.grab_set()
        body = ttk.Frame(dialog, padding=20)
        body.pack(fill="both", expand=True)
        ttk.Label(body, text=self.text("current_category")).grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        old_category = tk.StringVar(value=categories[0])
        ttk.Combobox(body, textvariable=old_category, state="readonly", values=categories,
                     width=30).grid(row=1, column=0, sticky="ew", pady=(0, 14))
        ttk.Label(body, text=self.text("new_category")).grid(
            row=2, column=0, sticky="w", pady=(0, 6)
        )
        new_category_entry = ttk.Entry(body, width=33)
        new_category_entry.grid(row=3, column=0, sticky="ew", pady=(0, 18))

        def apply_rename():
            new_category = new_category_entry.get().strip().capitalize()
            if not new_category:
                messagebox.showerror(
                    self.text("missing_name"), self.text("enter_new_name"), parent=dialog
                )
                return
            selected = old_category.get()
            for item in self.expenses:
                if isinstance(item, dict) and item.get("category", "General") == selected:
                    item["category"] = new_category
            self.persist_data()
            self.refresh()
            dialog.destroy()

        buttons = ttk.Frame(body)
        buttons.grid(row=4, column=0, sticky="e")
        ttk.Button(buttons, text=self.text("cancel"), style="Quiet.TButton",
                   command=dialog.destroy).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text=self.text("rename"), style="Accent.TButton",
                   command=apply_rename).pack(side="left")
        body.columnconfigure(0, weight=1)
        new_category_entry.focus_set()

    def reset_data(self):
        confirmed = messagebox.askyesno(
            self.text("reset_title"), self.text("reset_warning"),
            icon="warning", parent=self.root
        )
        if not confirmed:
            return
        self.incomes.clear()
        self.expenses.clear()
        self.recurring.clear()
        self.persist_data()
        self.refresh()


def is_new_user():
    return not os.path.exists(SETTINGS_FILE) and not os.path.exists(DATA_FILE)


def main():
    settings = load_settings()
    if is_new_user():
        settings = show_first_run_setup()
        if settings is None:
            return
    root = tk.Tk()
    set_app_icon(root)
    BudgetTrackerApp(root, settings)
    root.mainloop()


if __name__ == "__main__":
    main()