import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

class LCAVisualizer:
    def __init__(self):
        sns.set_style('whitegrid')
        self.colors = sns.color_palette('husl',8)
        self.labels = {
            'carbon_impact':'Carbon (kg CO₂e)',
            'energy_impact':'Energy (kWh)',
            'water_impact':'Water (L)',
            'waste_generated_kg':'Waste (kg)'
        }

    def plot_impact_breakdown(
        self, df: pd.DataFrame, impact: str, by: str, title: str=None
    ) -> plt.Figure:
        agg = df.groupby(by)[impact].sum()
        fig,ax = plt.subplots(figsize=(8,6))
        ax.pie(agg, labels=agg.index, autopct='%1.1f%%',
               colors=self.colors[:len(agg)])
        ax.set_title(title or f"{self.labels[impact]} by {by}")
        return fig

    def plot_life_cycle_impacts(
        self, df: pd.DataFrame, product_id: str
    ) -> plt.Figure:
        sub = df[df['product_id']==product_id]
        types = ['carbon_impact','energy_impact','water_impact','waste_generated_kg']
        fig,axes = plt.subplots(2,2,figsize=(12,10))
        axes = axes.flatten()
        for ax,key in zip(axes,types):
            tbl = sub.pivot_table(index='life_cycle_stage', values=key, aggfunc='sum')
            tbl.plot.bar(ax=ax, color=self.colors.pop(0))
            ax.set_title(self.labels[key])
            ax.tick_params(axis='x',rotation=45)
        plt.tight_layout()
        return fig

    def plot_product_comparison(
        self, df: pd.DataFrame, product_ids: list
    ) -> plt.Figure:
        tot = (
            df[df['product_id'].isin(product_ids)]
            .groupby('product_id')[['carbon_impact','energy_impact','water_impact']]
            .sum()
        )
        norm = tot.div(tot.max())
        cats = norm.columns.tolist()
        angles = np.linspace(0,2*np.pi,len(cats),endpoint=False).tolist()+[0]
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111,polar=True)
        for idx,row in norm.iterrows():
            vals = row.tolist()+[row.iloc[0]]
            ax.plot(angles,vals,label=idx)
            ax.fill(angles,vals,alpha=0.2)
        ax.set_xticks(angles[:-1]); ax.set_xticklabels(cats)
        ax.legend(loc='upper right',bbox_to_anchor=(1.3,1.1))
        ax.set_title("Product Comparison Across Impacts")
        return fig

    def plot_end_of_life_breakdown(
        self, df: pd.DataFrame, product_id: str
    ) -> plt.Figure:
        sub = df[df['product_id']==product_id]
        rates = sub[['recycling_rate','landfill_rate','incineration_rate']]
        fig,ax = plt.subplots(figsize=(8,6))
        rates.plot.bar(stacked=True,ax=ax)
        ax.set_ylim(0,1)
        ax.set_title(f"End-of-Life for {product_id}")
        return fig

    def plot_impact_correlation(
        self, df: pd.DataFrame
    ) -> plt.Figure:
        cols = ['carbon_impact','energy_impact','water_impact','waste_generated_kg']
        corr = df[cols].corr()
        fig,ax = plt.subplots(figsize=(6,5))
        sns.heatmap(corr,annot=True,cmap='coolwarm',ax=ax)
        ax.set_title("Impact Correlations")
        return fig