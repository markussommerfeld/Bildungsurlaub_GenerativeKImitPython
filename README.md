# Installation

## Environment

### Environment using `venv`

#### Installation und Aktivierung auf Mac/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Installation und Aktivierung auf Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Pakete installieren

Die benötigten Pakete sind in der requirements.txt Datei aufgelistet. Diese kann mit folgendem Befehl installiert werden:

```bash
pip install -r requirements.txt
```

Sofern die Pakete nicht installiert werden können, kann man sie auch einzeln installieren.

```bash
pip install <paketname>
```

### Environment using `uv`

```bash
pip install uv
```

## Install dependencies

```bash
uv sync --link-mode copy
```

## PyTorch special treatment

PyTorch is not yet fully supported for Python 3.13.

[PyTorch Issue #130249](https://github.com/pytorch/pytorch/issues/130249)

Thus, we need to install it manually.

```bash
pip3 install --pre torch --index-url https://download.pytorch.org/whl/nightly/cpu
```

# Weitere Materialien
