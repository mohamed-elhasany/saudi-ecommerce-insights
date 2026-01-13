# main.py
from theme import inject
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="تحليل منصات التجارة الإلكترونية - ماروف",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- GLOBAL THEME ----------
inject()
st.markdown("""
<style>
/* إزالة أيقونة السهم عند hover على sidebar */
.css-1d391kg { 
    display: none !important; 
}
</style>
""", unsafe_allow_html=True)

# ---------- GLOBAL DATA ----------
GOOGLE_FILE_ID = "1CJGNXI3yp0l1rpzERVyKCU1K55DzfqIS"
URL = f"https://drive.usercontent.google.com/download?id={GOOGLE_FILE_ID}&export=download&confirm=t"

@st.cache_data(show_spinner=False)
def get_stores_data() -> pd.DataFrame:
    """Download the CSV once and return a DataFrame."""
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content)) 


# ---------- MAIN PAGE ----------
# ---------- MAIN PAGE ----------
def main():
    # ---------- Welcome Header ----------
    st.markdown("""
# 🏪 أهلاً وسهلاً في منصة تحليل متاجر معروف
دليلك الذكي لاختيار أفضل مجال للتجارة الإلكترونية في 2026

""")  # <- breakline بعد العنوان

    # ---------- What you'll find ----------
    st.markdown("""
## 🎯 ماذا ستكتشف هنا؟

أكثر من **70,000 متجر إلكتروني** مسجل في منصة معروف السعودية، 
نحن هنا لنساعدك على اختيار المجال الأنسب لدخول سوق التجارة الإلكترونية بثقة.
                
### 📌 السؤال الأهم:
**"ما هو أفضل مجال للتجارة الإلكترونية أبدأ فيه عام 2026؟"**

""")  # <- breakline بعد القسم

    # ---------- How to use ----------
    st.markdown("""
## 🚀 كيف تبدأ رحلتك مع منصة معروف؟

اتبع هذه الخطوات البسيطة لتكتشف المجال الأنسب لك في التجارة الإلكترونية:

1️⃣ **اضغط على زر "🚀 ابدأ التحليل الآن"** لبدء تجربة التحليل الذكي.  
2️⃣ **تصفح التحليلات الرئيسية**: تعرف على أفضل المتاجر حسب التقييم، النشاط.  
3️⃣ **استخرج النتائج وابدأ التخطيط لمشروعك**: قراراتك الآن ستكون مبنية على بيانات حقيقية وموثوقة.

✨ تجربة تحليل المتاجر لم تكن يومًا أسهل أو أكثر متعة!

""")  # <- breakline بعد القسم

    # ---------- Start Button ----------
    if st.button("🚀 ابدأ التحليل الآن", key="start_analysis"):
        st.switch_page("pages/1_📊 منصة التحليل.py")

    # ---------- Quick info about the data ----------
    st.markdown("""
## 📋 عن البيانات

البيانات مأخوذة من منصة **معروف**، مبادرة مشتركة بين وزارة الموارد البشرية ووزارة التجارة، 
تضم أكثر من **70,000 متجر إلكتروني** مسجل.

👨‍💻 **المطور:** محمد الحسني - محلل بيانات  
📧 **للتواصل:** elhasanymohamed123@gmail.com  

🔒 كل البيانات تعرض بشكل آمن وموثوق لتساعدك في اتخاذ قراراتك بسهولة.
""")

    with st.container():
        st.markdown("""
        <div class="footer">
            <div class="analyst-info">
                <h3 style="color: var(--dark-text-warm); margin-bottom: 0.5rem;">👨‍💻 نبذة عن محلل البيانات</h3>
                <p style="color: var(--dark-text-secondary); margin-bottom: 0.5rem;">
                    <b>محمد الحسني</b> | محلل بيانات عام
                </p>
                <p style="color: var(--dark-text-secondary);">
                    📧 <b>البريد الإلكتروني:</b> elhasanymohamed123@gmail.com<br>
                    🔗 <b>روابط الأعمال:</b> 
                    <a href="https://github.com/mohamed-elhasany" target="_blank" style="color: var(--dark-text-cool); text-decoration: none;">GitHub</a> •
                    <a href="https://khamsat.com/user/elhasany_123" target="_blank" style="color: var(--dark-text-cool); text-decoration: none;">خمسات</a> •
                    <a href="https://www.freelancer.com/u/mohamede0226" target="_blank" style="color: var(--dark-text-cool); text-decoration: none;">Freelancer</a> •
                    <a href="https://cute-sawine-f485eb.netlify.app/" target="_blank" style="color: var(--dark-text-cool); text-decoration: none;">موقعي الشخصي</a>
                </p>
            </div>
            <p style="color: var(--dark-text-secondary); margin-top: 1rem; font-size: 0.9rem;">
                تم البناء باستخدام ❤️ عبر Streamlit و Plotly • مجموعة البيانات: بيانات التجارة الإلكترونية البرازيلية العامة من Olist
            </p>
        </div>
        """, unsafe_allow_html=True)



# ---------- LOAD DATA & RUN ----------
if __name__ == "__main__":
    # تحميل البيانات مرة واحدة وتخزينها في session state
    if 'df' not in st.session_state:
        with st.spinner("جاري تحميل بيانات المتاجر..."):
            df = get_stores_data()
            st.session_state.df = df

    # تشغيل الصفحة الرئيسية
    main()
