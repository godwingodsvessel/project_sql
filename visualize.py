"""
visualize.py

Generate visualizations for the Data Job Analysis queries.

Usage:
  - Set these environment variables for your Postgres connection:
      PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
  - Create a virtual environment and install requirements from `requirements.txt`.
  - Run:
      python project_sql\visualize.py

Outputs:
  - PNG charts are written to `project_sql/figures/`:
      - top_paying_jobs.png
      - top_demanded_skills.png
      - optimal_skills.png

The script will run three queries and produce simple, shareable charts.
"""
import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


FIG_DIR = Path(__file__).parent / 'figures'
FIG_DIR.mkdir(exist_ok=True)


def get_engine_from_env():
    host = os.getenv('PGHOST', 'localhost')
    port = os.getenv('PGPORT', '5432')
    user = os.getenv('PGUSER', 'postgres')
    password = os.getenv('PGPASSWORD', '')
    db = os.getenv('PGDATABASE', 'postgres')
    url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
    return create_engine(url)


def run_query(engine, sql):
    return pd.read_sql(sql, engine)


TOP_PAYING_JOBS_Q = '''
SELECT
    job_title_short AS job_title,
    COALESCE(company_dim.name, '') AS company_name,
    salary_year_avg
FROM job_postings_fact
LEFT JOIN company_dim ON job_postings_fact.company_id = company_dim.company_id
WHERE job_title_short = 'Data Analyst'
  AND salary_year_avg IS NOT NULL
ORDER BY salary_year_avg DESC
LIMIT 10;
'''


TOP_DEMANDED_SKILLS_Q = '''
SELECT
    sd.skills AS skill,
    COUNT(sjd.job_id) AS demand_count
FROM skills_job_dim sjd
INNER JOIN skills_dim sd ON sjd.skill_id = sd.skill_id
INNER JOIN job_postings_fact jpf ON sjd.job_id = jpf.job_id
WHERE jpf.job_title_short = 'Data Analyst'
GROUP BY sd.skills
ORDER BY demand_count DESC
LIMIT 10;
'''


OPTIMAL_SKILLS_Q = '''
SELECT
    sd.skills AS skill,
    COUNT(sjd.job_id) AS demand_count,
    AVG(jpf.salary_year_avg) AS avg_salary
FROM skills_job_dim sjd
INNER JOIN skills_dim sd ON sjd.skill_id = sd.skill_id
INNER JOIN job_postings_fact jpf ON sjd.job_id = jpf.job_id
WHERE jpf.job_title_short = 'Data Analyst' AND jpf.salary_year_avg IS NOT NULL
GROUP BY sd.skills
HAVING COUNT(sjd.job_id) > 10
ORDER BY avg_salary DESC
LIMIT 10;
'''


def plot_top_paying_jobs(df: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='salary_year_avg', y='job_title', palette='viridis')
    plt.title('Top 10 Paying Data Analyst Jobs')
    plt.xlabel('Annual Salary (USD)')
    plt.ylabel('Job Title')
    plt.tight_layout()
    out = FIG_DIR / 'top_paying_jobs.png'
    plt.savefig(out)
    print('Saved', out)


def plot_top_demanded_skills(df: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='demand_count', y='skill', palette='magma')
    plt.title('Top Demanded Skills (Data Analyst)')
    plt.xlabel('Number of Postings')
    plt.ylabel('Skill')
    plt.tight_layout()
    out = FIG_DIR / 'top_demanded_skills.png'
    plt.savefig(out)
    print('Saved', out)


def plot_optimal_skills(df: pd.DataFrame):
    # Scatter plot: demand_count vs avg_salary
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='demand_count', y='avg_salary', hue='skill', s=120)
    for i, row in df.iterrows():
        plt.text(row['demand_count'] + 0.1, row['avg_salary'], row['skill'], fontsize=9)
    plt.title('Optimal Skills: Demand vs Average Salary')
    plt.xlabel('Demand (postings)')
    plt.ylabel('Average Salary')
    plt.tight_layout()
    out = FIG_DIR / 'optimal_skills.png'
    plt.savefig(out)
    print('Saved', out)


def main():
    engine = get_engine_from_env()
    print('Connecting to database...')
    # Top paying jobs
    tp = run_query(engine, TOP_PAYING_JOBS_Q)
    if not tp.empty:
        plot_top_paying_jobs(tp)
    else:
        print('No rows returned for top paying jobs query')

    # Top demanded skills
    td = run_query(engine, TOP_DEMANDED_SKILLS_Q)
    if not td.empty:
        plot_top_demanded_skills(td)
    else:
        print('No rows returned for top demanded skills query')

    # Optimal skills
    op = run_query(engine, OPTIMAL_SKILLS_Q)
    if not op.empty:
        plot_optimal_skills(op)
    else:
        print('No rows returned for optimal skills query')


if __name__ == '__main__':
    main()
