import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
# Set style
plt.style.use('dark_background')
sns.set_theme(style="dark", rc={"axes.facecolor": "#121212", "figure.facecolor": "#121212", "grid.color": "#333333", "text.color": "white", "axes.labelcolor": "white", "xtick.color": "white", "ytick.color": "white"})


# Output directory
FIG_DIR = Path(__file__).parent / 'figures'
FIG_DIR.mkdir(exist_ok=True)

def load_data(file_name, dummy_data_func):
    """Load data from CSV or generate dummy data if file is missing."""
    file_path = Path(__file__).parent / file_name
    if file_path.exists():
        print(f"Loading data from {file_name}...")
        return pd.read_csv(file_path)
    else:
        print(f"{file_name} not found. Using dummy data...")
        return dummy_data_func()

# --- Dummy Data Generators ---

def get_dummy_top_paying_jobs():
    data = {
        'job_title': ['Data Analyst', 'Data Analyst', 'Senior Data Analyst', 'Data Analyst', 'Data Analyst', 
                      'Principal Data Analyst', 'Data Analyst', 'Lead Data Analyst', 'Data Analyst', 'Data Analyst'],
        'company_name': ['Mantys', 'Meta', 'AT&T', 'Pinterest', 'TikTok', 
                         'SmartAsset', 'Citigroup', 'Applovin', 'UCLA Health', 'Getir'],
        'salary_year_avg': [650000, 336500, 255829, 232423, 225000, 
                            205000, 200000, 190000, 185000, 180000]
    }
    return pd.DataFrame(data)

def get_dummy_top_demanded_skills():
    data = {
        'skill': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'R', 'SAS', 'Looker', 'Azure', 'AWS'],
        'demand_count': [7291, 4611, 4330, 2464, 1891, 1482, 1000, 850, 800, 750]
    }
    return pd.DataFrame(data)

def get_dummy_top_paying_skills():
    data = {
        'skill': ['pyspark', 'bitbucket', 'couchbase', 'watson', 'datarobot', 'gitlab', 'swift', 'jupyter', 'pandas', 'elasticsearch'],
        'avg_salary': [208172, 189155, 160515, 160515, 155486, 154500, 153750, 152777, 151821, 145000]
    }
    return pd.DataFrame(data)

def get_dummy_optimal_skills():
    data = {
        'skill': ['Go', 'Confluence', 'Hadoop', 'Snowflake', 'Azure', 'BigQuery', 'AWS', 'Java', 'Scala', 'Kafka'],
        'demand_count': [27, 62, 22, 37, 34, 13, 32, 17, 15, 40],
        'avg_salary': [115320, 114210, 113193, 112948, 111225, 109654, 108317, 106906, 124903, 129999]
    }
    return pd.DataFrame(data)

# --- Plotting Functions ---

def plot_top_paying_jobs(df):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='salary_year_avg', y='company_name', hue='company_name', palette='viridis', legend=False)
    plt.title('Top 10 Paying Companies for Data Analysts')
    plt.xlabel('Average Yearly Salary ($)')
    plt.ylabel('Company')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'top_paying_jobs.png')
    print("Saved top_paying_jobs.png")

def plot_top_demanded_skills(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='demand_count', y='skill', hue='skill', palette='magma', legend=False)
    plt.title('Top 10 Most Demanded Skills')
    plt.xlabel('Number of Job Postings')
    plt.ylabel('Skill')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'top_demanded_skills.png')
    print("Saved top_demanded_skills.png")

def plot_top_paying_skills(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='avg_salary', y='skill', hue='skill', palette='coolwarm', legend=False)
    plt.title('Top 10 Highest Paying Skills')
    plt.xlabel('Average Salary ($)')
    plt.ylabel('Skill')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'top_paying_skills.png')
    print("Saved top_paying_skills.png")

def plot_optimal_skills(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='demand_count', y='avg_salary', hue='skill', s=100, palette='deep', legend=False)
    
    # Add labels
    for i, row in df.iterrows():
        plt.text(row['demand_count']+0.5, row['avg_salary'], row['skill'], fontsize=9)
        
    plt.title('Optimal Skills: High Demand & High Salary')
    plt.xlabel('Demand Count')
    plt.ylabel('Average Salary ($)')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'optimal_skills.png')
    print("Saved optimal_skills.png")

def main():
    # 1. Top Paying Jobs
    df_jobs = load_data('top_paying_jobs.csv', get_dummy_top_paying_jobs)
    plot_top_paying_jobs(df_jobs)

    # 2. Top Demanded Skills
    df_demand = load_data('top_demanded_skills.csv', get_dummy_top_demanded_skills)
    plot_top_demanded_skills(df_demand)

    # 3. Top Paying Skills
    df_paying_skills = load_data('top_paying_skills.csv', get_dummy_top_paying_skills)
    plot_top_paying_skills(df_paying_skills)

    # 4. Optimal Skills
    df_optimal = load_data('optimal_skills.csv', get_dummy_optimal_skills)
    plot_optimal_skills(df_optimal)

    print(f"\nVisualizations saved to {FIG_DIR}")

if __name__ == "__main__":
    main()
