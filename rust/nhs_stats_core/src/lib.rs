//! Placeholder crate for hot paths that justify Rust (see docs/adr/0001).
//!
//! Nothing here is required by the Python package; the pure Python equivalents
//! remain the reference until profiling shows a need.

/// Valid ODS organisation codes are 3 to 5 upper-case ASCII letters or digits.
pub fn is_valid_ods_code(code: &str) -> bool {
    (3..=5).contains(&code.len())
        && code
            .bytes()
            .all(|b| b.is_ascii_uppercase() || b.is_ascii_digit())
}

/// Financial year label (April to March) for a calendar year and month, e.g. "2025-26".
pub fn financial_year(year: i32, month: u32) -> Option<String> {
    if !(1..=12).contains(&month) {
        return None;
    }
    let start = if month >= 4 { year } else { year - 1 };
    Some(format!("{}-{:02}", start, (start + 1).rem_euclid(100)))
}

#[cfg(feature = "python")]
mod python {
    use pyo3::prelude::*;

    #[pyfunction]
    fn is_valid_ods_code(code: &str) -> bool {
        super::is_valid_ods_code(code)
    }

    #[pyfunction]
    fn financial_year(year: i32, month: u32) -> Option<String> {
        super::financial_year(year, month)
    }

    #[pymodule]
    fn nhs_stats_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(is_valid_ods_code, m)?)?;
        m.add_function(wrap_pyfunction!(financial_year, m)?)?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ods_codes() {
        assert!(is_valid_ods_code("RJ1"));
        assert!(is_valid_ods_code("R0A01"));
        assert!(!is_valid_ods_code("rj1"));
        assert!(!is_valid_ods_code("RJ"));
        assert!(!is_valid_ods_code("RJ1234"));
        assert!(!is_valid_ods_code("RJ 1"));
    }

    #[test]
    fn financial_years() {
        assert_eq!(financial_year(2026, 3).as_deref(), Some("2025-26"));
        assert_eq!(financial_year(2026, 4).as_deref(), Some("2026-27"));
        assert_eq!(financial_year(1999, 12).as_deref(), Some("1999-00"));
        assert_eq!(financial_year(2026, 13), None);
    }
}
