import unittest

import pandas as pd

from scripts.process import create_aggregations, preprocess


class ProcessPipelineTests(unittest.TestCase):
    def test_preprocess_removes_invalid_rows_and_adds_date_features(self):
        raw = pd.DataFrame(
            [
                {
                    "Transaction_ID": "1",
                    "Transaction_date": "2018-01-15T10:30:00",
                    "Gender": " Female ",
                    "Age": "30",
                    "Marital_status": " Single ",
                    "State_names": " Texas ",
                    "Segment": " Gold ",
                    "Employees_status": " workers ",
                    "Payment_method": " Card ",
                    "Referral": "1",
                    "Amount_spent": "100.50",
                },
                {
                    "Transaction_ID": "2",
                    "Transaction_date": "not-a-date",
                    "Gender": "Male",
                    "Age": "40",
                    "Marital_status": "Married",
                    "State_names": "Ohio",
                    "Segment": "Basic",
                    "Employees_status": "workers",
                    "Payment_method": "Cash",
                    "Referral": "0",
                    "Amount_spent": "25.00",
                },
                {
                    "Transaction_ID": "3",
                    "Transaction_date": "2018-02-01T08:00:00",
                    "Gender": "Female",
                    "Age": "unknown",
                    "Marital_status": "Single",
                    "State_names": "Iowa",
                    "Segment": "Silver",
                    "Employees_status": "self-employed",
                    "Payment_method": "PayPal",
                    "Referral": "",
                    "Amount_spent": "70.00",
                },
            ]
        )

        cleaned = preprocess(raw)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned.loc[0, "Gender"], "Female")
        self.assertEqual(cleaned.loc[0, "Segment"], "Gold")
        self.assertEqual(cleaned.loc[0, "Year"], 2018)
        self.assertEqual(cleaned.loc[0, "Month"], 1)
        self.assertEqual(cleaned.loc[0, "Quarter"], 1)
        self.assertEqual(cleaned.loc[0, "Hour"], 10)
        self.assertEqual(cleaned.loc[0, "Month_Year"], "2018-01")

    def test_create_aggregations_produces_expected_totals(self):
        cleaned = pd.DataFrame(
            [
                {
                    "Transaction_ID": "1",
                    "Month_Year": "2018-01",
                    "Year": 2018,
                    "Quarter": 1,
                    "Segment": "Gold",
                    "State_names": "Texas",
                    "Payment_method": "Card",
                    "Amount_spent": 100.0,
                },
                {
                    "Transaction_ID": "2",
                    "Month_Year": "2018-01",
                    "Year": 2018,
                    "Quarter": 1,
                    "Segment": "Gold",
                    "State_names": "Texas",
                    "Payment_method": "Cash",
                    "Amount_spent": 50.0,
                },
                {
                    "Transaction_ID": "3",
                    "Month_Year": "2018-02",
                    "Year": 2018,
                    "Quarter": 1,
                    "Segment": "Basic",
                    "State_names": "Ohio",
                    "Payment_method": "Card",
                    "Amount_spent": 25.0,
                },
            ]
        )

        monthly, quarterly, segment, state, payment = create_aggregations(cleaned)

        january = monthly.loc[monthly["Month_Year"] == "2018-01"].iloc[0]
        self.assertEqual(january["total_sales"], 150.0)
        self.assertEqual(january["transaction_count"], 2)

        self.assertEqual(quarterly.loc[0, "total_sales"], 175.0)
        self.assertEqual(segment.loc[segment["Segment"] == "Gold", "total_sales"].iloc[0], 150.0)
        self.assertEqual(state.loc[state["State_names"] == "Texas", "transaction_count"].iloc[0], 2)
        self.assertEqual(payment.loc[payment["Payment_method"] == "Card", "total_sales"].iloc[0], 125.0)


if __name__ == "__main__":
    unittest.main()
