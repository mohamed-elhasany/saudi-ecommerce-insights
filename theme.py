import streamlit as st

def inject():
    st.markdown(
        """
        <style>
        /* IMPORT ARABIC FONT */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap');
        
        /* CSS VARIABLES - Dark Theme Only with Specified Accent Colors */
        :root {
            --dark-bg: #1a1a1a;
            --dark-bg-gradient: linear-gradient(135deg, #1a1a1a 0%, #222222 100%);
            --dark-card: #242424;
            --dark-card-border: #3a3a3a;
            --dark-text-primary: #e8e6e3;
            --dark-text-secondary: #b0a9a2;
            --dark-text-warm: #2C7D8B;  /* Specified accent color 1 */
            --dark-text-cool: #2A927A;  /* Specified accent color 2 */
            --dark-accent: #2C7D8B;     /* Primary accent - specified */
            --dark-accent-hover: #2A927A; /* Secondary accent - specified */
            --dark-sidebar: #1e1e1e;
            --dark-metric-bg: #242424;
            --dark-input-bg: #242424;
            --dark-slider-track: #3a3a3a;
            --dark-table-header: #2a2a2a;
            --dark-table-hover: #2f2f2f;
            --dark-scrollbar-track: #2a2a2a;
            --dark-scrollbar-thumb: #3a3a3a;
            --dark-tab-inactive: #2a2a2a;
            /* Hover colors for tooltips */
            --hover-bg: #C9D2BA;
            --hover-text: #202020;
        }

        /* ARABIC RTL SUPPORT */
        * { 
            font-family: 'Noto Sans Arabic', 'Segoe UI', system-ui, sans-serif !important;
            text-align: right;
            direction: rtl;
        }
        
        /* Exclude plots and charts from RTL */
        .stPlotlyChart *,
        .js-plotly-plot *,
        .plotly *,
        .stPlotlyChart,
        [class*="plotly"] *,
        [class*="hover"] *,
        .modebar,
        .modebar-container {
            text-align: left !important;
            direction: ltr !important;
            font-family: 'Roboto', sans-serif !important;
        }
        
        /* ROOT RESET */
        .stApp { 
            background: var(--dark-bg-gradient);
        }

        /* TYPOGRAPHY - Arabic optimized - Smaller font sizes */
        html, body, [class*="css"] { 
            font-weight: 400;
            line-height: 1.6;
            letter-spacing: -0.01em;
            font-size: 13px; /* Reduced from 14px */
        }

        /* Headers - Smaller sizes */
        h1 {
            font-size: 1.6rem; /* Reduced from 2rem */
            font-weight: 700;
            color: var(--dark-text-primary);
            border-right: 4px solid var(--dark-text-warm);
            padding-right: 12px;
            margin-top: 1.2em;
            margin-bottom: 0.8em;
        }
        
        h2 {
            font-size: 1.3rem; /* Reduced from 1.5rem */
            font-weight: 600;
            color: var(--dark-text-secondary);
            border-bottom: 1px solid var(--dark-card-border);
            padding-bottom: 6px;
            margin-top: 1em;
            margin-bottom: 0.6em;
        }
        
        h3 {
            font-size: 1.1rem; /* Reduced from 1.2rem */
            font-weight: 500;
            color: var(--dark-text-secondary);
            margin-top: 0.8em;
            margin-bottom: 0.5em;
        }
        
        h4 {
            font-size: 1rem; /* Reduced from 1.1rem */
            font-weight: 500;
            color: var(--dark-text-secondary);
            margin-top: 0.7em;
            margin-bottom: 0.4em;
        }

        /* TEXT COLORS */
        .main-text { 
            color: var(--dark-text-primary);
            font-weight: 500;
        }
        
        .sub-text  { 
            color: var(--dark-text-secondary);
            font-weight: 300;
        }
        
        .warm-text {
            color: var(--dark-text-warm);
            font-weight: 600;
        }
        
        .cool-text {
            color: var(--dark-text-cool);
            font-weight: 500;
        }

        /* CARDS & CONTAINERS */
        .stCard {
            background-color: var(--dark-card);
            border: 1px solid var(--dark-card-border);
            padding: 14px; /* Reduced from 16px */
            margin: 6px 0; /* Reduced from 8px */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* METRIC CARDS */
        div[data-testid="stMetric"] {
            background-color: var(--dark-metric-bg);
            border: 1px solid var(--dark-card-border);
            padding: 10px; /* Reduced from 12px */
            text-align: center;
        }
        
        div[data-testid="stMetric"] > div {
            color: var(--dark-text-primary) !important;
            font-size: 1em; /* Reduced from 1.1em */
        }
        
        div[data-testid="stMetricLabel"] {
            color: var(--dark-text-secondary) !important;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        /* BUTTONS */
        .stButton > button {
            background-color: var(--dark-accent);
            color: #ffffff;
            border: none;
            font-weight: 600;
            padding: 8px 20px; /* Reduced from 10x24 */
            font-size: 0.8em; /* Reduced from 0.9em */
            border-radius: 4px;
            margin: 3px; /* Reduced from 4px */
        }
        
        .stButton > button:hover {
            background-color: var(--dark-accent-hover);
            color: #ffffff;
            box-shadow: 0 3px 10px rgba(44, 125, 139, 0.3); /* Reduced shadow */
        }

        /* INPUT WIDGETS */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: var(--dark-input-bg);
            color: var(--dark-text-primary);
            border: 1px solid var(--dark-card-border);
            text-align: right;
            padding-right: 10px; /* Reduced from 12px */
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        /* SLIDERS */
        .stSlider > div > div > div {
            background-color: var(--dark-slider-track);
        }
        
        .stSlider > div > div > div > div {
            background-color: var(--dark-text-warm);
        }

        /* CHECKBOXES & RADIO - RTL */
        .stCheckbox > label,
        .stRadio > label {
            color: var(--dark-text-secondary);
            flex-direction: row-reverse;
            justify-content: flex-end;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        .stCheckbox > label > div:first-child,
        .stRadio > label > div:first-child {
            background-color: var(--dark-input-bg);
            border-color: var(--dark-card-border);
            margin-left: 8px; /* Reduced from 10px */
            margin-right: 0;
        }

        /* DATA TABLES */
        .dataframe {
            background-color: var(--dark-card) !important;
            color: var(--dark-text-primary) !important;
            text-align: right;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        .dataframe th {
            background-color: var(--dark-table-header) !important;
            color: var(--dark-text-warm) !important;
            font-weight: 600;
            border-bottom: 2px solid var(--dark-card-border) !important;
            text-align: right !important;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        .dataframe td {
            border-bottom: 1px solid var(--dark-card-border) !important;
            text-align: right !important;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        .dataframe tr:hover {
            background-color: var(--dark-table-hover) !important;
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background-color: var(--dark-sidebar);
            border-left: 1px solid var(--dark-card-border);
            border-right: none;
        }
        
        /* SIDEBAR NAVIGATION */
        section[data-testid="stSidebar"] div[role="radiogroup"] label {
            color: var(--dark-text-secondary);
            padding: 8px 16px 8px 12px; /* Reduced from 10x18x10x14 */
            margin: 2px 0; /* Reduced from 3px */
            border-right: 3px solid transparent;
            border-left: none;
            text-align: right;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background-color: var(--dark-table-header);
            border-right-color: var(--dark-text-warm);
            color: var(--dark-text-primary);
            padding-right: 18px; /* Reduced from 20px */
        }
        
        section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"][aria-checked="true"] {
            background-color: var(--dark-table-header);
            border-right: 3px solid var(--dark-text-warm);
            border-left: none;
            color: var(--dark-text-primary);
            padding-right: 18px; /* Reduced from 20px */
        }

        /* TABS */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background-color: var(--dark-card);
            padding: 3px; /* Reduced from 4px */
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--dark-tab-inactive);
            color: var(--dark-text-secondary);
            padding: 6px 14px; /* Reduced from 8x16 */
            text-align: center;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--dark-text-warm) !important;
            color: var(--dark-bg) !important;
            font-weight: 600;
        }

        /* PROGRESS BARS */
        .stProgress > div > div > div {
            background-color: var(--dark-text-warm);
        }

        /* SCROLLBARS */
        ::-webkit-scrollbar {
            width: 5px; /* Reduced from 6px */
            height: 5px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--dark-scrollbar-track);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--dark-scrollbar-thumb);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--dark-text-warm);
        }

        /* SELECTION */
        ::selection {
            background-color: rgba(44, 125, 139, 0.3);
            color: var(--dark-text-primary);
        }

        /* PLOT COMPATIBILITY - LTR for plots only */
        .stPlotlyChart,
        .stPlotlyChart > div,
        .stPlotlyChart svg,
        .stPlotlyChart .js-plotly-plot,
        .stPlotlyChart .plot-container,
        .stPlotlyChart .main-svg,
        .stPlotlyChart .bg {
            background-color: transparent !important;
            background: transparent !important;
            text-align: left !important;
            direction: ltr !important;
        }
        
        /* Ensure plot containers don't inherit RTL */
        div[data-testid="stPlotlyChart"],
        .stPlotlyChart {
            background: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
            border: none !important;
        }

        /* SMOOTH PAGE TRANSITIONS */
        .stApp {
            animation: pageLoad 0.5s ease-out;
        }
        
        @keyframes pageLoad {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        /* SPECIFIC FIXES FOR ARABIC TYPOGRAPHY */
        .rtl-container {
            text-align: right;
            direction: rtl;
            font-family: 'Noto Sans Arabic', sans-serif;
        }
        
        .ltr-container {
            text-align: left;
            direction: ltr;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Arabic list styling */
        ol.arabic-list, ul.arabic-list {
            padding-right: 18px; /* Reduced from 20px */
            padding-left: 0;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        li {
            margin-right: 6px; /* Reduced from 8px */
            margin-left: 0;
            margin-bottom: 3px; /* Reduced from 4px */
        }
        
        /* Arabic form controls */
        .stTextArea textarea {
            text-align: right;
            direction: rtl;
            font-size: 0.8em; /* Reduced from 0.9em */
        }
        
        /* Fix for number inputs in RTL */
        .stNumberInput input {
            text-align: right;
            direction: ltr; /* Numbers should be LTR */
        }

        /* Paragraph text */
        p {
            font-size: 0.8em; /* Reduced from 0.9em */
            line-height: 1.6;
            margin-bottom: 0.6em; /* Reduced from 0.8em */
        }
        
        /* Strong text */
        strong {
            color: var(--dark-text-warm);
            font-weight: 600;
        }
        
        /* Links */
        a {
            color: var(--dark-text-cool);
            text-decoration: none;
        }
        
        a:hover {
            color: var(--dark-text-warm);
            text-decoration: underline;
        }

        /* REMOVE THEME SWITCHER */
        .theme-switch {
            display: none !important;
        }
        
        /* Custom hover tooltip styling */
        .hoverlayer .hovertext {
            background-color: var(--hover-bg) !important;
            color: var(--hover-text) !important;
            font-family: 'Noto Sans Arabic', sans-serif !important;
            text-align: right !important;
            direction: rtl !important;
            border: 1px solid var(--dark-card-border) !important;
            border-radius: 4px !important;
            padding: 8px !important;
            font-size: 0.8em !important;
        }
        
        .hoverlayer .hovertext text {
            fill: var(--hover-text) !important;
            font-family: 'Noto Sans Arabic', sans-serif !important;
        }
        /*=========================================================================*/
        /* Hide sidebar expand/collapse keyboard hints */
        section[data-testid="stSidebar"] > div:first-child > div:first-child > div:first-child {
            display: none !important;
        }

        /* Remove ghost transparency effects on sidebar */
        section[data-testid="stSidebar"] > div {
            opacity: 1 !important;
            background-color: var(--dark-sidebar) !important;
        }

        /* Fix sidebar header icons */
        section[data-testid="stSidebar"] button[data-testid="baseButton-header"] {
            background-color: transparent !important;
            border: none !important;
            color: var(--dark-text-primary) !important;
        }

        /* Remove any floating action buttons that might cause ghost effects */
        section[data-testid="stSidebar"] > div > div > div[style*="position: absolute"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )