# Mango Chatbot Quality Audit

**Exploratory evaluation of Mango's Spanish-language customer-service chatbot**

Portfolio project developed as part of the Máster LEIA (Language and Artificial Intelligence), Universidad Autónoma de Madrid.

## Project overview

This project evaluates how a customer-service chatbot handles common e-commerce questions in Spanish. A manually designed test set of **30 interactions across eight categories** was collected and assessed with a five-criterion rubric. The responses were scored from 1 to 4 on accuracy, relevance, linguistic quality, tone, and handling of complex queries.

The goal is to identify response-quality patterns and formulate practical improvement recommendations. This is an exploratory audit of a limited sample, not a comprehensive benchmark of Mango's chatbot or its underlying technology.

## Key results

- **30** interactions, recorded between 13 and 16 November 2026.
- **8** query categories.
- **5** evaluation criteria, equally weighted; composite score out of 20.
- **12.97/20** mean composite score ("Mejorable" band in the project's rubric).
- Highest criterion means: accuracy and relevance (**2.83/4** each).
- Lowest criterion means: complex-query handling (**2.33/4**) and tone (**2.37/4**).
- Highest category means: complaints (**17.75/20**, n=4) and payments (**17.33/20**, n=3).
- Lowest category means: orders (**7.75/20**, n=4) and complex queries (**10.20/20**, n=5).
- Score bands: 6 insufficient, 11 needs improvement, 9 good, and 4 excellent.

These results are descriptive and should be interpreted in light of the small, uneven category sizes.

## Methodology

1. Designed 30 prompts in Spanish covering shipping, returns, orders, products, payments, availability, complaints, and complex queries.
2. Captured the chatbot's full responses and recorded the test dates.
3. Applied a rubric with five equally weighted criteria, each scored from 1 (insufficient) to 4 (excellent).
4. Calculated per-interaction totals (5-20), criterion means, category means, and the distribution across the rubric's four performance bands.

The detailed rubric is included in `data/`. The data dictionary is available in [`data_dictionary.md`](data_dictionary.md).

## Reproduce the analysis

Requires Python 3.10+ (or a compatible newer version). From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/analyze_chatbot.py
```

The script validates the dataset, exports summary CSV files to `outputs/`, regenerates the three detailed report figures in `figures/`, and creates three complementary charts in `charts/`. The final editable report is provided as a DOCX in `report/` (no PDF is included). The complementary charts show the same aggregates in a simpler format; they are not additional observations.

## Repository structure

```text
chatbot-quality-audit/
├── data/       # Scored dataset and evaluation rubric
├── figures/    # Three detailed report figures
├── charts/     # Three complementary Python/pandas charts
├── outputs/    # Criterion, category, band and interaction summaries
├── report/     # Final report (editable DOCX)
├── scripts/    # Reproducible pandas/Matplotlib analysis
├── data_dictionary.md
├── requirements.txt
└── README.md
```

## Visualizations

The repository preserves two complementary visual sets: three detailed figures embedded in the report, and three additional charts created during the analysis workflow with Python, pandas and Matplotlib. Both sets summarize the same 30 interactions and the same aggregated scores; the additional charts offer a simpler visual presentation rather than a separate analysis sample.

## Main findings and improvement opportunities

The sample suggests that the chatbot performed better on some focused transactional questions (notably complaints and payments) than on order-related and multi-step queries. Several low-scoring order and complex-query interactions entered an email-identification or validation flow without resolving the original request. The weakest criterion mean was handling complex queries, followed closely by tone.

Recommendations include improving recovery from repeated identity-validation loops, asking only for the information needed to progress a case, giving clearer next steps, and testing multi-step order scenarios with regression prompts.

## Limitations

- Small sample (30 prompts) with uneven category sizes (3-5 interactions per category).
- Manually designed prompts; the set is not a representative sample of all customer requests.
- Scores were assigned by one evaluator using a defined rubric; no inter-rater reliability test was performed.
- The chatbot was observed as a black box: no access to its model, system prompts, internal knowledge base, logs, or escalation tooling.
- No repeated trials or controlled prompt variants were used to measure response variability.
- Results reflect a short collection window (13-16 November 2026) and may change as the service is updated.
- Response time was intentionally excluded from the analysis.

## Tools

Python · pandas · Matplotlib · Excel · Git · GitHub

## Project status

Exploratory audit and first analysis completed. Further work could expand the test set, repeat prompts, and introduce a second evaluator before drawing broader conclusions.
