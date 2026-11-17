"""FIN 439 Project 2: interactive portfolio stability dashboard."""

import hashlib
import io

import pandas as pd
import streamlit as st

from portfolio import (
    SLEEVES,
    CORRELATIONS,
    RESERVE_ELIGIBLE,
    search_lowest_risk,
    estimate_from_prices,
)


st.set_page_config(
    page_title="Meridian Portfolio Dashboard",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }
    h1, h2, h3 {
        color: #132d46;
    }
    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce4ed;
        border-radius: 12px;
        padding: 18px;
    }
    [data-testid="stMetricValue"] {
        color: #132d46;
    }
    [data-testid="stSidebar"] {
        background-color: #eaf0f6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Meridian Portfolio Dashboard")
st.caption("Alyson Foster · FIN 439 · Project 2")
st.caption(
    "Built with ChatGPT assistance for code and presentation. "
    "The analysis and decision are mine. For education only. "
    "This is not investment advice."
)

with st.sidebar:
    st.header("Portfolio settings")

    objective = st.number_input(
        "Minimum annual return estimate (%)",
        value=6.5,
        step=0.1,
        format="%.2f",
    ) / 100

    reserve_min = st.number_input(
        "Minimum reserve-eligible weight (%)",
        min_value=0.0,
        max_value=100.0,
        value=3.0,
        step=1.0,
        format="%.2f",
    ) / 100

    upload = st.file_uploader(
        "Upload prices.csv",
        type=["csv"],
        help="The first column contains dates. Remaining columns contain prices.",
    )

    last_36 = st.checkbox("Use last 36 months", value=False)

    st.caption(
        "Upload the repository's prices.csv to reproduce the ETF results."
    )


def maximum_change(first, second):
    if first is None or second is None:
        return None

    return 100 * max(
        abs(first["weights"][name] - second["weights"][name])
        for name in first["weights"]
    )


def render_result(label, result, return_target, reserve_target):
    st.subheader(label)

    if result is None:
        st.warning("No portfolio meets both selected thresholds.")
        return

    return_pass = result["return"] >= return_target - 1e-9
    reserve_pass = result["reserve"] >= reserve_target - 1e-9

    if return_pass and reserve_pass:
        st.success("PASS · Return and reserve thresholds")
    else:
        st.error("FAIL · One or more selected thresholds")

    first, second, third = st.columns(3)

    first.metric(
        "Annual return estimate",
        f"{result['return']:.2%}",
    )
    second.metric(
        "Annual volatility estimate",
        f"{result['volatility']:.2%}",
    )
    third.metric(
        "Reserve-eligible weight",
        f"{result['reserve']:.2%}",
    )

    allocation = pd.DataFrame(
        {
            "Asset": list(result["weights"]),
            "Weight (%)": [
                100 * weight for weight in result["weights"].values()
            ],
        }
    )

    st.vega_lite_chart(
        allocation,
        {
            "height": 190,
            "mark": {"type": "bar", "cornerRadiusEnd": 5},
            "encoding": {
                "y": {
                    "field": "Asset",
                    "type": "nominal",
                    "sort": "-x",
                    "title": None,
                },
                "x": {
                    "field": "Weight (%)",
                    "type": "quantitative",
                    "scale": {"domain": [0, 100]},
                    "title": "Portfolio weight (%)",
                },
                "color": {"value": "#147d92"},
                "tooltip": [
                    {"field": "Asset", "type": "nominal"},
                    {
                        "field": "Weight (%)",
                        "type": "quantitative",
                        "format": ".2f",
                    },
                ],
            },
        },
        use_container_width=True,
    )

    with st.expander("View exact weights and threshold checks"):
        st.dataframe(
            allocation.set_index("Asset").round(2),
            use_container_width=True,
        )
        st.write(
            f"Return threshold: {return_target:.2%} · "
            f"{'PASS' if return_pass else 'FAIL'}"
        )
        st.write(
            f"Reserve threshold: {reserve_target:.2%} · "
            f"{'PASS' if reserve_pass else 'FAIL'}"
        )


def comparison_table(results):
    rows = []

    for label, result in results.items():
        row = {
            "Scenario": label,
            "Feasible": result is not None,
        }

        if result is not None:
            row.update(
                {
                    "Return estimate (%)": 100 * result["return"],
                    "Volatility estimate (%)": 100 * result["volatility"],
                    "Reserve weight (%)": 100 * result["reserve"],
                }
            )
            row.update(
                {
                    f"{name} weight (%)": 100 * weight
                    for name, weight in result["weights"].items()
                }
            )

        rows.append(row)

    return pd.DataFrame(rows).set_index("Scenario").round(2)


try:
    if upload is None:
        baseline_sleeves = {
            name: values.copy() for name, values in SLEEVES.items()
        }
        baseline_corr = [row.copy() for row in CORRELATIONS]

        active_sleeves = {
            name: values.copy()
            for name, values in baseline_sleeves.items()
        }
        active_corr = [row.copy() for row in baseline_corr]

        source_id = "meridian"
        st.info(
            "Meridian training assumptions are loaded. "
            "Upload prices.csv to analyze SGOV, IEF, AGG, and VT."
        )
    else:
        data = upload.getvalue()

        baseline_sleeves, baseline_corr, n_all = estimate_from_prices(
            io.BytesIO(data), False
        )
        active_sleeves, active_corr, n_used = estimate_from_prices(
            io.BytesIO(data), last_36
        )

        source_id = hashlib.sha256(data).hexdigest()[:16]
        source_id += "_36" if last_36 else "_all"

        window_label = "Last 36 months" if last_36 else "All months"
        st.info(
            f"{upload.name} · {n_used} monthly returns · {window_label}"
        )
        st.caption(
            "Returns, volatility, and correlations are historical estimates. "
            "Record the data source and actual download date in your validation file."
        )

    edited = {
        name: values.copy() for name, values in active_sleeves.items()
    }
    eligible = []

    with st.expander("Adjust return estimates and reserve eligibility"):
        st.caption(
            "Changing the estimation window refreshes the return inputs. "
            "The comparisons below use unedited estimates."
        )

        for name in edited:
            return_column, reserve_column = st.columns([3, 2])

            with return_column:
                annual_return = st.number_input(
                    f"{name} annual return estimate (%)",
                    value=round(active_sleeves[name]["return"] * 100, 4),
                    step=0.1,
                    format="%.2f",
                    key=f"return_{source_id}_{name}",
                )
                edited[name]["return"] = annual_return / 100

            with reserve_column:
                default_eligible = (
                    name in RESERVE_ELIGIBLE
                    or (
                        upload is not None
                        and name.upper() in {"SGOV", "IEF"}
                    )
                )
                checked = st.checkbox(
                    f"{name} is reserve eligible",
                    value=default_eligible,
                    key=f"eligible_{name}",
                )

                if checked:
                    eligible.append(name)

    current = search_lowest_risk(
        edited, active_corr, objective, reserve_min, eligible
    )
    baseline = search_lowest_risk(
        baseline_sleeves,
        baseline_corr,
        objective,
        reserve_min,
        eligible,
    )

    overview, stability, target_test = st.tabs(
        ["Portfolio overview", "Window stability", "Return target test"]
    )

    with overview:
        render_result(
            "Current portfolio",
            current,
            objective,
            reserve_min,
        )

        difference = maximum_change(current, baseline)

        if difference is not None:
            st.caption(
                "Largest asset-weight difference from the unedited "
                f"all-months portfolio: {difference:.0f} percentage points."
            )
        else:
            st.warning(
                "The weight comparison is unavailable because at least "
                "one portfolio is infeasible."
            )

        with st.expander("Compare with unedited all-months inputs"):
            render_result(
                "Unedited all-months portfolio",
                baseline,
                objective,
                reserve_min,
            )

    with stability:
        st.subheader("How much does the estimation window matter?")

        if upload is None:
            st.info("Upload prices.csv to compare estimation windows.")
        else:
            recent_sleeves, recent_corr, recent_n = estimate_from_prices(
                io.BytesIO(data), True
            )

            all_result = search_lowest_risk(
                baseline_sleeves,
                baseline_corr,
                objective,
                reserve_min,
                eligible,
            )
            recent_result = search_lowest_risk(
                recent_sleeves,
                recent_corr,
                objective,
                reserve_min,
                eligible,
            )

            left, right = st.columns(2)

            with left:
                render_result(
                    f"All months · {n_all} returns",
                    all_result,
                    objective,
                    reserve_min,
                )

            with right:
                render_result(
                    f"Recent window · {recent_n} returns",
                    recent_result,
                    objective,
                    reserve_min,
                )

            window_change = maximum_change(all_result, recent_result)

            if window_change is not None:
                st.metric(
                    "Largest asset-weight change",
                    f"{window_change:.0f} percentage points",
                )
                st.caption(
                    "A change in historical window can alter the selected "
                    "allocation. Both windows require review before adoption."
                )
            else:
                st.warning(
                    "At least one window has no feasible portfolio."
                )

    with target_test:
        st.subheader("What changes when the return target rises?")
        st.caption(
            "Compares 6.50% and 7.00% targets using unedited all-months "
            "inputs and the current reserve eligibility and minimum."
        )

        lower_target = search_lowest_risk(
            baseline_sleeves,
            baseline_corr,
            0.065,
            reserve_min,
            eligible,
        )
        higher_target = search_lowest_risk(
            baseline_sleeves,
            baseline_corr,
            0.07,
            reserve_min,
            eligible,
        )

        left, right = st.columns(2)

        with left:
            render_result(
                "6.50% target",
                lower_target,
                0.065,
                reserve_min,
            )

        with right:
            render_result(
                "7.00% target",
                higher_target,
                0.07,
                reserve_min,
            )

        target_comparison = comparison_table(
            {
                "6.50% target": lower_target,
                "7.00% target": higher_target,
            }
        )

        st.dataframe(target_comparison, use_container_width=True)

        st.download_button(
            "Download target comparison",
            data=target_comparison.to_csv().encode("utf-8"),
            file_name="portfolio-target-comparison.csv",
            mime="text/csv",
        )

    st.divider()
    st.caption(
        "The displayed pass/fail checks evaluate the selected return and "
        "reserve thresholds. Review the remaining mandate rules, data "
        "limitations, costs, and decision conditions in the project records."
    )

except Exception as error:
    st.error(f"Unable to compute this portfolio: {error}")
    st.stop()
