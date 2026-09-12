# Valuation Methods in Corporate Finance: A Comparative Toolkit

**Author:** Marc Aliaga — International Finance, MGIMO University, Moscow
**Website:** [marcaliaga.com](https://marcaliaga.com)

---

## Overview

This repository implements and compares classical and stochastic methods for corporate valuation, pairing each with a short academic paper covering its theoretical derivation. It is intended as a research and teaching reference: a bridge between the mathematics of valuation theory and reproducible code.

Each method is self-contained and includes:

* `algorithm.py` — executable Python implementation of the model
* a companion paper (`.pdf`) — the underlying mathematics and methodology

## Repository Structure

```
Valuation/
├── Discounted_Cash_Flow/
│   ├── CAPM/                     # Cost of equity / WACC estimation under the Capital Asset Pricing Model
│   │   ├── algorithm.py
│   │   └── CAPM_paper.pdf
│   └── Certainty-Equivalent/     # Risk-adjusted discounting via the certainty-equivalent method
│       ├── algorithm.py
│       └── Certanity_Equivalent_paper.pdf
│
├── Dynamic_Firm_valuation/       # Dynamic dividend discount model for firms without stable cash flows
│   ├── alogrithm.py
│   └── DDM-Valuation-paper.pdf
│
├── Case_Studies/                 # Applied valuations of real companies, built on the methods above
│   ├── _template/                # Copy this folder to start a new case study
│   └── <Company_Year>/           # e.g. Apple_2026/
│       ├── model.py / model.xlsx
│       ├── assumptions.md
│       └── output.md
│
└── logo.png
```

## Case Studies

Beyond the general-purpose implementations above, this repository includes applied valuations of individual public and private companies, using the DCF and Dynamic Firm Valuation methods on real (or realistically calibrated) inputs. Each case study documents its assumptions and sources separately from the model itself, so the reasoning behind every input is auditable. See `Case_Studies/_template/` for the structure used to add a new one.

## Methods Covered

| Method                   | Requires Historical Cash Flows | Applicable to Early-Stage Firms |
| ------------------------ | ------------------------------- | -------------------------------- |
| DCF — CAPM                | Yes                              | Limited                          |
| DCF — Certainty-Equivalent | Yes                             | Limited                          |
| Dynamic Firm Valuation (DDM) | No                          | Yes                               |

The Discounted Cash Flow implementations follow standard corporate finance theory (CAPM cost of capital; certainty-equivalent risk adjustment). The Dynamic Firm Valuation model follows Lazzati & Menichini (2018), *A Dynamic Model of Firm Valuation*, The Financial Review — a framework designed for private firms, pre-IPO companies, and new ventures where historical dividends or cash flows are unavailable.

## Academic Foundation

**Lazzati, A. & Menichini, A. A. (2018).** *A Dynamic Model of Firm Valuation.* The Financial Review.

> Applicable to private firms, pre-IPO valuations, and new projects lacking a dividend or cash-flow history.

## Quick Start

```bash
git clone https://github.com/marcaliaga/valuation-toolkit.git
cd valuation-toolkit

pip install numpy

python "Valuation/Dynamic_Firm_valuation/alogrithm.py"
```

## Citation

```bibtex
@misc{aliaga2026valuationtoolkit,
  title     = {Valuation Methods in Corporate Finance: A Comparative Toolkit},
  author    = {Aliaga, Marc},
  year      = {2026},
  note      = {MGIMO University, Moscow},
  url       = {https://marcaliaga.com}
}
```

## About the Author

**Marc Aliaga** studies International Finance at MGIMO University, Moscow. Research articles and further work are published at [marcaliaga.com](https://marcaliaga.com).

## License

MIT License — free for academic and commercial use.
© 2026 Marc Aliaga
