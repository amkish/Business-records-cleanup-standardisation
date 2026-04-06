# Field Mapping

## branch_north.xlsx
- Cust Name -> customer_name_raw
- Phone Number -> phone_raw
- Email Address -> email_raw
- Invoice Ref -> invoice_no_raw
- Date -> transaction_date_raw
- Service Type -> service_or_product_raw
- Category -> category_raw
- Branch -> branch_raw
- Town -> city_raw
- Qty -> quantity
- Amount (£) -> amount_raw

## branch_south.csv
- Client -> customer_name_raw
- Mobile -> phone_raw
- Email -> email_raw
- Ref_No -> invoice_no_raw
- Booking_Date -> transaction_date_raw
- Product/Service -> service_or_product_raw
- Group -> category_raw
- Office -> branch_raw
- City -> city_raw
- Units -> quantity
- Total -> amount_raw

## legacy_export.csv
- CUSTOMER_NAME -> customer_name_raw
- PHONE -> phone_raw
- EMAIL -> email_raw
- INVOICE -> invoice_no_raw
- TRANS_DATE -> transaction_date_raw
- ITEM_DESC -> service_or_product_raw
- CAT -> category_raw
- LOCATION_BRANCH -> branch_raw
- LOCATION_CITY -> city_raw
- QUANTITY -> quantity
- VALUE -> amount_raw

## manual_intake_forms.xlsx
- Full Entry -> parse name, phone, email
- Location Info -> parse branch and city
- Requested Service -> service_or_product_raw
- Notes -> review_notes

## contact_updates.csv
- Used as enrichment source to update phone, email, branch, city

## admin_notes.xlsx
- Used for issue tracking, duplicate hints, and manual review notes
