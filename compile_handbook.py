#!/usr/bin/env python3
"""
Compile the Privacy Researcher's Handbook into a professional PDF.

Generates forensic graphs with matplotlib (dark/light theme),
assembles all chapters into a single HTML document with professional
CSS styling, and converts to PDF via WeasyPrint.

Usage:
    python3 compile_handbook.py
    python3 compile_handbook.py --no-pdf
    python3 compile_handbook.py --output custom.pdf
    python3 compile_handbook.py --no-graphs
"""

import os, sys, re, subprocess, argparse
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
BOOK_DIR     = Path(__file__).parent
OUTPUT_DIR   = BOOK_DIR / "docs"
GRAPH_DIR    = OUTPUT_DIR / "graphs"
HTML_FILE    = OUTPUT_DIR / "handbook.html"
PDF_FILE     = OUTPUT_DIR / "Privacy_Researchers_Handbook.pdf"

DARK_BG      = "#0d1117"
DARKER_BG    = "#090c10"
CARD_BG      = "#161b22"
BORDER_CLR   = "#30363d"
TEXT_CLR     = "#e6edf3"
MUTED_CLR    = "#8b949e"
ACCENT_CYAN  = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_ORANGE= "#ff6b35"
ACCENT_PURPLE= "#7c3aed"
ACCENT_RED   = "#ff3333"
HEADER_FONT  = "'SF Mono', 'Fira Code', 'JetBrains Mono', 'Consolas', monospace"
BODY_FONT    = "'Inter', -apple-system, 'Segoe UI', 'Helvetica Neue', sans-serif"

GRAPH_COLORS = [ACCENT_CYAN, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE, "#ff6b6b", "#ffd93d"]

VERSION = "3.1"

# ── Dependencies ────────────────────────────────────────────────────────────
# Requires: matplotlib, markdown, numpy, weasyprint
#   pip install -r requirements.txt

# WeasyPrint on macOS needs Homebrew's pango/glib libraries
_homebrew = "/opt/homebrew/lib"
if sys.platform == "darwin" and os.path.isdir(_homebrew):
    os.environ.setdefault("DYLD_LIBRARY_PATH",
                          _homebrew + ":" + os.environ.get("DYLD_LIBRARY_PATH", ""))

PDF_AVAILABLE = False
try:
    import weasyprint
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx
import markdown as md_lib

# ── Matplotlib dark theme ──────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    DARK_BG,
    "axes.edgecolor":    BORDER_CLR,
    "axes.labelcolor":   TEXT_CLR,
    "axes.grid":         True,
    "grid.alpha":        0.15,
    "grid.color":        BORDER_CLR,
    "text.color":        TEXT_CLR,
    "xtick.color":       MUTED_CLR,
    "ytick.color":       MUTED_CLR,
    "legend.facecolor":  CARD_BG,
    "legend.edgecolor":  BORDER_CLR,
    "legend.labelcolor": TEXT_CLR,
    "savefig.facecolor": DARK_BG,
    "savefig.bbox":      "tight",
    "font.family":       "sans-serif",
    "font.size":         11,
})

def fig_save(fig, name):
    path = GRAPH_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  [\u2713] {name}")
    return path

# ── Graph generators ───────────────────────────────────────────────────────

