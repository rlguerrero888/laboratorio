# Power BI Assessment | Pre-Session Preparation

To make the most of our time together, we are sharing the dataset with you in advance.

## Context

You are working with shipment data from a distribution center network. The dataset comes from a layer equivalent to **Bronze** in the project's Medallion Architecture: raw, untransformed data with potential source inconsistencies.


---

## Dataset

`powerbi/data/synth_dataset.xlsx`

| Sheet | Description |
|---|---|
| `shipments` | One record per shipment|
| `date` | Calendar dimension |
| `warehouse` | Distribution centers |
| `customer` | Customer catalog |


---

## Part 1 — Explore the Data

- What anomalies or inconsistencies do you spot in the data?
- Is there anything in the structure that raises a flag when thinking about modeling?

There are no right or wrong answers.

---

## Part 2 — DAX Warm-Up

Load `shipments` into Power BI and write the following basic measures. No relationships needed yet, just practice writing DAX against a single table.

| # | Measure | Expected DAX |
|---|---|---|
| 1 | Total Shipments | `COUNTROWS(fact_shipments)` |
| 2 | Total Units Shipped | `SUM(fact_shipments[qty_shipped])` |
| 3 | Total Units Ordered | `SUM(fact_shipments[qty_ordered])` |
| 4 | Average Freight Cost | `AVERAGE(fact_shipments[freight_cost])` |
| 5 | Total Freight Cost | `SUM(fact_shipments[freight_cost])` |


> These are the building blocks for tomorrow's session. If any of them feel unfamiliar, review the [DAX basics documentation](https://learn.microsoft.com/en-us/dax/dax-overview) before the session.

---