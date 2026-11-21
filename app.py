"""FIN 439 Project 2: interactive portfolio stability dashboard."""

import hashlib
import io
from pathlib import Path

import pandas as pd
import streamlit as st

from portfolio import (
    SLEEVES,
    CORRELATIONS,
    RESERVE_ELIGIBLE,
    search_lowest_risk,
    estimate_from_prices,
    benchmark_weights,
    covariance_matrix,
    equal_weights,
    expected_return,
    inverse_volatility_weights,
    portfolio_volatility,
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


def portfolio_comparison(sleeves, correlations, optimized, eligible,
                         return_target, reserve_target):
    covariance = covariance_matrix(sleeves, correlations)
    allocations = {
        "Equal weight": equal_weights(sleeves),
        "Inverse volatility": inverse_volatility_weights(sleeves),
    }
    if set(sleeves) == set(SLEEVES):
        allocations["40% IG bonds / 60% global equity"] = benchmark_weights(sleeves)
    elif {"AGG", "VT"} <= set(sleeves):
        allocations["40% AGG / 60% VT"] = {
            name: {"AGG": 0.40, "VT": 0.60}.get(name, 0.0)
            for name in sleeves
        }

    rows = []
    for label, weights in allocations.items():
        rows.append((
            label,
            expected_return(weights, sleeves),
            portfolio_volatility(weights, covariance, sleeves),
            sum(weights[name] for name in eligible),
            weights,
        ))
    if optimized is not None:
        rows.append((
            "Optimized", optimized["return"], optimized["volatility"],
            optimized["reserve"], optimized["weights"],
        ))

    comparison = []
    modeled_holdings = set(SLEEVES) | {"SGOV", "IEF", "AGG", "VT"}
    for label, annual_return, volatility, reserve, weights in rows:
        return_pass = annual_return >= return_target - 1e-12
        reserve_pass = reserve >= reserve_target - 1e-12
        long_only = all(weight >= -1e-12 for weight in weights.values())
        unknown_weight = sum(
            weight for name, weight in weights.items() if name not in modeled_holdings
        )
        liquidity = "Pass (assumed)" if unknown_weight <= 0.10 + 1e-12 else "Not evaluated"
        issuer = "Exempt" if unknown_weight <= 1e-12 else "Not evaluated"
        if not (return_pass and reserve_pass and long_only):
            verdict = "Fail"
        elif liquidity == "Not evaluated" or issuer == "Not evaluated":
            verdict = "Incomplete"
        else:
            verdict = "Pass (screened rules)"
        comparison.append({
            "Portfolio": label,
            "Annual return estimate": f"{annual_return:.2%}",
            "Annual volatility": f"{volatility:.2%}",
            "Reserve weight": f"{reserve:.2%}",
            "Return rule": "Pass" if return_pass else "Fail",
            "Reserve rule": "Pass" if reserve_pass else "Fail",
            "Long-only": "Pass" if long_only else "Fail",
            "Liquidity": liquidity,
            "Issuer": issuer,
            "Turnover": "Not evaluated",
            "Verdict": verdict,
        })
    if optimized is None:
        comparison.append({"Portfolio": "Optimized", "Verdict": "No feasible portfolio"})
    return pd.DataFrame(comparison).set_index("Portfolio")


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

    overview, stability, target_test, rate_signal, cost_test = st.tabs(
        ["Portfolio overview", "Window stability", "Return target test", "Point-in-time signal", "Cost stress"]
    )

    with overview:
        render_result(
            "Current portfolio",
            current,
            objective,
            reserve_min,
        )

        with st.expander("Meridian investment mandate"):
            st.markdown(
                "- **Horizon:** Seven years, with annual rebalancing.\n"
                "- **Objective:** CPI + 4% annually, net of costs, over rolling five-year "
                "periods. The default 6.50% screening threshold assumes 2.50% CPI. "
                "The displayed return estimate excludes additional implementation costs.\n"
                "- **Universe:** U.S. Treasury bills (SGOV), intermediate U.S. Treasuries "
                "(IEF), investment-grade bonds (AGG), and global equities (VT).\n"
                "- **Benchmark:** 40% AGG and 60% VT. **Risk measure:** Annualized volatility.\n"
                "- **Reserve:** Four quarterly distributions of $0.75 million on $100 million "
                "require 3% in cash or eligible government securities.\n"
                "- **Long-only:** No borrowing, short sales, or derivatives in the model.\n"
                "- **Liquidity:** At least 90% redeemable within five business days. "
                "The model assumes the four ETFs and training sleeves meet this window "
                "and credits no liquidity to unclassified tickers. Confirm execution "
                "liquidity before allocating.\n"
                "- **Issuer:** 8% maximum per nonexempt issuer. The model treats the four ETFs "
                "and training sleeves as Treasury exposures or diversified funds. "
                "Unclassified holdings require issuer data.\n"
                "- **Turnover:** Above 25% annually requires committee approval. "
                "This check requires starting holdings.\n"
                "- **Calendar-year loss language:** Requires CIO clarification."
            )

        st.subheader("Portfolio comparison")
        st.caption(
            f"Same estimates for every portfolio. Annual return minimum: {objective:.2%}. "
            f"Reserve minimum: {reserve_min:.2%}."
        )
        st.dataframe(
            portfolio_comparison(edited, active_corr, current, eligible, objective, reserve_min),
            use_container_width=True,
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

    with cost_test:
        st.subheader("Annual implementation cost stress")
        annual_cost_bp = st.number_input(
            "Additional annual portfolio cost (basis points)",
            min_value=0.0, max_value=1000.0, value=10.0, step=1.0,
        )
        annual_cost = annual_cost_bp / 10000
        st.caption(
            "A uniform annual cost is deducted from estimated return. The optimizer "
            "uses the same window, estimates, and reserve minimum as Portfolio overview."
        )
        cost_adjusted = search_lowest_risk(
            edited, active_corr, objective + annual_cost, reserve_min, eligible
        )
        cost_rows = {}
        for label, result in {
            "Keep current weights": current,
            "Reoptimize after costs": cost_adjusted,
        }.items():
            if result is None:
                cost_rows[label] = {"Net return rule": "No feasible portfolio"}
                continue
            net_return = result["return"] - annual_cost
            cost_rows[label] = {
                "Gross return": f"{result['return']:.2%}",
                "Net return": f"{net_return:.2%}",
                "Annual volatility": f"{result['volatility']:.2%}",
                "Reserve weight": f"{result['reserve']:.2%}",
                "Net return rule": "Pass" if net_return >= objective - 1e-12 else "Fail",
                **{f"{name} weight": f"{weight:.2%}" for name, weight in result["weights"].items()},
            }
        if current is not None:
            cost_budget_bp = (current["return"] - objective) * 10_000
            remaining_bp = cost_budget_bp - annual_cost_bp
            budget, remaining = st.columns(2)
            budget.metric("Break-even annual cost", f"{cost_budget_bp:.2f} bp")
            remaining.metric("Net return cushion", f"{remaining_bp:+.2f} bp")
            st.caption(
                "The break-even cost is the current allocation's gross return "
                "minus the selected target. Above that cost, the current mix "
                "fails the net return screen."
            )

        st.dataframe(pd.DataFrame.from_dict(cost_rows, orient="index"))
        if cost_adjusted is None:
            st.warning("Pause the process: no portfolio meets the net return and reserve thresholds.")
        elif current is not None and current["return"] - annual_cost < objective - 1e-12:
            st.warning("Pause the current allocation and review the reoptimized mix before proceeding.")

    with rate_signal:
        st.subheader("10-year Treasury yield signal")
        decision_date = pd.Timestamp("2026-10-05")
        st.write(f"Decision date (ALFRED vintage): {decision_date.date()}")
        signal_file = Path(__file__).with_name("dgs10_asof_2026-10-05.csv")
        if signal_file.is_file():
            vintage = pd.read_csv(signal_file, parse_dates=["observation_date"])
            rates = pd.to_numeric(vintage["DGS10_20261005"], errors="coerce")
            known = (
                vintage.assign(yield_pct=rates)
                .loc[lambda frame: frame["observation_date"] <= decision_date]
                .dropna(subset=["yield_pct"])
                .sort_values("observation_date")
            )
            if len(known) >= 6:
                earlier, latest = known.iloc[-6], known.iloc[-1]
                change_bp = round((latest["yield_pct"] - earlier["yield_pct"]) * 100, 2)
                st.metric(
                    f"Latest yield · {latest['observation_date'].date()}",
                    f"{latest['yield_pct']:.2f}%",
                    f"{change_bp:+.2f} bp over five observations",
                )
                st.write(
                    f"Comparison: {earlier['yield_pct']:.2f}% on "
                    f"{earlier['observation_date'].date()}."
                )
                if change_bp >= 10:
                    st.warning("Review IEF duration exposure before increasing its weight.")
                else:
                    st.info("No duration review triggered by this signal.")
            else:
                st.warning("The vintage needs six available observations to calculate the signal.")
        else:
            st.warning("Place dgs10_asof_2026-10-05.csv next to app.py to reproduce the signal.")

        with st.expander("Point-in-time data card"):
            st.markdown(
                "- **Source:** [ALFRED DGS10 vintage CSV]"
                "(https://alfred.stlouisfed.org/graph/alfredgraph.csv?id=DGS10&vintage_date=2026-10-05) "
                "from the St. Louis Fed, originally Federal Reserve Board H.15.\n"
                "- **Series:** Daily 10-year U.S. Treasury constant-maturity yield, "
                "quoted on an investment basis, in percent. Downloaded November 18, 2026.\n"
                "- **Availability:** Use the October 5 archive for the information cutoff. "
                "The latest available observation is October 2. Observation dates measure "
                "the yield and can precede publication. The snapshot preserves the values "
                "available in that vintage if later corrections occur.\n"
                "- **Decision rule:** A rise of at least 10 basis points over five available "
                "observations flags IEF duration for review. This is an illustrative "
                "monitoring threshold. The signal does not change optimizer inputs or weights."
            )

    st.divider()
    st.caption(
        "The optimizer searches for the lowest-volatility long-only allocation meeting "
        "the selected return and reserve thresholds. The comparison reports the "
        "additional mandate checks and their assumptions."
    )

except Exception as error:
    st.error(f"Unable to compute this portfolio: {error}")
    st.stop()