def graph1_attack_surface():
    layers  = ["Cellular", "Wi-Fi", "ISP", "Application", "Physical\nCo-location", "Legal\nAccess"]
    phone_a = [10, 1, 1, 3, 4, 10]
    phone_b = [2, 8, 10, 4, 6, 8]
    computer= [1, 6, 10, 6, 3, 8]

    x = np.arange(len(layers))
    w = 0.25
    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(x - w, phone_a, w, label="Phone A (Flip)",     color=ACCENT_CYAN,   edgecolor="none", alpha=0.9)
    bars2 = ax.bar(x,     phone_b, w, label="Phone B (GrapheneOS)", color=ACCENT_GREEN,  edgecolor="none", alpha=0.9)
    bars3 = ax.bar(x + w, computer,w, label="Computer",            color=ACCENT_ORANGE, edgecolor="none", alpha=0.9)

    for bar in bars1 + bars2 + bars3:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.3, str(h),
                ha="center", va="bottom", fontsize=8, color=MUTED_CLR)

    ax.set_xticks(x)
    ax.set_xticklabels(layers, fontsize=10)
    ax.set_ylabel("Data Exposure Index (0\u201310)", color=TEXT_CLR, fontsize=11)
    ax.set_title("Attack Surface: Data Exposure by Device & Layer", color=TEXT_CLR,
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylim(0, 13)
    ax.legend(framealpha=0.2, fontsize=10, loc="upper right")
    ax.text(0.5, -0.15, "Higher = more forensic data leaked to potential adversaries",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph1_attack_surface.png")

def graph2_cellular_accuracy():
    years      = [2015, 2018, 2021, 2024, 2026, 2029]
    cell_id    = [5000, 3000, 1500, 1000, 800, 600]
    ta         = [None, 800, 500, 300, 200, 150]
    aoa        = [None, None, 200, 100, 80, 50]
    otdoa      = [None, None, None, 50, 30, 15]
    # Multi-RTT: LOS (best case) vs NLOS urban (realistic) — research shows
    # 3GPP Rel-16 LOS ~5-10m; NLOS urban degrades to 50-200m (3GPP TR 38.855)
    multirtt_los  = [None, None, None, None, 8,  2]
    multirtt_nlos = [None, None, None, None, 80, 40]

    fig, ax = plt.subplots(figsize=(11, 6))
    labels = ["4G Cell ID", "4G + TA", "4G + AoA", "5G OTDOA",
              "5G Multi-RTT (LOS)", "5G Multi-RTT (NLOS urban)"]
    series = [cell_id, ta, aoa, otdoa, multirtt_los, multirtt_nlos]
    colors = [ACCENT_RED, ACCENT_ORANGE, ACCENT_CYAN, ACCENT_GREEN,
              ACCENT_PURPLE, "#a78bfa"]
    styles = ["-o", "-o", "-o", "-o", "-o", "--s"]

    for data, lbl, clr, sty in zip(series, labels, colors, styles):
        valid = [(y, d) for y, d in zip(years, data) if d is not None]
        if valid:
            ys, ds = zip(*valid)
            ax.plot(ys, ds, sty, label=lbl, color=clr, linewidth=2.2,
                    markersize=7, markerfacecolor=clr, markeredgecolor="none")

    # Shade the LOS/NLOS uncertainty band for Multi-RTT at 2026+
    ax.fill_between([2026, 2029], [8, 2], [80, 40],
                    alpha=0.08, color=ACCENT_PURPLE,
                    label="_nolegend_")

    ax.set_yscale("log")
    ax.set_yticks([1, 5, 10, 50, 100, 500, 1000, 5000])
    ax.set_yticklabels(["1m", "5m", "10m", "50m", "100m", "500m", "1km", "5km"])
    ax.set_xlabel("Year", color=TEXT_CLR, fontsize=11)
    ax.set_ylabel("Location Accuracy (meters, log scale)", color=TEXT_CLR, fontsize=11)
    ax.set_title("Cellular Tracking Accuracy Over Time (4G \u2192 5G)", color=TEXT_CLR,
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlim(2014, 2030)
    ax.legend(framealpha=0.2, fontsize=9, loc="upper right")
    ax.text(0.5, -0.14,
            "5G Multi-RTT: 5\u201310m in line-of-sight; degrades to 50\u2013200m in urban NLOS environments (3GPP TR 38.855)",
            transform=ax.transAxes, ha="center", fontsize=8.5, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph2_cellular_accuracy.png")

def graph3_correlation_attack():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.axis("off")
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    G = nx.DiGraph()
    pos = {
        "identity": (0, 1.8), "isp": (0, 1.0), "router": (0, 0.2),
        "phone_b": (-1.0, 0.2), "computer": (1.0, 0.2),
        "phone_a": (-1.0, -0.6), "correlation": (0, -1.4),
    }
    edges = [
        ("identity","isp"), ("isp","router"), ("router","phone_b"),
        ("router","computer"), ("isp","phone_a"), ("phone_b","correlation"),
        ("phone_a","correlation"), ("computer","correlation"),
    ]
    G.add_edges_from(edges)
    for n in G.nodes(): G.add_node(n)

    node_colors = {
        "identity": ACCENT_RED, "isp": ACCENT_ORANGE, "router": ACCENT_CYAN,
        "phone_b": ACCENT_GREEN, "computer": ACCENT_PURPLE, "phone_a": ACCENT_CYAN,
        "correlation": ACCENT_RED,
    }
    node_labels = {
        "identity": "Your Real Identity\n(Name, Address, Face)",
        "isp": "Residential ISP\n(IP: 203.0.113.45)",
        "router": "Home Router\n(MAC: AA:BB:CC)",
        "phone_b": "Phone B\n(Wi-Fi Only)",
        "computer": "Computer\n(Tails/Proton)",
        "phone_a": "Phone A\n(Flip Phone)",
        "correlation": "CORRELATION\n\"John Doe = Both Phones\"",
    }
    sizes = {"identity": 2200, "isp": 2000, "router": 1800, "phone_b": 1600,
             "computer": 1600, "phone_a": 1600, "correlation": 2400}

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[sizes[n] for n in G.nodes()],
                           node_color=[node_colors[n] for n in G.nodes()],
                           edgecolors=BORDER_CLR, linewidths=1.5, alpha=0.95)
    nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax, font_size=7.5,
                            font_color=TEXT_CLR, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=MUTED_CLR, width=1.5,
                           arrows=True, arrowsize=20, arrowstyle="-|>",
                           connectionstyle="arc3,rad=0.12", alpha=0.6)

    ax.set_title("Data Flow & Correlation Attack \u2014 The \"Collapse\" Diagram",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)
    ax.text(0, -0.02,
            "Connecting Phone B to home Wi-Fi collapses the entire compartmentalization",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph3_correlation.png")

def graph4_probe_request():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)
    ax.axis("off")

    events = [
        (0,  "Phone powers on\nWi-Fi enables",         ACCENT_CYAN,   0.0),
        (3,  "Probe Request:\n\"Any remembered SSIDs?\"", ACCENT_ORANGE, 0.0),
        (6,  "Coffee Shop Beacon:\nBSSID 11:22:33:44:55:66", ACCENT_GREEN, 0.6),
        (9,  "Device caches BSSID\n+ signal strength",  ACCENT_PURPLE, 0.0),
        (12, "Adversary queries\nGoogle Geolocation API", ACCENT_RED,   0.0),
        (15, "GPS: 40.7128\u00b0N, 74.0060\u00b0W\n\"Starbucks, 123 Main St\"", ACCENT_RED, 0.0),
    ]

    for i, (label, desc, clr, extra) in enumerate(events):
        y = 4 - i * 0.7
        ax.plot([0, 0.05], [y, y], color=clr, linewidth=3, alpha=0.8)
        ax.plot([0.05, 0.1], [y, y], color=MUTED_CLR, linewidth=1.5, linestyle=":", alpha=0.5)
        t = i * 3
        ax.text(-0.02, y + 0.15, f"T+{t}s", fontsize=9, color=MUTED_CLR,
                ha="right", va="bottom", fontfamily="monospace")
        ax.text(0.15, y + 0.1, label, fontsize=10.5, color=clr,
                fontweight="bold", va="bottom")
        if desc:
            ax.text(0.15, y - 0.25, desc, fontsize=9, color=TEXT_CLR, va="top", alpha=0.85)

    ax.set_xlim(-0.3, 1.2)
    ax.set_ylim(-0.5, 4.5)
    ax.set_title("Wi-Fi Probe Request & BSSID Geolocation \u2014 Passive Tracking",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)
    ax.text(0.5, -0.06, "Your phone broadcasts identifying data even when not connected to any network",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph4_probe_request.png")

def graph5_threat_effectiveness():
    categories = ["Advertisers", "Local Police", "Civil\nLitigation", "Cybercriminal",
                  "Corporate\nEspionage", "Federal LE", "State Actor"]
    values = [95, 60, 70, 85, 40, 25, 15]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    ax.plot(angles, values, "o-", linewidth=2.5, color=ACCENT_CYAN, markersize=8)
    ax.fill(angles, values, alpha=0.15, color=ACCENT_CYAN)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, color=TEXT_CLR)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"], fontsize=8, color=MUTED_CLR)
    ax.tick_params(pad=8)

    for a, v in zip(angles[:-1], values[:-1]):
        ax.text(a, v + 6, f"{v}%", fontsize=8.5, ha="center", va="bottom",
                color=ACCENT_CYAN, fontweight="bold")

    ax.set_title("Two-Phone Strategy: Effectiveness by Adversary Type",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=20, va="bottom")
    ax.text(0.5, -0.08, "Effective against non-state actors; collapses against state-level adversaries",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph5_threat_effectiveness.png")

def graph6_failure_cascade():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2.5, 2.5)
    ax.axis("off")
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    G = nx.DiGraph()
    pos = {
        "mistake": (0, 2.2), "isp": (-1.2, 1.2), "router": (0, 1.2),
        "sniffer": (1.2, 1.2), "name": (-1.2, 0.2), "corr_a": (0, 0.2),
        "corr_b": (1.2, 0.2), "carrier": (-0.8, -0.8), "surveil": (0, -0.8),
        "tower": (0.8, -0.8), "deanonymized": (0, -1.8),
    }
    edges = [
        ("mistake","isp"), ("mistake","router"), ("mistake","sniffer"),
        ("isp","name"), ("router","corr_a"), ("sniffer","corr_b"),
        ("name","carrier"), ("corr_a","surveil"), ("corr_b","tower"),
        ("carrier","deanonymized"), ("surveil","deanonymized"), ("tower","deanonymized"),
    ]
    G.add_edges_from(edges)

    node_colors = {
        "mistake": ACCENT_RED, "isp": ACCENT_ORANGE, "router": ACCENT_CYAN,
        "sniffer": ACCENT_PURPLE, "name": ACCENT_ORANGE, "corr_a": ACCENT_CYAN,
        "corr_b": ACCENT_PURPLE, "carrier": ACCENT_CYAN, "surveil": ACCENT_GREEN,
        "tower": ACCENT_ORANGE, "deanonymized": ACCENT_RED,
    }
    node_labels = {
        "mistake": "MISTAKE:\nPhone B on Home Wi-Fi",
        "isp": "ISP Logs\nIP + MAC + Timestamp",
        "router": "Router Logs\nPhone B MAC at Home",
        "sniffer": "Wi-Fi Sniffer\nCaptures MAC Nearby",
        "name": "Name & Address\nFrom ISP Subscriber",
        "corr_a": "Phone A IMSI\nat Same Location",
        "corr_b": "Neighbor Probe\nMatches MAC",
        "carrier": "Carrier Subpoena\nPhone A \u2192 John Doe",
        "surveil": "Physical Surveillance\nJohn Doe Carries Both",
        "tower": "Tower Dump\nBoth IMSIs at Home",
        "deanonymized": "COMPLETE\nDEANONYMIZATION",
    }
    sizes = {"mistake": 2000, "deanonymized": 2400}
    for n in G.nodes():
        sizes.setdefault(n, 1600)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[sizes[n] for n in G.nodes()],
                           node_color=[node_colors[n] for n in G.nodes()],
                           edgecolors=BORDER_CLR, linewidths=1.5, alpha=0.95)
    nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax, font_size=7,
                            font_color=TEXT_CLR, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=MUTED_CLR, width=1.3,
                           arrows=True, arrowsize=18, arrowstyle="-|>",
                           connectionstyle="arc3,rad=0.1", alpha=0.5)

    ax.set_title("OpSec Failure Cascade \u2014 One Mistake Collapses Everything",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)
    ax.text(0.5, -0.06, "Time to cascade: 24 hours (ISP subpoena) to 30 days (carrier logs)",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph6_failure_cascade.png")

def graph7_privacy_convenience():
    strategies = ["Stock Android\niPhone", "Single De-Googled\nPhone", "Two-Phone\n(Original)", "Two-Phone\n+ Mitigations"]
    privacy    = [20, 65, 75, 85]
    conven     = [90, 60, 35, 15]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    colors = [ACCENT_RED, ACCENT_ORANGE, ACCENT_CYAN, ACCENT_GREEN]
    sizes  = [180, 200, 220, 250]

    for i, s in enumerate(strategies):
        ax.scatter(conven[i], privacy[i], s=sizes[i], c=colors[i], alpha=0.85,
                   edgecolors=BORDER_CLR, linewidths=1.5, zorder=5)
        offset_x = -8 if i != 2 else 8
        offset_y = 5
        ax.annotate(s, (conven[i], privacy[i]),
                    textcoords="offset points", xytext=(offset_x, offset_y),
                    fontsize=9, color=TEXT_CLR, ha="center", fontweight="bold")

    ax.axhspan(60, 80, xmin=0.45, xmax=0.75, alpha=0.06, color=ACCENT_GREEN)
    ax.text(70, 70, "OPTIMAL\nBALANCE", fontsize=11, color=ACCENT_GREEN,
            ha="center", va="center", fontweight="bold", alpha=0.5)

    ax.set_xlabel("Convenience \u2192", color=TEXT_CLR, fontsize=11)
    ax.set_ylabel("Privacy \u2192", color=TEXT_CLR, fontsize=11)
    ax.set_title("Privacy vs. Convenience Trade-Off", color=TEXT_CLR,
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.text(0.5, -0.08, "Most users should target the optimal balance: single de-Googled phone + Signal + VPN",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph7_privacy_convenience.png")

def graph8_data_retention():
    categories = ["Call\nRecords", "SMS\nMetadata", "Tower\nDumps", "Timing\nAdvance",
                  "5G Multi-\nRTT", "Wi-Fi BSSID\nLogs", "IP\nAssignment", "DNS\nQueries"]
    us = [18, 18, 12, 6, 3, 3, 18, 2]
    eu = [6, 6, 12, 3, 1, 1, 6, 0.5]
    cn = [99, 99, 99, 99, 99, 99, 99, 99]

    x = np.arange(len(categories))
    w = 0.25
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(x - w, us, w, label="US Carrier", color=ACCENT_CYAN,   alpha=0.85, edgecolor="none")
    ax.bar(x,     eu, w, label="EU Carrier", color=ACCENT_GREEN,  alpha=0.85, edgecolor="none")
    ax.bar(x + w, cn, w, label="China",      color=ACCENT_ORANGE, alpha=0.85, edgecolor="none")

    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylabel("Retention Period (months, log scale)", color=TEXT_CLR, fontsize=11)
    ax.set_yscale("symlog", linthresh=1)
    ax.set_yticks([0.5, 1, 3, 6, 12, 18, 99])
    ax.set_yticklabels(["0.5mo", "1mo", "3mo", "6mo", "12mo", "18mo", "\u221e"])
    ax.set_title("Forensic Data Retention by Carrier: US vs EU vs China",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)
    ax.legend(framealpha=0.2, fontsize=10)
    ax.text(0.5, -0.12, "US carriers retain location data for 18 months \u2014 your past never dies",
            transform=ax.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph8_data_retention.png")

def graph9_cost_benefit():
    strategies = ["Single De-Googled", "Two-Phone Original", "Two-Phone + Mitigations"]
    costs    = [200, 800, 1800]
    benefits = [65, 75, 85]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    colors = [ACCENT_ORANGE, ACCENT_CYAN, ACCENT_GREEN]
    bars = ax1.bar(strategies, costs, color=colors, alpha=0.85, edgecolor="none", width=0.5)

    for bar, cost in zip(bars, costs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40,
                f"${cost}/yr", ha="center", va="bottom", fontsize=10,
                color=TEXT_CLR, fontweight="bold")

    ax1.set_ylabel("Annual Cost (USD)", color=TEXT_CLR, fontsize=11)
    ax1.set_ylim(0, 2200)
    ax1.set_title("Cost-Benefit Analysis: Privacy Investment vs Return",
                  color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)

    ax2 = ax1.twinx()
    ax2.plot(strategies, benefits, "-o", color=ACCENT_GREEN, linewidth=2.5,
             markersize=10, markerfacecolor=ACCENT_GREEN, markeredgecolor="none", zorder=5)
    ax2.set_ylabel("Privacy Benefit (%)", color=ACCENT_GREEN, fontsize=11)
    ax2.tick_params(colors=ACCENT_GREEN)
    ax2.set_ylim(0, 100)

    for i, b in enumerate(benefits):
        ax2.annotate(f"{b}%", (i, b), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10,
                    color=ACCENT_GREEN, fontweight="bold")

    ax1.text(0.5, -0.12, "Mitigated two-phone costs ~$1,800/yr plus hundreds of OpSec hours",
            transform=ax1.transAxes, ha="center", fontsize=9, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph9_cost_benefit.png")

def graph10_decision_tree():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2.5, 2.5)
    ax.axis("off")
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    G = nx.DiGraph()
    pos = {
        "start":     (0, 2.2),
        "q1_yes":    (-0.8, 1.2),
        "q1_no":     (0.8, 1.2),
        "q2_yes":    (-1.6, 0.2),
        "q2_no":     (0, 0.2),
        "two_phone": (-1.6, -0.8),
        "single":    (0.8, -0.8),
        "opsec_yes": (-0.8, -1.8),
        "opsec_no":  (0.8, -1.8),
    }
    edges = [
        ("start","q1_yes"), ("start","q1_no"),
        ("q1_yes","q2_yes"), ("q1_yes","q2_no"),
        ("q2_yes","two_phone"), ("q2_no","single"),
        ("two_phone","opsec_yes"), ("two_phone","opsec_no"),
    ]
    G.add_edges_from(edges)

    labels = {
        "start": "START\nWho is tracking you?",
        "q1_yes": "Targeted\nSurveillance?",
        "q1_no": "Normal\nCitizen",
        "q2_yes": "Border\nCrosser?",
        "q2_no": "Journalist\nActivist?",
        "two_phone": "Two-Phone\nStrategy",
        "single": "Single Phone\n+ Signal + VPN",
        "opsec_yes": "80% Privacy\nvs L2 Adversary",
        "opsec_no": "60% Privacy\nAdequate",
    }
    colors = {
        "start": ACCENT_CYAN, "q1_yes": ACCENT_ORANGE, "q1_no": ACCENT_GREEN,
        "q2_yes": ACCENT_PURPLE, "q2_no": ACCENT_PURPLE,
        "two_phone": ACCENT_CYAN, "single": ACCENT_GREEN,
        "opsec_yes": ACCENT_GREEN, "opsec_no": ACCENT_ORANGE,
    }
    sizes = {"start": 2200, "q1_yes": 1800, "q1_no": 1800, "q2_yes": 1600,
             "q2_no": 1600, "two_phone": 1800, "single": 1800,
             "opsec_yes": 1600, "opsec_no": 1600}

    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[sizes[n] for n in G.nodes()],
                           node_color=[colors[n] for n in G.nodes()],
                           edgecolors=BORDER_CLR, linewidths=1.5, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=8,
                            font_color=TEXT_CLR, font_weight="bold")
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=MUTED_CLR, width=1.5,
                           arrows=True, arrowsize=18, arrowstyle="-|>",
                           connectionstyle="arc3,rad=0.08", alpha=0.5)

    ax.set_title("Decision Tree: Should You Use Two Phones?",
                 color=TEXT_CLR, fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    return fig_save(fig, "graph10_decision_tree.png")

def graph11_threat_tier_flowchart():
    """Threat tier decision flowchart for Ch47."""
    fig, ax = plt.subplots(figsize=(10, 15))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 15)
    ax.axis("off")
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    def box(cx, cy, w, h, label, color, fontsize=8.5, alpha=0.9, radius=0.18):
        rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle=f"round,pad=0.05,rounding_size={radius}",
                              facecolor=color, edgecolor=BORDER_CLR,
                              linewidth=1.2, alpha=alpha, zorder=3)
        ax.add_patch(rect)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fontsize, color=TEXT_CLR, fontweight="bold",
                wrap=True, zorder=4, multialignment="center")

    def diamond(cx, cy, w, h, label, color, fontsize=8):
        xs = [cx, cx + w/2, cx, cx - w/2, cx]
        ys = [cy + h/2, cy, cy - h/2, cy, cy + h/2]
        ax.fill(xs, ys, color=color, alpha=0.85, zorder=3)
        ax.plot(xs, ys, color=BORDER_CLR, linewidth=1.0, zorder=4)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fontsize, color=TEXT_CLR, fontweight="bold",
                zorder=5, multialignment="center")

    def arrow(x1, y1, x2, y2, label="", lx=None, ly=None):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED_CLR,
                                   lw=1.4, mutation_scale=14),
                    zorder=2)
        if label:
            mx = lx if lx else (x1 + x2) / 2
            my = ly if ly else (y1 + y2) / 2
            ax.text(mx, my, label, ha="center", va="center",
                    fontsize=7.5, color=ACCENT_GREEN, fontweight="bold",
                    bbox=dict(facecolor=DARK_BG, edgecolor="none", pad=1.5), zorder=5)

    # ── Nodes (top to bottom) ──────────────────────────────────────────────
    # START
    box(5, 14.2, 3.0, 0.65, "START — Who is trying to track you?", ACCENT_CYAN,
        fontsize=9, radius=0.3)

    # Q1
    diamond(5, 13.0, 6.5, 0.85,
            "Targeted by a foreign government\nor intelligence service?", CARD_BG, fontsize=8)

    # Q2
    diamond(5, 11.2, 6.5, 0.85,
            "Active federal investigation, NSL,\nor national security matter?", CARD_BG, fontsize=8)

    # Q3
    diamond(5, 9.4, 6.5, 0.9,
            "Journalist covering sensitive topics, activist,\nDV survivor, or regular border crosser?", CARD_BG, fontsize=7.5)

    # Q4
    diamond(5, 7.5, 6.5, 0.85,
            "Employer MDM, potential stalkerware,\nor active civil litigation?", CARD_BG, fontsize=8)

    # TIER outcomes (right side exits)
    tier_colors = {4: ACCENT_RED, 3: ACCENT_ORANGE, 2: "#e6c420",
                   1: ACCENT_GREEN, 0: "#3fb950"}
    tier_labels = {
        4: "TIER 4\nNation-State\nNo electronic strategy\nis adequate",
        3: "TIER 3\nFederal / Intelligence\nTwo-phone + legal\ncounsel required",
        2: "TIER 2\nInstitutional\nFull two-phone\nstrategy (Vol. 6)",
        1: "TIER 1\nPersonal Targeted\nCitizen Max +\ndevice hygiene",
    }
    tier_y   = {4: 13.0, 3: 11.2, 2: 9.4, 1: 7.5}
    tier_x   = 8.5
    for t, y in tier_y.items():
        box(tier_x, y, 2.6, 0.95, tier_labels[t], tier_colors[t], fontsize=7.5)
        arrow(6.25 + 0.5*(t==4), y, tier_x - 1.3, y, "YES", lx=7.1, ly=y + 0.18)

    # Default TIER 0
    box(5, 5.7, 4.2, 1.1,
        "TIER 0 — Passive Commercial\nAdvertisers & Data Brokers\nCitizen Max Stack (Ch.28 & App. I)",
        tier_colors[0], fontsize=8.5)

    # ── Vertical NO arrows ─────────────────────────────────────────────────
    for y_top, y_bot in [(13.57, 13.43), (12.57, 11.63), (10.77, 9.83), (9.07, 7.93)]:
        arrow(5, y_top, 5, y_bot, "NO", lx=4.5)
    arrow(5, 7.07, 5, 6.25, "NO", lx=4.5)

    # ── Legend ─────────────────────────────────────────────────────────────
    legend_items = [
        (ACCENT_RED,    "Tier 4 — Nation-State"),
        (ACCENT_ORANGE, "Tier 3 — Federal LE / Intelligence"),
        ("#e6c420",     "Tier 2 — Local / State Institutional"),
        (ACCENT_GREEN,  "Tier 1 — Targeted Personal"),
        ("#3fb950",     "Tier 0 — Commercial Surveillance"),
    ]
    lx, ly = 0.4, 4.4
    ax.text(lx, ly + 0.5, "THREAT TIERS", fontsize=7.5, color=MUTED_CLR,
            fontweight="bold", fontfamily="monospace")
    for i, (clr, lbl) in enumerate(legend_items):
        y = ly - i * 0.45
        rect = FancyBboxPatch((lx, y - 0.14), 0.25, 0.28,
                              boxstyle="round,pad=0.02",
                              facecolor=clr, edgecolor="none", alpha=0.85, zorder=3)
        ax.add_patch(rect)
        ax.text(lx + 0.35, y, lbl, fontsize=7.5, color=TEXT_CLR, va="center")

    ax.set_title("Threat Tier Decision Flowchart — Chapter 47",
                 color=TEXT_CLR, fontsize=13, fontweight="bold", pad=12)
    ax.text(0.5, 0.01,
            "Answer YES at any question to exit with that tier's strategy. All lower-tier actions remain in effect.",
            transform=ax.transAxes, ha="center", fontsize=8, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph11_threat_tier_flowchart.png")


def graph12_cellular_network_topology():
    """Cellular network topology and data collection points for Ch05."""
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor(DARK_BG)
    fig.patch.set_facecolor(DARK_BG)

    def node(cx, cy, w, h, lines, color, fs=8.0, alpha=0.9):
        rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor=BORDER_CLR,
                              linewidth=1.1, alpha=alpha, zorder=3)
        ax.add_patch(rect)
        text = "\n".join(lines)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
                color=TEXT_CLR, fontweight="bold", zorder=4, multialignment="center")

    def conn(x1, y1, x2, y2, clr=MUTED_CLR, lw=1.2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=clr, lw=lw,
                                   mutation_scale=12), zorder=2)
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx + 0.1, my, label, fontsize=6.5, color=clr,
                    va="center", fontfamily="monospace")

    def badge(cx, cy, num, clr):
        circle = plt.Circle((cx, cy), 0.22, color=clr, zorder=5)
        ax.add_patch(circle)
        ax.text(cx, cy, str(num), ha="center", va="center",
                fontsize=7.5, color=DARK_BG, fontweight="bold", zorder=6)

    # ── Layer labels ───────────────────────────────────────────────────────
    layers = [
        (8.3, "DEVICE"),
        (6.8, "RADIO ACCESS NETWORK"),
        (5.0, "CORE NETWORK"),
        (2.6, "EXTERNAL SYSTEMS"),
    ]
    for y, lbl in layers:
        ax.text(0.15, y, lbl, fontsize=6.8, color=MUTED_CLR,
                fontfamily="monospace", fontweight="bold", va="center",
                rotation=0, alpha=0.7)
        ax.axhline(y - 0.6, color=BORDER_CLR, linewidth=0.4, alpha=0.4, zorder=1)

    # ── UE ─────────────────────────────────────────────────────────────────
    node(6, 8.3, 2.4, 0.7, ["UE (Your Phone)", "IMSI · IMEI · IP"], ACCENT_CYAN, fs=8.5)

    # ── RAN ────────────────────────────────────────────────────────────────
    node(3.5, 6.8, 2.2, 0.7, ["eNodeB / gNodeB", "Cell Tower"], ACCENT_PURPLE, fs=8)
    node(8.5, 6.8, 2.2, 0.7, ["Wi-Fi AP", "BSSID / MAC logs"], "#7c5aed", fs=8)

    # ── Core ───────────────────────────────────────────────────────────────
    node(2.2, 5.0, 1.9, 0.7,  ["MME / AMF", "Attach · Location"], ACCENT_ORANGE, fs=7.5)
    node(4.5, 5.0, 1.9, 0.7,  ["HSS / UDM", "Subscriber DB"], ACCENT_ORANGE, fs=7.5)
    node(6.8, 5.0, 1.9, 0.7,  ["SGW / UPF", "Session · Traffic"], ACCENT_ORANGE, fs=7.5)
    node(9.0, 5.0, 1.9, 0.7,  ["PGW / IMS", "Internet gateway"], ACCENT_ORANGE, fs=7.5)

    # ── External ───────────────────────────────────────────────────────────
    node(1.5, 2.6, 2.0, 0.75, ["Billing System", "CDR retention"], ACCENT_GREEN, fs=7.5)
    node(4.0, 2.6, 2.0, 0.75, ["Lawful Intercept", "CALEA / ETSI"], ACCENT_RED, fs=7.5)
    node(6.5, 2.6, 2.0, 0.75, ["DPI System", "Traffic analysis"], "#e6c420", fs=7.5)
    node(9.0, 2.6, 2.0, 0.75, ["Interconnect", "Signalling / SS7"], ACCENT_PURPLE, fs=7.5)

    # ── Connections ────────────────────────────────────────────────────────
    conn(6, 7.95,  3.5, 7.15)          # UE → tower
    conn(6, 7.95,  8.5, 7.15)          # UE → Wi-Fi AP
    conn(3.5, 6.45, 2.2, 5.35)         # tower → MME
    conn(3.5, 6.45, 4.5, 5.35)         # tower → HSS
    conn(3.5, 6.45, 6.8, 5.35)         # tower → SGW
    conn(6.8, 4.65, 9.0, 5.35)         # SGW → PGW (bidirectional implied)
    conn(2.2, 4.65, 1.5, 2.98)         # MME → Billing
    conn(4.5, 4.65, 4.0, 2.98)         # HSS → LI
    conn(6.8, 4.65, 6.5, 2.98)         # SGW → DPI
    conn(9.0, 4.65, 9.0, 2.98)         # PGW → Interconnect
    conn(8.5, 6.45, 9.0, 5.35, clr=MUTED_CLR, lw=0.8)  # Wi-Fi → PGW

    # ── Collection point badges ────────────────────────────────────────────
    badge_data = [
        (3.5, 6.8, 1, ACCENT_CYAN),
        (2.2, 5.0, 2, ACCENT_ORANGE),
        (4.5, 5.0, 3, ACCENT_ORANGE),
        (6.8, 5.0, 4, ACCENT_ORANGE),
        (1.5, 2.6, 5, ACCENT_GREEN),
        (4.0, 2.6, 6, ACCENT_RED),
        (6.5, 2.6, 7, "#e6c420"),
    ]
    for bx, by, num, clr in badge_data:
        badge(bx + 1.1, by + 0.42, num, clr)

    # ── Legend ─────────────────────────────────────────────────────────────
    ax.text(10.3, 4.5, "DATA COLLECTED", fontsize=7, color=MUTED_CLR,
            fontweight="bold", fontfamily="monospace")
    badge_legend = [
        (1, ACCENT_CYAN,   "Cell ID, TA, signal"),
        (2, ACCENT_ORANGE, "IMSI, attach, location"),
        (3, ACCENT_ORANGE, "Subscriber identity"),
        (4, ACCENT_ORANGE, "Session metadata"),
        (5, ACCENT_GREEN,  "CDRs (18 mo US)"),
        (6, ACCENT_RED,    "Lawful intercept"),
        (7, "#e6c420",     "Traffic fingerprint"),
    ]
    for i, (n, clr, lbl) in enumerate(badge_legend):
        y = 4.1 - i * 0.53
        circle = plt.Circle((10.42, y), 0.18, color=clr, zorder=5)
        ax.add_patch(circle)
        ax.text(10.42, y, str(n), ha="center", va="center",
                fontsize=6.5, color=DARK_BG, fontweight="bold", zorder=6)
        ax.text(10.68, y, lbl, fontsize=7, color=TEXT_CLR, va="center")

    ax.set_title("Cellular Network Architecture — Data Collection Points",
                 color=TEXT_CLR, fontsize=13, fontweight="bold", pad=12)
    ax.text(0.5, 0.01,
            "Numbered badges mark forensic data collection points. All are subject to subpoena.",
            transform=ax.transAxes, ha="center", fontsize=8, color=MUTED_CLR)
    fig.tight_layout()
    return fig_save(fig, "graph12_cellular_network_topology.png")


