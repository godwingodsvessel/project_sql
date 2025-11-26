/*
Question: What are the top-paying data analyst jobs?
- Identify the top 10 highest-paying Data Analyst jobs that are available in African countries.
- Focuses on job postings with specified salaries (remove nulls).
- Why? Highlight the top-paying opportunities for Data Analysts, offering insights into employment options and location flexibility.
*/

-- Remote Data Analyst jobs in Africa with top salaries
SELECT
    job_id,
    job_title,
    job_location,
    job_schedule_type,
    salary_year_avg,
    job_posted_date,
    name AS company_name,
    CASE 
        WHEN job_work_from_home = true THEN 'Remote'
        ELSE 'On-site'
    END AS work_mode
FROM
    job_postings_fact
LEFT JOIN company_dim ON job_postings_fact.company_id = company_dim.company_id
WHERE
    job_title_short = 'Data Analyst' AND
    job_work_from_home = true AND
    salary_year_avg IS NOT NULL
ORDER BY
    salary_year_avg DESC
LIMIT 10;
