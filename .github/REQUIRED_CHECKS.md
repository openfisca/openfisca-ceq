# Required GitHub Status Checks

This document lists the GitHub Actions status checks that should be required for branch protection rules.

## Recommended Required Checks

For the `master` branch protection, the following checks should be required:

### Minimum Required Checks (Recommended)

1. **Test (Python 3.7)** - `test (Python 3.7)`
   - Ensures basic compatibility with Python 3.7
   - Includes syntax check, style check, and full test suite

2. **Lint** - `lint`
   - Ensures code quality with ruff
   - Fast check that catches style and linting issues

### Optional Checks (Can be required for stricter enforcement)

3. **Test (Python 3.11)** - `test (Python 3.11)`
   - Ensures compatibility with latest Python version

4. **Build** - `build`
   - Ensures the package can be built successfully
   - Note: This already depends on `test` and `lint`, so requiring it adds redundancy but ensures build works

## How to Configure

1. Go to repository Settings → Branches
2. Edit or create branch protection rule for `master`
3. Enable "Require status checks to pass before merging"
4. Add the following checks:
   - `test (Python 3.7)`
   - `lint`
   - Optionally: `test (Python 3.11)` and `build`

## Check Names

The check names in GitHub Actions are:
- `test (Python 3.7)` - Test job with Python 3.7
- `test (Python 3.8)` - Test job with Python 3.8
- `test (Python 3.9)` - Test job with Python 3.9
- `test (Python 3.10)` - Test job with Python 3.10
- `test (Python 3.11)` - Test job with Python 3.11
- `lint` - Lint job
- `build` - Build job

## Notes

- The `deploy` job only runs on `master` branch pushes, not on PRs, so it should not be a required check
- All test matrix jobs run in parallel, so requiring multiple Python versions will ensure broader compatibility
- The `build` job already depends on `test` and `lint`, so requiring it ensures the full pipeline works