def graph13_android_stack_comparison():
    """Side-by-side Android OS stack comparison: Stock vs GrapheneOS (Ch11)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 9))
    fig.patch.set_facecolor(DARK_BG)

    layers_stock = [
        ("SYSTEM APPS",         ["Chrome · GBoard · Google Maps",
                                  "Gmail · YouTube · Wallet"],          ACCENT_RED,    0.9),
        ("GOOGLE PLAY SERVICES",["Location Scanner · Ad ID Manager",
                                  "FCM Watcher · SafetyNet · Backup"],   ACCENT_RED,    0.85),
        ("APP FRAMEWORK",       ["Activity Manager · Package Manager",
                                  "Location Manager · Notification Svc"], ACCENT_ORANGE, 0.85),
        ("ANDROID RUNTIME",     ["ART (JIT) · Core Libraries",
                                  "Dalvik Compatibility"],               ACCENT_ORANGE, 0.75),
        ("HAL",                 ["Camera · Audio · Sensors",
                                  "Wi-Fi · Bluetooth · GPS HALs"],       ACCENT_PURPLE, 0.75),
        ("LINUX KERNEL",        ["Binder IPC · Ashmem · Wakelocks",
                                  "Staging drivers · Permissive SELinux"],"#4a5568",    0.85),
        ("HARDWARE",            ["SoC · Baseband · Wi-Fi FW",
                                  "TEE · GPS · NFC"],                    "#2d3748",     0.9),
    ]

    layers_graphene = [
        ("USER APPS",           ["Sandboxed Google Play (optional)",
                                  "Auditor · Vanadium · Camera"],        ACCENT_GREEN,  0.9),
        ("HARDENED SANDBOX",    ["Exec-spawning · ptrace restrictions",
                                  "MAC spoofing · Sensor deny"],         ACCENT_CYAN,   0.9),
        ("APP FRAMEWORK",       ["Activity Manager · Package Manager",
                                  "Network Permission Toggle"],          ACCENT_GREEN,  0.8),
        ("HARDENED RUNTIME",    ["Memory-safe allocator (scudo)",
                                  "ASLR improvements · CFI"],            ACCENT_CYAN,   0.8),
        ("HAL",                 ["Minimal HAL surface",
                                  "Stricter permissions on sensors"],    ACCENT_PURPLE, 0.75),
        ("HARDENED KERNEL",     ["Stronger SELinux · Seccomp BPF",
                                  "Extra KASLR · Kernel hardening CFI"], ACCENT_CYAN,   0.85),
        ("HARDWARE",            ["SoC · Titan M (verified boot)",
                                  "Pixel-specific TEE attestation"],     "#2d5016",     0.9),
    ]

    risk_labels_stock = [
        "HIGH — tracks location, sends to Google",
        "HIGH — persistent background; cannot be removed",
        "MED  — no permission; all apps can request",
        "MED  — JIT profiling; no memory safety",
        "MED  — broad sensor access by default",
        "MED  — staging drivers; permissive policy",
        "FIXED — cannot be modified",
    ]
    risk_labels_graphene = [
        "LOW  — optional; full isolation if installed",
        "LOW  — exec-spawning prevents persistent exploits",
        "LOW  — per-app network/sensor kill switches",
        "LOW  — hardened alloc; spatial mem safety",
        "LOW  — minimal attack surface",
        "LOW  — enforcing policy; exploit mitigations",
        "LOW  — Titan M enforces verified boot chain",
    ]

    for ax, layers, risk_labels, title in [
        (ax1, layers_stock,   risk_labels_stock,   "Stock Android\n(AOSP + Google Services)"),
        (ax2, layers_graphene, risk_labels_graphene, "GrapheneOS\n(Hardened AOSP, no Google)"),
    ]:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, len(layers) * 1.2 + 0.5)
        ax.axis("off")
        ax.set_facecolor(DARK_BG)

        for i, (name, sublabels, color, alpha) in enumerate(layers):
            y = (len(layers) - 1 - i) * 1.2 + 0.5
            rect = FancyBboxPatch((0.2, y), 9.6, 1.05,
                                  boxstyle="round,pad=0.06",
                                  facecolor=color, edgecolor=BORDER_CLR,
                                  linewidth=1.0, alpha=alpha, zorder=3)
            ax.add_patch(rect)
            ax.text(0.5, y + 0.78, name, fontsize=8.5, color=TEXT_CLR,
                    fontweight="bold", va="center", fontfamily="monospace", zorder=4)
            ax.text(0.5, y + 0.38, "  ".join(sublabels), fontsize=6.8, color=TEXT_CLR,
                    va="center", alpha=0.85, zorder=4)
            risk = risk_labels[i]
            risk_color = ACCENT_RED if "HIGH" in risk else (ACCENT_ORANGE if "MED" in risk else ACCENT_GREEN)
            ax.text(9.7, y + 0.55, risk, fontsize=6.0, color=risk_color,
                    va="center", ha="right", fontfamily="monospace", zorder=4)

        ax.set_title(title, color=TEXT_CLR, fontsize=11, fontweight="bold", pad=10)

    fig.suptitle("Android OS Architecture — Stock vs GrapheneOS",
                 color=TEXT_CLR, fontsize=13, fontweight="bold", y=0.98)
    fig.text(0.5, 0.01,
             "GrapheneOS removes Google telemetry entirely and adds hardening at every layer",
             ha="center", fontsize=8.5, color=MUTED_CLR)
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    return fig_save(fig, "graph13_android_stack_comparison.png")


GRAPH_FUNCTIONS = [
    graph1_attack_surface, graph2_cellular_accuracy, graph3_correlation_attack,
    graph4_probe_request, graph5_threat_effectiveness, graph6_failure_cascade,
    graph7_privacy_convenience, graph8_data_retention, graph9_cost_benefit,
    graph10_decision_tree,
    graph11_threat_tier_flowchart, graph12_cellular_network_topology,
    graph13_android_stack_comparison,
]

# Maps graph stem -> (volume_num, chapter_num)
# Volume number disambiguates duplicate chapter numbers across volumes
GRAPH_CHAPTER_MAP = {
    "graph1_attack_surface":             (4, 18),
    "graph2_cellular_accuracy":          (4, 19),
    "graph3_correlation":                (4, 20),
    "graph4_probe_request":              (4, 21),
    "graph5_threat_effectiveness":       (4, 22),
    "graph6_failure_cascade":            (4, 23),
    "graph7_privacy_convenience":        (4, 24),
    "graph8_data_retention":             (4, 25),
    "graph9_cost_benefit":               (4, 26),
    "graph10_decision_tree":             (4, 27),
    "graph11_threat_tier_flowchart":     (7, 47),
    "graph12_cellular_network_topology": (2, 5),
    "graph13_android_stack_comparison":  (2, 11),
}

# ── Light theme CSS ─────────────────────────────────────────────────────────

def build_css_light():
    """Print-ready light theme — white background, dark text, no gradients."""
    LBG    = "#ffffff"
    LLBG   = "#f6f8fa"
    LCARD  = "#f0f2f5"
    LBDR   = "#d0d7de"
    LTXT   = "#1a1a2e"
    LMUTED = "#57606a"
    LHEAD  = "#0a6bcb"
    LGREEN = "#1a7f37"
    LORG   = "#d1242f"
    LPURP  = "#6e40c9"
    LCYAN  = "#0969da"

    return f"""
