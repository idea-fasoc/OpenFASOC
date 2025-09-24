import re
import ast
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RANK_RE = re.compile(r"^RANK\s+(\d+):\s+(\S+)\s+\(ID:\s*(\d+)\)")
SEP_RE = re.compile(r"^-{5,}")


def safe_parse_value(raw: str) -> Any:
    s = raw.strip()
    # try: literal structures first
    try:
        return ast.literal_eval(s)
    except Exception:
        pass
    # try: numeric types
    try:
        if "." in s or "e" in s.lower():
            return float(s)
        return int(s)
    except Exception:
        pass
    # booleans
    if s in {"True", "False"}:
        return s == "True"
    return s


def parse_scores_txt(scores_path: Path) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    with scores_path.open("r", encoding="utf-8", errors="ignore") as f:
        in_block = False
        current: Dict[str, Any] = {}
        section: str = ""
        for line in f:
            line = line.rstrip("\n")
            if not in_block:
                m = RANK_RE.match(line)
                if m:
                    # start new block
                    in_block = True
                    current = {}
                    current["rank"] = int(m.group(1))
                    current["component_name_header"] = m.group(2)
                    current["id"] = int(m.group(3))
                    section = ""
                else:
                    continue
            else:
                # inside a block
                if SEP_RE.match(line):
                    # end of block
                    rows.append(current)
                    in_block = False
                    current = {}
                    section = ""
                    continue
                if not line.strip():
                    continue
                if RANK_RE.match(line):
                    # If a rank header appears without a separator, close previous block
                    if current:
                        rows.append(current)
                    m = RANK_RE.match(line)
                    current = {
                        "rank": int(m.group(1)),
                        "component_name_header": m.group(2),
                        "id": int(m.group(3)),
                    }
                    section = ""
                    continue

                # detect section headers like "Individual Scores:" or "Raw Data:"
                if line.strip().endswith(":") and ":" not in line.strip()[:-1]:
                    section = line.strip()[:-1]
                    continue

                # parse key: value lines
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    parsed = safe_parse_value(value)
                    # namespace keys by section to avoid collisions if needed
                    if section in {"Individual Scores", "Raw Data"}:
                        namespaced_key = key
                    else:
                        namespaced_key = key
                    current[namespaced_key] = parsed

        # flush last block if file didn't end with separator
        if in_block and current:
            rows.append(current)

    df = pd.DataFrame(rows)

    # Derived features
    with np.errstate(divide="ignore", invalid="ignore"):
        df["resistance_density"] = df["total_resistance_ohms"] / df["area_um2"]
        df["capacitance_density"] = df["total_capacitance_farads"] / df["area_um2"]
    df["symmetry_mean"] = (df.get("symmetry_horizontal", np.nan) + df.get("symmetry_vertical", np.nan)) / 2.0

    # Convenient log features (guard zeros/negatives)
    def safe_log10(x: pd.Series) -> pd.Series:
        return np.log10(x.where(x > 0))

    df["log10_resistance_density"] = safe_log10(df["resistance_density"]) 
    df["log10_capacitance_density"] = safe_log10(df["capacitance_density"]) 

    # Normalize booleans
    for col in ["success", "drc_pass", "lvs_pass"]:
        if col in df.columns:
            df[col] = df[col].astype("boolean")

    return df


def ensure_outdir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_hist(
    ax,
    series: pd.Series,
    title: str,
    bins: int = 50,
    logy: bool = False,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = "Count",
    formula: Optional[str] = None,
):
    data = series.dropna().values
    ax.hist(data, bins=bins, color="#4C78A8", alpha=0.85)
    ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if logy:
        ax.set_yscale("log")
    if formula:
        ax.text(
            0.02,
            0.98,
            formula,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.2"),
        )


