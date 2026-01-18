import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class FuzzySystem:
    def __init__(self):
        # 1. Define Antecedents (Inputs)
        # Caps Ratio: 0 to 100%
        self.caps_ratio = ctrl.Antecedent(np.arange(0, 101, 1), 'caps_ratio')
        
        # Provocative Score: 0 to 100
        self.provocative_score = ctrl.Antecedent(np.arange(0, 101, 1), 'provocative_score')
        
        # 2. Define Consequent (Output)
        # Hoax Likelihood: 0 to 100%
        self.hoax_likelihood = ctrl.Consequent(np.arange(0, 101, 1), 'hoax_likelihood')

        # 3. Define Membership Functions (Calibration)
        
        # Caps Ratio Memberships
        # Real news usually has low caps. Fake news screams with CAPS.
        self.caps_ratio['low'] = fuzz.trimf(self.caps_ratio.universe, [0, 0, 20])
        self.caps_ratio['medium'] = fuzz.trimf(self.caps_ratio.universe, [10, 30, 50])
        self.caps_ratio['high'] = fuzz.trapmf(self.caps_ratio.universe, [40, 60, 100, 100])

        # Provocative Score Memberships
        self.provocative_score['low'] = fuzz.trimf(self.provocative_score.universe, [0, 0, 30])
        self.provocative_score['medium'] = fuzz.trimf(self.provocative_score.universe, [20, 50, 80])
        self.provocative_score['high'] = fuzz.trapmf(self.provocative_score.universe, [60, 80, 100, 100])

        # Hoax Likelihood Memberships
        self.hoax_likelihood['safe'] = fuzz.trimf(self.hoax_likelihood.universe, [0, 0, 40])
        self.hoax_likelihood['suspicious'] = fuzz.trimf(self.hoax_likelihood.universe, [30, 50, 70])
        self.hoax_likelihood['hoax'] = fuzz.trapmf(self.hoax_likelihood.universe, [60, 80, 100, 100])

        # 4. Define Rules
        # Rule 1: High Caps OR High Provocation -> High Hoax Likelihood
        rule1 = ctrl.Rule(self.caps_ratio['high'] | self.provocative_score['high'], self.hoax_likelihood['hoax'])
        
        # Rule 2: Medium Caps AND Medium Provocation -> Suspicious
        rule2 = ctrl.Rule(self.caps_ratio['medium'] & self.provocative_score['medium'], self.hoax_likelihood['suspicious'])
        
        # Rule 3: Low Caps AND Low Provocation -> Safe
        rule3 = ctrl.Rule(self.caps_ratio['low'] & self.provocative_score['low'], self.hoax_likelihood['safe'])
        
        # Rule 4: High Provocation but Low Caps -> Suspicious (Smart clickbait)
        rule4 = ctrl.Rule(self.provocative_score['high'] & self.caps_ratio['low'], self.hoax_likelihood['suspicious'])

        # 5. Build Control System
        self.hoax_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self.hoax_sim = ctrl.ControlSystemSimulation(self.hoax_ctrl)

    def calculate(self, caps_val, prov_val):
        """
        Compute the fuzzy output.
        Returns: 
           - result_score: float (0-100)
           - label: str (Safe/Suspicious/Hoax)
        """
        self.hoax_sim.input['caps_ratio'] = min(caps_val, 100)
        self.hoax_sim.input['provocative_score'] = min(prov_val, 100)
        
        try:
            self.hoax_sim.compute()
            result_score = self.hoax_sim.output['hoax_likelihood']
        except Exception as e:
            # Fallback for edge cases
            result_score = 50.0

        # Determine label based on score (Defuzzified Label for UI)
        if result_score < 40:
            label = "REAL NEWS (Aman)"
        elif result_score < 70:
            label = "SUSPICIOUS (Perlu Verifikasi)"
        else:
            label = "HOAX (Berita Palsu)"
            
        return result_score, label

    def get_plots(self):
        """Returns matplotlib figures of the membership functions for visualization."""
        figs = []
        
        # Plot Caps Ratio
        fig1, ax1 = plt.subplots()
        self.caps_ratio.view(ax=ax1)
        ax1.set_title("Membership: Caps-lock Ratio")
        figs.append(fig1)
        
        # Plot Provocative Score
        fig2, ax2 = plt.subplots()
        self.provocative_score.view(ax=ax2)
        ax2.set_title("Membership: Provocative Score")
        figs.append(fig2)

        # Plot Output High
        fig3, ax3 = plt.subplots()
        self.hoax_likelihood.view(ax=ax3)
        ax3.set_title("Membership: Hoax Likelihood")
        figs.append(fig3)
        
        return figs
