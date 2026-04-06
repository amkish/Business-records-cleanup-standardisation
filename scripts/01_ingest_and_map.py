
import re
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
STAGING = BASE / "data" / "staging"
STAGING.mkdir(parents=True, exist_ok=True)

MASTER_COLUMNS = [
    "record_id", "customer_id", "source_file", "source_type",
    "customer_name_raw", "customer_name_clean",
    "phone_raw", "phone_clean",
    "email_raw", "email_clean",
    "invoice_no_raw", "invoice_no_clean",
    "transaction_date_raw", "transaction_date_clean",
    "service_or_product_raw", "service_or_product_clean",
    "category_raw", "category_clean",
    "branch_raw", "branch_clean",
    "city_raw", "city_clean",
    "country", "amount_raw", "amount_clean",
    "quantity", "duplicate_flag", "missing_field_flag",
    "contact_valid_flag", "date_valid_flag", "amount_valid_flag",
    "validation_status", "review_notes"
]


def load_raw_files():
    north = pd.read_excel(BASE / 'data/raw/branch_north.xlsx', sheet_name='North_Records')
    south = pd.read_csv(BASE / 'data/raw/branch_south.csv')
    legacy = pd.read_csv(BASE / 'data/raw/legacy_export.csv')
    manual_new = pd.read_excel(BASE / 'data/raw/manual_intake_forms.xlsx', sheet_name='New_Customers')
    manual_walk = pd.read_excel(BASE / 'data/raw/manual_intake_forms.xlsx', sheet_name='Walk_In_Log')
    updates = pd.read_csv(BASE / 'data/raw/contact_updates.csv')
    notes = pd.read_excel(BASE / 'data/raw/admin_notes.xlsx', sheet_name='Ops_Notes')
    return north, south, legacy, manual_new, manual_walk, updates, notes


def parse_full_entry(text):
    text = '' if pd.isna(text) else str(text)
    phone_match = re.search(r'(?:\+44\s?|0044|0)?7\d[\d\s]{8,}', text)
    email_match = re.search(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+(?:\.[A-Za-z]{2,})?', text)
    phone = phone_match.group(0) if phone_match else ''
    email = email_match.group(0) if email_match else ''
    cleaned = text
    for part in [phone, email]:
        if part:
            cleaned = cleaned.replace(part, ' ')
    cleaned = re.sub(r'[,/|]+', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(' ,')
    return cleaned, phone, email


def parse_location(text):
    text = '' if pd.isna(text) else str(text)
    text_low = text.lower()
    city = ''
    branch = ''
    for city_token in ['birmingham', 'birminham', 'bham', 'bristol city', 'bristol', 'leedz', 'leeds']:
        if city_token in text_low:
            city = city_token
            break
    for branch_token in ['north', 'south', 'central office', 'central branch', 'north branch', 'south office']:
        if branch_token in text_low:
            branch = branch_token
            break
    return branch, city


def standardise_columns(df, mapping, source_file, source_type):
    df = df.rename(columns=mapping).copy()
    for col in MASTER_COLUMNS:
        if col not in df.columns:
            df[col] = ''
    df['source_file'] = source_file
    df['source_type'] = source_type
    return df[MASTER_COLUMNS]


def build_manual_records(manual_new, manual_walk):
    manual = pd.concat([
        manual_new.assign(source_tab='New_Customers'),
        manual_walk.assign(source_tab='Walk_In_Log')
    ], ignore_index=True)

    rows = []
    for _, r in manual.iterrows():
        name, phone, email = parse_full_entry(r.get('Full Entry', ''))
        branch, city = parse_location(r.get('Location Info', ''))
        service = '' if pd.isna(r.get('Requested Service')) else str(r.get('Requested Service'))
        note = '' if pd.isna(r.get('Notes')) else str(r.get('Notes'))
        date_text = '' if pd.isna(r.get('Date Mentioned')) else str(r.get('Date Mentioned'))
        rows.append({
            'record_id': '',
            'customer_id': '',
            'source_file': 'manual_intake_forms.xlsx',
            'source_type': 'manual',
            'customer_name_raw': name,
            'customer_name_clean': '',
            'phone_raw': phone,
            'phone_clean': '',
            'email_raw': email,
            'email_clean': '',
            'invoice_no_raw': '',
            'invoice_no_clean': '',
            'transaction_date_raw': date_text,
            'transaction_date_clean': '',
            'service_or_product_raw': service,
            'service_or_product_clean': '',
            'category_raw': service,
            'category_clean': '',
            'branch_raw': branch,
            'branch_clean': '',
            'city_raw': city,
            'city_clean': '',
            'country': 'United Kingdom',
            'amount_raw': '',
            'amount_clean': '',
            'quantity': '',
            'duplicate_flag': '',
            'missing_field_flag': '',
            'contact_valid_flag': '',
            'date_valid_flag': '',
            'amount_valid_flag': '',
            'validation_status': '',
            'review_notes': f"{r.get('source_tab','')} | {note}",
        })
    return pd.DataFrame(rows, columns=MASTER_COLUMNS)


def main():
    north, south, legacy, manual_new, manual_walk, updates, notes = load_raw_files()

    north_map = {
        'Cust Name':'customer_name_raw','Phone Number':'phone_raw','Email Address':'email_raw',
        'Invoice Ref':'invoice_no_raw','Date':'transaction_date_raw','Service Type':'service_or_product_raw',
        'Category':'category_raw','Branch':'branch_raw','Town':'city_raw','Qty':'quantity','Amount (£)':'amount_raw'
    }
    south_map = {
        'Client':'customer_name_raw','Mobile':'phone_raw','Email':'email_raw',
        'Ref_No':'invoice_no_raw','Booking_Date':'transaction_date_raw','Product/Service':'service_or_product_raw',
        'Group':'category_raw','Office':'branch_raw','City':'city_raw','Units':'quantity','Total':'amount_raw'
    }
    legacy_map = {
        'CUSTOMER_NAME':'customer_name_raw','PHONE':'phone_raw','EMAIL':'email_raw',
        'INVOICE':'invoice_no_raw','TRANS_DATE':'transaction_date_raw','ITEM_DESC':'service_or_product_raw',
        'CAT':'category_raw','LOCATION_BRANCH':'branch_raw','LOCATION_CITY':'city_raw',
        'QUANTITY':'quantity','VALUE':'amount_raw'
    }

    north_std = standardise_columns(north, north_map, 'branch_north.xlsx', 'branch')
    south_std = standardise_columns(south, south_map, 'branch_south.csv', 'branch')
    legacy_std = standardise_columns(legacy, legacy_map, 'legacy_export.csv', 'legacy')
    manual_std = build_manual_records(manual_new, manual_walk)

    staged = pd.concat([north_std, south_std, legacy_std, manual_std], ignore_index=True)
    staged['country'] = staged['country'].replace('', 'United Kingdom')
    staged.insert(0, 'source_row_number', range(1, len(staged) + 1))

    staged.to_csv(STAGING / 'staged_records.csv', index=False)
    updates.to_csv(STAGING / 'contact_updates_staged.csv', index=False)
    notes.to_csv(STAGING / 'admin_notes_staged.csv', index=False)

    print(f"Staged records written: {len(staged)}")
    print(f"Contact updates written: {len(updates)}")
    print(f"Admin notes written: {len(notes)}")


if __name__ == '__main__':
    main()
