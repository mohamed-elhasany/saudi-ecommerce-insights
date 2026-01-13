# pages/1_📊 Dashboard.py
import streamlit as st
from theme import inject
import pandas as pd
from analysis import (
    business_mix_chart,
    create_ratings_analysis_chart,
    create_reviews_analysis_chart,
    rating_reviews_heatmap  # إضافة الوظيفة الجديدة
)

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="لوحة تحليل المتاجر - معروف",
    page_icon="📊",
    layout="wide"
)

inject()

# ---------- TITLE AND DESCRIPTION ----------
st.markdown("<h1 class='warm-text'>📊 لوحة تحليل متاجر ماروف</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>تحليل بسيط لأكثر من 70,000 متجر إلكتروني لاختيار أفضل مجال في 2026</p>", unsafe_allow_html=True)

# ---------- CHECK DATA ----------
if 'df' not in st.session_state:
    st.warning("⚠️ يرجى العودة إلى الصفحة الرئيسية أولاً لتحميل البيانات")
    st.stop()

df = st.session_state.df

# ---------- KEY METRICS ----------
st.markdown("<h2 class='cool-text'>📈 المؤشرات الرئيسية</h2>", unsafe_allow_html=True)
st.text('')
# Create metrics using theme styling
col1, col2, col3, col4 = st.columns(4)
total_stores = len(df)
avg_rating = df['rating'].mean()
total_reviews = df['total_reviews'].sum()
high_rated = len(df[df['rating'] >= 4.5])

with col1:
    st.metric(label="إجمالي المتاجر", value=f"{total_stores:,}")
with col2:
    st.metric(label="متوسط التقييم", value=f"{avg_rating:.2f}")
with col3:
    st.metric(label="إجمالي التقييمات", value=f"{total_reviews:,}")
with col4:
    st.metric(label="متاجر ممتازة ≥ 4.5", value=f"{high_rated:,}")

st.divider()

# ---------- CHARTS SECTION ----------
st.markdown("<h2 class='cool-text'>📊 التحليلات</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 أنواع المتاجر",
    "⭐ الأعلى تقييماً",
    "📝 الأكثر نشاطاً",
    "🔥 كثافة التقييمات"  # علامة تبويب جديدة
])

