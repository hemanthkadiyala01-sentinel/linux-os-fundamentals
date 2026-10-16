# Synthetic Authentication Evaluation Corpus

This corpus contains 26 labeled, manually constructed scenarios
for the repository's sudo detection rule.

## Activity labels

- `suspicious`: scenario context is intended to represent suspicious
  activity relevant to this detection use case.
- `benign`: scenario context says the activity is authorized, routine,
  or a controlled benign test.
- `ambiguous`: the available events do not support a reliable benign
  or suspicious judgment. These cases are excluded from activity-label
  classification metrics.

## Corpus summary

| Activity label | Scenarios |
|---|---:|
| Suspicious | 10 |
| Benign | 11 |
| Ambiguous | 5 |
| Total | 26 |

`expected_alert` is a separate rule-regression expectation. It means
what the current detection rule is expected to output for the supplied
events; it does not mean the activity is truly malicious.

Each scenario includes a `labeling_rationale` describing why the
activity label was assigned and why the rule should or should not alert.

## Evaluation interpretation

Two results are kept separate:

1. Rule-regression agreement: actual output versus `expected_alert`.
2. Activity-label metrics: actual alerts versus the scenario's benign
   or suspicious contextual label, excluding ambiguous scenarios.

This distinction matters. An authorized but non-allowlisted command
can trigger a rule alert, producing a context-driven false positive.
A suspicious scenario with missing telemetry can fail to trigger an
alert, producing a false negative.

The dataset is small, manually designed, and not representative of
production traffic. It must not be used to claim real-world accuracy,
operational false-positive rates, or generalization to unseen attacks.
