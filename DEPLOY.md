# Deployment Guide for PyPI

## Prerequisites

1. Install build tools:
```bash
pip install --upgrade pip setuptools wheel twine build
```

2. Ensure you have PyPI credentials ready:
   - Username (or `__token__` for API tokens)
   - Password (or your API token)

## Pre-deployment Checklist

- [ ] Version number updated in:
  - [ ] `setup.py` (version='1.0.9')
  - [ ] `pyproject.toml` (version = "1.0.9")
  - [ ] Update download_url in both files to match new version tag
- [ ] CHANGELOG or release notes updated (if you have one)
- [ ] All tests passing
- [ ] README.md is up to date
- [ ] Git changes committed

## Building the Distribution

### Clean old builds
```bash
rm -rf build/ dist/ *.egg-info
```

### Build using modern tools (recommended)
```bash
python -m build
```

Or using setup.py:
```bash
python setup.py sdist bdist_wheel
```

### Check the build
```bash
twine check dist/*
```

## Testing on TestPyPI (Optional but Recommended)

1. Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```

2. Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps iaklogger
```

3. Test the package works correctly

## Deploy to PyPI

### Upload to PyPI
```bash
twine upload dist/*
```

You'll be prompted for:
- Username: (your PyPI username or `__token__`)
- Password: (your PyPI password or API token)

### Verify Installation
```bash
pip install --upgrade iaklogger
```

## Post-deployment

1. Create and push a git tag:
```bash
git tag -a v1.0.9 -m "Release version 1.0.9"
git push origin v1.0.9
```

2. Create a GitHub release:
   - Go to https://github.com/Iakl/iaklogger/releases
   - Click "Create a new release"
   - Select the tag you just created
   - Add release notes
   - Publish release

3. Verify the package on PyPI:
   - Check https://pypi.org/project/iaklogger/

## Using API Tokens (Recommended)

For better security, use PyPI API tokens instead of passwords:

1. Generate token at https://pypi.org/manage/account/token/
2. Create/update `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-API-TOKEN-HERE
```

3. Set permissions:
```bash
chmod 600 ~/.pypirc
```

## Troubleshooting

### "File already exists" error
- You cannot overwrite an existing version on PyPI
- Increment the version number and rebuild

### Authentication errors
- Verify your credentials
- Try using API tokens instead of passwords
- Check ~/.pypirc permissions (should be 600)

### Import errors after installation
- Check that all dependencies are listed in install_requires
- Verify package structure with `pip show iaklogger`

### Missing files in distribution
- Check MANIFEST.in includes all necessary files
- Use `tar -tzf dist/iaklogger-1.0.9.tar.gz` to inspect contents

## Quick Commands Reference

```bash
# Complete workflow
rm -rf build/ dist/ *.egg-info
python -m build
twine check dist/*
twine upload dist/*
git tag -a v1.0.9 -m "Release version 1.0.9"
git push origin v1.0.9
```
