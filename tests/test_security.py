import unittest
import pandas as pd
import utils

class TestSecurity(unittest.TestCase):
    def test_csv_injection_mitigation(self):
        # malicious data
        rows = [
            {"Question": "=1+1", "Value Score": 10},
            {"Question": "@SUM(1,1)", "Value Score": 5},
            {"Question": "+2-1", "Value Score": 8},
            {"Question": "-1+2", "Value Score": 7},
            {"Question": "Safe Question", "Value Score": 1},
        ]

        df = pd.DataFrame(rows)
        sanitized_df = utils.sanitize_dataframe_for_csv(df)

        # Verify changes
        self.assertEqual(sanitized_df.iloc[0]["Question"], "'=1+1")
        self.assertEqual(sanitized_df.iloc[1]["Question"], "'@SUM(1,1)")
        self.assertEqual(sanitized_df.iloc[2]["Question"], "'+2-1")
        self.assertEqual(sanitized_df.iloc[3]["Question"], "'-1+2")
        self.assertEqual(sanitized_df.iloc[4]["Question"], "Safe Question")

        # Verify original df is unchanged (if copy was made)
        self.assertEqual(df.iloc[0]["Question"], "=1+1")

    def test_non_string_columns(self):
        rows = [{"Score": 10}, {"Score": -5}]
        df = pd.DataFrame(rows)
        sanitized_df = utils.sanitize_dataframe_for_csv(df)
        self.assertEqual(sanitized_df.iloc[1]["Score"], -5) # Number starting with - should remain number

if __name__ == '__main__':
    unittest.main()
