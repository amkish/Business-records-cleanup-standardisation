
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
CLEANED = BASE / "data" / "cleaned"
REPORTS = BASE / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def flag_missing(df, required_cols):
    missing_mask = df[required_cols].isna() | (df[required_cols].astype(str).apply(lambda s: s.str.strip()) == '')
    return missing_mask.any(axis=1)


def main():
    df = pd.read_csv(CLEANED / 'cleaned_records_intermediate.csv')
    issues = []

    df['contact_valid_flag'] = ((df['phone_clean'].fillna('') != '') | (df['email_clean'].fillna('') != '')).map(lambda x: 'yes' if x else 'no')
    parsed_dates = pd.to_datetime(df['transaction_date_clean'], errors='coerce')
    df['date_valid_flag'] = parsed_dates.notna().map(lambda x: 'yes' if x else 'no')
    df['amount_valid_flag'] = df['amount_clean'].notna() & (df['amount_clean'] > 0)
    df['amount_valid_flag'] = df['amount_valid_flag'].map(lambda x: 'yes' if x else 'no')
    df['missing_field_flag'] = flag_missing(df, ['customer_name_clean','branch_clean','city_clean']).map(lambda x: 'yes' if x else 'no')

    duplicate_mask = df.duplicated(subset=['customer_name_clean','transaction_date_clean','amount_clean'], keep=False)
    duplicate_mask |= df.duplicated(subset=['invoice_no_clean'], keep=False) & (df['invoice_no_clean'].fillna('') != '')
    df['duplicate_flag'] = duplicate_mask.map(lambda x: 'yes' if x else 'no')

    statuses = []
    notes = []
    for _, row in df.iterrows():
        row_notes = []
        if row['duplicate_flag'] == 'yes':
            row_notes.append('possible duplicate')
        if row['missing_field_flag'] == 'yes':
            row_notes.append('missing core field')
        if row['contact_valid_flag'] == 'no':
            row_notes.append('no valid phone or email')
        if row['date_valid_flag'] == 'no':
            row_notes.append('invalid or missing date')
        if row['amount_valid_flag'] == 'no' and row['source_type'] != 'manual':
            row_notes.append('invalid amount')
        if row['source_type'] == 'manual' and pd.isna(row['amount_clean']):
            row_notes.append('manual record requires amount follow up')

        if row['duplicate_flag'] == 'yes' or row['missing_field_flag'] == 'yes':
            status = 'review'
        elif row['contact_valid_flag'] == 'no' and row['date_valid_flag'] == 'no':
            status = 'rejected'
        elif row['amount_valid_flag'] == 'no' and row['source_type'] != 'manual':
            status = 'review'
        else:
            status = 'valid'
        statuses.append(status)

        base_note = str(row.get('review_notes', '')).strip()
        merged = ' | '.join([x for x in [base_note] + row_notes if x and x.lower() != 'nan'])
        notes.append(merged)

    df['validation_status'] = statuses
    df['review_notes'] = notes

    issue_records = []
    for _, row in df.iterrows():
        if row['validation_status'] != 'valid':
            issue_records.append({
                'record_id': row['record_id'],
                'customer_name_clean': row['customer_name_clean'],
                'source_file': row['source_file'],
                'issue_type': row['validation_status'],
                'duplicate_flag': row['duplicate_flag'],
                'missing_field_flag': row['missing_field_flag'],
                'contact_valid_flag': row['contact_valid_flag'],
                'date_valid_flag': row['date_valid_flag'],
                'amount_valid_flag': row['amount_valid_flag'],
                'review_notes': row['review_notes'],
            })

    issue_df = pd.DataFrame(issue_records)
    issue_df.to_csv(REPORTS / 'issue_log.csv', index=False)
    df.to_csv(CLEANED / 'master_records.csv', index=False)

    summary = {
        'total_records_received': int(len(df)),
        'valid_records': int((df['validation_status'] == 'valid').sum()),
        'review_records': int((df['validation_status'] == 'review').sum()),
        'rejected_records': int((df['validation_status'] == 'rejected').sum()),
        'possible_duplicates': int((df['duplicate_flag'] == 'yes').sum()),
        'records_missing_core_fields': int((df['missing_field_flag'] == 'yes').sum()),
        'records_without_valid_contact': int((df['contact_valid_flag'] == 'no').sum()),
        'records_with_invalid_dates': int((df['date_valid_flag'] == 'no').sum()),
        'records_with_invalid_amounts': int((df['amount_valid_flag'] == 'no').sum()),
    }
    pd.DataFrame([summary]).to_csv(REPORTS / 'data_quality_summary.csv', index=False)
    print(summary)


if __name__ == '__main__':
    main()
