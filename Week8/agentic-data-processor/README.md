# Week 8: Agentic Data Processing (Advanced CSV & JSON Workflows)

A config-driven "Data Agent" that runs a pipeline of CSV/JSON tasks defined in
`configs/data_pipeline_config.json`, passing data between tasks through an internal `data_store`.

## Run
```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
python main.py
```
No third-party libraries are required (only built-in `csv` and `json`).

## Outputs
- `data/processed_sales_by_customer.csv` – sales aggregated per customer
- `data/sales_data.json` – raw sales converted to JSON
- `data/updated_inventory.json` – inventory after updates + new product
- `reports/audit_report_*.json` – audit log of every task

## Structure
```
src/   data_agent.py, csv_tasks.py, json_tasks.py, conversion_tasks.py, config_parser.py, utils.py
configs/data_pipeline_config.json
data/  input_sales.csv, input_inventory.json (+ generated outputs)
main.py
```
