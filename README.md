# Business Records Cleanup Project

A working portfolio project designed as a real client style deliverable.

## Project purpose

This project simulates a freelance data cleanup and consolidation job for a multi branch business. Raw records arrive from multiple spreadsheets, manual intake files, contact updates, and internal notes. The goal is to map, clean, standardise, validate, and consolidate those records into a reliable master dataset ready for operational use and reporting.

## Business scenario

A multi branch retail and service business stores customer and transaction records across different systems and admin files. Over time, inconsistencies have appeared in names, phone numbers, emails, dates, categories, branch names, and city values. Some records are duplicated and some require structured data entry from notes or combined fields.

## What this project demonstrates

- field mapping across inconsistent file structures
- structured data entry from semi structured records
- cleaning and standardisation of customer and transaction data
- duplicate handling
- validation and quality checks
- creation of a reporting ready master dataset
- issue logging and delivery documentation

## Raw input files

- `data/raw/branch_north.xlsx`
- `data/raw/branch_south.csv`
- `data/raw/legacy_export.csv`
- `data/raw/manual_intake_forms.xlsx`
- `data/raw/contact_updates.csv`
- `data/raw/admin_notes.xlsx`

## Current status

Project scaffold and raw messy source files created. Cleaning and validation pipeline to be completed in the next step.


## Current generated outputs

The pipeline has already been run for this portfolio project.

### Available cleaned outputs
- `data/cleaned/master_records.csv`
- `data/cleaned/master_records.xlsx`

### Available reporting outputs
- `reports/issue_log.csv`
- `reports/data_quality_report.xlsx`
- `reports/data_quality_summary.csv`
- `reports/cleaning_summary.md`

### Latest processing totals
- Total records received: 438
- Valid records: 240
- Review records: 196
- Rejected records: 2
