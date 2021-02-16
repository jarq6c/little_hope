# Workflow options
PYENV?=env
PYTHON=$(PYENV)/bin/python3
SCRIPT=little_hope.py
OUTPUTS=peak_histogram.png streamflow.png nwisiv_cache.sqlite

.PHONY: clean

run: $(PYENV)/bin/activate
	$(PYTHON) $(SCRIPT)

$(PYENV)/bin/activate: requirements.txt
	test -d $(PYENV) || python3 -m venv $(PYENV)
	$(PYTHON) -m pip install -U pip wheel setuptools
	$(PYTHON) -m pip install -r requirements.txt
	touch $(PYENV)/bin/activate

clean:
	rm -rf $(PYENV) $(OUTPUTS)
	