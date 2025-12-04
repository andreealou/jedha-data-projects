import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Getaround – Delay & Pricing Dashboard",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------------------------
# Data loading & preparation – Delay Analysis
# --------------------------------------------------
@st.cache_data
def load_delay_data(path: str = "get_around_delay_analysis.xlsx"):
    df = pd.read_excel(path)
    return df


def build_delay_tables(df: pd.DataFrame):
    """Build df_delay and df_chain + 'problematic' flag."""
    df_delay = df[
        (df["state"] == "ended")
        & (df["delay_at_checkout_in_minutes"].notna())
    ].copy()

    # Merge with previous rental to get its delay
    df_merge = df_delay.merge(
        df_delay[["rental_id", "delay_at_checkout_in_minutes"]],
        left_on="previous_ended_rental_id",
        right_on="rental_id",
        how="left",
        suffixes=("", "_previous")
    )

    # Keep only rentals that have a previous rental < 12h
    df_chain = df_merge[
        df_merge["delay_at_checkout_in_minutes_previous"].notna()
    ].copy()

    # Problematic cases: previous delay > available gap
    df_chain["problematic"] = (
        df_chain["delay_at_checkout_in_minutes_previous"]
        > df_chain["time_delta_with_previous_rental_in_minutes"]
    )

    return df_delay, df_chain


def simulate_thresholds(df_chain: pd.DataFrame, thresholds):
    """Return a DataFrame with % of conflicts resolved for each threshold."""
    df_prob = df_chain[df_chain["problematic"] == True].copy()
    total = len(df_prob)

    rows = []
    for t in thresholds:
        solved = (df_prob["delay_at_checkout_in_minutes_previous"] <= t).sum()
        rows.append({
            "threshold_minutes": t,
            "conflicts_resolved": solved,
            "conflicts_total": total,
            "percent_resolved": (solved / total * 100) if total > 0 else 0
        })

    return pd.DataFrame(rows)


# --------------------------------------------------
# Data & model loading – Pricing Prediction
# --------------------------------------------------
@st.cache_data
def load_pricing_raw(path: str = "get_around_pricing_project.csv"):
    """
    Load the original pricing dataset (before encoding).
    Used to populate dropdowns in the Pricing tab.
    """
    df = pd.read_csv(path)
    return df


@st.cache_resource
def load_pricing_model_and_features(
    model_path: str = "getaround_pricing_model.joblib",
    template_path: str = "get_around_pricing_project_model.csv"
):
    """
    Load the trained model (joblib) and the feature columns
    from the encoded template CSV used during training.
    """
    model = joblib.load(model_path)
    df_template = pd.read_csv(template_path)
    feature_columns = df_template.drop(columns=["rental_price_per_day"]).columns
    return model, feature_columns


