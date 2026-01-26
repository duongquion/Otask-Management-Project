# GitHub Actions Workflow: Detailed Explanation

## Table of Contents
1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Execution Flow](#execution-flow)
4. [Advanced Syntax Explained](#advanced-syntax-explained)
5. [Key Concepts](#key-concepts)
6. [Step-by-Step Breakdown](#step-by-step-breakdown)

---

## Overview

This GitHub Actions workflow automates the CI/CD pipeline for a Django backend application. It performs:
- **Code Quality Checks** (linting, formatting)
- **Testing** (unit tests with coverage)
- **Security Scanning** (vulnerability detection)
- **Docker Image Building** (multi-platform)
- **Smoke Testing** (post-deployment validation)

---

## File Structure

```yaml
name: Backend CI/CD          # Workflow name (displayed in GitHub UI)
on:                         # Trigger conditions
env:                        # Global environment variables
jobs:                       # Workflow jobs (run in parallel or sequence)
  job-name:
    steps:                  # Individual commands/actions
```

---

## Execution Flow

### High-Level Flow Diagram

```
┌─────────────────┐
│  Push/PR Event  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Concurrency     │  ← Cancel in-progress runs
│  Check           │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │  PARALLEL  │
    └─────┬─────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
┌─────────┐ ┌─────────────┐
│  lint   │ │  security   │
│  check  │ │   scan      │
└────┬────┘ └──────┬──────┘
     │             │
     └──────┬──────┘
            │
            ▼
     ┌──────────────┐
     │ quality-check│  ← Depends on lint-and-format
     │   (tests)    │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ build-and-   │  ← Depends on quality-check + security-scan
     │   push       │
     └──────┬───────┘
            │
            ▼
     ┌──────────────┐
     │ smoke-test   │  ← Only on main branch pushes
     └──────────────┘
```

### Detailed Execution Sequence

1. **Trigger**: Push to `main`/`dev` or PR targeting these branches
2. **Path Filtering**: Only runs if files in `src/backend/**` or Docker files change
3. **Concurrency**: Cancels any in-progress runs for the same branch/PR
4. **Parallel Jobs**:
   - `lint-and-format` (runs first)
   - `security-scan` (runs in parallel with lint)
5. **Sequential Jobs**:
   - `quality-check` (waits for `lint-and-format`)
   - `build-and-push` (waits for both `quality-check` and `security-scan`)
   - `smoke-test` (waits for `build-and-push`, only on main branch)

---

## Advanced Syntax Explained

### 1. **Workflow Triggers (`on:`)** - Lines 3-15

```yaml
on:
  push:
    branches: [ "main", "dev" ]
    paths:
      - './src/backend/**' 
  pull_request:
    branches: [ "main", "dev" ]
    paths:
      - './src/backend/**'
```

**Explanation:**
- **`on:`** - Defines when the workflow runs
- **`push:`** - Triggers on git push events
- **`pull_request:`** - Triggers on PR creation/updates
- **`branches:`** - Specific branches that trigger the workflow
- **`paths:`** - Path filters (only runs if these paths change)
  - `**` is a glob pattern meaning "any file/folder recursively"
  - `./src/backend/**` matches all files under `src/backend/`

**Advanced:** Path filters use AND logic - if ANY path matches, workflow runs.

---

### 2. **Concurrency Control** - Lines 17-20

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Explanation:**
- **`concurrency:`** - Controls parallel workflow runs
- **`group:`** - Groups workflows that should be mutually exclusive
  - `${{ github.workflow }}` = workflow name ("Backend CI/CD")
  - `${{ github.ref }}` = git ref (branch name or PR ref)
  - Example group: `Backend CI/CD-refs/heads/main`
- **`cancel-in-progress: true`** - Cancels older runs when a new one starts

**Use Case:** Prevents multiple runs for the same branch, saving CI minutes.

---

### 3. **Global Environment Variables (`env:`)** - Lines 22-26

```yaml
env:
  REGISTRY: docker.io
  IMAGE_NAME: otask-backend
  PYTHON_VERSION: "3.12"
  COVERAGE_THRESHOLD: "80"
```

**Explanation:**
- **`env:`** - Variables available to ALL jobs
- Accessible via `${{ env.VARIABLE_NAME }}`
- Can be overridden at job or step level

**Example Usage:**
```yaml
run: echo "Building ${{ env.IMAGE_NAME }}"
```

---

### 4. **Job Dependencies (`needs:`)** - Line 77

```yaml
quality-check:
  needs: lint-and-format
```

**Explanation:**
- **`needs:`** - Defines job dependencies
- `quality-check` waits for `lint-and-format` to complete successfully
- If `lint-and-format` fails, `quality-check` is skipped (unless `if:` condition overrides)

**Multiple Dependencies:**
```yaml
build-and-push:
  needs: [quality-check, security-scan]  # Waits for BOTH
```

---

### 5. **Conditional Execution (`if:`)** - Line 313

```yaml
build-and-push:
  if: github.event_name == 'push'
```

**Explanation:**
- **`if:`** - Conditional execution
- Only runs if condition is true
- Uses GitHub Actions expression syntax

**Common Conditions:**
```yaml
if: github.event_name == 'push'                    # Only on push
if: github.ref == 'refs/heads/main'               # Only main branch
if: success()                                      # Previous step succeeded
if: always()                                       # Always run (even on failure)
if: failure()                                      # Only on failure
if: github.event_name == 'push' && github.ref == 'refs/heads/main'  # Combined
```

---

### 6. **Service Containers (`services:`)** - Lines 80-103

```yaml
services:
  postgres:
    image: postgres:17
    env:
      POSTGRES_DB: ${{ secrets.DB_NAME || 'test_db' }}
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
```

**Explanation:**
- **`services:`** - Docker containers that run alongside the job
- Available on `localhost` during job execution
- **`env:`** - Environment variables for the service
- **`ports:`** - Port mappings (host:container)
- **`options:`** - Docker run options
  - `>-` is YAML multiline string (folds newlines into spaces)
  - `--health-cmd` - Health check command
  - Health checks ensure service is ready before job starts

**Access Pattern:**
```yaml
run: |
  psql -h localhost -U user -d database  # Connect to postgres service
```

---

### 7. **Expression Syntax (`${{ }}`)** - Throughout

```yaml
${{ github.ref_name }}           # Branch name (e.g., "main")
${{ github.sha }}                # Commit SHA (full)
${{ github.event_name }}          # Event type ("push", "pull_request")
${{ secrets.DB_NAME }}            # Secret value
${{ secrets.DB_NAME || 'test_db' }}  # Default value if secret missing
${{ env.IMAGE_NAME }}             # Environment variable
${{ steps.meta.outputs.tags }}    # Step output
```

**Explanation:**
- **`${{ }}`** - GitHub Actions expression syntax
- Evaluated at runtime
- Can use operators: `==`, `!=`, `&&`, `||`, `!`
- **`||`** - Logical OR, used for default values

**Advanced Examples:**
```yaml
# Conditional value
${{ github.event_name == 'push' && 'production' || 'staging' }}

# String concatenation
${{ github.ref_name }}-${{ github.sha }}

# Array access
${{ github.event.pull_request.labels[0].name }}
```

---

### 8. **Step Outputs (`id:` and `outputs`)** - Lines 125, 334, 347

```yaml
- name: Extract metadata
  id: meta                    # Step identifier
  uses: docker/metadata-action@v5
  # ... outputs available as steps.meta.outputs.*

- name: Use output
  run: echo "${{ steps.meta.outputs.tags }}"
```

**Explanation:**
- **`id:`** - Unique identifier for a step
- Allows referencing step outputs later
- Outputs accessed via `${{ steps.STEP_ID.outputs.OUTPUT_NAME }}`

**Custom Outputs:**
```yaml
- name: Set output
  id: custom
  run: |
    echo "value=hello" >> $GITHUB_OUTPUT  # Set output
    # Or in older syntax:
    echo "::set-output name=value::hello"
```

---

### 9. **Multiline Strings (`|` and `>-`)** - Lines 89-93, 185-196

```yaml
# Literal block scalar (preserves newlines)
options: |
  --health-cmd pg_isready
  --health-interval 10s

# Folded block scalar (folds newlines into spaces)
options: >-
  --health-cmd pg_isready
  --health-interval 10s
```

**Explanation:**
- **`|`** - Literal block (preserves line breaks)
- **`>-`** - Folded block (converts newlines to spaces, trims trailing newline)
- **`>`** - Folded block (keeps final newline)

**When to Use:**
- `|` - Multi-line scripts, commands
- `>-` - Long single-line strings (Docker options)
- `>` - Similar to `>-` but keeps trailing newline

---

### 10. **Caching (`actions/cache`)** - Lines 43-49

```yaml
- name: Cache linting dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-linting-${{ hashFiles('src/backend/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-linting-
```

**Explanation:**
- **`path:`** - Directory to cache
- **`key:`** - Unique cache key
  - `${{ runner.os }}` - Operating system (Linux, Windows, macOS)
  - `hashFiles()` - Generates hash of file contents
  - If requirements.txt changes, cache key changes
- **`restore-keys:`** - Fallback keys (partial matches)
  - If exact key not found, tries partial matches
  - `-` at end means "any key starting with this prefix"

**Cache Flow:**
1. Check for exact key match
2. If not found, check restore-keys (partial matches)
3. Restore cache if found
4. After step completes, save cache with new key

---

### 11. **Docker Build Cache (`cache-from`/`cache-to`)** - Lines 132-133

```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

**Explanation:**
- **`cache-from: type=gha`** - Use GitHub Actions cache for Docker layers
- **`cache-to: type=gha,mode=max`** - Save cache to GitHub Actions
  - `mode=max` - Cache all layers (not just final image)
- **`type=gha`** - GitHub Actions cache backend

**Benefits:**
- Faster builds (reuses layers)
- Reduces Docker Hub API calls
- Works across workflow runs

---

### 12. **Docker Metadata Action** - Lines 333-344

```yaml
- name: Extract metadata
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: ${{ secrets.DOCKER_USERNAME }}/${{ env.IMAGE_NAME }}
    tags: |
      type=ref,event=branch
      type=ref,event=pr
      type=semver,pattern={{version}}
      type=sha,prefix={{branch}}-
      type=raw,value=latest,enable={{is_default_branch}}
```

**Explanation:**
- Generates Docker image tags automatically
- **Tag Types:**
  - `type=ref,event=branch` - Tag with branch name (e.g., `main`, `dev`)
  - `type=ref,event=pr` - Tag with PR number (e.g., `pr-123`)
  - `type=semver` - Semantic versioning tags (e.g., `v1.2.3`)
  - `type=sha` - Commit SHA with prefix (e.g., `main-abc123`)
  - `type=raw` - Static tag (e.g., `latest`)
  - `enable={{is_default_branch}}` - Only tag if default branch

**Output:**
```yaml
steps.meta.outputs.tags: "user/otask-backend:main,user/otask-backend:main-abc123,user/otask-backend:latest"
steps.meta.outputs.labels: "org.opencontainers.image.title=..."
```

---

### 13. **Conditional Step Execution (`if:` on steps)** - Lines 201, 218, 244

```yaml
- name: Parse and Display Test Results
  if: always()    # Run even if previous step failed
  run: ...

- name: Copy test results
  if: success()   # Only if previous step succeeded
  run: ...
```

**Explanation:**
- **`if: always()`** - Always run (even on failure)
- **`if: success()`** - Only if all previous steps succeeded
- **`if: failure()`** - Only if previous step failed
- **`if: cancelled()`** - Only if workflow was cancelled

**Use Cases:**
- `always()` - Cleanup, artifact uploads, notifications
- `success()` - Deployment, publishing
- `failure()` - Error reporting, rollback

---

### 14. **GitHub Step Summary (`$GITHUB_STEP_SUMMARY`)** - Lines 204-211

```yaml
echo "## Test Results Summary" >> $GITHUB_STEP_SUMMARY
echo "- **Total Tests:** $tests" >> $GITHUB_STEP_SUMMARY
```

**Explanation:**
- **`$GITHUB_STEP_SUMMARY`** - Special file for job summary
- Content appears in GitHub Actions UI
- Supports Markdown formatting
- Multiple steps can append to it

**Markdown Support:**
- Headers (`##`)
- Lists (`-`, `*`)
- Bold (`**text**`)
- Emojis (`✅`, `❌`, `⚠️`)

---

### 15. **Docker Volume Mounts (`-v`)** - Line 183

```yaml
docker run -v ${{ github.workspace }}/test-results:/app/test-results
```

**Explanation:**
- **`-v host:container`** - Bind mount
- `${{ github.workspace }}` - GitHub Actions workspace directory
- Files written in container at `/app/test-results` appear in host at `./test-results`
- Enables sharing files between container and host

**Pattern:**
```yaml
-v ${{ github.workspace }}/local-path:/container-path
```

---

### 16. **Shell Script Syntax (`set -e`)** - Line 186

```yaml
sh -c "
  set -e              # Exit on error
  command1 &&         # Run command2 only if command1 succeeds
  command2 &&         # Run command3 only if command2 succeeds
  command3
"
```

**Explanation:**
- **`set -e`** - Exit immediately if any command fails
- **`&&`** - Logical AND (run next command only if previous succeeds)
- **`||`** - Logical OR (run next command if previous fails)
- **`;`** - Sequential execution (always runs)

**Examples:**
```bash
command1 && command2    # command2 only if command1 succeeds
command1 || command2    # command2 only if command1 fails
command1 ; command2     # Always run both
```

---

### 17. **Permissions** - Lines 316-318

```yaml
permissions:
  contents: read
  packages: write
```

**Explanation:**
- **`permissions:`** - Fine-grained access control
- **`contents: read`** - Read repository contents
- **`packages: write`** - Write to GitHub Packages (Docker registry)
- Default permissions depend on repository settings
- Explicit permissions recommended for security

**Common Permissions:**
- `contents: read/write` - Repository access
- `packages: read/write` - Package registry
- `actions: read/write` - Workflow access
- `pull-requests: write` - PR comments/labels

---

### 18. **Timeout** - Lines 32, 78, 289

```yaml
timeout-minutes: 10
```

**Explanation:**
- Prevents jobs from running indefinitely
- Job is cancelled if timeout exceeded
- Useful for preventing stuck builds

---

### 19. **Working Directory (`working-directory:`)** - Line 52

```yaml
- name: Install dependencies
  working-directory: ./src/backend
  run: pip install ...
```

**Explanation:**
- Changes current directory for the step
- All commands in step run from this directory
- Relative paths are relative to this directory

---

### 20. **Continue on Error (`continue-on-error:`)** - Line 71

```yaml
- name: Type check
  continue-on-error: true
  run: mypy ...
```

**Explanation:**
- Step failure doesn't fail the job
- Job continues even if step fails
- Useful for optional checks

---

## Key Concepts

### 1. **Job vs Step**
- **Job**: Independent unit of work (runs on separate runner)
- **Step**: Individual command/action within a job
- Jobs can run in parallel or sequence
- Steps always run sequentially within a job

### 2. **Runner**
- Virtual machine that executes jobs
- `runs-on: ubuntu-latest` specifies runner OS
- Each job gets a fresh runner

### 3. **Actions**
- Reusable units of work
- **`uses:`** - Uses a pre-built action
- **`run:`** - Executes shell commands
- Actions can be:
  - Official GitHub actions (`actions/checkout@v4`)
  - Community actions (`docker/login-action@v3`)
  - Local actions (`.github/actions/my-action`)

### 4. **Secrets**
- Stored in repository settings
- Accessed via `${{ secrets.SECRET_NAME }}`
- Automatically masked in logs
- Never exposed in workflow files

### 5. **Artifacts**
- Files saved from workflow runs
- Can be downloaded later
- **`actions/upload-artifact`** - Upload files
- **`actions/download-artifact`** - Download files

---

## Step-by-Step Breakdown

### Job 1: `lint-and-format`

**Purpose:** Code quality checks

**Steps:**
1. Checkout code
2. Set up Python
3. Cache dependencies
4. Install linting tools
5. Run formatting checks (black, isort)
6. Run linting (flake8)
7. Optional type checking (mypy)

**Key Features:**
- Runs first (other jobs depend on it)
- Fast execution (< 10 minutes)
- Fails fast if code quality issues found

---

### Job 2: `quality-check`

**Purpose:** Run tests and generate reports

**Dependencies:** `lint-and-format`

**Services:**
- PostgreSQL (database)
- Redis (cache/queue)

**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Create .env file
4. Build Docker image
5. Wait for services
6. Run migrations
7. Run tests with coverage
8. Parse test results
9. Check coverage threshold
10. Upload artifacts
11. Copy files for SonarQube
12. Run SonarQube scan

**Key Features:**
- Longest job (45 min timeout)
- Generates test and coverage reports
- Enforces coverage threshold
- Integrates with SonarQube

---

### Job 3: `security-scan`

**Purpose:** Vulnerability scanning

**Dependencies:** `lint-and-format`

**Steps:**
1. Checkout code
2. Run Trivy scanner
3. Upload results to GitHub Security

**Key Features:**
- Runs in parallel with quality-check
- Scans for CRITICAL and HIGH vulnerabilities
- Results appear in GitHub Security tab

---

### Job 4: `build-and-push`

**Purpose:** Build and push Docker image

**Dependencies:** `quality-check`, `security-scan`

**Condition:** Only on push events (not PRs)

**Steps:**
1. Checkout code
2. Set up Docker Buildx
3. Login to Docker Hub
4. Extract metadata (tags)
5. Build and push image
6. Display image details

**Key Features:**
- Multi-platform build (amd64, arm64)
- Automatic tagging
- Docker layer caching
- Only runs on push (not PRs)

---

### Job 5: `smoke-test`

**Purpose:** Validate deployed image

**Dependencies:** `build-and-push`

**Condition:** Only on main branch pushes

**Steps:**
1. Checkout code
2. Install tools
3. Pull and run image
4. Wait for application
5. Health checks
6. Cleanup

**Key Features:**
- Validates image actually works
- Tests real deployment scenario
- Only runs on main branch
- Always cleans up containers

---

## Advanced Patterns

### 1. **Error Handling with Fallbacks**

```yaml
docker pull image:tag || docker pull image:latest
```

### 2. **Conditional Values**

```yaml
${{ github.event_name == 'push' && 'prod' || 'dev' }}
```

### 3. **String Manipulation**

```yaml
${{ github.ref_name }}-${{ github.sha }}  # Concatenation
```

### 4. **Array Operations**

```yaml
needs: [job1, job2]  # Array syntax
```

### 5. **Nested Expressions**

```yaml
${{ steps.meta.outputs.tags }}  # Access nested properties
```

---

## Best Practices Demonstrated

1. ✅ **Path filtering** - Only runs when relevant files change
2. ✅ **Concurrency control** - Prevents duplicate runs
3. ✅ **Caching** - Speeds up builds
4. ✅ **Timeouts** - Prevents stuck builds
5. ✅ **Error handling** - Proper cleanup and reporting
6. ✅ **Conditional execution** - Efficient resource usage
7. ✅ **Security** - Proper secret handling
8. ✅ **Artifacts** - Saves test results
9. ✅ **Multi-platform** - Supports different architectures
10. ✅ **Health checks** - Ensures services are ready

---

## Learning Resources

1. **GitHub Actions Documentation**
   - https://docs.github.com/en/actions

2. **Expression Syntax**
   - https://docs.github.com/en/actions/learn-github-actions/expressions

3. **Contexts and Variables**
   - https://docs.github.com/en/actions/learn-github-actions/contexts

4. **YAML Syntax**
   - https://yaml.org/spec/1.2.2/

5. **Docker Actions**
   - https://github.com/docker/build-push-action

---

## Common Issues and Solutions

### Issue: Workflow doesn't trigger
**Solution:** Check path filters and branch names

### Issue: Secrets not available
**Solution:** Ensure secrets are set in repository settings

### Issue: Docker build fails
**Solution:** Check Dockerfile path and context

### Issue: Tests timeout
**Solution:** Increase `timeout-minutes` or optimize tests

### Issue: Cache not working
**Solution:** Verify cache key includes file hashes

---

This workflow demonstrates production-ready CI/CD practices with comprehensive error handling, caching, and multi-stage validation.
