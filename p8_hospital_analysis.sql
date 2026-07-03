-- ============================================================
--  PROJECT 8 — HOSPITAL OPERATIONS ANALYTICS
--  Dataset  : Hospital Admissions Data — Ashish Sahani (Kaggle)
--  Tool     : MySQL Workbench
--  Author   : Charlie | TheBuild Data Analysis Programme
--  Date     : June 2026
-- ============================================================

CREATE DATABASE IF NOT EXISTS hospital_ops;
USE hospital_ops;

CREATE TABLE IF NOT EXISTS patients (
    patient_id      INT AUTO_INCREMENT PRIMARY KEY,
    age             INT,
    gender          ENUM('M','F','Other'),
    blood_type      VARCHAR(5),
    insurance_type  VARCHAR(60)
);

CREATE TABLE IF NOT EXISTS departments (
    dept_id         INT AUTO_INCREMENT PRIMARY KEY,
    dept_name       VARCHAR(100) NOT NULL UNIQUE,
    bed_capacity    INT DEFAULT 0,
    dept_head       VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS admissions (
    admission_id    INT AUTO_INCREMENT PRIMARY KEY,
    patient_id      INT             NOT NULL,
    dept_id         INT             NOT NULL,
    admission_date  DATE            NOT NULL,
    discharge_date  DATE,
    diagnosis       VARCHAR(200),
    admission_type  ENUM('Emergency','Elective','Urgent'),
    readmission     TINYINT(1)      DEFAULT 0,
    billing_amount  DECIMAL(12,2),
    INDEX idx_dept   (dept_id),
    INDEX idx_admit  (admission_date),
    INDEX idx_patient(patient_id),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (dept_id)    REFERENCES departments(dept_id)
);

-- ── ANALYSIS QUERIES ─────────────────────────────────────────────────────────

-- Q1: Monthly admission trends with readmission rate and avg LOS
SELECT
    DATE_FORMAT(admission_date, '%Y-%m')                           AS month,
    COUNT(admission_id)                                            AS total_admissions,
    SUM(readmission)                                               AS readmissions,
    ROUND(SUM(readmission) * 100.0 / COUNT(admission_id), 2)      AS readmission_rate_pct,
    ROUND(AVG(DATEDIFF(discharge_date, admission_date)), 2)        AS avg_los_days
FROM admissions
WHERE discharge_date IS NOT NULL
GROUP BY month
ORDER BY month;

-- Q2: Dept patient load — admissions, avg LOS, readmission rate
SELECT
    d.dept_name,
    COUNT(a.admission_id)                                          AS total_admissions,
    ROUND(AVG(DATEDIFF(a.discharge_date, a.admission_date)), 2)   AS avg_stay_days,
    SUM(a.readmission)                                             AS readmit_count,
    ROUND(SUM(a.readmission) * 100.0 / COUNT(a.admission_id), 2) AS readmit_rate_pct,
    ROUND(AVG(a.billing_amount), 2)                               AS avg_billing
FROM departments d
JOIN admissions a ON d.dept_id = a.dept_id
WHERE a.discharge_date IS NOT NULL
GROUP BY d.dept_name
ORDER BY total_admissions DESC;

-- Q3: Seasonal admission patterns (quarter breakdown)
SELECT
    YEAR(admission_date)                                           AS year,
    QUARTER(admission_date)                                        AS quarter,
    CASE QUARTER(admission_date)
        WHEN 1 THEN 'Q1 (Winter: Jan–Mar)'
        WHEN 2 THEN 'Q2 (Spring: Apr–Jun)'
        WHEN 3 THEN 'Q3 (Summer: Jul–Sep)'
        WHEN 4 THEN 'Q4 (Autumn: Oct–Dec)'
    END                                                            AS season_label,
    COUNT(*)                                                       AS admissions,
    ROUND(AVG(DATEDIFF(discharge_date, admission_date)), 2)       AS avg_los
FROM admissions
WHERE discharge_date IS NOT NULL
GROUP BY year, quarter, season_label
ORDER BY year, quarter;

-- Q4: Patient age group analysis
SELECT
    CASE
        WHEN p.age < 18  THEN 'A. Child     (0–17)'
        WHEN p.age < 35  THEN 'B. Young Adult (18–34)'
        WHEN p.age < 55  THEN 'C. Adult     (35–54)'
        WHEN p.age < 70  THEN 'D. Senior    (55–69)'
        ELSE                  'E. Elderly   (70+)'
    END                                                            AS age_group,
    COUNT(a.admission_id)                                          AS admissions,
    ROUND(AVG(DATEDIFF(a.discharge_date, a.admission_date)), 2)   AS avg_los,
    ROUND(SUM(a.readmission) * 100.0 / COUNT(a.admission_id), 2) AS readmit_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.discharge_date IS NOT NULL
GROUP BY age_group
ORDER BY age_group;

-- Q5: Insurance type vs avg billing
SELECT
    p.insurance_type,
    COUNT(a.admission_id)                                          AS admissions,
    ROUND(AVG(a.billing_amount), 2)                               AS avg_billing,
    ROUND(SUM(a.billing_amount), 2)                               AS total_billing,
    ROUND(SUM(a.readmission) * 100.0 / COUNT(*), 2)              AS readmit_pct
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY p.insurance_type
ORDER BY avg_billing DESC;

-- Q6: Admission type breakdown
SELECT
    admission_type,
    COUNT(*)                                                       AS count,
    ROUND(AVG(DATEDIFF(discharge_date, admission_date)), 2)       AS avg_los,
    ROUND(SUM(readmission) * 100.0 / COUNT(*), 2)                AS readmit_pct,
    ROUND(AVG(billing_amount), 2)                                  AS avg_billing
FROM admissions
WHERE discharge_date IS NOT NULL
GROUP BY admission_type
ORDER BY count DESC;
