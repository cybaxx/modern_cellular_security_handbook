PYTHON   = python3
SCRIPT   = compile_handbook.py
OUTPUT   = output

.PHONY: all build html light pdf epub clean install-deps

all: build

build: | install-deps
	@$(PYTHON) $(SCRIPT)

html: | install-deps
	@$(PYTHON) $(SCRIPT) --no-pdf

light: | install-deps
	@$(PYTHON) $(SCRIPT) --theme light

pdf: | install-deps
	@$(PYTHON) $(SCRIPT)

epub: | install-deps
	@$(PYTHON) $(SCRIPT) --epub

clean:
	@echo "  Cleaning build artifacts..."
	@rm -f $(OUTPUT)/*.pdf $(OUTPUT)/*.html $(OUTPUT)/*.epub
	@rm -f $(OUTPUT)/graphs/*.png
	@echo "  Done."

install-deps:
	@$(PYTHON) -m pip install -q -r requirements.txt 2>/dev/null || \
		echo "  [*] Run: pip install -r requirements.txt"
