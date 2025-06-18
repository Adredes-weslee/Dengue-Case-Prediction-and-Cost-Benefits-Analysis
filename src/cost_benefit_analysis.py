"""
Cost-Benefit Analysis Module

This module contains functions to calculate the cost-effectiveness of
the Wolbachia and Dengvaxia interventions based on the number of
dengue cases and associated DALYs (Disability-Adjusted Life Years).
"""
import json
from pathlib import Path
import pandas as pd

def calculate_cost_benefit(
    total_cases_2020: int,
    population: int,
    wolbachia_cost_pp: float,
    dengvaxia_cost_pp: float,
    daly_per_case: float,
    cases_averted_wolbachia_pct: float,
    cases_averted_dengvaxia_pct: float
) -> dict:
    """
    Performs the cost-benefit analysis for both interventions.

    Args:
        total_cases_2020 (int): Total dengue cases in the analysis year.
        population (int): The total population.
        wolbachia_cost_pp (float): Cost per person for Wolbachia.
        dengvaxia_cost_pp (float): Cost per person for Dengvaxia.
        daly_per_case (float): DALYs lost per dengue case.
        cases_averted_wolbachia_pct (float): Efficacy of Wolbachia.
        cases_averted_dengvaxia_pct (float): Efficacy of Dengvaxia.

    Returns:
        dict: A dictionary containing the results of the analysis.
    """
    print("Running Cost-Benefit Analysis...")
    print(f"Base scenario: {total_cases_2020:,} cases in 2020")
    print(f"Population: {population:,}")

    # --- Wolbachia Analysis ---
    wolbachia_total_cost = population * wolbachia_cost_pp
    wolbachia_cases_averted = total_cases_2020 * cases_averted_wolbachia_pct
    wolbachia_dalys_averted = wolbachia_cases_averted * daly_per_case
    
    # Avoid division by zero
    if wolbachia_dalys_averted > 0:
        wolbachia_cost_per_daly = wolbachia_total_cost / wolbachia_dalys_averted
    else:
        wolbachia_cost_per_daly = float('inf')

    # --- Dengvaxia Analysis ---
    dengvaxia_total_cost = population * dengvaxia_cost_pp
    dengvaxia_cases_averted = total_cases_2020 * cases_averted_dengvaxia_pct
    dengvaxia_dalys_averted = dengvaxia_cases_averted * daly_per_case
    
    # Avoid division by zero
    if dengvaxia_dalys_averted > 0:
        dengvaxia_cost_per_daly = dengvaxia_total_cost / dengvaxia_dalys_averted
    else:
        dengvaxia_cost_per_daly = float('inf')

    # Determine most cost-effective intervention
    most_cost_effective = "Wolbachia" if wolbachia_cost_per_daly < dengvaxia_cost_per_daly else "Dengvaxia"
    
    # Calculate cost difference
    cost_difference = abs(wolbachia_cost_per_daly - dengvaxia_cost_per_daly)
    cost_savings_pct = (cost_difference / max(wolbachia_cost_per_daly, dengvaxia_cost_per_daly)) * 100

    results = {
        "analysis_metadata": {
            "base_year": 2020,
            "total_cases_analyzed": total_cases_2020,
            "population": population,
            "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "wolbachia": {
            "total_cost_usd": round(wolbachia_total_cost, 2),
            "cost_per_person_usd": wolbachia_cost_pp,
            "cases_averted": round(wolbachia_cases_averted, 0),
            "dalys_averted": round(wolbachia_dalys_averted, 2),
            "cost_per_daly_averted_usd": round(wolbachia_cost_per_daly, 2),
            "efficacy_percent": cases_averted_wolbachia_pct * 100
        },
        "dengvaxia": {
            "total_cost_usd": round(dengvaxia_total_cost, 2),
            "cost_per_person_usd": dengvaxia_cost_pp,
            "cases_averted": round(dengvaxia_cases_averted, 0),
            "dalys_averted": round(dengvaxia_dalys_averted, 2),
            "cost_per_daly_averted_usd": round(dengvaxia_cost_per_daly, 2),
            "efficacy_percent": cases_averted_dengvaxia_pct * 100
        },
        "analysis_summary": {
            "most_cost_effective_intervention": most_cost_effective,
            "cost_difference_per_daly_usd": round(cost_difference, 2),
            "cost_savings_percent": round(cost_savings_pct, 1),
            "who_cost_effectiveness_threshold_usd": 1800,  # WHO threshold for Singapore
            "wolbachia_meets_threshold": wolbachia_cost_per_daly <= 1800,
            "dengvaxia_meets_threshold": dengvaxia_cost_per_daly <= 1800
        }
    }
    
    # Print summary
    print(f"\nWolbachia Results:")
    print(f"  Cost per DALY: ${wolbachia_cost_per_daly:,.2f}")
    print(f"  Cases averted: {wolbachia_cases_averted:,.0f}")
    
    print(f"\nDengvaxia Results:")
    print(f"  Cost per DALY: ${dengvaxia_cost_per_daly:,.2f}")
    print(f"  Cases averted: {dengvaxia_cases_averted:,.0f}")
    
    print(f"\nConclusion: {most_cost_effective} is more cost-effective")
    print("Cost-Benefit Analysis complete.")
    
    return results

def save_analysis_results(results: dict, filepath: Path):
    """Saves the analysis results to a JSON file."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Analysis results saved to {filepath}")

def load_analysis_results(filepath: Path) -> dict:
    """Loads analysis results from a JSON file."""
    with open(filepath, 'r') as f:
        results = json.load(f)
    return results