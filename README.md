# Lab 1 – CI with GitHub Actions

[![Testing with Pytest](https://github.com/1AlgoRythm/mlops-lab1/actions/workflows/github_lab1_pytest_action.yml/badge.svg)](https://github.com/1AlgoRythm/mlops-lab1/actions/workflows/github_lab1_pytest_action.yml)
[![Python Unittests](https://github.com/1AlgoRythm/mlops-lab1/actions/workflows/github_lab2_unittest_action.yml/badge.svg)](https://github.com/1AlgoRythm/mlops-lab1/actions/workflows/github_lab2_unittest_action.yml)

A small Python calculator module with a continuous integration (CI) pipeline. On every
push, GitHub Actions runs the test suite on several Python versions and reports the result.

Based on `Github_Labs/Lab1` from https://github.com/raminmohammadi/MLOps
(MLOps, DADS 7305, Northeastern University).

## Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Continuous Integration](#continuous-integration)
- [Testing](#testing)
- [Changes From the Upstream Lab](#changes-from-the-upstream-lab)
- [Known Limitations](#known-limitations)
- [Lessons Learned](#lessons-learned)
- [Attribution and AI Use](#attribution-and-ai-use)

## Overview

The project has three parts:

1. **`src/calculator.py`**: four small functions that add, subtract and multiply numbers.
2. **`test/`**: the same behavior tested twice, once with `pytest` and once with `unittest`.
3. **`.github/workflows/`**: two GitHub Actions workflows that run those tests automatically.

## Requirements

- Python 3.10 or 3.12 (the versions tested in CI)
- `pytest` (listed in `requirements.txt`; the version is not pinned)
- `unittest` is part of the Python standard library and needs no installation

## Installation

```bash
git clone https://github.com/1AlgoRythm/mlops-lab1.git
cd mlops-lab1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the tests from the repository root:

```bash
pytest                                        # every test (16, see the note below)
pytest test/test_pytest.py -v                 # the 8 pytest tests
python3 -m unittest test.test_unittest -v     # the 8 unittest tests
```

Plain `pytest` also collects the `unittest` file, so it reports `16 passed`: 8 from each file.

## Project Structure

```text
mlops-lab1/
├── .github/workflows/
│   ├── github_lab1_pytest_action.yml     # "Testing with Pytest"
│   └── github_lab2_unittest_action.yml   # "Python Unittests"
├── data/__init__.py                      # empty package kept from the original lab
├── src/
│   ├── __init__.py
│   └── calculator.py                     # the code under test
├── test/
│   ├── __init__.py
│   ├── test_pytest.py                    # pytest tests
│   └── test_unittest.py                  # unittest tests
├── requirements.txt
└── README.md
```

## API Reference

All functions live in `src/calculator.py`. Every argument must be an `int` or a `float`;
anything else raises `ValueError`.

### `fun1(x, y)`

Return the sum of `x` and `y`.

```python
>>> from src import calculator
>>> calculator.fun1(2, 3)
5
>>> calculator.fun1(0.1, 0.2)
0.30000000000000004
>>> calculator.fun1("2", 3)
Traceback (most recent call last):
    ...
ValueError: Both inputs must be numbers.
```

### `fun2(x, y)`

Return `x` minus `y`. Raises `ValueError` if either argument is not a number.

```python
>>> calculator.fun2(2, 3)
-1
```

### `fun3(x, y)`

Return the product of `x` and `y`. Raises `ValueError` if either argument is not a number.

```python
>>> calculator.fun3(2, 3.5)
7.0
```

### `fun4(x, y, z)`

Return the sum of `x`, `y` and `z`. Raises `ValueError` if any argument is not a number.

```python
>>> calculator.fun4(2, 3, 5)
10
>>> calculator.fun4("a", 2, 3)
Traceback (most recent call last):
    ...
ValueError: All the inputs must be numbers
```

> **Note:** `bool` is a subclass of `int` in Python, so `True` and `False` are accepted
> as numbers (`calculator.fun1(True, 1)` returns `2`).

## Continuous Integration

### How it works

1. A push to the repository triggers a workflow.
2. GitHub starts a fresh Ubuntu machine for each Python version in the matrix.
3. The machine checks out the code and installs the requested Python version.
4. It installs the packages in `requirements.txt`.
5. It runs the tests.
6. GitHub shows a green check if every step passed and a red cross if any step failed.

The tests run on GitHub's machines, not on the developer's computer. If they pass there,
the code works in a clean environment, not only on one laptop.

### Workflows

| Workflow | File | Runs on | Command | Artifacts |
|---|---|---|---|---|
| Testing with Pytest | `github_lab1_pytest_action.yml` | push to `main` or `releases/**`; also `label` created and `issues` opened or labeled (inherited from the original lab) | `pytest --junitxml=pytest-report.xml` | `test-results-3.10`, `test-results-3.12` |
| Python Unittests | `github_lab2_unittest_action.yml` | push to `main` | `python -m unittest test.test_unittest` | none |

### Python version matrix

Both workflows use a matrix. The job is written once, and GitHub runs it once per version
listed under `strategy.matrix.python-version`: currently **3.10** and **3.12**. Each job
reads its version from `${{ matrix.python-version }}`.

- Versions are written in quotes (`"3.10"`). YAML reads an unquoted `3.10` as the number
  3.1, which is a different version.
- `fail-fast: false` is set, so one failing version does not cancel the others.

### Artifacts

The pytest workflow uploads its XML report (`pytest-report.xml`) for each version, named
`test-results-<version>`. To download one, open a run on the **Actions** tab and scroll
to **Artifacts**.

## Testing

| File | Tests | Original lab |
|---|---|---|
| `test/test_pytest.py` | 8 | 4 |
| `test/test_unittest.py` | 8 | 4 |

The tests cover three kinds of cases:

- **Normal cases:** positive, negative and zero values, and floats.
- **Error cases:** non-numbers (text, `None`, a list) raise `ValueError` in `fun1` to
  `fun4`, with the bad value in different argument positions.
- **Float comparison:** `0.1 + 0.2` is `0.30000000000000004`, so the tests compare it with
  `pytest.approx` and `assertAlmostEqual`, not `==`.

To check that the tests can fail, they were run against deliberately broken copies of the
calculator. Removing the input check from `fun4` made the new `fun4` tests fail in both
frameworks. Removing it from `fun1` made the `fun1`, `fun2` and `fun3` error tests fail.

## Changes From the Upstream Lab

Each change is its own commit.

### Fixed

- **Pytest workflow rejected by GitHub.** It used both `branches` and `branches-ignore`
  under `push:` and had a typo (`run-nam`). The first run reported a "workflow file issue"
  and never started. Removed `branches-ignore` and fixed the typo
  ([`9b331b5`](https://github.com/1AlgoRythm/mlops-lab1/commit/9b331b5)).
- **Workflow files in the wrong folder.** GitHub only runs workflows from
  `.github/workflows/`, so the two files were moved there
  ([`4f41255`](https://github.com/1AlgoRythm/mlops-lab1/commit/4f41255)).
- **`actions/upload-artifact` v2 is blocked.** GitHub failed the job before any test ran,
  with the message that v2 is deprecated. Updated to v4
  ([`312017d`](https://github.com/1AlgoRythm/mlops-lab1/commit/312017d)).
- **`fun4` accepted non-numbers**, unlike `fun1` to `fun3`: `fun4("a", "b", "c")` returned
  `"abc"`. It now raises `ValueError`
  ([`a548dc3`](https://github.com/1AlgoRythm/mlops-lab1/commit/a548dc3)).

### Added

- **Python version matrix** on both workflows
  ([`adf0743`](https://github.com/1AlgoRythm/mlops-lab1/commit/adf0743),
  [`4640d00`](https://github.com/1AlgoRythm/mlops-lab1/commit/4640d00)). The original lab
  tested one hard-coded version.
- **One test report per Python version**, named `test-results-<version>`
  ([`10187b1`](https://github.com/1AlgoRythm/mlops-lab1/commit/10187b1)). With one shared
  name the reports could not be told apart.
- **`fail-fast: false`**
  ([`336545c`](https://github.com/1AlgoRythm/mlops-lab1/commit/336545c)).
- **Error-case, float and normal-case tests** in both test files
  ([`a548dc3`](https://github.com/1AlgoRythm/mlops-lab1/commit/a548dc3)).

### Changed

- **The matrix was narrowed from 3.8, 3.10 and 3.12 to 3.10 and 3.12.** GitHub announced
  that the `ubuntu-latest` label moves to Ubuntu 26 on 2026-10-19, and it could not be
  confirmed that Python 3.8 would still install there.

## Known Limitations

- **`fail-fast: false` has not been demonstrated.** While every job passes it makes no
  visible difference, and no version has been forced to fail.
- **Duplicate artifact names were accepted.** The `upload-artifact@v4` documentation says
  names must be unique, but when three jobs uploaded `test-results` all three succeeded.
  The reason is unknown. This is why each report now has its own name.
- **Older action versions.** The workflows use `actions/checkout@v2` and
  `actions/setup-python@v2`. They still work, but GitHub prints a warning that Node.js 20 is
  deprecated.
- **Inherited triggers.** The pytest workflow also runs on `label` and `issues` events.
  These come from the original lab and are not needed for this project.
- **`ubuntu-latest` is changing.** See the last item under *Changed* above.

## Lessons Learned

- CI is a safety check that runs on every change, so mistakes show up right away.
- A matrix tests many environments from one job definition. Quote the versions.
- Documentation and behavior can disagree. Read what the run actually did.
- Tests should check failures as well as normal results, and compare floats with a
  tolerance.

## Attribution and AI Use

This repository is based on the lab in the course repository linked at the top. Claude (an
AI assistant) was used to explain concepts, help read failed workflow runs, write and draft
 this README. The code was run, and the results checked on GitHub.

---

# Original lab README (kept for reference)

# LAB1 - MLOps (IE-7374) 

This lab focuses on 5 modules, which includes creating a virtual environment, creating a GitHub repository, creating Python files, creating test files using pytest and unittest, and implementing GitHub Actions.




## Step 1: Creating a Virtual Environment

In software development, it's crucial to manage project dependencies and isolate your project's environment from the global Python environment. This isolation ensures that your project remains consistent, stable, and free from conflicts with other Python packages or projects. To achieve this, we create a virtual environment dedicated to our project. <br>
<br>
To create a virtual environment, follow these steps:

1. Open a Command Prompt or Terminal in the directory where you want to create your project.
2. Choose a name for your virtual environment (e.g "lab_01") and run the appropriate command:
    ```
    python -m venv lab_01
    ```
3. Activate the virtual environment
    ```
    lab01\Scripts\activate
    ```
After activation, you will see the virtual environment's name in your command prompt or terminal, indicating that you are working within the virtual environment.


## Step 2: Creating a GitHub Repository, Cloning and Folder Structure
Now that we have set up our virtual environment, the next step is to create a GitHub repository for our project and establish a structured folder layout. This organization helps maintain your project's code, data, and tests in an organized manner.

### Fork the Repository: 
Click the "Fork" button at the top right of this [repository](https://github.com/raminmohammadi/MLOps/) to create your own copy.

### Creating a GitHub Repository
- Open a web browser and go to GitHub.
- In the upper right corner, click the "+" button and select "New repository."
- Choose a name for your repository.
- Choose the visibility of your repository—either public (visible to everyone) or private (accessible only to selected collaborators)
- Check the "Initialize this repository with a README" box. This will create an initial README file that you can edit to provide project documentation.
- Click the "Create repository" button.

### Cloning the Repository
- Open a Command Prompt or Terminal.
- Navigate to the directory where you want to clone your GitHub repository. This should be the same directory where you created your virtual environment.
- Run the following command to clone your GitHub repository into the current directory:
    ```
    git clone <repository_url>
    ```
- Replace <repository_url> with the URL of your GitHub repository. You can find this URL on your GitHub repository's main page.
After running the command, the repository will be cloned, and you'll have a local copy of your GitHub project in your chosen directory.

### Establishing Folder Structure
- Once you have cloned yor repository, you can establish a structured folder layout within it. This layout helps organize your project into key directories for code, data, and tests. Create the following subfolders within your repository: <br>
- data: This folder is used for storing project data files or datasets. <br>
- src: This folder is where you'll store your project's source code files. <br>
- test: This folder is dedicated to unit tests and test scripts for your code. <br>
- Create a file named .gitignore. This is useful to exclude the virtual environment and other unnecessary files from version control.
- Add the virtual environment folder name inside your gitignore file so that its not tracked by Git.

### Adding and Pushing Your Project Code to GitHub
Now that we have our virtual environment set up, the GitHub repository created, and the folder structure organized, let's add our project's code and push it to GitHub. 

**Adding Your Project Code** <br>
- Navigate to your project directory using the Command Prompt or Terminal, where you have the virtual environment and folder structure set up.
- Create and write your Python code or other project files within the specified directories (src, data, etc.) according to your project requirements.
- Once your project files are ready, it's time to add them to Git's staging area. In your project directory, run the following command:
    ```
    git add .
    ```
- This command stages all the changes and new files in your project directory for the next commit.

**Committing Your Changes** <br>
- After staging your changes, commit them with a meaningful commit message that describes the changes you made. Replace <your_commit_message> with a descriptive message:
    ```
    git commit -m "<your_commit_message>"
    ```

**Pushing to GitHub** <br>
- To push your committed changes to your GitHub repository, use the following command:
    ```
    git push origin main
    ```
## Step 3: Creating calculator.py in src Folder
- In this step, we create a Python script named calculator.py within the src folder of your project. This script contains a set of mathematical functions designed to perform basic arithmetic operations.
- fun1(x, y) adds two input numbers, x and y.
- fun2(x, y) subtracts y from x.
- fun3(x, y) multiplies x and y.
- fun4(x, y) combines the results of the above functions and returns their sum.
- To view the code and gain a deeper understanding, please refer to the calculator.py file located under the src folder in this [link](https://github.com/raminmohammadi/MLOps/blob/main/src/lab1/calculator.py).

> **Note:** <br>
Whenever you want to push files to your repository follow this step
[Adding and Pushing Your Project Code to GitHub](#adding-and-pushing-your-project-code-to-github)

## Step 4: Creating tests using Pytest and Unittests
- In this step, we'll set up unit tests for the functions in our calculator.py script using two popular testing frameworks: [pytest](https://docs.pytest.org/en/7.4.x/) and [unittest](https://docs.python.org/3/library/unittest.html). Unit testing ensures that individual components of your code work as expected, helping you catch and fix bugs early in the development process.

**Using Pytest** <br>
- Installation (if not already installed):
- If you haven't already installed pytest, you can do so using pip:
    ```
    pip install pytest
    ```
### Writing Pytest Tests
- Pytest makes it easy to write tests for your Python code. Tests are written as regular Python functions, and test file names typically start with test_ or end with _test.py.
- To run your Pytest tests, you can use the pytest command followed by the name of the test file or directory containing your tests:
    ```
    pytest test_sample.py
    ```
- Pytest automatically discovers test functions based on naming conventions. It searches for functions starting with test_ or ending with _test, and it can discover tests in subdirectories as well. This makes it easy to organize your tests.
- Pytest supports parametrized tests, which allow you to run the same test function with multiple sets of inputs and expected outputs. This is particularly useful for testing functions with different input scenarios. Please refer the commented out code in the test_pytest.py file for your reference.
- Let's create a test file named test_pytest.py within the test folder. This file will contain a series of test functions, each aimed at verifying the behavior of specific functions within calculator.py.
- We've prepared four test functions (test_fun1, test_fun2, test_fun3, and test_fun4) to test the functions within calculator.py. Each test function uses the assert statement to validate the expected outcomes. Refer the file under test folder for your [reference](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/test/test_pytest.py).
- By running these pytest tests, you can verify that your calculator functions are working correctly.

### Writing Tests with UnitTest
- Unittest allows you to write tests as classes that inherit from the unittest.TestCase class. Test methods are identified by their names, which must start with "test_" to be recognized as test cases.
- To run Unittest tests, you typically execute your test script, which should include a call to unittest.main() at the end. Here's how you can run the tests:
    ```
    python test_sample.py
    ```
- Unittest relies on test discovery, which means it will find test methods based on naming conventions, similar to Pytest. Test methods must start with "test_" to be recognized as test cases.
- Unittest provides a variety of assertion methods, such as assertEqual, assertTrue, assertFalse, and others, to check conditions in your tests. You can choose the assertion method that best suits your testing needs.
- Let's create a test file named test_unittest.py within the test folder. This file will contain a series of test functions, each aimed at verifying the behavior of specific functions within calculator.py.
- We've prepared four test functions (test_fun1, test_fun2, test_fun3, and test_fun4) to test the functions within calculator.py. Each test function uses the self.assertEqual statement to validate the expected outcomes. Refer the file under test folder for your [reference](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/test/test_unittest.py).
- By running these unittest tests, you can verify that your calculator functions are working correctly.

## Step 5. Implementing GitHub Actions
- GitHub Actions is a powerful automation and CI/CD (Continuous Integration/Continuous Deployment) platform provided by GitHub. It enables you to automate various workflows and tasks directly within your GitHub repository. GitHub Actions can be used for a wide range of purposes, such as running tests, deploying applications, and automating release processes.

**How GitHub Actions Work:** <br>

- GitHub Actions work based on events, actions, and triggers:
- **Events:** These are specific activities that occur within your GitHub repository, such as code pushes, pull requests, or issue comments. GitHub Actions can respond to these events.
- **Actions:** Actions are individual tasks or steps that you define in a workflow file. These tasks can be anything from building your code to running tests or deploying your application.
- **Triggers:** Triggers are conditions that cause a workflow to run. They can be based on events (e.g., a new pull request) or scheduled to run at specific times.

**The Purpose of GitHub Actions:** <br>

- GitHub Actions serves several purposes:
- **Automation:** It automates repetitive tasks, reducing manual effort and ensuring consistency in your development process.
- **Continuous Integration (CI):** It allows you to set up CI pipelines to automatically build, test, and validate your code changes whenever new code is pushed to the repository.
- **Continuous Deployment (CD):** It enables automatic deployment of your application when changes are merged into a specific branch, ensuring a smooth and reliable release process.

### Using Pytest and Unittest with GitHub Actions:
- Integrating Pytest and Unittest with GitHub Actions can significantly improve the quality and reliability of your codebase. Here's how:
- Pytest with GitHub Actions: You can create a GitHub Actions workflow (e.g., pytest_action.yml) that specifies the steps for running your Pytest tests. When events like code pushes or pull requests occur, GitHub Actions will automatically trigger the workflow, running your Pytest tests and reporting the results back to you. This helps you catch bugs and ensure that your code meets quality standards early in the development process.
- Unittest with GitHub Actions: Similarly, you can create a separate GitHub Actions workflow (e.g., unittest_action.yml) to run your Unittest tests. This ensures that both your Pytest and Unittest suites are executed automatically whenever code changes are made or pull requests are submitted. It provides a robust validation mechanism for your codebase.
- When collaborating in teams, the automated testing process ensures that all test cases pass successfully before allowing the merge of a pull request into the main branch.

### Creating GitHub Actions Workflow Files:
- To implement Pytest and Unittest with GitHub Actions, you'll create two workflow files under the .github/workflows directory in your repository: pytest_action.yml and unittest_action.yml. These workflow files define the specific actions and triggers for running your tests.

**pytest_action.yml** <br>
Please refer [this](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/workflows/pytest_action.yml) file for your reference
1. Workflow Name: The workflow is named "Testing with Pytest."
2. Event Trigger: It specifies the event that triggers the workflow. In this case, it triggers when code is pushed to the main branch.
3. Jobs: The workflow contains a single job named "build," which runs on the ubuntu-latest virtual machine environment.
4. Steps:
- Checkout code: This step checks out the code from the repository using actions/checkout@v2.
- Set up Python: It sets up the Python environment using actions/setup-python@v2 and specifies Python version 3.8.
- Install Dependencies: This step installs the project dependencies by running pip install -r requirements.txt.
- Run Tests and Generate XML Report: The core testing step runs Pytest with the --junitxml flag to generate an XML report named pytest-report.xml. The continue-on-error: false setting ensures that the workflow will be marked as failed if any test fails.
- Upload Test Results: In this step, the generated XML report is uploaded as an artifact using actions/upload-artifact@v2. The name of the artifact is "test-results," and the path to the report is specified as pytest-report.xml.
- Notify on Success and Failure: These two steps use conditional logic to notify based on the outcome of the tests.
- if: success() checks if the tests passed successfully and runs the "Tests passed successfully" message.
- if: failure() checks if the tests failed and runs the "Tests failed" message.

**unittest_action.yml** <br>
 Please refer [this](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/workflows/unittest_action.yml) file for your reference
1. Workflow Name: This GitHub Actions workflow is named "Python Unittests."
2. Event Trigger: The workflow is triggered by the "push" event, specifically when changes are pushed to the main branch.
3. Jobs: The workflow defines a single job named "build" that runs on the ubuntu-latest virtual machine environment.
4. Steps:
- Checkout code: This step uses the actions/checkout@v2 action to check out the code from the repository. It ensures that the workflow has access to the latest code.
- Set up Python: The "Set up Python" step uses the actions/setup-python@v2 action to configure the Python environment. It specifies that Python version 3.8 should be used.
- Install Dependencies: This step runs the command pip install -r requirements.txt to install the project's Python dependencies. It assumes that the project's dependencies are listed in the requirements.txt file.
- Run unittests: In this step, the unittest tests are executed using the command python -m unittest test.test_unittest. It runs the unittest test suite defined in the test.test_unittest module.
- Notify on success: This step uses conditional logic with if: success() to check if all the unittest tests passed successfully. If they did, it runs the message "Unit tests passed successfully."
- Notify on failure: Similarly, this step uses conditional logic with if: failure() to check if any of the unittest tests failed. If any test failed, it runs the message "Unit tests failed."
