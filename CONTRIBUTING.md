# Contributing to Zero-Shield CLI

We welcome contributions! Here's how you can help:

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/zero-shield-cli.git`
3. Create a branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Run tests: `python3 tests/test_comprehensive_e2e.py`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp environments/local/.env.example .env
# Edit .env with your credentials

# Run tests
python3 test_comprehensive_e2e.py
python3 test_security_fixes.py
```

## Code Style

- Follow PEP 8 guidelines
- Add docstrings to new functions
- Include type hints where appropriate
- Write tests for new features

## Testing

All new features must include tests:
- Add tests to `test_comprehensive_e2e.py`
- Ensure 100% pass rate before submitting PR

## Documentation

Update documentation for new features:
- User-facing: `docs/user-guide/`
- Technical: `docs/architecture/`
- Examples: `docs/user-guide/EXAMPLES.md`

## Questions?

Open an issue or discussion on GitHub.

Thank you for contributing! 


---

**Project Maintainer:** Jeri L3D | JeriSadeuM  
**Repository:** https://github.com/jerisadeumai/zero-shield-cli  
**Copyright © 2026 Jeri L3D | JeriSadeuM | All Rights Reserved**
