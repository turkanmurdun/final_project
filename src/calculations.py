import pandas as pd
from typing import List, Dict, Union
from pathlib import Path
from data_input import DataInput

class LCACalculator:
    def __init__(self, impact_factors_path: Union[str, Path]=None):
        self.impact_factors = {}
        if impact_factors_path:
            di = DataInput()
            self.impact_factors = di.read_impact_factors(impact_factors_path)

    def calculate_impacts(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        # normalize keys
        df['material_type']   = df['material_type'].str.lower()
        df['life_cycle_stage']= df['life_cycle_stage'].str.lower()
        # flatten the JSON into a lookup DataFrame
        fac_rows = []
        for mat, stages in self.impact_factors.items():
            for stg, imp in stages.items():
                fac_rows.append({'material_type':mat,'life_cycle_stage':stg,**imp})
        fac_df = pd.DataFrame(fac_rows)
        # merge + fill missing factors with 0
        merged = df.merge(fac_df, on=['material_type','life_cycle_stage'], how='left').fillna(0)

        # vectorized impact calculations
        merged['carbon_impact'] = (
            merged['quantity_kg']*merged['carbon_impact']+
            merged['carbon_footprint_kg_co2e']
        )
        merged['energy_impact'] = (
            merged['quantity_kg']*merged['energy_impact']+
            merged['energy_consumption_kwh']
        )
        merged['water_impact'] = (
            merged['quantity_kg']*merged['water_impact']+
            merged['water_usage_liters']
        )
        return merged

    def calculate_total_impacts(self, imp: pd.DataFrame) -> pd.DataFrame:
        return (
            imp.groupby(['product_id','product_name'])
               .agg({
                 'carbon_impact':'sum',
                 'energy_impact':'sum',
                 'water_impact':'sum',
                 'waste_generated_kg':'sum'
               }).reset_index()
        )

    def normalize_impacts(self, tot: pd.DataFrame) -> pd.DataFrame:
        out = tot.copy()
        for c in ['carbon_impact','energy_impact','water_impact']:
            mx = tot[c].max()
            if mx>0:
                out[c] = tot[c]/mx
        return out

    def compare_alternatives(self, imp: pd.DataFrame, product_ids: List[str]) -> pd.DataFrame:
        # sum per product
        tot = (
            imp[imp['product_id'].isin(product_ids)]
            .groupby(['product_id','product_name'])
            [['carbon_impact','energy_impact','water_impact']]
            .sum().reset_index()
        )
        # for each impact, compute % difference relative to the **minimum** value
        for c in ['carbon_impact','energy_impact','water_impact']:
            mn = tot[c].min()
            tot[f'{c}_relative'] = 0 if mn==0 else (tot[c]-mn)/mn*100
        return tot
