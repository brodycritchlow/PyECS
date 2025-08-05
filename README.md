<div>
<img align="left" src="https://github.com/user-attachments/assets/381e5656-b717-4748-8733-3ecc1889a23d" width="256" height="256" style="margin-right: 20px;" />
<br>
<br>
<br>
<br>

PyECS is a high-performance, type-safe Entity Component System (ECS) implementation in Python with runtime validation via [beartype](https://github.com/beartype/beartype).

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![ECS](https://img.shields.io/badge/pattern-ECS-orange.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://brodycritchlow.github.io/pyecs/)
[![CI](https://github.com/brodycritchlow/pyecs/actions/workflows/ci.yml/badge.svg)](https://github.com/brodycritchlow/pyecs/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/brodycritchlow/pyecs/branch/main/graph/badge.svg)](https://codecov.io/gh/brodycrit
chlow/pyecs)

<br clear="left"/>

---

### Documentation

Full documentation is available at [brodycritchlow.github.io/pyecs](https://brodycritchlow.github.io/PyECS/index.html)

### Features

- **Type-safe** - Runtime type checking with beartype ensures component and system integrity
- **Fast** - Archetype-based storage for efficient component queries
- **Pythonic** - Clean, intuitive API that follows Python conventions
- **Pure Python** - No C extensions or complex dependencies
- **Well-tested** - Comprehensive test suite with high coverage
- **Exception-based error handling** - Optional unsafe operations that raise exceptions instead of returning status codes

### Quick Start

### Installation

```bash
pip install pyecs
```

### Development

### Setup Development Environment

```bash
git clone https://github.com/brodycritchlow/pyecs.git
cd pyecs

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt
pip install -e .
```

### Building Documentation

```bash
pip install -e ".[docs]"

make docs-build
make docs-serve
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Type safety powered by [beartype](https://github.com/beartype/beartype)

---
