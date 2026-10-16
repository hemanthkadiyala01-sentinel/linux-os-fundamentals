# Synthetic Authentication Evaluation Corpus

This dataset contains 11 manually designed synthetic scenarios for
evaluating the repository's sudo detection rule.

- 4 scenarios expect an alert under the current rule.
- 7 scenarios expect no alert under the current rule.

## Schema

Each scenario contains:
- `scenario_id`: stable identifier
- `description`: purpose of the scenario
- `expected_alert`: expected result from the implemented rule
- `events`: synthetic input events

## Important interpretation

These labels specify expected rule behavior for these constructed
test cases. They do not establish whether any real-world activity
is malicious.

The dataset is small and intentionally designed around known rule
conditions. Results from this corpus must not be presented as
real-world detection accuracy or as a representative estimate of
false-positive or false-negative rates.
