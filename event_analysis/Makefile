REPOSITORY=https://repo.anaconda.com/miniconda
INSTALLER=Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
HASH=aef279d6baea7f67940f16aad17ebe5f6aac97487c7c03466ff01f4819e5a651
HASHFILE=sha256sum.txt
PYENV=miniconda3
CONDA=$(PYENV)/bin/conda

.PHONY: checksum clean

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
