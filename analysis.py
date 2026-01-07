# analysis.py
"""
Business-mix horizontal bar-chart generator.
Use:
    from analysis import business_mix_chart
    fig = business_mix_chart(df, top_n=15, sort_by='Reviews')
    st.plotly_chart(fig, use_container_width=True)
"""
from __future__ import annotations
import re
import pandas as pd
import plotly.graph_objects as go


def _build_business_mix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Internal helper:
    - Groups by 'business_type_ar' and 'other_type_name'
    - Drops 'أخرى' and empty/whitespace-only labels
    - Returns unified frame with columns: Type | Total | Reviews
    """
    # 1. mainstream types
    wdf = (
        df.groupby("business_type_ar", as_index=False)
        .agg(Total=("business_type_ar", "count"), Reviews=("total_reviews", "sum"))
        .rename(columns={"business_type_ar": "Type"})
        .query("Type != 'أخرى'")  # drop 'others' placeholder
    )

    # 2. free-text types
    wdf2 = (
        df.dropna(subset=["other_type_name"])
        .groupby("other_type_name", as_index=False)
        .agg(Total=("other_type_name", "count"), Reviews=("total_reviews", "sum"))
        .rename(columns={"other_type_name": "Type"})
    )

    mixed = pd.concat([wdf, wdf2], ignore_index=True)

    # drop purely whitespace labels
    mask = mixed["Type"].str.contains(r"^\s*$", regex=True, na=False)
    return mixed.loc[~mask]


def _bus_type(row: pd.Series) -> str:
    """Unified business-type logic with proper NaN handling."""
    # Try business_type_ar first
    bus_type = row.get("business_type_ar")
    if pd.notna(bus_type):
        bus_str = str(bus_type).strip()
        if bus_str and bus_str not in {"أخرى", "nan", "NaN", "None", ""}:
            return bus_str
    
    # Try other_type_name next
    other_type = row.get("other_type_name")
    if pd.notna(other_type):
        other_str = str(other_type).strip()
        if other_str and other_str not in {"nan", "NaN", "None", ""}:
            return other_str
    
    return "لم يتم التحديد"


def _hover_text(row: pd.Series) -> str:
    """Unified hover text with proper Arabic formatting and NaN handling."""
    # Get business type
    bus_type = _bus_type(row)
    
    # Handle description safely
    desc = row.get("description")
    if pd.isna(desc):
        desc_text = "لا يوجد وصف متاح"
    else:
        desc_str = str(desc).strip()
        desc_text = (desc_str[:197] + "...") if len(desc_str) > 200 else desc_str
    
    # Handle rating and reviews
    rating_val = row.get('rating')
    reviews_val = row.get('total_reviews')
    
    # Format rating
    if pd.isna(rating_val):
        rating_text = "غير متاح"
    else:
        rating_text = f"{float(rating_val):.2f}"
    
    # Format reviews
    if pd.isna(reviews_val):
        reviews_text = "غير متاح"
    else:
        reviews_num = int(reviews_val)
        reviews_text = f"{reviews_num:,}"
    
    # Get name
    name_val = row.get('name_ar', 'N/A')
    name_text = str(name_val) if pd.notna(name_val) else "غير متاح"
    
    # Create Arabic hover text with theme-matching colors
    hover_text = (
        f"<b style='color:#202020;'>{name_text}</b><br>"
        f"<b style='color:#202020;'>النوع:</b> <span style='color:#202020;'>{bus_type}</span><br>"
        f"<b style='color:#202020;'>التقييم:</b> <span style='color:#202020;'>{rating_text}</span><br>"
        f"<b style='color:#202020;'>عدد التقييمات:</b> <span style='color:#202020;'>{reviews_text}</span><br>"
        f"<b style='color:#202020;'>الوصف:</b> <span style='color:#202020;'>{desc_text}</span>"
    )
    
    return hover_text


def business_mix_chart(
    df: pd.DataFrame,
    *,
    top_n: int = 10,
    sort_by: str = "Total",
) -> go.Figure:
    """
    Return a horizontal bar chart (Plotly) of the top-N business types.
    """
    if sort_by not in {"Total", "Reviews"}:
        raise ValueError("sort_by must be 'Total' or 'Reviews'")

    data = _build_business_mix(df).sort_values(sort_by, ascending=True).tail(top_n)

    fig = go.Figure()

    # Determine Arabic labels
    if sort_by == "Total":
        sort_text = "عدد المتاجر"
        total_label = "عدد المتاجر"
        reviews_label = "عدد التقييمات"
    else:
        sort_text = "عدد التقييمات"
        total_label = "عدد التقييمات"
        reviews_label = "عدد المتاجر"

    # --- Total bar ---
    fig.add_bar(
        y=data["Type"],
        x=data["Total"],
        name=total_label,
        orientation="h",
        marker_color="#2C7D8B",  # Specified accent color
        text=data["Total"],
        textposition="outside",
        hovertemplate="%{y}<br>%{x} متجر<extra></extra>",
        width=0.3,
    )

    # --- Reviews bar ---
    fig.add_bar(
        y=data["Type"],
        x=data["Reviews"],
        name=reviews_label,
        orientation="h",
        marker_color="#2A927A",  # Specified accent color
        text=data["Reviews"],
        textposition="outside",
        hovertemplate="%{y}<br>%{x} تقييم<extra></extra>",
        width=0.3,
    )

    fig.update_layout(
        title=dict(
            text=f"أعلى {top_n} نوع متجر حسب {sort_text}",
            font=dict(size=16, family='Noto Sans Arabic')  # Reduced size
        ),
        barmode="group",
        xaxis_title="العدد",
        yaxis_title=None,
        yaxis_categoryorder="total ascending",
        height=max(400, top_n * 35),  # Reduced height per item
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            title="المؤشرات",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hoverlabel=dict(
            bgcolor="#C9D2BA",  # Specified hover background
            font_size=12,  # Reduced size
            font_family="Noto Sans Arabic",
            align="right",
            font_color="#202020"  # Specified hover text color
        ),
        font=dict(family='Noto Sans Arabic')
    )
    return fig


def create_ratings_analysis_chart(df: pd.DataFrame, *, min_rating: float = 4.5, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart: highest-rated businesses."""
    d = df[df["rating"] >= min_rating].copy()
    if d.empty:
        return go.Figure().add_annotation(
            text=f"لا توجد متاجر بتقييم ≥ {min_rating}",
            showarrow=False,
            font=dict(size=14, family='Noto Sans Arabic')  # Reduced size
        )

    d = (
        d.assign(hover=lambda x: x.apply(_hover_text, axis=1))
        .sort_values("rating", ascending=True)
        .tail(top_n)
    )

    fig = go.Figure(
        [
            go.Bar(
                y=d["name_ar"],
                x=d["rating"],
                name="التقييم",
                orientation="h",
                marker_color="#2C7D8B",  # Specified accent color
                text=d["rating"].round(2),
                textposition="outside",
                hovertemplate="%{hovertext}<extra></extra>",
                hovertext=d["hover"],
                width=0.3,
            ),
            go.Bar(
                y=d["name_ar"],
                x=d["total_reviews"],
                name="عدد التقييمات",
                orientation="h",
                marker_color="#2A927A",  # Specified accent color
                text=d["total_reviews"],
                textposition="outside",
                hovertemplate="%{hovertext}<extra></extra>",
                hovertext=d["hover"],
                width=0.3,
            ),
        ]
    )

    fig.update_layout(
        title=dict(
            text=f"أعلى {top_n} متجر بتقييم ≥ {min_rating}",
            font=dict(size=16, family='Noto Sans Arabic')  # Reduced size
        ),
        barmode='group',
        xaxis_title="التقييم / العدد",
        yaxis_title=None,
        yaxis_categoryorder="total ascending",
        height=max(400, top_n * 35),  # Reduced height per item
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            title="المؤشرات",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hoverlabel=dict(
            bgcolor="#C9D2BA",  # Specified hover background
            font_size=12,  # Reduced size
            font_family="Noto Sans Arabic",
            align="right",
            font_color="#202020"  # Specified hover text color
        ),
        font=dict(family='Noto Sans Arabic')
    )
    return fig