# --------------------------------------------------
# Main app
# --------------------------------------------------
def main():
    st.title("🚗 Getaround – Delay & Pricing Dashboard")

    st.markdown(
        """
This dashboard has two main objectives:

1. **Delay analysis** – understand late checkouts and their impact on back-to-back rentals.  
2. **Pricing prediction** – estimate a daily rental price based on car features.
"""
    )

    # ====== Load data ======
    df = load_delay_data()
    df_delay, df_chain = build_delay_tables(df)

    # Pricing data & model
    df_pricing_raw = load_pricing_raw()
    pricing_model, feature_columns = load_pricing_model_and_features()

    # ====== Sidebar filters (Delay Analysis) ======
    st.sidebar.header("⚙️ Filters (Delay Analysis)")

    checkin_types = sorted(df["checkin_type"].dropna().unique())
    selected_checkins = st.sidebar.multiselect(
        "Check-in type",
        options=checkin_types,
        default=checkin_types
    )

    st.sidebar.markdown("<hr style='margin-top:20px;margin-bottom:10px;'>", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<small style='color:#666;'>ℹ️ The slider below only affects the "
        "<b>Conflicts & Thresholds</b> tab.</small>",
        unsafe_allow_html=True
    )

    chosen_threshold = st.sidebar.slider(
        "Minimum time buffer between rentals (minutes)",
        min_value=0,
        max_value=180,
        value=60,
        step=15
    )

    # Apply check-in type filter
    if selected_checkins:
        mask_all = df["checkin_type"].isin(selected_checkins)
        mask_delay = df_delay["checkin_type"].isin(selected_checkins)
        mask_chain = df_chain["checkin_type"].isin(selected_checkins)

        df_f = df[mask_all].copy()
        df_delay_f = df_delay[mask_delay].copy()
        df_chain_f = df_chain[mask_chain].copy()
    else:
        df_f = df.copy()
        df_delay_f = df_delay.copy()
        df_chain_f = df_chain.copy()

    # ====== Global KPIs (Delay part) ======
    total_rentals = len(df_f)
    total_cars = df_f["car_id"].nunique()
    total_chains = len(df_chain_f)
    total_conflicts = int(df_chain_f["problematic"].sum())

    rate_chain_overall = total_chains / total_rentals * 100 if total_rentals > 0 else 0
    rate_conflict_overall = total_conflicts / total_rentals * 100 if total_rentals > 0 else 0
    rate_conflict_on_chains = (
        total_conflicts / total_chains * 100 if total_chains > 0 else 0
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total rentals", f"{total_rentals:,}".replace(",", " "))
    kpi2.metric("Total cars", f"{total_cars}")
    kpi3.metric(
        "Chain rentals (<12h gap)",
        f"{total_chains} ({rate_chain_overall:.1f}%)"
    )
    kpi4.metric(
        "Actual conflicts",
        f"{total_conflicts} ({rate_conflict_overall:.2f}% overall, {rate_conflict_on_chains:.1f}% on chains)"
    )

    st.markdown("---")

    # ====== Tabs ======
    tab_overview, tab_outcomes, tab_conf_thresholds, tab_conf_scatter, tab_pricing = st.tabs([
        "🔍 Overview",
        "⏱️ Checkout Outcomes",
        "🔥 Conflicts & Thresholds",
        "📈 Visualization of actual conflicts",
        "💰 Pricing prediction",
    ])

    # --------------------------------------------------
    # TAB 1 — OVERVIEW
    # --------------------------------------------------
    with tab_overview:
        st.subheader("🔍 Overview")

        col_text, _ = st.columns([2, 1])
        with col_text:
            st.markdown(
                """
- Most rentals are done via **Mobile check-in**.  
- Only a small share of the fleet belongs to **tight chains (<12h)**.  
- Among those chains, a significant portion results in **true conflicts**  
  (the next driver cannot start on time).
"""
            )
            st.markdown("**Key Product questions:**")
            st.markdown(
                """
1. What **minimum buffer** should be enforced between rentals?  
2. Should this apply to **all cars**, or only **Connect**?  
3. What is the **trade-off** between reducing conflicts and preserving **owner revenue**?
"""
            )

        st.markdown("### Mix of reservations and rental states")

        pie_col1, pie_col2 = st.columns(2)

        # Pie chart 1 — Check-in type
        with pie_col1:
            counts_ci = df_f["checkin_type"].value_counts()
            labels_ci = counts_ci.index
            sizes_ci = counts_ci.values

            if len(sizes_ci) == 0:
                st.info("No reservations for current filters.")
            else:
                fig_ci, ax_ci = plt.subplots(figsize=(2.5, 2.5))
                ax_ci.pie(
                    sizes_ci,
                    labels=labels_ci,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#B01AA7", "#CFC6B9"],
                    textprops={"fontsize": 10}
                )
                ax_ci.axis("equal")
                ax_ci.set_title("By check-in type", fontsize=12, fontweight="bold")
                st.pyplot(fig_ci)

        # Pie chart 2 — Rental state
        with pie_col2:
            state_counts = df_f["state"].value_counts()
            labels_st = state_counts.index
            sizes_st = state_counts.values

            if len(sizes_st) == 0:
                st.info("No rentals for current filters.")
            else:
                fig_st, ax_st = plt.subplots(figsize=(2.5, 2.5))
                ax_st.pie(
                    sizes_st,
                    labels=labels_st,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#B01AA7", "#FFB347"],
                    textprops={"fontsize": 10}
                )
                ax_st.axis("equal")
                ax_st.set_title("By rental state", fontsize=12, fontweight="bold")
                st.pyplot(fig_st)

    # --------------------------------------------------
    # TAB 2 — CHECKOUT OUTCOMES
    # --------------------------------------------------
    with tab_outcomes:
        st.subheader("⏱️ Checkout Outcomes (Early / On-time / Late)")

        df_delay_local = df_delay_f.copy()
        df_delay_local = df_delay_local[df_delay_local["delay_at_checkout_in_minutes"].notna()]

        if len(df_delay_local) == 0:
            st.info("No ended rentals with delay info for selected filters.")
        else:
            early = (df_delay_local["delay_at_checkout_in_minutes"] < 0).sum()
            on_time = (df_delay_local["delay_at_checkout_in_minutes"] == 0).sum()
            late = (df_delay_local["delay_at_checkout_in_minutes"] > 0).sum()

            categories = ["Early returns", "On-time", "Late returns"]
            values = [early, on_time, late]

            total = sum(values)
            percentages = [v / total * 100 for v in values]

            # Sort descending (Late first) like notebook
            sorted_data = sorted(
                zip(categories, values, percentages),
                key=lambda x: x[1],
                reverse=True
            )
            labels, sorted_values, sorted_perc = zip(*sorted_data)

            fig, ax = plt.subplots(figsize=(8, 5))
            bars = ax.bar(
                labels,
                sorted_values,
                color=["#E93E3E", "#90D6C6", "#FFD723"],
                edgecolor="black"
            )

            ax.set_title("Checkout Outcomes", fontsize=18, fontweight="bold", color="#B01AA7")
            ax.set_ylabel("Number of rentals")
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            ax.set_ylim(0, 11000)

            for bar, value, pct in zip(bars, sorted_values, sorted_perc):
                height = bar.get_height()
                offset = 0.03 * height + 50
                if value < 500:
                    offset = 300
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + offset,
                    f"{value} ({pct:.1f}%)",
                    ha="center",
                    fontsize=12
                )

            st.pyplot(fig)

    # --------------------------------------------------
    # TAB 3 — CONFLICTS & THRESHOLDS
    # --------------------------------------------------
    with tab_conf_thresholds:
        st.subheader("🔥 Conflicts & Thresholds")

        if len(df_chain_f) == 0:
            st.info("No back-to-back rentals for current filters.")
        else:
            thresholds = list(range(0, 181, 15))
            df_sim = simulate_thresholds(df_chain_f, thresholds)

            # KPI for chosen threshold
            row_focus = df_sim[df_sim["threshold_minutes"] == chosen_threshold].iloc[0]
            c1, c2 = st.columns(2)

            c1.metric(
                f"Conflicts resolved at {chosen_threshold} min",
                f"{int(row_focus['conflicts_resolved'])} / {int(row_focus['conflicts_total'])}",
                f"{row_focus['percent_resolved']:.1f}%"
            )
            c2.markdown(
                f"""
With a **{chosen_threshold}-minute buffer**,  
approximately **{row_focus['percent_resolved']:.1f}%** of all conflicts would be prevented.
"""
            )

            # Curve (only violet line + annotations)
            x = df_sim["threshold_minutes"]
            p = df_sim["percent_resolved"]
            c = df_sim["conflicts_resolved"]

            fig2, ax1 = plt.subplots(figsize=(10, 6))

            ax1.plot(
                x,
                p,
                "o-",
                color="#B01AA7",
                markersize=10,
                markerfacecolor="white",
                markeredgewidth=2,
                linewidth=3,
            )

            ax1.set_xlabel("Threshold (minutes)", fontsize=12)
            ax1.set_ylabel("Conflicts resolved (%)", fontsize=12, color="#B01AA7")
            ax1.grid(alpha=0.3, linestyle="--")
            ax1.set_ylim(-10, p.max() + 15)
            ax1.set_xticks(thresholds)

            ax2 = ax1.twinx()
            ax2.set_ylabel("Resolved conflicts (count)", fontsize=12, color="#40C1AC")
            ax2.tick_params(axis="y", labelcolor="#40C1AC")
            ax2.set_ylim(-10, c.max() + 15)

            for xi, yp, yc in zip(x, p, c):
                ax1.text(
                    xi,
                    yp + 4,
                    f"{yp:.0f}%",
                    ha="center",
                    fontsize=11,
                    color="#B01AA7"
                )
                ax1.text(
                    xi,
                    yp - 6,
                    str(int(yc)),
                    ha="center",
                    fontsize=10,
                    color="#40C1AC"
                )

            ax1.set_title("Impact of minimum gap on conflict resolution",
                          fontsize=16, fontweight="bold", color="#B01AA7")
            st.pyplot(fig2)

    # --------------------------------------------------
    # TAB 4 — ACTUAL CONFLICTS (SCATTER)
    # --------------------------------------------------
    with tab_conf_scatter:
        st.subheader("📈 Visualization of actual conflicts")

        if len(df_chain_f) == 0:
            st.info("No back-to-back rentals for selected filters.")
        else:
            safe = df_chain_f[df_chain_f["problematic"] == False]
            prob = df_chain_f[df_chain_f["problematic"] == True]

            fig3, ax3 = plt.subplots(figsize=(8, 5))
            ax3.scatter(
                safe["time_delta_with_previous_rental_in_minutes"],
                safe["delay_at_checkout_in_minutes_previous"],
                color="#B01AA7",
                alpha=0.5,
                label="Non-conflicting"
            )
            ax3.scatter(
                prob["time_delta_with_previous_rental_in_minutes"],
                prob["delay_at_checkout_in_minutes_previous"],
                color="red",
                alpha=0.7,
                label="Conflicting"
            )

            max_gap = df_chain_f["time_delta_with_previous_rental_in_minutes"].max()
            ax3.plot(
                [0, max_gap],
                [0, max_gap],
                linestyle="--",
                color="black",
                linewidth=1.5,
                label="Delay = Gap"
            )

            ax3.set_xlabel("Available gap before next rental (minutes)")
            ax3.set_ylabel("Previous checkout delay (minutes)")
            ax3.set_title("Conflicts caused by late previous checkouts",
                          fontsize=14, fontweight="bold", color="#B01AA7")
            ax3.grid(alpha=0.3)
            ax3.legend()
            st.pyplot(fig3)

            st.markdown(
                """
Red points represent **true conflicts**:  
the previous driver's delay was **longer** than the gap before the next rental.  

The diagonal line shows the boundary between **safe** and **conflicting** cases.
"""
            )

    # --------------------------------------------------
    # TAB 5 — PRICING PREDICTION
    # --------------------------------------------------
    with tab_pricing:
        st.subheader("💰 Pricing prediction")

        st.markdown(
            """
Use this tab to estimate a **daily rental price** based on car characteristics.  
The model is the same Random Forest that was trained and tracked with **MLflow**.
"""
        )

        # Build sensible defaults from the pricing dataset
        mileage_min = int(df_pricing_raw["mileage"].min())
        mileage_max = int(df_pricing_raw["mileage"].max())
        mileage_default = int(df_pricing_raw["mileage"].median())

        power_min = int(df_pricing_raw["engine_power"].min())
        power_max = int(df_pricing_raw["engine_power"].max())
        power_default = int(df_pricing_raw["engine_power"].median())

        col1, col2 = st.columns(2)

        with col1:
            model_key = st.selectbox("Model", sorted(df_pricing_raw["model_key"].unique()))
            mileage = st.number_input(
                "Mileage",
                min_value=mileage_min,
                max_value=mileage_max,
                value=mileage_default,
                step=1000
            )
            engine_power = st.number_input(
                "Engine power (hp)",
                min_value=power_min,
                max_value=power_max,
                value=power_default,
                step=10
            )
            fuel = st.selectbox("Fuel", sorted(df_pricing_raw["fuel"].unique()))
            paint_color = st.selectbox("Paint color", sorted(df_pricing_raw["paint_color"].unique()))
            car_type = st.selectbox("Car type", sorted(df_pricing_raw["car_type"].unique()))

        with col2:
            private_parking_available = st.checkbox("Private parking available", value=True)
            has_gps = st.checkbox("GPS", value=True)
            has_air_conditioning = st.checkbox("Air conditioning", value=False)
            automatic_car = st.checkbox("Automatic transmission", value=False)
            has_getaround_connect = st.checkbox("Getaround Connect", value=True)
            has_speed_regulator = st.checkbox("Speed regulator (cruise control)", value=True)
            winter_tires = st.checkbox("Winter tires", value=False)

        if st.button("Predict daily price"):
            # Build raw input as a one-row DataFrame
            raw_dict = {
                "model_key": model_key,
                "mileage": mileage,
                "engine_power": engine_power,
                "fuel": fuel,
                "paint_color": paint_color,
                "car_type": car_type,
                "private_parking_available": private_parking_available,
                "has_gps": has_gps,
                "has_air_conditioning": has_air_conditioning,
                "automatic_car": automatic_car,
                "has_getaround_connect": has_getaround_connect,
                "has_speed_regulator": has_speed_regulator,
                "winter_tires": winter_tires,
            }
            df_input = pd.DataFrame([raw_dict])

            # One-hot encode with same strategy as training
            df_input_enc = pd.get_dummies(df_input, drop_first=False)

            # Create a fully-aligned feature row (55 columns)
            X_input = pd.DataFrame(
                data=np.zeros((1, len(feature_columns))),
                columns=feature_columns
            )

            for col in df_input_enc.columns:
                if col in X_input.columns:
                    X_input.loc[0, col] = df_input_enc.loc[0, col]

            # Predict
            pred = pricing_model.predict(X_input)[0]

            st.success(f"Estimated daily price: **{pred:.0f} €**")

            st.markdown(
                """
_This prediction is based on the same feature engineering and Random Forest model  
that were tracked in MLflow during the pricing optimization phase._
"""
            )


# --------------------------------------------------
# Run main
# --------------------------------------------------
if __name__ == "__main__":
    main()
