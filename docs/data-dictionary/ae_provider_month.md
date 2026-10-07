# ae_provider_month (gold)

Monthly A&E attendances and emergency admissions, one row per provider per reporting month.
Source: NHS England Monthly A&E Attendances and Emergency Admissions. Tier: official. Grain: `reporting_month`, `org_code`.
Status: draft. Layout verified against synthetic fixtures only.

| Column | Type | Description |
|---|---|---|
| reporting_month | date | First day of the month |
| org_code | string | ODS provider code |
| org_name | string | Provider name as published |
| parent_org | string | Parent organisation as published |
| total_attendances | int | Sum of type 1, type 2, other and booked-appointment attendances (nulls as zero) |
| total_over_4h | int | Matching sum of attendances over four hours |
| pct_within_4h | double | 1 - total_over_4h / total_attendances, 4 decimal places. Check against the published headline measure before use |
| total_emergency_admissions_via_ae | int | Type 1, type 2 and other A&E emergency admissions |
| dta_wait_4_to_12h | int | Decision to admit to admission, 4 to 12 hours |
| dta_wait_over_12h | int | Decision to admit to admission, over 12 hours |
| quality_tier | string | official, experimental or management_information |
| status | string | provisional, revised or final, as recorded at ingestion |
| source_sha256 | string | Hash of the bronze file |

## Caveats

- Counts are as published; suppressed or blank values are null in silver and treated as zero in gold totals.
- Provider and system mappings change (ICB changes from April 2026). No restatement is applied yet.
- Recent months only; history and series-break flags are not yet loaded.
