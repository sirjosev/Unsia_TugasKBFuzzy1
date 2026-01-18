import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from nlp_engine import NLPEngine
    from fuzzy_logic import FuzzySystem
    print("[INFO] Modules imported successfully.")
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)

def test_system():
    nlp = NLPEngine()
    fuzzy = FuzzySystem()

    test_cases = [
        "VIRAL!! BABI NGEPET TERTANGKAP DI DEPOK!!",
        "Presiden Jokowi Meresmikan Tol Baru",
    ]

    print("\n--- Running Logic Verification ---")
    for text in test_cases:
        print(f"\nInput: {text}")
        
        # 1. NLP
        analysis = nlp.analyze(text)
        print(f"  NLP Metrics: Caps={analysis['caps_ratio']:.1f}%, Provocative={analysis['provocative_score']}")
        
        # 2. Fuzzy
        score, label = fuzzy.calculate(analysis['caps_ratio'], analysis['provocative_score'])
        print(f"  Fuzzy Result: {score:.1f}% -> {label}")
        
        # 3. Test Plotting (Logic check only)
        try:
            figs = fuzzy.get_plots(show_result=True)
            print(f"  Plots generated successfully: {len(figs)} figures.")
            plt.close('all')
        except Exception as e:
            print(f"  [ERROR] Plotting failed: {e}")

    print("\n[SUCCESS] Logic verification complete.")

if __name__ == "__main__":
    test_system()
