-- Serving table: one row per provider per month with headline four-hour performance.
-- Reads the `silver` view over all silver partitions; nulls count as zero in totals.
WITH totals AS (
    SELECT
        *,
        coalesce(attendances_type1, 0) + coalesce(attendances_type2, 0) + coalesce(attendances_other, 0)
            + coalesce(attendances_booked_type1, 0) + coalesce(attendances_booked_type2, 0)
            + coalesce(attendances_booked_other, 0) AS total_attendances,
        coalesce(over_4h_type1, 0) + coalesce(over_4h_type2, 0) + coalesce(over_4h_other, 0)
            + coalesce(over_4h_booked_type1, 0) + coalesce(over_4h_booked_type2, 0)
            + coalesce(over_4h_booked_other, 0) AS total_over_4h,
        coalesce(emergency_admissions_type1, 0) + coalesce(emergency_admissions_type2, 0)
            + coalesce(emergency_admissions_other, 0) AS total_emergency_admissions_via_ae
    FROM silver
)
SELECT
    reporting_month,
    org_code,
    org_name,
    parent_org,
    total_attendances,
    total_over_4h,
    round(1 - total_over_4h::DOUBLE / nullif(total_attendances, 0), 4) AS pct_within_4h,
    total_emergency_admissions_via_ae,
    dta_wait_4_to_12h,
    dta_wait_over_12h,
    quality_tier,
    status,
    source_sha256
FROM totals
ORDER BY reporting_month, org_code
