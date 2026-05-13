#!/usr/bin/env python3
"""
Stock scorecard data fetcher.

Pulls real financial data from Yahoo Finance to keep scorecard metrics
grounded in actual numbers instead of AI memory.

Usage:
  python scorecard_data.py GOOGL AMZN MSFT          # markdown table
  python scorecard_data.py --json GOOGL AMZN         # JSON output
  python scorecard_data.py --all                     # all scorecard tickers
  python scorecard_data.py --update-seed             # patch stock_scorecard.jsx

Requires:
  pip install yfinance
  Python 3.9+ (for yfinance compatibility)
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional

import yfinance as yf


# All tickers from the stock scorecard SEED data
SCORECARD_TICKERS = [
    "MSFT", "META", "GOOG", "ANET", "7741.T", "TSM", "ASML",
    "AVGO", "4975.T", "KLAC", "CDNS", "SNPS", "6857.T", "AMZN",
    "BESI.AS", "CRDO", "MRVL", "CAMT", "GLW", "AMAT", "LRCX",
    "FN", "COHR", "LITE", "VRT", "MTSI", "6920.T",
]


@dataclass
class StockData:
    """Container for fetched financial data."""
    ticker: str
    company: str = ""
    currency: str = "USD"
    fetch_date: str = ""

    # Price data
    price: Optional[float] = None
    market_cap: Optional[float] = None

    # Valuation
    pe: Optional[float] = None
    fwd_pe: Optional[float] = None
    peg: Optional[float] = None
    ev_ebitda: Optional[float] = None

    # Profitability
    gross_margin: Optional[float] = None  # percentage
    op_margin: Optional[float] = None     # percentage
    roe: Optional[float] = None           # percentage

    # Earnings
    eps_ttm: Optional[float] = None
    eps_fwd: Optional[float] = None
    book_value: Optional[float] = None

    # Growth
    rev_growth_ttm: Optional[float] = None   # percentage
    rev_growth_3yr: Optional[float] = None   # percentage (CAGR)
    revenue_ttm: Optional[float] = None

    # Balance sheet
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    free_cash_flow: Optional[float] = None

    # Dividend
    dividend_yield: Optional[float] = None

    # Meta
    sector: str = ""
    industry: str = ""
    errors: list = field(default_factory=list)


class ScorecardFetcher:
    """Fetches financial data from Yahoo Finance for scorecard updates."""

    def fetch(self, ticker: str) -> StockData:
        """Fetch all available financial data for a single ticker."""
        data = StockData(
            ticker=ticker,
            fetch_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        try:
            stock = yf.Ticker(ticker)
            info = stock.info or {}
        except Exception as e:
            data.errors.append(f"Failed to fetch info: {e}")
            return data

        if not info or info.get("trailingPegRatio") is None and info.get("currentPrice") is None:
            # Might have gotten an empty/error response
            if not info.get("shortName"):
                data.errors.append("No data returned (ticker may be invalid)")
                return data

        # Basic info
        data.company = info.get("longName") or info.get("shortName") or ""
        data.currency = info.get("currency") or "USD"
        data.sector = info.get("sector") or ""
        data.industry = info.get("industry") or ""

        # Price
        data.price = _get(info, "currentPrice", "regularMarketPrice")
        data.market_cap = info.get("marketCap")

        # Valuation ratios
        data.pe = info.get("trailingPE")
        data.fwd_pe = info.get("forwardPE")
        data.peg = info.get("trailingPegRatio") or info.get("pegRatio")
        data.ev_ebitda = info.get("enterpriseToEbitda")

        # Profitability (Yahoo returns as decimals, convert to %)
        data.gross_margin = _pct(info.get("grossMargins"))
        data.op_margin = _pct(info.get("operatingMargins"))
        data.roe = _pct(info.get("returnOnEquity"))

        # Earnings
        data.eps_ttm = info.get("trailingEps")
        data.eps_fwd = info.get("forwardEps")
        data.book_value = info.get("bookValue")

        # Revenue
        data.revenue_ttm = info.get("totalRevenue")
        data.rev_growth_ttm = _pct(info.get("revenueGrowth"))

        # 3-year revenue CAGR from annual financials
        data.rev_growth_3yr = self._compute_revenue_cagr(stock, years=3)

        # Balance sheet
        de = info.get("debtToEquity")
        if de is not None:
            data.debt_to_equity = round(de / 100, 2)  # Yahoo gives as %, normalize
        data.current_ratio = info.get("currentRatio")
        data.free_cash_flow = info.get("freeCashflow")

        # Dividend — use trailingAnnualDividendYield (true decimal) over
        # dividendYield (which Yahoo inconsistently formats)
        dy = info.get("trailingAnnualDividendYield")
        data.dividend_yield = _pct(dy)

        return data

    def fetch_many(self, tickers: list[str], delay: float = 0.3) -> list[StockData]:
        """Fetch data for multiple tickers with rate-limit friendly delays."""
        results = []
        for i, ticker in enumerate(tickers, 1):
            print(f"[{i}/{len(tickers)}] Fetching {ticker}...", file=sys.stderr)
            results.append(self.fetch(ticker))
            if i < len(tickers):
                time.sleep(delay)
        return results

    def fetch_all(self) -> list[StockData]:
        """Fetch data for all scorecard tickers."""
        return self.fetch_many(SCORECARD_TICKERS)

    def _compute_revenue_cagr(self, stock: yf.Ticker, years: int = 3) -> Optional[float]:
        """Compute revenue CAGR from annual income statement."""
        try:
            financials = stock.financials
            if financials is None or financials.empty:
                return None

            # Look for revenue row
            rev_row = None
            for label in ["Total Revenue", "Revenue", "Operating Revenue"]:
                if label in financials.index:
                    rev_row = financials.loc[label]
                    break

            if rev_row is None or len(rev_row) < 2:
                return None

            # Sort by date (most recent first)
            rev_row = rev_row.sort_index(ascending=False)
            values = [v for v in rev_row.values if v is not None and v > 0]

            if len(values) < 2:
                return None

            n = min(years, len(values) - 1)
            recent = values[0]
            older = values[n]

            if older <= 0:
                return None

            cagr = ((recent / older) ** (1 / n) - 1) * 100
            return round(cagr, 1)

        except Exception:
            return None


# ---------- helpers ----------

def _get(info: dict, *keys):
    """Return first non-None value from info dict."""
    for k in keys:
        v = info.get(k)
        if v is not None:
            return v
    return None


def _pct(value) -> Optional[float]:
    """Convert decimal ratio to percentage, rounded."""
    if value is None:
        return None
    return round(value * 100, 1)


def _fmt(value, fmt: str = ".1f", suffix: str = "") -> str:
    """Format a value for display, handling None."""
    if value is None:
        return "—"
    if fmt == "cap":
        if abs(value) >= 1e12:
            return f"${value/1e12:.2f}T"
        if abs(value) >= 1e9:
            return f"${value/1e9:.1f}B"
        if abs(value) >= 1e6:
            return f"${value/1e6:.0f}M"
        return f"${value:,.0f}"
    return f"{value:{fmt}}{suffix}"


# ---------- output formatters ----------

def to_markdown_table(results: list[StockData]) -> str:
    """Format results as a markdown comparison table."""
    lines = []
    lines.append(f"# Stock Data — {datetime.now().strftime('%Y-%m-%d')}\n")

    lines.append("| Ticker | Price | P/E | Fwd P/E | PEG | EV/EBITDA | GM% | Op% | ROE% | Rev Gr% | 3yr CAGR% | Mkt Cap |")
    lines.append("|--------|-------|-----|---------|-----|-----------|-----|-----|------|---------|-----------|---------|")

    for d in results:
        lines.append(
            f"| **{d.ticker}** "
            f"| {_fmt(d.price, '.2f')} "
            f"| {_fmt(d.pe)} "
            f"| {_fmt(d.fwd_pe)} "
            f"| {_fmt(d.peg, '.2f')} "
            f"| {_fmt(d.ev_ebitda)} "
            f"| {_fmt(d.gross_margin, '.1f')} "
            f"| {_fmt(d.op_margin, '.1f')} "
            f"| {_fmt(d.roe, '.1f')} "
            f"| {_fmt(d.rev_growth_ttm, '.1f')} "
            f"| {_fmt(d.rev_growth_3yr, '.1f')} "
            f"| {_fmt(d.market_cap, 'cap')} |"
        )

    errors = [(d.ticker, d.errors) for d in results if d.errors]
    if errors:
        lines.append("\n### Fetch Errors\n")
        for ticker, errs in errors:
            for e in errs:
                lines.append(f"- **{ticker}**: {e}")

    return "\n".join(lines)


def to_json(results: list[StockData]) -> str:
    """Format results as JSON."""
    return json.dumps([asdict(d) for d in results], indent=2, default=str)


def to_detail(data: StockData) -> str:
    """Format a single stock's data as a detailed card."""
    lines = [
        f"## {data.ticker} — {data.company}",
        f"_Fetched: {data.fetch_date} | {data.sector} > {data.industry}_\n",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Price | {_fmt(data.price, '.2f')} {data.currency} |",
        f"| Market Cap | {_fmt(data.market_cap, 'cap')} |",
        f"| P/E (TTM) | {_fmt(data.pe)} |",
        f"| Forward P/E | {_fmt(data.fwd_pe)} |",
        f"| PEG | {_fmt(data.peg, '.2f')} |",
        f"| EV/EBITDA | {_fmt(data.ev_ebitda)} |",
        f"| Gross Margin | {_fmt(data.gross_margin, '.1f')}% |",
        f"| Operating Margin | {_fmt(data.op_margin, '.1f')}% |",
        f"| ROE | {_fmt(data.roe, '.1f')}% |",
        f"| EPS (TTM) | {_fmt(data.eps_ttm, '.2f')} |",
        f"| EPS (Forward) | {_fmt(data.eps_fwd, '.2f')} |",
        f"| Book Value | {_fmt(data.book_value, '.2f')} |",
        f"| Revenue (TTM) | {_fmt(data.revenue_ttm, 'cap')} |",
        f"| Rev Growth (TTM) | {_fmt(data.rev_growth_ttm, '.1f')}% |",
        f"| Rev Growth (3yr CAGR) | {_fmt(data.rev_growth_3yr, '.1f')}% |",
        f"| D/E Ratio | {_fmt(data.debt_to_equity, '.2f')} |",
        f"| Free Cash Flow | {_fmt(data.free_cash_flow, 'cap')} |",
        f"| Dividend Yield | {_fmt(data.dividend_yield, '.1f')}% |",
    ]

    if data.errors:
        lines.append(f"\n⚠️ Errors: {'; '.join(data.errors)}")

    return "\n".join(lines)


