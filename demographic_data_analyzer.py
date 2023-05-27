import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby("race").size().sort_values(ascending=False).values

    # What is the average age of men?
    group_sex = df[["sex", "age"]].groupby("sex")
    average_age_men = group_sex.get_group("Male")["age"].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    total_bachelors = df.groupby("education")["education"].get_group("Bachelors").count()
    total_data = df["education"].count()
    percentage_bachelors = ((total_bachelors/total_data)*100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`    
    higher_education = df.loc[(df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")]["education"].count()
    higher_education_50K = df.loc[((df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")) & (df["salary"] == ">50K")]["salary"].count()

    lower_education = total_data - higher_education
    lower_education_50K = df.loc[((df["education"] != "Bachelors") & (df["education"] != "Masters") & (df["education"] != "Doctorate")) & (df["salary"] == ">50K")]["salary"].count()

    # percentage with salary >50K
    higher_education_rich = ((higher_education_50K/higher_education)*100).round(1)
    lower_education_rich = ((lower_education_50K/lower_education)*100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_working_count = df.loc[(df["hours-per-week"] == min_work_hours)]["hours-per-week"].count()
    num_min_workers = df.loc[(df["hours-per-week"] == min_work_hours) & (df["salary"] == ">50K")]["hours-per-week"].count()

    rich_percentage = ((num_min_workers/min_working_count)*100).round(1)

    # What country has the highest percentage of people that earn >50K?
    salary_50K_df = df[df["salary"] == ">50K"]
    gb_country_50K_count = salary_50K_df.groupby("native-country")["native-country"].count()
    gb_country = df.groupby("native-country")["native-country"].count()
    percentage = (gb_country_50K_count/gb_country)*100

    highest_percentage = percentage.max()
    highest_earning_country_percentage = round(highest_percentage, ndigits=1)
    highest_earning_df = pd.DataFrame({"native-country":percentage.index, "percentage":percentage.values})
    highest_earning_country = highest_earning_df.loc[highest_earning_df["percentage"] == highest_percentage, "native-country"].item()

    # Identify the most popular occupation for those who earn >50K in India.
    india_50k_occupation = salary_50K_df.groupby("native-country").get_group("India").groupby("occupation")["occupation"].count()
    india_50k_occupation_df = pd.DataFrame({"occupation":india_50k_occupation.index, "count":india_50k_occupation.values})
    top_IN_occupation = india_50k_occupation_df.loc[india_50k_occupation_df["count"] == india_50k_occupation.max(), "occupation"].item()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
