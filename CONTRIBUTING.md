### Prerequisites

- Python 3.11
- Git

### Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Automatic Formatting

```bash
# Format the code
black .

# Sort the imports
isort .
```

### Check your code

```bash
pre-commit run --all-files
```