@page {{
    size: letter;
    margin: 0.75in 0.7in 0.85in 0.8in;
    @top-left {{
        content: string(chapter-running);
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 7.5pt; color: {LMUTED};
        border-bottom: 1px solid {LBDR}; padding-bottom: 4px;
    }}
    @top-right {{
        content: "Privacy Researcher's Handbook";
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 7.5pt; color: {LMUTED};
        border-bottom: 1px solid {LBDR}; padding-bottom: 4px;
    }}
    @bottom-center {{
        content: "— " counter(page) " —";
        font-family: Georgia, serif; font-size: 8pt; color: {LMUTED};
    }}
}}
@page :first {{ @top-left {{ content: ""; }} @top-right {{ content: ""; }} @bottom-center {{ content: ""; }} }}
.toc {{ page: toc-page; }}
@page toc-page {{ @top-left {{ content: ""; }} @top-right {{ content: ""; }} }}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
    background: {LBG}; color: {LTXT};
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 11pt; line-height: 1.72;
}}
.cover {{
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center;
    min-height: 9.5in; padding: 0.5in 1in; page-break-after: always;
    border-bottom: 3px solid {LHEAD};
}}
.cover h1 {{ font-size: 24pt; font-weight: 700; color: {LHEAD}; letter-spacing: 0.5px; margin-bottom: 0.15in; line-height: 1.3; }}
.cover .shield {{ font-size: 44pt; margin-bottom: 0.4in; }}
.cover .subtitle {{ font-size: 13pt; color: {LTXT}; max-width: 5in; margin-bottom: 0.4in; }}
.cover .meta {{ font-size: 9pt; color: {LMUTED}; margin-top: 0.3in; }}
.cover .version {{ font-size: 10pt; color: {LGREEN}; border: 1px solid {LGREEN}; padding: 5px 16px; border-radius: 3px; display: inline-block; margin-top: 0.3in; }}
.cover .classification {{ font-size: 8pt; color: {LORG}; margin-top: 0.5in; letter-spacing: 2px; text-transform: uppercase; }}
.toc {{ page-break-after: always; padding-top: 0.2in; }}
.toc h2 {{ font-size: 16pt; color: {LHEAD}; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.25in; border-bottom: 1px solid {LBDR}; padding-bottom: 0.1in; }}
.toc .vol-label {{ font-size: 9.5pt; font-weight: 700; color: {LGREEN}; text-transform: uppercase; margin-top: 0.12in; margin-bottom: 0.04in; padding: 3px 0; border-bottom: 1px solid {LBDR}; }}
.toc .ch-entry {{ display: flex; align-items: baseline; padding: 2px 0 2px 0.18in; }}
.toc .ch-entry a {{ font-size: 9.5pt; color: {LTXT}; text-decoration: none; white-space: nowrap; flex-shrink: 1; min-width: 0; }}
.toc .ch-dots {{ flex: 1; border-bottom: 1px dotted {LBDR}; margin: 0 6px 3px 6px; }}
.chapter {{ page-break-before: always; padding-top: 0.15in; }}
.chapter-title {{ string-set: chapter-running content(); font-size: 17pt; font-weight: 700; color: {LTXT}; margin-top: 0.05in; line-height: 1.25; }}
.chapter-header {{ margin-bottom: 0.3in; padding-bottom: 0.12in; border-bottom: 2px solid {LHEAD}; }}
.chapter-number {{ font-size: 8.5pt; color: {LHEAD}; text-transform: uppercase; letter-spacing: 3px; }}
.chapter-volume {{ font-size: 7.5pt; color: {LMUTED}; margin-top: 0.04in; }}
.appendix-group .chapter-number {{ color: {LGREEN}; }}
.appendix-group .chapter-header {{ border-bottom-color: {LGREEN}; }}
.content {{ padding-top: 0.08in; }}
.content h2 {{ font-size: 13pt; font-weight: 700; color: {LHEAD}; margin: 0.28in 0 0.1in 0; page-break-after: avoid; }}
.content h3 {{ font-size: 11.5pt; font-weight: 600; color: {LGREEN}; margin: 0.2in 0 0.08in 0; page-break-after: avoid; }}
.content h4 {{ font-size: 11pt; font-weight: 600; color: {LORG}; margin: 0.14in 0 0.06in 0; page-break-after: avoid; }}
.content p {{ margin: 0.07in 0; text-align: justify; orphans: 3; widows: 3; }}
.content a {{ color: {LHEAD}; text-decoration: underline; }}
.content strong {{ color: {LTXT}; font-weight: 700; }}
.content ul, .content ol {{ margin: 0.07in 0 0.07in 0.22in; }}
.content li {{ margin: 0.03in 0; orphans: 2; widows: 2; }}
.content pre {{ background: {LCARD}; border: 1px solid {LBDR}; border-left: 3px solid {LPURP}; border-radius: 3px; padding: 9px 13px; margin: 0.12in 0; font-family: 'Courier New', Courier, monospace; font-size: 8pt; color: {LTXT}; line-height: 1.5; white-space: pre-wrap; word-break: break-word; overflow: visible; }}
.content code {{ font-family: 'Courier New', Courier, monospace; font-size: 8.5pt; background: {LCARD}; padding: 1px 4px; border-radius: 2px; color: {LORG}; }}
.content pre code {{ background: none; padding: 0; color: inherit; }}
.content table {{ width: 100%; border-collapse: collapse; margin: 0.14in 0; font-size: 9pt; table-layout: fixed; }}
.content thead {{ display: table-header-group; }}
.content th {{ background: {LCARD}; color: {LHEAD}; font-size: 8pt; text-transform: uppercase; letter-spacing: 1px; padding: 6px 9px; text-align: left; font-weight: 700; border: 1px solid {LBDR}; word-break: break-word; }}
.content td {{ padding: 5px 9px; border: 1px solid {LBDR}; color: {LTXT}; vertical-align: top; word-break: break-word; }}
.content tr {{ page-break-inside: avoid; }}
.content tr:nth-child(even) td {{ background: {LLBG}; }}
.content tr:nth-child(odd) td {{ background: {LBG}; }}
.content blockquote {{ border-left: 3px solid {LCYAN}; background: {LLBG}; margin: 0.12in 0; padding: 10px 16px; color: {LTXT}; font-size: 11pt; page-break-inside: avoid; font-style: italic; }}
.content blockquote strong {{ color: {LHEAD}; font-style: normal; }}
.content blockquote p {{ margin: 0; text-align: left; }}
.content hr {{ border: none; border-top: 1px solid {LBDR}; margin: 0.18in 0; }}
.ref-card {{ page-break-inside: avoid; margin: 0.15in 0; }}
.ref-card pre {{ page-break-inside: avoid !important; font-size: 7.5pt; line-height: 1.45; }}
.footnote {{ font-size: 8.5pt; color: {LMUTED}; margin-top: 0.25in; padding-top: 0.1in; border-top: 1px solid {LBDR}; }}
.footnote > h3 {{ font-size: 8.5pt; font-weight: 700; color: {LMUTED}; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.06in; }}
.footnote ol {{ margin-left: 0.15in; }}
.footnote li {{ margin: 0.04in 0; line-height: 1.5; }}
sup {{ font-size: 7pt; color: {LCYAN}; vertical-align: super; line-height: 0; }}
sup a {{ color: {LCYAN}; text-decoration: none; }}
.graph-figure {{ text-align: center; margin: 0.25in 0; page-break-inside: avoid; max-width: 100%; }}
.graph-figure img {{ max-width: 100%; width: 100%; height: auto; border: 1px solid {LBDR}; border-radius: 3px; display: block; margin: 0 auto; }}
.graph-figure .caption {{ font-size: 8.5pt; color: {LMUTED}; margin-top: 0.06in; font-style: italic; }}
.page-footer {{ display: none; }}
@media screen {{ body {{ padding: 0.5in; max-width: 9in; margin: 0 auto; }} }}

