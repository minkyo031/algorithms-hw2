PYTHON ?= python3
.PHONY: test serve experiment

test:
	$(PYTHON) -m unittest discover -s tests -v

serve:
	$(PYTHON) -m src.server

experiment:
	$(PYTHON) -m experiments.probe_experiment
	$(PYTHON) -m experiments.compare_experiment
