# Data dictionary

The scored dataset contains 30 manually designed Spanish-language test interactions with Mango customer-service chatbot.

| Field | Description |
|---|---|
| `id` | Unique test identifier (Q01-Q30). |
| `category` | Query category: shipping, returns, orders, products, payments, availability, complaints, complex_queries. |
| `user_query` | Prompt submitted to the chatbot. |
| `assistant_response` | Full captured chatbot response. |
| `test_date` | Date of the recorded interaction (ISO date). |
| `accuracy_score` | Accuracy and reliability score (1-4). |
| `relevance_score` | Relevance and resolution score (1-4). |
| `language_score` | Linguistic quality score (1-4). |
| `tone_score` | Tone and communication appropriateness score (1-4). |
| `complexity_score` | Handling of complex queries score (1-4). |
| `notes` | Evaluator's qualitative observation. |

The composite score is calculated in the analysis script as the sum of the five criterion scores (range 5-20). It is a derived variable and is not stored as an input field in the source dataset.
