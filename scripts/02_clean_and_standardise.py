
import re
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
STAGING = BASE / "data" / "staging"
CLEANED = BASE / "data" / "cleaned"
CLEANED.mkdir(parents=True, exist_ok=True)


def load_mapping(filename):
    mapping = pd.read_csv(BASE / 'data/reference' / filename)
    return {str(k).strip().lower(): str(v).strip() for k, v in zip(mapping['raw_value'], mapping['standard_value'])}


def clean_text(value):
    if pd.isna(value):
        return ''
    value = str(value)
    value = re.sub(r'\s+', ' ', value).strip()
    return '' if value.lower() in {'n/a', 'na', 'none', 'nil', 'unknown', 'nan'} else value


def clean_name(name):
    name = clean_text(name)
    return name.title()


def clean_phone(phone):
    phone = clean_text(phone)
    digits = re.sub(r'\D', '', phone)
    if digits.startswith('0044'):
        digits = '0' + digits[4:]
    elif digits.startswith('44') and len(digits) >= 12:
        digits = '0' + digits[2:]
    if len(digits) == 10 and digits.startswith('7'):
        digits = '0' + digits
    if len(digits) == 11 and digits.startswith('07') and digits != '00000000000':
        return digits
    return ''


def fix_missing_email_domain(email):
    if email.endswith('@examplemail'):
        return email + '.co.uk'
    if email.endswith('@gmail'):
        return email + '.com'
    if email.endswith('@hotmail'):
        return email + '.com'
    if email.endswith('@outlook'):
        return email + '.com'
    if email.endswith('.co'):
        return email + '.uk'
    return email


def clean_email(email):
    email = clean_text(email).lower().replace(' ', '')
    email = email.replace('@@', '@')
    email = fix_missing_email_domain(email)
    pattern = r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$'
    return email if re.match(pattern, email) else ''


def clean_invoice(invoice):
    invoice = clean_text(invoice).upper().replace(' ', '').replace('-', '')
    digits = re.sub(r'\D', '', invoice)
    if digits:
        return f'INV-{int(digits):04d}'
    return ''


def clean_service(text):
    text = clean_text(text).lower()
    replacements = {
        'dc': 'Deep Cleaning',
        'deep cleaning package': 'Deep Cleaning',
        'deep clean': 'Deep Cleaning',
        'deep cleaning': 'Deep Cleaning',
        'consult': 'Consultation',
        'consultation': 'Consultation',
        'maint visit': 'Maintenance Visit',
        'maintenance visit': 'Maintenance Visit',
        'inventory audit': 'Inventory Audit',
        'install support': 'Installation Support',
        'installation support': 'Installation Support',
        'store refresh': 'Store Refresh',
    }
    return replacements.get(text, text.title())


def clean_amount(value):
    text = clean_text(value)
    if not text:
        return None
    text = text.replace('£', '').replace(',', '.')
    text = re.sub(r'[^0-9.\-]', '', text)
    if text.count('.') > 1:
        first = text.find('.')
        text = text[:first + 1] + text[first + 1:].replace('.', '')
    try:
        return round(float(text), 2)
    except Exception:
        return None


def clean_quantity(value):
    text = clean_text(value)
    if not text:
        return None
    digits = re.sub(r'[^0-9\-]', '', text)
    try:
        return int(digits)
    except Exception:
        return None


def parse_date(value):
    text = clean_text(value)
    if not text:
        return pd.NaT
    if re.fullmatch(r'\d{1,2}/\d{2}', text):
        text = f'{text}/2025'
    if text.lower() == 'next fri':
        return pd.Timestamp('2025-03-14')
    return pd.to_datetime(text, errors='coerce', dayfirst=True)


def apply_contact_updates(df, updates):
    updates = updates.copy()
    updates['match_name'] = updates['Name'].map(clean_name)
    updates['New Phone Clean'] = updates['New Phone'].map(clean_phone)
    updates['New Email Clean'] = updates['New Email'].map(clean_email)
    updates['Branch Update Clean'] = updates['Branch Update'].map(clean_text)
    updates['City Correction Clean'] = updates['City Correction'].map(clean_text)

    update_map = updates.drop_duplicates('match_name').set_index('match_name').to_dict('index')

    review_notes = []
    for idx, row in df.iterrows():
        note = clean_text(row.get('review_notes', ''))
        key = row['customer_name_clean']
        upd = update_map.get(key)
        if upd:
            if not row['phone_clean'] and upd.get('New Phone Clean'):
                df.at[idx, 'phone_clean'] = upd['New Phone Clean']
                note = (note + ' | phone updated from contact_updates').strip(' |')
            if not row['email_clean'] and upd.get('New Email Clean'):
                df.at[idx, 'email_clean'] = upd['New Email Clean']
                note = (note + ' | email updated from contact_updates').strip(' |')
            if upd.get('Branch Update Clean'):
                df.at[idx, 'branch_raw'] = upd['Branch Update Clean']
            if upd.get('City Correction Clean'):
                df.at[idx, 'city_raw'] = upd['City Correction Clean']
        review_notes.append(note)
    df['review_notes'] = review_notes
    return df


def main():
    df = pd.read_csv(STAGING / 'staged_records.csv')
    updates = pd.read_csv(STAGING / 'contact_updates_staged.csv')

    branch_map = load_mapping('branch_mapping.csv')
    category_map = load_mapping('category_mapping.csv')
    city_map = load_mapping('city_mapping.csv')

    for raw in ['customer_name_raw','phone_raw','email_raw','invoice_no_raw','transaction_date_raw',
                'service_or_product_raw','category_raw','branch_raw','city_raw','amount_raw','review_notes']:
        df[raw] = df[raw].map(clean_text)

    df['customer_name_clean'] = df['customer_name_raw'].map(clean_name)
    df['phone_clean'] = df['phone_raw'].map(clean_phone)
    df['email_clean'] = df['email_raw'].map(clean_email)
    df['invoice_no_clean'] = df['invoice_no_raw'].map(clean_invoice)
    parsed_dates = df['transaction_date_raw'].map(parse_date)
    df['transaction_date_clean'] = parsed_dates.dt.strftime('%Y-%m-%d').fillna('')
    df['service_or_product_clean'] = df['service_or_product_raw'].map(clean_service)
    df['category_clean'] = df['category_raw'].map(lambda x: category_map.get(clean_text(x).lower(), clean_service(x)))
    df['branch_clean'] = df['branch_raw'].map(lambda x: branch_map.get(clean_text(x).lower(), clean_text(x).title()))
    df['city_clean'] = df['city_raw'].map(lambda x: city_map.get(clean_text(x).lower(), clean_text(x).title()))
    df['amount_clean'] = df['amount_raw'].map(clean_amount)
    df['quantity'] = df['quantity'].map(clean_quantity)
    df['country'] = 'United Kingdom'

    df = apply_contact_updates(df, updates)

    df['customer_id'] = pd.factorize(df['customer_name_clean'].fillna('') + '|' + df['phone_clean'].fillna(''))[0] + 1000
    df['customer_id'] = df['customer_id'].map(lambda x: f'CUST-{x}')
    df['record_id'] = [f'REC-{i:05d}' for i in range(1, len(df) + 1)]

    df.to_csv(CLEANED / 'cleaned_records_intermediate.csv', index=False)
    print(f"Cleaned intermediate file written: {len(df)}")


if __name__ == '__main__':
    main()
