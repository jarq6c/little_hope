REPOSITORY=https://repo.anaconda.com/miniconda
INSTALLER=Miniconda3-py39_4.11.0-Linux-x86_64.sh
HASH=4ee9c3aa53329cd7a63b49877c0babb49b19b7e5af29807b793a76bdb1d362b4
HASHFILE=sha256sum.txt
PYENV=miniconda3
CONDA=$(PYENV)/bin/conda
PYTHON=$(PYENV)/bin/python3

.PHONY: environment checksum clean

environment: requirements.txt $(PYENV)/bin/activate
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -U wheel
	$(PYTHON) -m pip install -r requirements.txt
	
$(PYENV)/bin/activate: checksum
	test -d $(PYENV) || bash ./$(INSTALLER) -b -p $(PYENV)
	$(CONDA) update conda -y
	$(CONDA) install pip wheel -y
	touch $(PYENV)/bin/activate

checksum: $(INSTALLER) $(HASHFILE)
	sha256sum -c $(HASHFILE)

$(INSTALLER):
	wget $(REPOSITORY)/$(INSTALLER)

$(HASHFILE):
	echo "$(HASH) $(INSTALLER)" > $(HASHFILE)

clean:
	rm -rf $(PYENV) $(HASHFILE) $(INSTALLER)
