# Business Records Cleanup and Standardisation Workflow

This repository presents the project as a **client commissioned data cleanup and standardisation delivery**.

The brief was to take messy business records spread across multiple files, clean and standardise them, validate the results, and hand back a reliable master dataset that the client could use for reporting, dashboarding, and daily operations.

## Client brief

I was brought in to help a growing multi branch retail and service business that had customer and transaction records stored across:

- branch spreadsheets maintained by different staff members
- a legacy CSV export from an older system
- manually entered intake forms
- contact correction files from admin staff
- internal notes containing partial customer and booking details

The client's main problem was not lack of data. It was lack of **trustworthy, usable data**.

The records were inconsistent, duplicated, incomplete, and difficult to analyse. Contact details were unreliable, dates were stored in mixed formats, categories and locations were entered differently by each team, and several records needed structured data entry before they could be used properly.

My role was to turn those scattered records into a clean and dependable master dataset.

## What the client needed

The client wanted a workflow that could:

- consolidate records from multiple raw files and layouts
- convert semi structured information into standard fields
- clean and standardise names, emails, phone numbers, dates, categories, branches, and cities
- identify and flag possible duplicates
- validate key fields before final delivery
- produce clean outputs that were ready for reporting and operational use
- leave behind a repeatable process rather than a one off manual fix

## What I delivered

I built a working data cleanup pipeline that:

1. ingests raw records from Excel and CSV files
2. maps inconsistent columns into a common schema
3. extracts structured values from messy intake records and admin notes
4. standardises core business fields
5. validates data quality across contact, date, amount, and completeness checks
6. flags duplicates and review items
7. exports a final master dataset together with quality reporting outputs

This was designed as a practical client handoff, not a theory exercise.

## Source files received from the client

### Raw input files
- `data/raw/branch_north.xlsx`
- `data/raw/branch_south.csv`
- `data/raw/legacy_export.csv`
- `data/raw/manual_intake_forms.xlsx`
- `data/raw/contact_updates.csv`
- `data/raw/admin_notes.xlsx`

### Reference files created to support the cleanup
- `data/reference/category_mapping.csv`
- `data/reference/branch_mapping.csv`
- `data/reference/city_mapping.csv`

## My workflow

### 1. Source intake and field mapping
Each source file used different headers and structures. I first aligned them into a shared schema so they could be processed consistently.

### 2. Structured data entry and extraction
Some records arrived in note style or combined field formats. I split and mapped those values into usable fields where reliable rules could be applied, and I flagged uncertain cases for review instead of forcing assumptions.

### 3. Cleaning and standardisation
I cleaned whitespace, normalised text casing, standardised invoice references, parsed dates, mapped category values, standardised branch and city names, and converted amount fields into consistent numeric values.

### 4. Validation and issue flagging
I checked for missing key fields, invalid contact details, invalid dates, invalid amounts, and possible duplicates. Each record was assigned a validation status so the client could clearly see what was ready to use and what still needed attention.

### 5. Final delivery
I produced a cleaned master dataset in both CSV and Excel format, alongside an issue log and data quality report so the client could review unresolved items and understand the overall condition of the data.

## Final schema highlights

The final master dataset includes both raw and cleaned versions of important fields so the client can see how values were transformed.

Key columns include:
- `customer_name_raw`
- `customer_name_clean`
- `phone_raw`
- `phone_clean`
- `email_raw`
- `email_clean`
- `transaction_date_raw`
- `transaction_date_clean`
- `category_raw`
- `category_clean`
- `branch_raw`
- `branch_clean`
- `city_raw`
- `city_clean`
- `amount_raw`
- `amount_clean`
- `duplicate_flag`
- `validation_status`
- `review_notes`

## Delivery outputs

### Cleaned data
- `data/cleaned/master_records.csv`
- `data/cleaned/master_records.xlsx`

### Quality and review outputs
- `reports/issue_log.csv`
- `reports/data_quality_report.xlsx`
- `reports/data_quality_summary.csv`
- `reports/cleaning_summary.md`

### Supporting documents
- `reports/field_mapping.md`
- `docs/upwork_portfolio_summary.md`
- `docs/github_project_summary.md`

## Processing summary

Latest run totals:
- Total records processed: 438
- Valid records: 240
- Review records: 196
- Rejected records: 2
- Possible duplicates flagged: 113
- Records missing core fields: 22
- Records without a valid contact method: 52
- Records with invalid dates: 16
- Records with invalid amounts: 144

## Repository structure

```text
business-records-cleanup-project/
├── data/
│   ├── raw/
│   ├── staging/
│   ├── cleaned/
│   └── reference/
├── scripts/
├── README.md
└── requirements.txt
```

## Scripts

- `scripts/01_ingest_and_map.py`
- `scripts/02_clean_and_standardise.py`
- `scripts/03_validate_and_flag.py`
- `scripts/04_export_outputs.py`

Run in sequence:

```bash
python scripts/01_ingest_and_map.py
python scripts/02_clean_and_standardise.py
python scripts/03_validate_and_flag.py
python scripts/04_export_outputs.py
```

## Tools used

- Python
- pandas
- openpyxl
- Excel compatible deliverables

## Business value delivered

This type of workflow is useful before a business:

- moves data into a CRM or new system
- builds a dashboard or reporting layer
- prepares for operational reporting
- cleans branch level records after years of inconsistent entry
- reviews duplicate or unreliable customer records

## Portfolio positioning

This project is intentionally written and structured like a real freelance delivery. It shows how I would respond to a client brief, organise messy business records, apply structured data cleanup, and deliver usable outputs with clear documentation and review notes.
