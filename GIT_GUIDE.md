# Git Guide — Essential Commands

## Basic concepts

Git stores the project history as **commits**; each person works on their own **branch** and only then merges the result into `develop`.

| Term | What it is |
| --- | --- |
| Repository | The project folder with its full version history |
| Commit | A "snapshot" of changes, with a message explaining what changed |
| Branch | A separate line of work; changes there do not affect other branches |
| Remote (`origin`) | The copy of the repository on GitHub |
| `master` | Stable code, ready to use |
| `develop` | Where new features are integrated before going to `master` |

Rule for the `api_demo` project: nobody commits directly to `master` or `develop`. Every change starts on a branch created from `develop`.

## Initial setup and clone

Done once per computer: identify yourself to Git and download the `api_demo` repository.

1. Set your name and email (they appear on every commit):
    ```bash
    git config --global user.name "Your Name"
    git config --global user.email "you@email.com"
    ```
2. Clone the repository from GitHub:
    ```bash
    git clone https://github.com/lgbuffa/api_demo.git
    cd api_demo
    ```
3. Switch to the `develop` branch:
    ```bash
    git checkout develop
    ```
4. Create the `.env` from the template (`.env` never goes to GitHub):
    ```bash
    cp .env.example .env
    ```

On the first `git push`, Windows opens the browser to log in to GitHub; after that the credential is saved.

## Workflow: from branch to push

Every task follows the same 6 steps, always starting from an up-to-date `develop`.

1. Go to `develop` and pull the latest changes:
    ```bash
    git checkout develop
    git pull
    ```
2. Create your branch from it (`-b` creates the branch and switches to it):
    ```bash
    git checkout -b feature/task-name
    ```
3. Edit the files in your editor and check what changed:
    ```bash
    git status
    git diff
    ```
4. Stage the changes for the commit (`.` includes everything in the current folder):
    ```bash
    git add .
    ```
5. Record the commit with a clear message:
    ```bash
    git commit -m "Add severity filter to alarms"
    ```
6. Push the branch to GitHub (`-u` links the local branch to the remote; next time just `git push`):
    ```bash
    git push -u origin feature/task-name
    ```

Branch names: `feature/...` for something new, `fix/...` for a bug fix. Before `git add .`, check in `git status` that no unwanted file (such as `.env`) shows up.

## Integrating your work: pull request and merge

A branch gets into `develop` through a **pull request** on GitHub, where someone else reviews it before the merge.

1. On GitHub, open the repository and click **Compare & pull request**.
2. Choose **base: `develop`** and **compare: `feature/task-name`**, describe what changed and create the PR.
3. The reviewer approves and clicks **Merge pull request**.
4. On your computer, update `develop` and delete the local branch that was already merged:
    ```bash
    git checkout develop
    git pull
    git branch -d feature/task-name
    ```

When `develop` is stable, open a PR from `develop` to `master` the same way.

If someone else changed `develop` while you were working, bring those changes into your branch before the PR:

```bash
git checkout feature/task-name
git merge develop
```

## Useful commands for checking and fixing

| Command | What it does |
| --- | --- |
| `git status` | Shows which branch you are on and which files changed |
| `git branch -a` | Lists local and remote branches |
| `git log --oneline --graph --all` | Short commit history, with the branches drawn |
| `git diff` | Shows changed lines not yet staged |
| `git restore file.py` | Discards uncommitted changes to a file |
| `git restore --staged file.py` | Unstages a file, keeping the change |
| `git commit --amend -m "new msg"` | Fixes the last commit message (only before pushing) |
| `git stash` / `git stash pop` | Shelves changes temporarily to switch branches, then brings them back |
| `git fetch` | Downloads what is new on GitHub without touching your files |
