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

### Code Style

We follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) with one exception:

- Indentation: 4 spaces (PEP 8) instead of 2 spaces (Google Style)

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

### Running the Tests

```bash
# Run the tests
pytest
```
