import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# EcoMat-LCA: Sustainable Textile Material & Lifecycle Analyzer
# Author: Sabbir Ahmed Riad
# Target Discipline: Materials Science / Environmental Science / Textile Sustainability
# ==============================================================================

class TextileMaterialAnalyzer:
    def __init__(self):
        # Database containing physical properties and lifecycle environmental metrics
        self.data = {
            'Material': ['Organic Cotton', 'Recycled PET', 'Hemp Fiber', 'Chitosan Bio-Polymer', 'Conventional Cotton'],
            'Tensile_Strength_MPa': [350, 750, 690, 120, 300],          # Mechanical property
            'Water_Consumption_L_kg': [2500, 100, 500, 50, 10000],        # Environmental metric
            'CO2_Emissions_kg_kg': [4.0, 3.5, 1.8, 1.2, 15.0],            # Global Warming Potential
            'Biodegradation_Days': [180, 18250, 90, 60, 180]            # End-of-life metric
        }
        self.df = pd.DataFrame(self.data)

    def calculate_sustainability_index(self):
        """
        Calculates a normalized Polymer Sustainability Index (PSI).
        Higher tensile strength + lower environmental impact = Higher PSI Score.
        """
        # Normalize metrics (0 to 1 scale)
        norm_strength = self.df['Tensile_Strength_MPa'] / self.df['Tensile_Strength_MPa'].max()
        norm_water = 1 - (self.df['Water_Consumption_L_kg'] / self.df['Water_Consumption_L_kg'].max())
        norm_co2 = 1 - (self.df['CO2_Emissions_kg_kg'] / self.df['CO2_Emissions_kg_kg'].max())
        norm_degradability = 1 - (self.df['Biodegradation_Days'] / self.df['Biodegradation_Days'].max())

        # Weighted calculation (Custom material science weighting matrix)
        self.df['PSI_Score'] = np.round(
            (norm_strength * 0.25) + 
            (norm_water * 0.25) + 
            (norm_co2 * 0.25) + 
            (norm_degradability * 0.25), 3
        ) * 100

        return self.df.sort_values(by='PSI_Score', ascending=False)

    def generate_tradeoff_plot(self):
        """Generates a Materials Selection Trade-off Plot (Tensile Strength vs CO2 Impact)."""
        plt.figure(figsize=(9, 5))
        plt.scatter(self.df['CO2_Emissions_kg_kg'], self.df['Tensile_Strength_MPa'], 
                    color='#2d6a4f', s=self.df['PSI_Score']*5, alpha=0.7, edgecolors='black')

        for i, txt in enumerate(self.df['Material']):
            plt.annotate(txt, (self.df['CO2_Emissions_kg_kg'][i]+0.2, self.df['Tensile_Strength_MPa'][i]+5), fontsize=10)

        plt.title('Material Property Trade-off: Mechanical Strength vs. Carbon Footprint', fontsize=12, fontweight='bold')
        plt.xlabel('Carbon Footprint (kg CO2e / kg material)', fontsize=10)
        plt.ylabel('Tensile Strength (MPa)', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('material_tradeoff_analysis.png', dpi=300)
        print("Chart successfully exported as 'material_tradeoff_analysis.png'")

if __name__ == "__main__":
    analyzer = TextileMaterialAnalyzer()
    results = analyzer.calculate_sustainability_index()
    print("=== POLYMER & TEXTILE SUSTAINABILITY INDEX RESULTS ===")
    print(results[['Material', 'Tensile_Strength_MPa', 'CO2_Emissions_kg_kg', 'PSI_Score']])
    analyzer.generate_tradeoff_plot()