# ---------- Tab 1: Business Mix ----------
with tab1:
    col_set1, col_set2 = st.columns([1, 3])
    
    with col_set1:
        st.markdown("<h3>إعدادات التحليل</h3>", unsafe_allow_html=True)
        
        sort_by = st.selectbox(
            "الترتيب حسب:",
            ["Total", "Reviews"],
            index=0,
            key="mix_sort",
            help="اختر الترتيب حسب عدد المتاجر أو عدد التقييمات"
        )
        top_n_mix = st.slider(
            "عدد المجالات:",
            min_value=5,
            max_value=25,
            value=12,
            key="mix_top_n"
        )

        st.markdown("""
        <div class='stCard'>
        <h4>💡 كيف تقرأ التحليل:</h4>
        <ul class='arabic-list'>
        <li><strong class='warm-text'>الأخضر:</strong> عدد المتاجر</li>
        <li><strong class='cool-text'>الأزرق:</strong> عدد التقييمات (النشاط)</li>
        <li><strong class='warm-text'>الفرصة الذهبية:</strong> مجال فيه نشاط عالي لكن عدد متاجر قليل</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_set2:
        fig_mix = business_mix_chart(df, top_n=top_n_mix, sort_by=sort_by)
        fig_mix.update_layout(
            margin=dict(l=120, r=50, t=50, b=50),
            yaxis=dict(
                tickfont=dict(size=12),
                automargin=True,
                title_standoff=20
            )
        )
        st.plotly_chart(fig_mix, use_container_width=True)
        
        st.markdown("""
        <div class='stCard' style='border-left: 4px solid var(--dark-text-warm);'>
        <h4 class='warm-text'>🎯 توصية بناءً على البيانات:</h4>
        <p class='main-text'>ابحث عن المجالات التي:</p>
        <ul class='arabic-list'>
        <li>عدد المتاجر فيها < 500 (غير مشبعة)</li>
        <li>عدد التقييمات أعلى من المتوسط (نشاط جيد)</li>
        <li>تخصص ضمن مجال واسع (niche)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------- Tab 2: Ratings ----------
with tab2:
    col_set3, col_set4 = st.columns([1, 3])
    
    with col_set3:
        st.markdown("<h3>إعدادات التحليل</h3>", unsafe_allow_html=True)
        
        min_rating = st.slider(
            "الحد الأدنى للتقييم:",
            min_value=4.0,
            max_value=5.0,
            value=4.5,
            step=0.1,
            key="min_rating"
        )
        top_n_rating = st.slider(
            "عدد المتاجر:",
            min_value=5,
            max_value=20,
            value=10,
            key="rating_top_n"
        )

        high_rated_count = len(df[df['rating'] >= min_rating])
        percentage = (high_rated_count / total_stores) * 100

        st.markdown(f"""
        <div class='stCard'>
        <h4>📊 إحصائية واقعية:</h4>
        <ul class='arabic-list'>
        <li>متاجر بتقييم ≥ {min_rating}: <strong class='warm-text'>{high_rated_count:,}</strong></li>
        <li>نسبة: <strong class='cool-text'>{percentage:.1f}%</strong></li>
        <li>التميز نادر، فرصتك في تقديم خدمة ممتازة</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_set4:
        fig_rating = create_ratings_analysis_chart(df, min_rating=min_rating, top_n=top_n_rating)
        fig_rating.update_layout(
            margin=dict(l=120, r=50, t=50, b=50),
            yaxis=dict(
                tickfont=dict(size=12),
                automargin=True,
                title_standoff=20
            )
        )
        st.plotly_chart(fig_rating, use_container_width=True)
        
        st.markdown("""
        <div class='stCard' style='border-left: 4px solid var(--dark-text-cool);'>
        <h4 class='cool-text'>💎 دروس من الأفضل:</h4>
        <ul class='arabic-list'>
        <li>وصف دقيق للمنتجات (لا خداع)</li>
        <li>استجابة خلال أقل من ساعة</li>
        <li>توصيل أسرع من المتوقع</li>
        <li>تغليف أنيق يُظهر الاهتمام</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------- Tab 3: Reviews ----------
with tab3:
    col_set5, col_set6 = st.columns([1, 3])
    
    with col_set5:
        st.markdown("<h3>إعدادات التحليل</h3>", unsafe_allow_html=True)
        
        top_n_reviews = st.slider(
            "عدد المتاجر:",
            min_value=5,
            max_value=20,
            value=10,
            key="reviews_top_n"
        )

        top_store = df.sort_values('total_reviews', ascending=False).iloc[0]
        avg_reviews = df['total_reviews'].mean()

        st.markdown(f"""
        <div class='stCard'>
        <h4>🏆 الأكثر نشاطاً:</h4>
        <ul class='arabic-list'>
        <li><strong class='warm-text'>{top_store['name_ar']}</strong></li>
        <li>{top_store['total_reviews']:,} تقييم</li>
        <li>بمعدل {top_store['rating']}/5</li>
        <li>متوسط السوق: <strong class='cool-text'>{avg_reviews:.0f}</strong> تقييم</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_set6:
        fig_reviews = create_reviews_analysis_chart(df, top_n=top_n_reviews)
        fig_reviews.update_layout(
            margin=dict(l=120, r=50, t=50, b=50),
            yaxis=dict(
                tickfont=dict(size=12),
                automargin=True,
                title_standoff=20
            )
        )
        st.plotly_chart(fig_reviews, use_container_width=True)
        
        st.markdown("""
        <div class='stCard' style='border-left: 4px solid var(--dark-text-warm);'>
        <h4 class='warm-text'>📈 استراتيجيات زيادة التقييمات:</h4>
        <ul class='arabic-list'>
        <li>بعد كل عملية شراء، أرسل رسالة شكر</li>
        <li>اطلب التقييم بلطف بعد أسبوع من التوصيل</li>
        <li>قدم خصم 5% للمقيّمين</li>
        <li>رد على كل تقييم (يوضح اهتمامك)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# ---------- Tab 4: Heatmap ----------
# ---------- Tab 4: Heatmap ----------
with tab4:
    col_set7, col_set8 = st.columns([1, 3])
    
    with col_set7:
        st.markdown("<h3>إعدادات التحليل</h3>", unsafe_allow_html=True)
        
        # قسم 1: الإدخال اليدوي
        st.markdown("<h4>🔢 الإدخال اليدوي:</h4>", unsafe_allow_html=True)
        
        # تهيئة session state إذا لم تكن موجودة
        if 'heatmap_min_manual' not in st.session_state:
            st.session_state.heatmap_min_manual = 0
        if 'heatmap_max_manual' not in st.session_state:
            st.session_state.heatmap_max_manual = 100
        
        # الحصول على الحد الأقصى الحقيقي للبيانات
        max_reviews_in_data = int(df['total_reviews'].max())
        
        # إصلاح: استخدام القيمة الفعلية القصوى
        st.session_state.heatmap_max_manual = min(st.session_state.heatmap_max_manual, max_reviews_in_data)
        
        # إدخال الحد الأدنى
        min_reviews_manual = st.number_input(
            "الحد الأدنى للمراجعات:",
            min_value=0,
            max_value=max_reviews_in_data,
            value=st.session_state.heatmap_min_manual,
            step=10,
            key="heatmap_min_input",
            help="أدخل الحد الأدنى لعدد المراجعات"
        )
        
        # إدخال الحد الأقصى
        max_reviews_manual = st.number_input(
            "الحد الأقصى للمراجعات:",
            min_value=min_reviews_manual + 1,
            max_value=max_reviews_in_data,
            value=st.session_state.heatmap_max_manual,
            step=10,
            key="heatmap_max_input",
            help=f"أدخل الحد الأقصى لعدد المراجعات (الحد الأقصى في البيانات: {max_reviews_in_data:,})"
        )
        
        # زر تطبيق الإدخال اليدوي
        if st.button("تطبيق النطاق اليدوي", key="apply_manual_range", type="primary"):
            st.session_state.heatmap_min_manual = min_reviews_manual
            st.session_state.heatmap_max_manual = max_reviews_manual
            st.rerun()
        
        st.divider()
        
        # قسم 2: النطاقات السريعة
        st.markdown("<h4>🚀 نطاقات سريعة:</h4>", unsafe_allow_html=True)
        
        # إنشاء نطاقات سريعة بناءً على القيم الفعلية للبيانات
        quick_ranges = {
            "0-100 مراجعة (مبتدئين)": (0, 100),
            "100-500 مراجعة (متوسطين)": (100, 500),
            "500-1000 مراجعة (نشطين)": (500, 1000),
        }
        
        # إضافة نطاقات إضافية فقط إذا كانت القيم موجودة
        if max_reviews_in_data > 1000:
            if max_reviews_in_data >= 5000:
                quick_ranges["1000-5000 مراجعة (محترفين)"] = (1000, 5000)
                quick_ranges[f"{max_reviews_in_data}+ مراجعة (كبار)"] = (5000, max_reviews_in_data)
            else:
                quick_ranges[f"1000+ مراجعة (محترفين)"] = (1000, max_reviews_in_data)
        
        # إنشاء أزرار للنطاقات السريعة مع مفاتيح فريدة
        range_counter = 0
        for range_name, (min_val, max_val) in quick_ranges.items():
            if st.button(
                f"{range_name}",
                key=f"quick_range_{range_counter}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.heatmap_min_manual = min_val
                st.session_state.heatmap_max_manual = max_val
                st.rerun()
            range_counter += 1
        
        st.divider()
        
        # قسم 3: معلومات النطاق الحالي
        current_min = st.session_state.heatmap_min_manual
        current_max = min(st.session_state.heatmap_max_manual, max_reviews_in_data)
        
        st.markdown(f"""
        <div class='stCard'>
        <h4>📊 النطاق الحالي:</h4>
        <div style='text-align: center; padding: 15px; background-color: var(--light-cool); border-radius: 8px; margin: 10px 0;'>
            <h2 style='margin: 0; color: var(--dark-text-cool);'>
            {current_min:,} ← {current_max:,}
            </h2>
            <p style='margin: 5px 0 0 0; color: var(--dark-text-cool);'>
            عرض النطاق: {current_max - current_min:,} مراجعة
            </p>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        # قسم 4: كيفية القراءة
        st.markdown("""
        <div class='stCard'>
        <h4>💡 كيف تقرأ الخريطة الحرارية:</h4>
        <ul class='arabic-list'>
        <li><strong class='warm-text'>الألوان الفاتحة:</strong> مناطق قليلة المتاجر</li>
        <li><strong class='cool-text'>الألوان الداكنة:</strong> مناطق كثيفة المتاجر</li>
        <li><strong class='warm-text'>✅ الفرصة:</strong> تقييم عالي مع مراجعات قليلة</li>
        <li><strong class='cool-text'>⚠️ التحدي:</strong> تقييم منخفض مع مراجعات كثيرة</li>
        <li><strong>🎯 المستهدف:</strong> تقييم 4.5+ مع مراجعات متوسطة</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_set8:
        # استخدام القيم من session state
        current_min = st.session_state.heatmap_min_manual
        current_max = min(st.session_state.heatmap_max_manual, max_reviews_in_data)
        
        if current_max <= current_min:
            current_max = min(current_min + 100, max_reviews_in_data)
            st.session_state.heatmap_max_manual = current_max
        
        # العثور على اسم النطاق السريع المناسب
        range_name = "مخصص"
        for name, (min_val, max_val) in quick_ranges.items():
            if current_min == min_val and current_max == max_val:
                range_name = name.split(" (")[0]  # إزالة النص بين قوسين
        
        fig_heatmap = rating_reviews_heatmap(
            df, 
            reviews_range=(current_min, current_max),
            title=f"كثافة التقييمات مقابل المراجعات - {range_name}"
        )
        
        fig_heatmap.update_layout(
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # تحليل البيانات
        filtered_data = df[
            (df['total_reviews'] >= current_min) & 
            (df['total_reviews'] <= current_max)
        ]
        
        if len(filtered_data) > 0:
            avg_rating_in_range = filtered_data['rating'].mean()
            total_stores_in_range = len(filtered_data)
            avg_reviews_in_range = filtered_data['total_reviews'].mean()
            
            # حساب النسب المئوية
            percentage_of_total = (total_stores_in_range / total_stores) * 100
            
            # العثور على أفضل متاجر في هذا النطاق
            best_in_range = filtered_data.sort_values(['rating', 'total_reviews'], ascending=[False, False]).head(3)
            
            # العثور على مناطق الفرص (تقييم عالي + مراجعات قليلة)
            opportunity_stores = filtered_data[
                (filtered_data['rating'] >= 4.5) & 
                (filtered_data['total_reviews'] <= avg_reviews_in_range)
            ].head(3)
            
            best_stores_html = ""
            if len(best_in_range) > 0:
                for idx, row in best_in_range.iterrows():
                    store_name = row['name_ar'][:30] + "..." if len(row['name_ar']) > 30 else row['name_ar']
                    best_stores_html += f"""
                    <li style="
                        margin-bottom: 12px;
                        padding: 14px 16px;
                        background-color: #161b1c;
                        border-left: 3px solid #2C7D8B;
                        list-style-type: none;
                        box-shadow: 0 6px 14px rgba(0,0,0,0.35);
                    ">
                        <strong style="color: #C9D2BA;">{store_name}</strong><br>
                        <span style="color: #2C7D8B;">⭐ {row['rating']}/5</span>
                        &nbsp;|&nbsp;
                        <span style="color: #2A927A;">📝 {row['total_reviews']:,}</span>
                    </li>
                    """


            opportunity_html = ""
            if len(opportunity_stores) > 0:
                for idx, row in opportunity_stores.iterrows():
                    store_name = row['name_ar'][:30] + "..." if len(row['name_ar']) > 30 else row['name_ar']
                    opportunity_html += f"""
                    <li style="
                        margin-bottom: 12px;
                        padding: 14px 16px;
                        background-color: #151c1b;
                        border-left: 3px solid #2A927A;
                        list-style-type: none;
                        box-shadow: 0 6px 14px rgba(0,0,0,0.35);
                    ">
                        <strong style="color: #C9D2BA;">{store_name}</strong><br>
                        <span style="color: #2C7D8B;">⭐ {row['rating']}/5</span>
                        &nbsp;|&nbsp;
                        <span style="color: #2A927A;">📝 {row['total_reviews']:,}</span>
                    </li>
                    """

            if len(filtered_data) > 0:
                st.markdown(f"""
                <div class='stCard' style='border-left: 4px solid var(--dark-text-warm);'>
                <h4 class='warm-text'>📊 تحليل النطاق الحالي:</h4>
                <ul class='arabic-list'>
                <li>عدد المتاجر في النطاق: <strong>{total_stores_in_range:,}</strong></li>
                <li>متوسط التقييم: <strong>{avg_rating_in_range:.2f}/5</strong></li>
                <li>متوسط المراجعات: <strong>{avg_reviews_in_range:.0f}</strong></li>
                <li>نسبة من إجمالي المتاجر: <strong>{percentage_of_total:.1f}%</strong></li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
                
                if best_stores_html:
                    st.markdown(f"""
                    <div class='stCard' style='border-left: 4px solid var(--dark-text-cool); margin-top: 20px;'>
                    <h4 class='cool-text'>🏆 أفضل 3 متاجر في هذا النطاق:</h4>
                    <ul class='arabic-list' style='list-style-type: none; padding-left: 0;'>
                    {best_stores_html}
                    </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
                if opportunity_html:
                    st.markdown(f"""
                    <div class='stCard' style='border-left: 4px solid #28a745; margin-top: 20px;'>
                    <h4 style='color: #28a745;'>🎯 فرص للدراسة (تقييم عالي + مراجعات قليلة):</h4>
                    <ul class='arabic-list' style='list-style-type: none; padding-left: 0;'>
                    {opportunity_html}
                    </ul>
                    <p style='color: var(--dark-text-cool); font-size: 12px; margin-top: 10px;'>
                    هذه المتاجر حصلت على تقييمات عالية بأقل من متوسط المراجعات، قد تكون نموذجاً جيداً للدراسة.
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='stCard' style='border-left: 4px solid var(--warm);'>
                <h4 class='warm-text'>⚠️ ملاحظة:</h4>
                <p>لا توجد متاجر في هذا النطاق من المراجعات. حاول اختيار نطاق أوسع.</p>
                </div>
                """, unsafe_allow_html=True)

st.divider()

# ---------- FINAL RECOMMENDATIONS ----------
st.markdown("<h2 class='cool-text'>🎯 توصياتنا لعام 2026</h2>", unsafe_allow_html=True)

st.markdown("""
<style>
body, p, div, li, span, .stMarkdown, .rtl-container {
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

# إصلاح: استخدام column واحد بشكل صحيح
col_rec1, = st.columns(1)

with col_rec1:
    st.markdown("""
    <div class='stCard'>
    <h3 class='warm-text'>📊 استراتيجية الدخول:</h3>
    <ol class='arabic-list'>
    <li><strong>اختر مجالك:</strong>
        <ul class='arabic-list'>
        <li>أنشط من المتاجر < 500 (غير مشبع)</li>
        <li>تقييماته أعلى من 1000 (سوق حي)</li>
        <li>يمكنك التخصص في جزء منه</li>
        </ul>
    </li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------- EVIDENCE SECTION ----------
st.markdown("<h3 class='cool-text'>📈 أدلتنا من البيانات</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class='stCard' style='border-left: 4px solid var(--dark-text-cool);'>
<h4 class='warm-text'>ما تخبرنا به الأرقام:</h4>
<ol class='arabic-list'>
<li><strong>السوق ناضج لكن فيه فرص:</strong>
    <ul class='arabic-list'>
    <li>{total_stores:,} متجر يعني تنوع وخيارات</li>
    <li>متوسط التقييم {avg_rating:.2f}/5 يدل على جودة عامة</li>
    <li>فقط {high_rated:,} متجر ممتاز (فرصة للتميز)</li>
    </ul>
</li>
</ol>
</div>
""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px;' class='sub-text'>
👨‍💻 محمد الحسني - محلل بيانات | 📧 elhasanymohamed123@gmail.com<br>
البيانات من منصة "معروف" | التحليل لمساعدتك في اتخاذ قرار مدروس
</div>
""", unsafe_allow_html=True)