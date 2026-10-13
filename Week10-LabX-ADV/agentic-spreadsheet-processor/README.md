
# Week 16: Advanced Spreadsheet Automation &amp; Agentic Workflows

This project implements an &quot;Agentic Spreadsheet Processor&quot; that performs a series of complex
tasks on Excel `.xlsx` files based on a declarative JSON configuration. It showcases advanced
`openpyxl` features like charts, conditional formatting, and formula application within a robust,
task-driven automation framework.

## Key Concepts Demonstrated

* **`openpyxl` Advanced Features**:
* Programmatic creation of **charts** (Bar, Line, Pie).
* Applying **conditional formatting** (color scales, data bars, custom formulas).
* Inserting and managing **Excel formulas**.
* Basic sheet and cell manipulation.
* **Agentic Design with Configuration**: The core logic is driven by an
  `example_spreadsheet_config.json` file, which defines a sequence of tasks (e.g., `copy_data`,
  `calculate_column`, `conditional_format`, `chart`). This allows for highly flexible and reusable
  automation workflows.
* **Modular Code Structure**: Separation of concerns into `spreadsheet_agent.py`,
  `config_parser.py`, `utils.py`, enhancing maintainability and scalability.
* **Robustness**: Includes comprehensive error handling for file operations and `openpyxl`
  interactions, with detailed logging.
* **Audit Logging**: Generates a dedicated &quot;Audit Log&quot; sheet in the output workbook, recording
  every step of the agent&#39;s execution, including successes and failures.

## Setup &amp; How to Run

1. **Clone the repository:**

```bash

git clone [https://github.com/YOUR_USERNAME/agentic-spreadsheet-
processor.git](https://github.com/YOUR_USERNAME/agentic-spreadsheet-processor.git)
cd agentic-spreadsheet-processor
```

2. **Install Dependencies:**
   It&#39;s highly recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate.bat
pip install openpyxl
```

3. **Prepare Input Data:**

* Create a folder named `data` in the root of your project: `mkdir data`.
* Inside the `data` folder, create an Excel file named `input_data.xlsx`.
* Populate `input_data.xlsx` with sample sales data in a sheet named `SalesData`. The columns should
  be &quot;Product Name&quot;, &quot;Quantity&quot;, and &quot;Unit Price&quot;.
  **Example `data/input_data.xlsx` content (Sheet: `SalesData`):**| Product Name | Quantity | Unit Price |
  | :----------- | :------- | :--------- |
  | Laptop       | 2        | 1200.50    |
  | Mouse        | 5        | 25.00      |
  | Keyboard     | 3        | 75.99      |
  | Monitor      | 1        | 300.00     |
  | Projector    | 1        | 850.00     |
  | Webcam       | 10       | 45.00      |
  | Headset      | 4        | 99.99      |
  | SSD          | 2        | 180.00     |
  | Router       | 1        | 70.00      |

4. **Review `configs/example_spreadsheet_config.json`:**

* This JSON file defines the sequence of tasks the agent will perform.
* **Crucially**, ensure the sheet names (`&quot;SalesData&quot;`, `&quot;Raw Data&quot;`) and cell ranges
  (`&quot;D2:D100&quot;`, `&quot;A1:A5&quot;`, etc.) in the config match your `input_data.xlsx` structure or your desired
  output layout.
* Feel free to experiment by changing task parameters or adding new tasks.

5. **Run the script:**

```bash
python main.py
```

The script will:

* Load the `input_data.xlsx`.
* Execute tasks as defined in `example_spreadsheet_config.json`.
* Generate `output_report.xlsx` in the `data` folder, containing a &quot;Raw Data&quot; sheet (with calculated
  columns and conditional formatting), a chart, and an &quot;Audit Log&quot; sheet summarizing the execution.

## Project Structure

agentic-spreadsheet-processor/
├── src/
│ ├── init.py # Python package marker
│ ├── spreadsheet_agent.py # Core agent logic: task dispatching, Excel manipulation
│ ├── config_parser.py # Loads and validates JSON configurations
│ ├── utils.py # Logging and general helper functions
│ └── google_sheets_utils.py # Placeholder for future Google Sheets API integration
├── configs/
│ └── example_spreadsheet_config.json # Site-specific scraping rules
├── data/
│ ├── input_data.xlsx # Sample input Excel file (create this yourself)
│ └── output_report.xlsx # Generated output Excel file
├── main.py # Application entry point
├── .gitignore # Files/folders to ignore in Git
└── README.md # This project overview

## Debugging Advanced Spreadsheet Automation

* **`KeyError: &#39;SheetName&#39;`**: Means `openpyxl` couldn&#39;t find a sheet with that exact name.
  Double-check sheet names in your `input_data.xlsx` and `example_spreadsheet_config.json`.
* **`AttributeError`**: Often happens when trying to access a property (`.value`, `.font`, etc.) on a
  `None` object, which typically means a cell or range was not found as expected. Verify your cell
  references and ranges in the config.
* **`Formula Error` in Excel**: If your generated Excel file shows `#NAME?`, `#VALUE!`, or
  other errors in formula cells, it means the formula string provided in the config is incorrect for
  Excel&#39;s syntax, or the referenced cells don&#39;t contain valid data. Test formulas directly in Excel
  first.
* **Chart/Conditional Formatting Not Appearing**:
* Ensure the `data_range` and `category_range` for charts are correct and contain actual
  data.
* Verify the `range` for conditional formatting is correct and refers to cells that will contain
  data after other tasks run.
* Check `rule_type` and its associated parameters in the config.
* **Unexpected Output/Formatting**: Review the `spreadsheet_agent.py` code for the task type
  you&#39;re working on. Ensure the `openpyxl` calls are precisely what you intend (e.g., `font.bold = True`, `fill.bgColor = Color(&quot;FF0000&quot;)`).
* **Log Messages**: Pay close attention to the console output and the &quot;Audit Log&quot; sheet in the
  `output_report.xlsx`. They provide valuable information about which tasks succeeded or failed.

## Extension Ideas (Future Work)

* **Google Sheets API Integration**: Fully implement `google_sheets_utils.py` to allow tasks in
  `example_spreadsheet_config.json` to target Google Sheets directly using the `gspread` library
  and Google Cloud API credentials.
* **Database Integration**: Add tasks to read data from a SQL database (e.g., SQLite,
  PostgreSQL with `psycopg2`) and write it to a sheet, or vice-versa.
* **Web API Data Ingestion**: Create a task type to fetch data from a public REST API and
  populate a new sheet.
* **User Input / CLI Arguments**: Allow `main.py` to take command-line arguments for the
  config file path or output file name.
* **More Advanced Chart Types &amp; Customization**: Explore more `openpyxl.chart` options (e.g.,
  scatter plots, dual-axis charts, custom colors for chart elements).
* **Interactive Controls**: Add tasks to insert buttons, dropdowns, or checkboxes (via
  VBA/macros if needed, though `openpyxl` focuses on data/structure).
* **Task Dependencies**: Implement a system where one task&#39;s execution depends on the
  successful completion of another.
* **GUI for Config Generation**: Build a simple GUI application (e.g., using `Tkinter` or `PyQt`)
  that helps users visually create and save these JSON configuration files.
* **Version Control for Reports**: Integrate with Git to automatically commit generated reports or
  log files.
  แหล่งที่มา

1. https://github.com/kykoo/gcam
2. https://github.com/dreamYiZ/AutoSite