# ---------- seed updater ----------

def update_seed_file(results: list[StockData], jsx_path: str = "stock_scorecard.jsx"):
    """
    Update numeric fields in stock_scorecard.jsx SEED data.
    Preserves all qualitative scores, notes, bull/bear cases.
    Only updates: price, date, pe, fwd_pe, peg, ev_ebitda,
    gross_margin, op_margin, roe, rev_growth_ttm, rev_growth_3yr.
    """
    with open(jsx_path, "r", encoding="utf-8") as f:
        content = f.read()

    lookup = {d.ticker: d for d in results if d.price is not None}
    today = datetime.now().strftime("%Y-%m-%d")
    updates = 0

    for ticker, d in lookup.items():
        ticker_esc = re.escape(ticker)
        if not re.search(rf'ticker:"{ticker_esc}"', content):
            print(f"  ! {ticker}: not found in SEED data", file=sys.stderr)
            continue

        # Update price and date
        content = _replace_field(content, ticker, "price", f'"{_fmt_price(d.price)}"')
        content = _replace_field(content, ticker, "date", f'"{today}"')

        # Update numeric metrics
        metric_updates = {
            "pe": d.pe,
            "fwd_pe": d.fwd_pe,
            "peg": d.peg,
            "ev_ebitda": d.ev_ebitda,
            "gross_margin": d.gross_margin,
            "op_margin": d.op_margin,
            "roe": d.roe,
            "rev_growth_ttm": d.rev_growth_ttm,
            "rev_growth_3yr": d.rev_growth_3yr,
        }

        for key, value in metric_updates.items():
            if value is not None:
                if key == "peg":
                    formatted = f"{value:.2f}"
                elif key in ("pe", "fwd_pe", "ev_ebitda"):
                    formatted = str(int(value)) if value == int(value) else f"{value:.1f}"
                else:
                    formatted = str(int(value)) if value == int(value) else f"{value:.1f}"
                content = _replace_metric(content, ticker, key, formatted)

        updates += 1
        print(f"  ✓ {ticker}: updated ({_fmt_price(d.price)} {d.currency})", file=sys.stderr)

    with open(jsx_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\nUpdated {updates}/{len(lookup)} tickers in {jsx_path}", file=sys.stderr)


def _fmt_price(price: float) -> str:
    """Format price for SEED data."""
    if price >= 1000:
        return f"{price:,.0f}"
    return f"{price:.2f}"


def _replace_field(content: str, ticker: str, field_name: str, value: str) -> str:
    """Replace a top-level field in a SEED entry (e.g., price:"xxx")."""
    ticker_esc = re.escape(ticker)
    pattern = rf'(ticker:"{ticker_esc}"[^}}]*?){field_name}:"[^"]*"'
    replacement = rf'\g<1>{field_name}:{value}'
    result = re.sub(pattern, replacement, content)
    if result == content:
        pattern = rf'(ticker:"{ticker_esc}"[^}}]*?){field_name}:[^,}}]+'
        replacement = rf'\g<1>{field_name}:{value}'
        result = re.sub(pattern, replacement, content)
    return result


def _replace_metric(content: str, ticker: str, metric: str, value: str) -> str:
    """Replace a metric value inside the metrics:{} block of a SEED entry."""
    ticker_esc = re.escape(ticker)
    pattern = rf'(ticker:"{ticker_esc}"[^}}]*?metrics:\{{[^}}]*?){metric}:[^,}}]+'
    replacement = rf'\g<1>{metric}:{value}'
    return re.sub(pattern, replacement, content)


# ---------- CLI ----------

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch financial data for stock scorecard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scorecard_data.py GOOGL AMZN MSFT      # markdown table
  python scorecard_data.py --json GOOGL          # JSON output
  python scorecard_data.py --detail GOOGL        # detailed single-stock view
  python scorecard_data.py --all                 # all scorecard tickers
  python scorecard_data.py --update-seed         # update stock_scorecard.jsx
        """,
    )
    parser.add_argument("tickers", nargs="*", help="Ticker symbols to fetch")
    parser.add_argument("--all", action="store_true", help="Fetch all scorecard tickers")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--detail", action="store_true", help="Detailed single-stock view")
    parser.add_argument("--update-seed", action="store_true",
                        help="Update stock_scorecard.jsx with fresh data")
    parser.add_argument("--seed-file", default="stock_scorecard.jsx",
                        help="Path to scorecard JSX file (default: stock_scorecard.jsx)")

    args = parser.parse_args()

    fetcher = ScorecardFetcher()

    if args.all or args.update_seed:
        tickers = SCORECARD_TICKERS
    elif args.tickers:
        tickers = [t.upper() if not t.endswith(".T") and not t.endswith(".AS")
                   else t for t in args.tickers]
    else:
        parser.print_help()
        sys.exit(1)

    results = fetcher.fetch_many(tickers)

    if args.update_seed:
        update_seed_file(results, args.seed_file)
        print(to_markdown_table(results))
    elif args.json:
        print(to_json(results))
    elif args.detail:
        for d in results:
            print(to_detail(d))
            print("\n---\n")
    else:
        print(to_markdown_table(results))


if __name__ == "__main__":
    main()
