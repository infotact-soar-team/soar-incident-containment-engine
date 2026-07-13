# Branch Protection Setup (main)

Configured under: Repo → Settings → Branches → Add branch protection rule

## Rule target
Branch name pattern: `main`

## Settings enabled
- [x] Require a pull request before merging
- [x] Require approvals (minimum 1)
- [x] Require status checks to pass before merging
  - Required check: `CI / test`
- [x] Require branches to be up to date before merging
- [x] Do not allow bypassing the above settings (applies to admins too)

## Why
Ensures no one (including admins) can push directly to main, every change goes
through review, and CI must pass before any merge.