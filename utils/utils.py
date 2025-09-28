
# Define domains
domain_list = ["Inclusion", "Sustainability", "Resilience"]

# Define sub-domains
sub_domain_inclusion = ["Social", "Economic", "Gender"]

sub_domain_sustainability = ["Environmental", "Social", "Economic"]

sub_domain_resilience = ["Social", "Economic", "Infrastructure", "Institutional", "Hazard"]

# Define sub-domain kpis
social_inclusion_kpis = { 
    "Disability employment gap": "tepsr_sp200",
    "Youth Unemployment": "edat_lfse_22",
    "Slum Household": "ilc_lvhl21n"
}

economic_inclusion_kpis = {
    "Gini coefficient": "tessi190",
    "Poverty Rate": "ilc_li41"
}

gender_inclusion_kpis = {
    "Gender employment gap": "tepsr_lm220",
    "Equitable Bachelor's Enrolment": "educ_uoe_enra11"
}

environment_sustainability_topics = ["Air Quality", "Energy", "Biodiversity", "Environmental quality"]

economic_sustainability_topics = ["Employment", "Infrastructure", "Innovation"]

social_resilience_topics = ["Educational equality", "Demography", "Transportation access"]

economic_resilience_topics = ["Health access", "Market access"]

air_quality_kpis = {
    "Greenhouse gas (GHG) emissions": "cei_gsr011",
    "Concentration of NO2 (µg/m³)": "no2", 
    "Concentration of PM10 (µg/m³)": "pm10",
}

energy_kpis = {
    "Renewable energy sources": "REN",
    "Renewable energy sources in transport": "REN_TRA",
    "Renewable energy sources in electricity": "REN_ELC",
    "Renewable energy sources in heating and cooling": "REN_HEAT_CL",
}

economic_sustainability_kpis = {
    "Persons employed in productive age": "tgs00007",
    "Household level of internet access": "tgs00047",
    "HR in science and technology": "tgs00038"
}

social_sustainability_kpis = {
    "Share of murders and violent deaths": "urb_clivcon",
    "Share of students in higher education": "urb_ceduc",
    "Share of total deaths": "hlth_cd_yro",
    "Infant mortality": "hlth_cd_yinfr"
}

edu_equality_kpis = {
    "Tertiary educational attainment": "tgs00109",
    "Population with 0-2 educational levels": "edat_lfse_04"
}

demography_kpis = {
    "Population in productive age": "demo_r_pjangrp3",
    "Population aged 65 years and older": "demo_r_pjangrp3_aged",
    "Population density": "demo_r_d3dens"
}

economic_resilience_kpis = {
    "Regional gross domestic product": "tgs00006",
    "Number of Physicians": "hlth_rs_physreg"
}

# Define regions
nat_dict = {
    "Finland": "FI",
    "Portugal": "PT",
    "Slovakia": "SK", 
    "France": "FR", 
    "Germany": "DE"
}

nuts2_dict = {
    "Köln": "DEA2",
    "Helsinki-U.": "FI1B",
    "S. Slovensko": "SK03",
    "A. M. Lisboa": "PT17",
    "Ile de France": "FR10"
}


def add_informative_texts(dataset_code):
    
    if dataset_code == "tepsr_sp200":
        text = "The disability employment gap is defined as the difference between the employment rates of people with no and those with some or severe limitation in their daily activities, aged 20-64. The employment rate is calculated by dividing the number of persons aged 20 to 64 in employment by the total population of the same age group."
    elif dataset_code == "edat_lfse_22":
        text = "The indicator on young people neither in employment nor in education and training (NEET) corresponds to the percentage of the population of a given age group and sex who is not employed and not involved in further education or training. The numerator of the indicator refers to persons who meet the following two conditions: (a) they are not employed (i.e. unemployed or inactive according to the International Labour Organisation definition) and (b) they have not received any education or training (i.e. neither formal nor non-formal) in the four weeks preceding the survey."
    elif dataset_code == "ilc_lvhl21n":
        text = "The indicator persons living in households with very low work intensity is defined as the number of persons living in a household where the members of working age worked a working time equal or less than 20% of their total work-time potential during the previous year."
    else:
        text = "No text available yet."
    return text