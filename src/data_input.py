import pandas as pd
import json
from pathlib import Path
from typing import Dict, Union

class DataInput:
    def __init__(self):
        self.supported_formats = {'.csv', '.xlsx', '.json'}
        self.required_columns = [
            'product_id','product_name','life_cycle_stage','material_type',
            'quantity_kg','energy_consumption_kwh','transport_distance_km',
            'transport_mode','waste_generated_kg','recycling_rate',
            'landfill_rate','incineration_rate',
            'carbon_footprint_kg_co2e','water_usage_liters'
        ]

    def read_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        if p.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported format: {p.suffix}")
        if p.suffix == '.csv':
            return pd.read_csv(p)
        if p.suffix == '.xlsx':
            return pd.read_excel(p)
        return pd.read_json(p)

    def validate_data(self, df: pd.DataFrame) -> bool:
        # must have all required columns
        if not set(self.required_columns).issubset(df.columns):
            return False

        # numeric conversions
        num_cols = [
            'quantity_kg','energy_consumption_kwh','transport_distance_km',
            'waste_generated_kg','recycling_rate','landfill_rate',
            'incineration_rate','carbon_footprint_kg_co2e','water_usage_liters'
        ]
        for c in num_cols:
            if not pd.to_numeric(df[c], errors='coerce').notna().all():
                return False

        # only rows with any EoL rate >0 must sum ≈1
        rates = df[['recycling_rate','landfill_rate','incineration_rate']]
        mask = (rates.sum(axis=1) > 0)
        if mask.any():
            sums = rates.sum(axis=1)[mask]
            if not (sums.sub(1).abs().lt(1e-3).all()):
                return False

        return True

    def read_impact_factors(self, file_path: Union[str, Path]) -> Dict:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"Impact factors not found: {p}")
        if p.suffix != '.json':
            raise ValueError("Impact factors must be JSON")
        return json.loads(p.read_text())
