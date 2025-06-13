# %%
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_input      import DataInput
from calculations    import LCACalculator
from visualization   import LCAVisualizer
import matplotlib.pyplot as plt

# %%
# %%
di = DataInput()
df = di.read_data("data/raw/sample_data.csv")
assert di.validate_data(df)
calc = LCACalculator("data/raw/impact_factors.json")
imp  = calc.calculate_impacts(df)
viz  = LCAVisualizer()

# %%
# %%
fig1 = viz.plot_impact_breakdown(imp, "carbon_impact", "material_type")
fig1.suptitle("Carbon by Material")

# %%
# %%
pid  = imp.product_id.iloc[0]
fig2 = viz.plot_life_cycle_impacts(imp, pid)

# %%
prods = ["P001", "P002"]
fig3 = viz.plot_product_comparison(imp, prods)
fig3.suptitle("Comparison: P001 vs P002")
plt.show()

# %%
fig4 = viz.plot_end_of_life_breakdown(imp, pid)

# %%
fig5 = viz.plot_impact_correlation(imp)

# %%
plt.show()
# %%
if __name__ == "__main__":
    main()
# %%