def make_plots(df: pd.DataFrame, outdir: Path) -> None:
    ensure_outdir(outdir)

    # Save the parsed data for future analysis
    parsed_csv = outdir / "scores_parsed.csv"
    df.to_csv(parsed_csv, index=False)

    # 1) Score histograms (each saved individually)
    score_cols = [
        "Final Score",
        "Resistance Score",
        "Capacitance Score",
        "Symmetry Score",
        "Verification Score",
    ]
    # Detailed descriptions sourced from experiments/weights.py logic
    w_str = "w=0.99"
    score_desc_map: Dict[str, str] = {
        "Final Score": (
            "final_score = resistance_score + capacitance_score + symmetry_score + verification_score\n"
            "If verification_score == 0 (HARDSTOP), all components and final_score are set to 0.\n"
            "Interpretation: Higher total indicates better overall performance across components."
        ),
        "Resistance Score": (
            "raw_pos = exp(-w*(median_R - R)/IQR_R), raw_neg = exp(-w*(R - median_R)/IQR_R)\n"
            "resistance_score = 0.5 + 0.5*(raw_pos/max_pos) if R<=median_R else 0.5*(-raw_neg/max_neg)\n"
        ),
        "Capacitance Score": (
            "raw_pos = exp(-w*(median_C - C)/IQR_C), raw_neg = exp(-w*(C - median_C)/IQR_C)\n"
            "capacitance_score = 0.5 + 0.5*(raw_pos/max_pos) if C<=median_C else 0.5*(-raw_neg/max_neg)\n"
        ),
        "Symmetry Score": (
            "symmetry_score = 0.5*(symmetry_horizontal + symmetry_vertical)\n"
            "Interpretation: Average of horizontal and vertical symmetry measures; higher suggests better symmetry."
        ),
        "Verification Score": (
            "verification_score = max(0, 1 - total_errors/threshold), threshold=50\n"
            "Errors are derived from DRC/LVS reports when those checks fail.\n"
            "If score == 1 it's a HARDPASS; if score == 0 it triggers HARDSTOP in the final score."
        ),
    }
    for col in score_cols:
        if col in df.columns:
            fig, ax = plt.subplots(figsize=(7, 5))
            plot_hist(
                ax,
                df[col],
                col,
                bins=50,
                logy=False,
                xlabel=col,
                ylabel="Count",
                formula=score_desc_map.get(col, col),
            )
            fname = f"hist_{col.lower().replace(' ', '_')}.png"
            fig.tight_layout()
            fig.savefig(outdir / fname, dpi=220)
            plt.close(fig)

    # 2) Feature histograms (each saved individually)
    # Resistance density
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_hist(
        ax,
        df["resistance_density"],
        "Resistance Density",
        bins=60,
        logy=True,
        xlabel="resistance_density (ohms per µm²)",
        ylabel="Count",
        formula=(
            "resistance_density = total_resistance_ohms / area_um2\n"
            "Interpretation: Lower values indicate lower resistive parasitics per unit area.\n"
            "Log-scaled y-axis to emphasize tail behavior."
        ),
    )
    fig.tight_layout()
    fig.savefig(outdir / "hist_resistance_density.png", dpi=220)
    plt.close(fig)

    # Capacitance density
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_hist(
        ax,
        df["capacitance_density"],
        "Capacitance Density",
        bins=60,
        logy=True,
        xlabel="capacitance_density (farads per µm²)",
        ylabel="Count",
        formula=(
            "capacitance_density = total_capacitance_farads / area_um2\n"
            "Interpretation: Lower values indicate lower capacitive parasitics per unit area.\n"
            "Log-scaled y-axis to emphasize tail behavior."
        ),
    )
    fig.tight_layout()
    fig.savefig(outdir / "hist_capacitance_density.png", dpi=220)
    plt.close(fig)

    # Execution time
    if "execution_time" in df.columns:
        fig, ax = plt.subplots(figsize=(7, 5))
        plot_hist(
            ax,
            df["execution_time"],
            "Execution Time (s)",
            bins=60,
            logy=True,
            xlabel="execution_time (seconds)",
            ylabel="Count",
            formula=(
                "execution_time = parsed runtime in seconds\n"
                "Interpretation: Distribution of end-to-end run times (log-scaled y-axis)."
            ),
        )
        fig.tight_layout()
        fig.savefig(outdir / "hist_execution_time.png", dpi=220)
        plt.close(fig)

    # Symmetry mean
    fig, ax = plt.subplots(figsize=(7, 5))
    plot_hist(
        ax,
        df["symmetry_mean"],
        "Mean Symmetry",
        bins=60,
        logy=False,
        xlabel="symmetry_mean",
        ylabel="Count",
        formula=(
            "symmetry_mean = (symmetry_horizontal + symmetry_vertical) / 2\n"
            "Interpretation: Average of the two symmetry measures; higher suggests better overall symmetry."
        ),
    )
    fig.tight_layout()
    fig.savefig(outdir / "hist_symmetry_mean.png", dpi=220)
    plt.close(fig)

    # 3) Scatter: density vs density colored by Final Score
    if "Final Score" in df.columns:
        fig, ax = plt.subplots(figsize=(8, 6))
        x = df["log10_resistance_density"]
        y = df["log10_capacitance_density"]
        c = df["Final Score"]
        sc = ax.scatter(x, y, c=c, cmap="viridis", s=8, alpha=0.7)
        ax.set_xlabel("log10(resistance_density)")
        ax.set_ylabel("log10(capacitance_density)")
        ax.set_title("Density Map colored by Final Score")
        cb = fig.colorbar(sc, ax=ax)
        cb.set_label("Final Score")
        # Add formulas used on this plot
        formula_text = (
            "resistance_density = total_resistance_ohms / area_um2\n"
            "capacitance_density = total_capacitance_farads / area_um2\n"
            "log10_resistance_density = log10(resistance_density)\n"
            "log10_capacitance_density = log10(capacitance_density)\n"
            "Color = Final Score (higher indicates better overall performance).\n"
            "Lower values along each axis indicate lower parasitic densities."
        )
        ax.text(
            0.02,
            0.98,
            formula_text,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.2"),
        )
        fig.tight_layout()
        fig.savefig(outdir / "scatter_density_vs_density_colored_final.png", dpi=220)
        plt.close(fig)

    # 4) Pairwise scatter matrix of key features
    from pandas.plotting import scatter_matrix

    pair_cols = [
        "log10_resistance_density",
        "log10_capacitance_density",
        "symmetry_mean",
        "Final Score",
    ]
    existing_pair_cols = [c for c in pair_cols if c in df.columns]
    if len(existing_pair_cols) >= 2:
        fig = plt.figure(figsize=(10, 10))
        axarr = scatter_matrix(df[existing_pair_cols].dropna(), figsize=(10, 10), diagonal="hist", alpha=0.6, color="#4C78A8")
        # rotate x tick labels for readability
        for ax in axarr.ravel():
            for tick in ax.get_xticklabels():
                tick.set_rotation(45)
        plt.suptitle("Scatter Matrix of Key Features")
        # Provide formulas for derived features used in the matrix
        matrix_formula_text = (
            "resistance_density = total_resistance_ohms / area_um2\n"
            "capacitance_density = total_capacitance_farads / area_um2\n"
            "log10_resistance_density = log10(resistance_density)\n"
            "log10_capacitance_density = log10(capacitance_density)\n"
            "symmetry_mean = (symmetry_horizontal + symmetry_vertical) / 2\n"
            "Diagonal: histograms; off-diagonal: scatter. Helps visualize pairwise relationships."
        )
        fig.text(
            0.01,
            0.01,
            matrix_formula_text,
            va="bottom",
            ha="left",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.2"),
        )
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(outdir / "scatter_matrix_key_features.png", dpi=200)
        plt.close(fig)

    # 5) Correlation heatmap using matplotlib
    corr_cols = [
        "Final Score",
        "Resistance Score",
        "Capacitance Score",
        "Symmetry Score",
        "Verification Score",
        "resistance_density",
        "capacitance_density",
        "symmetry_mean",
        "execution_time",
    ]
    corr_cols = [c for c in corr_cols if c in df.columns]
    if len(corr_cols) >= 2:
        corr = df[corr_cols].corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr_cols)))
        ax.set_yticks(range(len(corr_cols)))
        ax.set_xticklabels(corr_cols, rotation=45, ha="right")
        ax.set_yticklabels(corr_cols)
        ax.set_xlabel("Features")
        ax.set_ylabel("Features")
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label("Pearson correlation (\u03c1)")
        ax.set_title("Correlation Heatmap")
        # Add Pearson correlation formula and interpretation
        heatmap_formula_text = (
            "Pearson \u03c1(X,Y) = cov(X,Y) / (\u03c3_X \u03c3_Y)\n"
            "Interpretation: values near 1 = strong positive, near -1 = strong negative, near 0 = weak linear relationship."
        )
        fig.text(
            0.01,
            0.01,
            heatmap_formula_text,
            va="bottom",
            ha="left",
            fontsize=9,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none", boxstyle="round,pad=0.2"),
        )
        fig.tight_layout()
        fig.savefig(outdir / "corr_heatmap.png", dpi=200)
        plt.close(fig)


def main():
    base_dir = Path(__file__).resolve().parent
    # Look for scores.txt in current directory first, then in base_dir
    scores_path = Path("scores.txt")
    if not scores_path.exists():
        scores_path = base_dir / "scores.txt"
    outdir = Path("eda")
    ensure_outdir(outdir)
    if not scores_path.exists():
        raise SystemExit(f"scores.txt not found at: {scores_path}")

    print("Parsing scores.txt ...")
    df = parse_scores_txt(scores_path)
    print(f"Parsed {len(df)} samples with {df.shape[1]} columns")

    print("Generating plots ...")
    make_plots(df, outdir)
    print(f"Saved outputs to {outdir}")


if __name__ == "__main__":
    main()