def create_reviews_analysis_chart(df: pd.DataFrame, *, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart: most-reviewed businesses."""
    d = (
        df.assign(hover=lambda x: x.apply(_hover_text, axis=1))
        .sort_values("total_reviews", ascending=True)
        .tail(top_n)
    )

    fig = go.Figure(
        [
            go.Bar(
                y=d["name_ar"],
                x=d["total_reviews"],
                name="عدد التقييمات",
                orientation="h",
                marker_color="#2C7D8B",  # Specified accent color
                text=d["total_reviews"],
                textposition="outside",
                hovertemplate="%{hovertext}<extra></extra>",
                hovertext=d["hover"],
                width=0.3,
            ),
            go.Bar(
                y=d["name_ar"],
                x=d["rating"],
                name="التقييم",
                orientation="h",
                marker_color="#2A927A",  # Specified accent color
                text=d["rating"].round(2),
                textposition="outside",
                hovertemplate="%{hovertext}<extra></extra>",
                hovertext=d["hover"],
                width=0.3,
            ),
        ]
    )

    fig.update_layout(
        title=dict(
            text=f"أعلى {top_n} متجر حسب عدد التقييمات",
            font=dict(size=16, family='Noto Sans Arabic')  # Reduced size
        ),
        barmode='group',
        xaxis_title="العدد / التقييم",
        yaxis_title=None,
        yaxis_categoryorder="total ascending",
        height=max(400, top_n * 35),  # Reduced height per item
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(
            title="المؤشرات",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        hoverlabel=dict(
            bgcolor="#C9D2BA",  # Specified hover background
            font_size=12,  # Reduced size
            font_family="Noto Sans Arabic",
            align="right",
            font_color="#202020"  # Specified hover text color
        ),
        font=dict(family='Noto Sans Arabic')
    )
    return fig

# ================================================================
def rating_reviews_heatmap(df: pd.DataFrame, *, 
                          reviews_range: tuple = (0, 100),
                          title: str = "كثافة التقييمات مقابل المراجعات") -> go.Figure:
    """
    Create a heatmap of rating vs reviews for a specific reviews range.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataframe containing the data
    reviews_range : tuple
        Range of total_reviews to display (min, max)
    title : str
        Title of the plot
    """
    import numpy as np
    import plotly.graph_objects as go
    
    # Filter out rows with NaN values
    filtered_df = df.dropna(subset=["total_reviews", "rating"])
    
    # Apply reviews range filter
    min_reviews, max_reviews = reviews_range
    filtered_df = filtered_df[
        (filtered_df["total_reviews"] >= min_reviews) & 
        (filtered_df["total_reviews"] <= max_reviews)
    ]
    
    # Ensure we have data to plot
    if len(filtered_df) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text=f"لا توجد بيانات في نطاق {min_reviews}-{max_reviews} مراجعة",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, family="Noto Sans Arabic")
        )
        return fig
    
    # Get data
    reviews = filtered_df["total_reviews"]
    ratings = filtered_df["rating"]
    
    # Use the provided range for x-axis
    x_min, x_max = min_reviews, max_reviews
    if x_max <= x_min:
        x_max = x_min + 1
    
    # For y-axis (ratings) - always 0 to 5
    y_min, y_max = 0, 5
    
    # Determine number of bins based on range size
    range_width = x_max - x_min
    if range_width <= 10:
        x_bins = range_width + 1  # One bin per integer
    elif range_width <= 50:
        x_bins = min(30, int(range_width / 2))  # Bins of size ~2
    elif range_width <= 200:
        x_bins = min(50, int(range_width / 5))  # Bins of size ~5
    else:
        x_bins = min(100, int(np.sqrt(len(filtered_df)) * 2))
    
    y_bins = 20  # Fixed for ratings 0-5
    
    # Create 2D histogram for density
    hist, x_edges, y_edges = np.histogram2d(
        x=reviews,
        y=ratings,
        bins=[x_bins, y_bins],
        range=[[x_min, x_max], [y_min, y_max]]
    )
    
    # Transpose histogram for correct orientation
    hist = hist.T
    
    # Create hover text
    hover_texts = []
    for i in range(len(y_edges) - 1):
        row_texts = []
        for j in range(len(x_edges) - 1):
            # Format x range based on bin width
            x_start = int(x_edges[j])
            x_end = int(x_edges[j+1])
            x_range_str = f"{x_start}" if x_end - x_start <= 1 else f"{x_start}–{x_end}"
            
            text = (f"مراجعات: {x_range_str}<br>"
                    f"تقييم: {y_edges[i]:.2f}–{y_edges[i+1]:.2f}<br>"
                    f"عدد المتاجر: {int(hist[i, j])}")
            row_texts.append(text)
        hover_texts.append(row_texts)
    
    # Calculate color scale normalization
    hist_nonzero = hist[hist > 0]
    if len(hist_nonzero) > 0:
        # Use percentile to handle outliers
        z_min = np.percentile(hist_nonzero, 1) if len(hist_nonzero) > 10 else 0
        z_max = np.percentile(hist_nonzero, 99) if len(hist_nonzero) > 10 else np.max(hist_nonzero)
        
        # Use log scale if data spans large range
        if z_max / max(z_min, 1) > 100:
            z_data = np.log1p(hist)
            colorbar_title = "عدد المتاجر (مقياس لوغاريتمي)"
            z_min = np.log1p(z_min) if z_min > 0 else 0
            z_max = np.log1p(z_max)
        else:
            z_data = hist
            colorbar_title = "عدد المتاجر"
    else:
        z_data = hist
        colorbar_title = "عدد المتاجر"
        z_min, z_max = 0, 1
    
    # Create heatmap
    fig = go.Figure(go.Heatmap(
        z=z_data,
        x=[(x_edges[i] + x_edges[i+1])/2 for i in range(len(x_edges)-1)],
        y=[(y_edges[i] + y_edges[i+1])/2 for i in range(len(y_edges)-1)],
        text=hover_texts,
        hovertemplate="%{text}<extra></extra>",
        colorscale = [
            [0.0, 'rgba(255, 255, 255, 0)'],   # Transparent for zero
            [0.001, "#6B2F1D"],                # Dark gray
            [0.33, "#236A77"],                 # Teal gray
            [0.66, "#26AD90"],                 # Main teal
            [1.0, "#1CC741"]                   # Green teal
        ],
        
        colorbar=dict(title=colorbar_title, tickformat=",d"),
        zmin=z_min,
        zmax=z_max,
        showscale=True,
    ))
    
    # Update layout with Arabic titles only
    fig.update_layout(
        title=dict(
            text=f"{title}<br><span style='font-size:12px;'>نطاق المراجعات: {min_reviews}–{max_reviews}</span>",
            font=dict(size=16, family="Noto Sans Arabic")
        ),
        xaxis_title="عدد التقييمات",
        yaxis_title="التقييم",
        font=dict(family="Noto Sans Arabic", size=12),
        hoverlabel=dict(
            bgcolor="#C9D2BA",
            font_color="#202020",
            font_family="Noto Sans Arabic",
            font_size=12
        ),
        margin=dict(l=10, r=10, t=70, b=50),  # Increased top margin for subtitle
        height=500,
        xaxis=dict(tickformat=",d"),
        yaxis=dict(tickformat=".1f"),
            # أضف هذين السطرين لتغيير الخلفية إلى رمادية:
    plot_bgcolor='rgba(255, 255, 255, 0)',  # خلفية منطقة الرسم

    )
    
    return fig