/* ── Syntax highlighting (codehilite / light theme) ────────────────────────── */
.codehilite {{ background: {LCARD}; border: 1px solid {LBDR}; border-left: 3px solid {LPURP}; border-radius: 3px; padding: 9px 13px; margin: 0.12in 0; }}
.codehilite pre {{ border: none; padding: 0; margin: 0; background: transparent; }}
.codehilite .hll {{ background-color: #e8eaed; }}
.codehilite .c  {{ color: #6e7781; font-style: italic; }}
.codehilite .k  {{ color: #0550ae; font-weight: bold; }}
.codehilite .n  {{ color: {LTXT}; }}
.codehilite .o  {{ color: {LORG}; }}
.codehilite .s  {{ color: #0a6e25; }}
.codehilite .s1 {{ color: #0a6e25; }}
.codehilite .s2 {{ color: #0a6e25; }}
.codehilite .m  {{ color: {LPURP}; }}
.codehilite .mi {{ color: {LPURP}; }}
.codehilite .nb {{ color: #0550ae; }}
.codehilite .nf {{ color: {LORG}; font-weight: bold; }}
.codehilite .nv {{ color: {LTXT}; }}
.codehilite .nt {{ color: #0550ae; }}
.codehilite .p  {{ color: {LMUTED}; }}
.codehilite .cm {{ color: #6e7781; font-style: italic; }}
.codehilite .cp {{ color: {LORG}; }}
.codehilite .err {{ color: {LORG}; background: none; }}
"""

# ── Chapter reader ──────────────────────────────────────────────────────────

def extract_title(text, chapter_dir):
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    name = chapter_dir.name
    name = re.sub(r"^Ch\d+_", "", name)
    name = re.sub(r"^Appendix_\w+_", "", name)
    return name.replace("_", " ").title()

def read_all_chapters():
    chapters = []
    volumes = sorted(BOOK_DIR.iterdir())
    for vol in volumes:
        if not vol.is_dir() or not vol.name.startswith("Volume_"):
            continue
        vm = re.search(r"Volume_(\d+)", vol.name)
        vol_num = int(vm.group(1)) if vm else 0
        vol_label = vol.name.replace("Volume_", "Volume ").replace("_", " ")

        for chap_dir in sorted(vol.iterdir()):
            if not chap_dir.is_dir():
                continue
            readme = chap_dir / "README.md"
            if not readme.exists():
                continue
            text = readme.read_text("utf-8")
            title = extract_title(text, chap_dir)
            cm = re.search(r"Ch(\d+)", chap_dir.name)
            ch_num = int(cm.group(1)) if cm else 0
            chapters.append({
                "vol_num": vol_num, "vol_label": vol_label,
                "ch_num": ch_num, "title": title, "text": text,
                "dir_name": chap_dir.name,
            })

    app_dir = BOOK_DIR / "Appendices"
    if app_dir.exists():
        for app_d in sorted(app_dir.iterdir()):
            if not app_d.is_dir():
                continue
            readme = app_d / "README.md"
            if not readme.exists():
                continue
            text = readme.read_text("utf-8")
            title = extract_title(text, app_d)
            chapters.append({
                "vol_num": 8, "vol_label": "Appendices",
                "ch_num": 0, "title": title, "text": text,
                "dir_name": app_d.name,
            })

    chapters.sort(key=lambda c: (c["vol_num"], c["ch_num"]))
    return chapters

# ── CSS ─────────────────────────────────────────────────────────────────────

def build_css():
    return f"""
/* ── Page setup with running headers ─────────────────────────────────────── */
@page {{
    size: letter;
    margin: 0.7in 0.65in 0.8in 0.75in;
    @top-left {{
        content: string(chapter-running);
        font-family: {HEADER_FONT};
        font-size: 7pt;
        color: {MUTED_CLR};
        border-bottom: 1px solid {BORDER_CLR};
        padding-bottom: 4px;
    }}
    @top-right {{
        content: "Privacy Researcher's Handbook";
        font-family: {HEADER_FONT};
        font-size: 7pt;
        color: {MUTED_CLR};
        border-bottom: 1px solid {BORDER_CLR};
        padding-bottom: 4px;
    }}
    @bottom-center {{
        content: "— " counter(page) " —";
        font-family: {HEADER_FONT};
        font-size: 7.5pt;
        color: {MUTED_CLR};
    }}
}}
/* Suppress headers on cover AND TOC pages */
@page :first {{ @top-left {{ content: ""; }} @top-right {{ content: ""; }} @bottom-center {{ content: ""; }} }}
.toc {{ page: toc-page; }}
@page toc-page {{ @top-left {{ content: ""; }} @top-right {{ content: ""; }} }}

/* ── Reset ────────────────────────────────────────────────────────────────── */
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{
    font-size: clamp(15px, 1.4vw, 19px);
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
}}
body {{
    background: {DARK_BG};
    color: {TEXT_CLR};
    font-family: {BODY_FONT};
    font-size: 1rem;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: auto;
    text-size-adjust: auto;
    min-width: 0;
    overflow-x: hidden;
    overflow-y: auto;
}}

/* ── Cover ────────────────────────────────────────────────────────────────── */
.cover {{
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; text-align: center;
    min-height: 9.5in; padding: 0.5in 1in; page-break-after: always;
    background: linear-gradient(160deg, {DARKER_BG} 0%, {DARK_BG} 60%, {CARD_BG} 100%);
    border-bottom: 3px solid {ACCENT_CYAN};
}}
.cover .shield {{ font-size: 48pt; margin-bottom: 0.4in; opacity: 0.9; }}
.cover h1 {{
    font-family: {HEADER_FONT};
    font-size: 24pt; font-weight: 700; color: {ACCENT_CYAN};
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 0.15in; line-height: 1.3;
}}
.cover .subtitle {{
    font-size: 13pt; color: {TEXT_CLR};
    max-width: 5in; margin-bottom: 0.4in; line-height: 1.5;
}}
.cover .meta {{
    font-family: {HEADER_FONT};
    font-size: 9pt; color: {MUTED_CLR};
    margin-top: 0.3in;
}}
.cover .version {{
    font-family: {HEADER_FONT};
    font-size: 10pt; color: {ACCENT_GREEN};
    border: 1px solid {ACCENT_GREEN};
    padding: 6px 18px; border-radius: 4px;
    display: inline-block; margin-top: 0.3in;
}}
.cover .classification {{
    font-family: {HEADER_FONT};
    font-size: 8pt; color: {ACCENT_ORANGE};
    margin-top: 0.5in; letter-spacing: 2px;
    text-transform: uppercase;
}}

/* ── Table of Contents ────────────────────────────────────────────────────── */
.toc {{ page-break-after: always; padding-top: 0.2in; }}
.toc h2 {{
    font-family: {HEADER_FONT};
    font-size: 16pt; color: {ACCENT_CYAN};
    text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 0.25in; border-bottom: 1px solid {BORDER_CLR};
    padding-bottom: 0.1in;
}}
.toc .vol-group {{ margin-bottom: 0.15in; }}
.toc .vol-label {{
    font-family: {HEADER_FONT};
    font-size: 9.5pt; font-weight: 700; color: {ACCENT_GREEN};
    text-transform: uppercase; letter-spacing: 1px;
    margin-top: 0.15in; margin-bottom: 0.04in;
    padding: 3px 0; border-bottom: 1px solid {BORDER_CLR};
}}
.toc .ch-entry {{
    display: flex; align-items: baseline;
    padding: 2px 0 2px 0.2in;
}}
.toc .ch-entry a {{
    font-size: 9.5pt; color: {TEXT_CLR}; text-decoration: none;
    white-space: nowrap; overflow: visible;
    flex-shrink: 1; min-width: 0;
}}
.toc .ch-entry a:hover {{ color: {ACCENT_CYAN}; }}
.toc .ch-dots {{
    flex: 1; border-bottom: 1px dotted {BORDER_CLR};
    margin: 0 6px 3px 6px; min-width: 0.2in;
}}
.toc .ch-pg {{
    font-family: {HEADER_FONT};
    font-size: 8.5pt; color: {MUTED_CLR};
    white-space: nowrap;
    /* CSS target-counter not fully supported; placeholder for HTML view */
}}

/* ── Chapter layout ───────────────────────────────────────────────────────── */
.chapter {{
    page-break-before: always;
    padding-top: 0.15in;
}}
/* Inject chapter title into running header string */
.chapter-title {{
    string-set: chapter-running content();
    font-family: {HEADER_FONT};
    font-size: 17pt; font-weight: 700; color: {TEXT_CLR};
    margin-top: 0.05in; line-height: 1.25;
}}
.chapter-header {{
    margin-bottom: 0.3in; padding-bottom: 0.12in;
    border-bottom: 2px solid {ACCENT_CYAN};
}}
.chapter-number {{
    font-family: {HEADER_FONT};
    font-size: 8.5pt; color: {ACCENT_CYAN};
    text-transform: uppercase; letter-spacing: 3px;
}}
.chapter-volume {{
    font-size: 7.5pt; color: {MUTED_CLR};
    font-family: {HEADER_FONT};
    margin-top: 0.04in;
}}
.appendix-group .chapter-number {{ color: {ACCENT_GREEN}; }}
.appendix-group .chapter-header {{ border-bottom-color: {ACCENT_GREEN}; }}
.appendix-group .chapter-title {{ string-set: chapter-running content(); }}

/* ── Body content ─────────────────────────────────────────────────────────── */
.content {{ padding-top: 0.08in; }}

.content h2 {{
    font-family: {HEADER_FONT};
    font-size: clamp(20px, 2.2vw, 28px); font-weight: 700; color: {ACCENT_CYAN};
    margin: 0.28in 0 0.1in 0;
    page-break-after: avoid;
}}
.content h3 {{
    font-family: {HEADER_FONT};
    font-size: clamp(17px, 1.8vw, 24px); font-weight: 600; color: {ACCENT_GREEN};
    margin: 0.2in 0 0.08in 0;
    page-break-after: avoid;
}}
.content h4 {{
    font-size: clamp(16px, 1.5vw, 21px); font-weight: 600; color: {ACCENT_ORANGE};
    margin: 0.14in 0 0.06in 0;
    page-break-after: avoid;
}}
.content p {{
    margin: 0.07in 0;
    text-align: justify;
    orphans: 3;
    widows: 3;
}}
.content a {{ color: {ACCENT_CYAN}; text-decoration: none; }}
.content strong {{ color: {TEXT_CLR}; font-weight: 600; }}
.content em {{ color: {MUTED_CLR}; font-style: italic; }}
.content ul, .content ol {{ margin: 0.07in 0 0.07in 0.22in; }}
.content li {{
    margin: 0.035in 0;
    orphans: 2; widows: 2;
}}

/* ── Code blocks ──────────────────────────────────────────────────────────── */
.content pre {{
    background: {CARD_BG};
    border: 1px solid {BORDER_CLR};
    border-left: 3px solid {ACCENT_PURPLE};
    border-radius: 4px;
    padding: 10px 14px;
    margin: 0.12in 0;
    font-family: {HEADER_FONT};
    font-size: clamp(11px, 1.0vw, 14px);
    color: {ACCENT_CYAN};
    line-height: 1.55;
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: break-word;
    overflow: auto;
    resize: both;
    min-width: 200px;
    min-height: 60px;
    /* Do NOT set page-break-inside: avoid — long scripts span multiple pages */
}}
.content code {{
    font-family: {HEADER_FONT};
    font-size: 0.9em;
    background: {CARD_BG};
    padding: 1px 5px;
    border-radius: 3px;
    color: {ACCENT_ORANGE};
}}
.content pre code {{ background: none; padding: 0; color: inherit; font-size: inherit; }}

/* ── Syntax highlighting (codehilite / dark theme) ────────────────────────── */
.codehilite {{ background: {CARD_BG}; border: 1px solid {BORDER_CLR}; border-left: 3px solid {ACCENT_PURPLE}; border-radius: 4px; padding: 10px 14px; margin: 0.12in 0; overflow: visible; }}
.codehilite pre {{ border: none; padding: 0; margin: 0; background: transparent; }}
.codehilite .hll {{ background-color: #2a3040; }}
.codehilite .c  {{ color: #586e75; font-style: italic; }}  /* Comment */
.codehilite .k  {{ color: {ACCENT_CYAN}; font-weight: bold; }}  /* Keyword */
.codehilite .n  {{ color: {TEXT_CLR}; }}  /* Name */
.codehilite .o  {{ color: {ACCENT_ORANGE}; }}  /* Operator */
.codehilite .s  {{ color: {ACCENT_GREEN}; }}  /* String */
.codehilite .s1 {{ color: {ACCENT_GREEN}; }}
.codehilite .s2 {{ color: {ACCENT_GREEN}; }}
.codehilite .m  {{ color: {ACCENT_PURPLE}; }}  /* Number */
.codehilite .mi {{ color: {ACCENT_PURPLE}; }}
.codehilite .nb {{ color: {ACCENT_CYAN}; }}  /* Name.Builtin */
.codehilite .nf {{ color: {ACCENT_ORANGE}; font-weight: bold; }}  /* Name.Function */
.codehilite .nv {{ color: {TEXT_CLR}; }}  /* Name.Variable */
.codehilite .nt {{ color: {ACCENT_CYAN}; }}  /* Name.Tag */
.codehilite .p  {{ color: {MUTED_CLR}; }}  /* Punctuation */
.codehilite .cm {{ color: #586e75; font-style: italic; }}  /* Comment.Multiline */
.codehilite .cp {{ color: {ACCENT_ORANGE}; }}  /* Comment.Preproc */
.codehilite .err {{ color: {ACCENT_RED}; background: none; }}

/* ── Tables ───────────────────────────────────────────────────────────────── */
.content table {{
    width: 100%; border-collapse: collapse;
    margin: 0.14in 0; font-size: clamp(12px, 1.1vw, 15px);
    table-layout: auto;
    display: block;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}}
.content thead {{ display: table-header-group; }}
.content th {{
    background: {CARD_BG};
    color: {ACCENT_CYAN};
    font-family: {HEADER_FONT};
    font-size: 8pt; text-transform: uppercase; letter-spacing: 1px;
    padding: 7px 10px; text-align: left; font-weight: 700;
    border: 1px solid {BORDER_CLR};
    word-break: break-word;
}}
.content td {{
    padding: 6px 10px;
    border: 1px solid {BORDER_CLR};
    color: {TEXT_CLR};
    vertical-align: top;
    word-break: break-word;
    overflow-wrap: break-word;
}}
.content tr {{ page-break-inside: avoid; }}
.content tr:nth-child(even) td {{ background: {CARD_BG}; }}
.content tr:nth-child(odd) td  {{ background: transparent; }}

/* ── Blockquotes ──────────────────────────────────────────────────────────── */
.content blockquote {{
    border-left: 3px solid {ACCENT_CYAN};
    background: {CARD_BG};
    margin: 0.12in 0; padding: 10px 16px;
    color: {TEXT_CLR}; font-size: 10.5pt;
    page-break-inside: avoid;
    font-style: italic;
}}
.content blockquote strong {{ color: {ACCENT_CYAN}; font-style: normal; }}
.content blockquote p {{ margin: 0; text-align: left; }}

/* ── Horizontal rules ─────────────────────────────────────────────────────── */
.content hr {{
    border: none; border-top: 1px solid {BORDER_CLR};
    margin: 0.18in 0;
}}

/* ── Printable reference cards (Appendix G) ──────────────────────────────── */
.ref-card {{
    page-break-inside: avoid;
    margin: 0.15in 0;
}}
.ref-card pre {{
    /* Override the no-break rule from general pre — cards are short enough */
    page-break-inside: avoid !important;
    font-size: 7.5pt;
    line-height: 1.45;
}}

/* ── Footnotes (markdown extra footnote extension) ────────────────────────── */
.footnote {{
    font-size: 8.5pt; color: {MUTED_CLR};
    margin-top: 0.25in; padding-top: 0.1in;
    border-top: 1px solid {BORDER_CLR};
}}
/* Style the auto-generated "Footnotes" h3 heading */
.footnote > h3, div.footnote > h3 {{
    font-family: {HEADER_FONT};
    font-size: 8.5pt; font-weight: 700;
    color: {MUTED_CLR}; text-transform: uppercase;
    letter-spacing: 1.5px; margin-bottom: 0.06in;
    border: none;
}}
.footnote ol {{ margin-left: 0.15in; }}
.footnote li {{ margin: 0.04in 0; line-height: 1.5; }}
.footnote li p {{ margin: 0; }}
sup {{ font-size: 7pt; color: {ACCENT_CYAN}; vertical-align: super; line-height: 0; }}
sup a {{ color: {ACCENT_CYAN}; text-decoration: none; }}
a.footnote-ref {{ color: {ACCENT_CYAN}; font-size: 7.5pt; }}
a.footnote-backref {{ color: {MUTED_CLR}; font-size: 7pt; }}

/* ── Graphs ───────────────────────────────────────────────────────────────── */
.graph-figure {{
    text-align: center; margin: 0.25in 0;
    page-break-inside: avoid;
    page-break-before: auto;
    max-width: 100%;
    overflow: visible;
}}
.graph-figure img {{
    max-width: 100%; width: 100%; height: auto;
    border: 1px solid {BORDER_CLR};
    border-radius: 4px;
    display: block; margin: 0 auto;
    resize: both;
    overflow: auto;
    min-width: 200px;
    min-height: 100px;
}}
.graph-figure .caption {{
    font-size: 8.5pt; color: {MUTED_CLR};
    font-family: {HEADER_FONT};
    margin-top: 0.06in;
    font-style: italic;
}}

/* ── Legacy page-frame / footer (HTML view only) ─────────────────────────── */
.page-footer {{
    display: none;
}}
@media screen {{
    body {{ padding: clamp(0.15in, 2vw, 0.5in); max-width: min(9in, 95vw); margin: 0 auto; }}
    .page-footer {{
        display: block;
        text-align: center;
        font-family: {HEADER_FONT};
        font-size: 7.5pt; color: {MUTED_CLR};
        padding: 0.2in 0; margin-top: 0.5in;
        border-top: 1px solid {BORDER_CLR};
    }}
}}
@media screen and (max-width: 600px) {{
    body {{ padding: 0.1in; max-width: 100vw; }}
    html {{ font-size: 16px; }}
    .content table {{ font-size: 11px; }}
    .content pre {{ font-size: 10px; }}
    .graph-figure img {{ resize: none; }}
}}
"""

# ── HTML builder ────────────────────────────────────────────────────────────

def strip_chapter_prefix(title):
    return re.sub(r"^Chapter\s+\d+[\s:\u2014-]*", "", title).strip()

def build_html(chapters, graph_paths, theme="dark"):
    graph_by_ch = {}
    for gp in graph_paths:
        key = GRAPH_CHAPTER_MAP.get(gp.stem)
        if key:
            graph_by_ch[key] = gp

    total_chapters = len([c for c in chapters if c["ch_num"] > 0])
    total_appendix = len([c for c in chapters if c["ch_num"] == 0])
    vol_count = len(set(c["vol_label"] for c in chapters if c["vol_num"] < 8))

    css = build_css_light() if theme == "light" else build_css()

    parts = []
    parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style>{css}</style>
</head>
<body>""")

    # ── Cover ──
    parts.append(f"""
<div class="cover">
  <div class="shield">&#x1f6e1;</div>
  <h1>The Complete Privacy<br>Researcher's Handbook</h1>
  <div class="subtitle">Two-Phone Strategy &amp; Forensic Threat Model<br>
  A rigorous, evidence-based resource for privacy researchers,<br>
  journalists, and security professionals</div>
  <div class="version">Version {VERSION} &mdash; {datetime.now().strftime('%B %d, %Y')}</div>
  <div class="meta">
    {vol_count} Volumes &middot; {total_chapters} Chapters &middot; {len(graph_paths)} Forensic Graphs &middot; {total_appendix} Appendices
  </div>
  <div class="classification">&#x26a0; Educational &amp; Threat Modeling Purposes Only</div>
</div>""")

    # (No page-frame wrapper — @page margins handle spacing in PDF)

    # ── TOC ──
    parts.append('<div class="toc"><h2>Table of Contents</h2>')
    cur_vol = None
    for ch in chapters:
        vl = ch["vol_label"]
        if vl != cur_vol:
            if cur_vol is not None:
                parts.append("</div>")
            cur_vol = vl
            parts.append(f'<div class="vol-group"><div class="vol-label">{vl}</div>')
        cn = ch["ch_num"]
        anchor = f"v{ch['vol_num']}ch{cn}" if cn else f'app-{ch["dir_name"]}'
        num_str = f"Chapter {cn}" if cn else ""
        toc_title = strip_chapter_prefix(ch["title"])
        label = f"{num_str} {toc_title}".strip()
        parts.append(
            f'<div class="ch-entry">'
            f'<a href="#{anchor}">{label}</a>'
            f'<span class="ch-dots"></span>'
            f'</div>'
        )
    if cur_vol is not None:
        parts.append("</div>")
    parts.append('</div>')

    # ── Chapters ──
    for ch in chapters:
        anchor = f'v{ch["vol_num"]}ch{ch["ch_num"]}' if ch["ch_num"] else f'app-{ch["dir_name"]}'
        is_appendix = ch["vol_label"] == "Appendices"
        num_str = f"Chapter {ch['ch_num']}" if ch["ch_num"] else ""
        clean_title = strip_chapter_prefix(ch["title"])

        parts.append(f"""<div class="chapter {"appendix-group" if is_appendix else ""}" id="{anchor}">
<div class="chapter-header">
<div class="chapter-number">{num_str}</div>
<div class="chapter-title">{clean_title}</div>
<div class="chapter-volume">{ch["vol_label"]}</div>
</div><div class="content">""")

        body = ch["text"]
        body = re.sub(r"^#\s+.+$", "", body, count=1, flags=re.MULTILINE)
        body = body.strip()
        html_body = md_lib.markdown(
            body,
            extensions=["extra", "codehilite", "tables", "footnotes", "toc"],
            extension_configs={
                "codehilite": {"guess_lang": False, "noclasses": False},
                "footnotes": {"BACKLINK_TEXT": "&#8617;"},
            },
        )
        parts.append(html_body)

        graph_path = graph_by_ch.get((ch["vol_num"], ch["ch_num"]))
        if graph_path:
            parts.append(f"""<p style="text-align:center;font-style:italic;color:{MUTED_CLR};margin:0.15in 0 0.05in 0">See Figure below</p>""")
            parts.append(f"""<div class="graph-figure">
<img src="graphs/{graph_path.name}" alt="{ch["title"]}">
<div class="caption">{ch["title"]}</div>
</div>""")

        parts.append("</div></div>")

    parts.append("""
  <div class="page-footer">
    Privacy Researcher's Handbook v""" + VERSION + """ &mdash; &#x25cf; Page <span class="page-num"></span>
  </div>
</body>
</html>""")
    return "\n".join(parts)

# ── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(
        description="Compile the Privacy Researcher's Handbook into a professional PDF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 compile_handbook.py                        # Full compile (HTML + PDF, dark theme)
  python3 compile_handbook.py --no-pdf               # HTML only
  python3 compile_handbook.py --no-graphs            # Skip graph generation
  python3 compile_handbook.py --theme light          # Print-ready light theme
  python3 compile_handbook.py --epub                 # Also generate EPUB via pandoc
  python3 compile_handbook.py --output out/ --no-pdf
        """)
    ap.add_argument("--output", "-o", default=str(PDF_FILE),
                    help=f"Output path (default: {PDF_FILE}). If a directory, filename is inferred.")
    ap.add_argument("--no-pdf", action="store_true",
                    help="Only generate HTML, skip PDF conversion")
    ap.add_argument("--no-graphs", action="store_true",
                    help="Skip graph generation (use existing PNGs)")
    ap.add_argument("--theme", choices=["dark", "light"], default="dark",
                    help="Color theme: dark (screen, default) or light (print-ready)")
    ap.add_argument("--epub", action="store_true",
                    help="Also generate EPUB via pandoc (requires pandoc in PATH)")
    ap.add_argument("--version", action="version",
                    version=f"%(prog)s {VERSION}")
    args = ap.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    # Resolve output path: if a directory, append default filename
    output_path = Path(args.output)
    if output_path.is_dir():
        output_path = output_path / PDF_FILE.name

    # ── Generate graphs ──
    graph_paths = []
    if not args.no_graphs:
        print(f"[*] Generating {len(GRAPH_FUNCTIONS)} forensic graphs...")
        for fn in GRAPH_FUNCTIONS:
            try:
                graph_paths.append(fn())
            except Exception as e:
                print(f"  [\u2717] {fn.__name__}: {e}")
        print(f"  -> {len(graph_paths)} graphs saved to {GRAPH_DIR}")
    else:
        for gp in sorted(GRAPH_DIR.glob("graph*.png")):
            graph_paths.append(gp)

    # ── Read chapters ──
    print("[*] Reading chapters...")
    chapters = read_all_chapters()
    ch_count = len([c for c in chapters if c["ch_num"] > 0])
    app_count = len([c for c in chapters if c["ch_num"] == 0])
    print(f"  -> {ch_count} chapters + {app_count} appendices found")

    # ── Build HTML ──
    print(f"[*] Building HTML document (theme: {args.theme})...")
    html = build_html(chapters, graph_paths, theme=args.theme)
    HTML_FILE.write_text(html, "utf-8")
    print(f"  -> Saved {HTML_FILE}")

    # ── PDF ──
    if not args.no_pdf:
        if not PDF_AVAILABLE:
            print("  [\u2717] WeasyPrint not available. Install with: pip install weasyprint")
            print(f"  -> HTML available at: {HTML_FILE}")
            return
        print("[*] Converting to PDF (this may take a minute)...")
        try:
            from weasyprint import HTML
            pdf_path = output_path
            # Use filename= (not string=) so WeasyPrint resolves relative
            # image paths (graphs/*.png) relative to the HTML file's directory.
            HTML(filename=str(HTML_FILE)).write_pdf(str(pdf_path))
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            print(f"  [\u2713] PDF saved: {pdf_path} ({size_mb:.1f} MB)")
        except Exception as e:
            print(f"  [\u2717] PDF conversion failed: {e}")
            print(f"  -> HTML available at: {HTML_FILE}")
    else:
        print(f"[*] HTML available at: {HTML_FILE}")

    # ── EPUB ──
    if args.epub:
        epub_path = output_path.with_suffix(".epub")
        print("[*] Generating EPUB via pandoc...")
        try:
            result = subprocess.run(
                [
                    "pandoc",
                    str(HTML_FILE),
                    "-f", "html",
                    "-t", "epub3",
                    "--metadata", "title=The Complete Privacy Researcher's Handbook",
                    "--metadata", "author=Privacy Research Collective",
                    "--metadata", f"date={datetime.now().strftime('%Y-%m-%d')}",
                    "--toc",
                    "--toc-depth=2",
                    "-o", str(epub_path),
                ],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                size_mb = epub_path.stat().st_size / (1024 * 1024)
                print(f"  [\u2713] EPUB saved: {epub_path} ({size_mb:.1f} MB)")
            else:
                print(f"  [\u2717] pandoc error: {result.stderr.strip()}")
        except FileNotFoundError:
            print("  [\u2717] pandoc not found. Install from https://pandoc.org/installing.html")

    print("[*] Done.")

if __name__ == "__main__":
    main()
