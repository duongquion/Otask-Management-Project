# GitHub Actions Workflow Troubleshooting Guide

## Issue: Workflow Not Triggering

### Problem Identified
The workflow file had **path filters** that excluded the workflow file itself. When you changed `.github/workflows/backend-cicd.yml`, it didn't match any of the filtered paths, so the workflow didn't trigger.

### Solution Applied
✅ Added `.github/workflows/backend-cicd.yml` to the path filters

### Additional Troubleshooting Steps

#### 1. Verify Workflow File Location
- ✅ File must be in `.github/workflows/` directory
- ✅ File must have `.yml` or `.yaml` extension
- ✅ File must be committed to the repository

#### 2. Check for Syntax Errors
Run this command locally to validate YAML:
```bash
# Install yamllint (if not installed)
pip install yamllint

# Validate the workflow file
yamllint .github/workflows/backend-cicd.yml
```

Or use online validator: https://www.yamllint.com/

#### 3. Verify Branch Names
The workflow triggers on:
- `main` branch
- `dev` branch

**Check your default branch:**
```bash
git branch -a
```

If your default branch is `master` instead of `main`, update the workflow:
```yaml
branches: [ "master", "main", "dev" ]
```

#### 4. Check Path Filters
Current path filters:
- `./src/backend/**`
- `./contrib/container/docker-compose.dev.yml`
- `./contrib/container/Dockerfile`
- `./.github/workflows/backend-cicd.yml` ✅ (just added)

**To trigger on ANY change** (remove path filters):
```yaml
on:
  push:
    branches: [ "main", "dev" ]
  pull_request:
    branches: [ "main", "dev" ]
```

#### 5. Check for Old Workflow Files
If you have an old `actions.yml` file, it might still be active:

```bash
# List all workflow files
ls -la .github/workflows/

# If actions.yml exists, either:
# Option A: Delete it
rm .github/workflows/actions.yml

# Option B: Rename it
mv .github/workflows/actions.yml .github/workflows/actions.yml.disabled
```

#### 6. Force Workflow Trigger
To manually trigger the workflow:

**Option A: Make a dummy change to trigger paths**
```bash
# Touch a file in src/backend
touch src/backend/.trigger
git add src/backend/.trigger
git commit -m "Trigger workflow"
git push
```

**Option B: Use workflow_dispatch (add to workflow)**
```yaml
on:
  workflow_dispatch:  # Allows manual trigger
  push:
    branches: [ "main", "dev" ]
    paths:
      - './src/backend/**'
      # ... other paths
```

Then trigger manually from GitHub Actions UI.

#### 7. Check GitHub Actions Settings
1. Go to repository Settings → Actions → General
2. Verify "Workflow permissions" are set correctly
3. Check if workflows are disabled for this repository

#### 8. Verify Commit and Push
```bash
# Check if workflow file is committed
git status

# If not committed:
git add .github/workflows/backend-cicd.yml
git commit -m "Update backend CI/CD workflow"
git push origin main  # or your branch name
```

#### 9. Check GitHub Actions Logs
1. Go to repository → Actions tab
2. Check if workflow appears in the list (even if not triggered)
3. Look for any error messages or warnings
4. Check "Workflow runs" section

#### 10. Test Workflow Syntax
Create a simple test workflow to verify GitHub Actions is working:

`.github/workflows/test.yml`:
```yaml
name: Test Workflow
on:
  push:
    branches: [ "main", "dev" ]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Test
        run: echo "Workflow is working!"
```

If this doesn't trigger, there's a repository-level issue.

## Common Issues and Solutions

### Issue: Workflow shows but doesn't run
**Cause:** Path filters don't match changed files
**Solution:** Add workflow file path to filters (already done) or remove filters

### Issue: Workflow runs but fails immediately
**Cause:** YAML syntax error
**Solution:** Validate YAML syntax, check indentation

### Issue: Old workflow still running
**Cause:** Old workflow file still exists
**Solution:** Delete or disable old workflow file

### Issue: Workflow not visible in Actions tab
**Cause:** File not committed or wrong location
**Solution:** Verify file location and commit status

## Next Steps

1. ✅ **Path filter fixed** - Workflow file path added to filters
2. **Commit and push** the updated workflow file
3. **Make a test change** to trigger the workflow:
   ```bash
   # Make a small change to trigger
   echo "# Test" >> src/backend/README.md
   git add src/backend/README.md
   git commit -m "Test workflow trigger"
   git push
   ```
4. **Monitor Actions tab** - Check if workflow appears and runs

## Verification Checklist

- [ ] Workflow file is in `.github/workflows/backend-cicd.yml`
- [ ] File is committed and pushed
- [ ] Branch name matches (`main` or `dev`)
- [ ] Path filters include workflow file path
- [ ] No YAML syntax errors
- [ ] No old `actions.yml` file exists
- [ ] GitHub Actions is enabled for repository
- [ ] Workflow appears in Actions tab

## Still Not Working?

If the workflow still doesn't trigger after following these steps:

1. **Check repository settings:**
   - Settings → Actions → General
   - Verify workflows are enabled

2. **Check branch protection:**
   - Settings → Branches
   - Verify workflow can run on protected branches

3. **Check for workflow_dispatch:**
   - Add `workflow_dispatch:` to allow manual triggers
   - Then trigger manually from Actions UI

4. **Contact GitHub Support:**
   - If nothing works, there might be a repository-level issue
