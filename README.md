# GEDCOM_Project
SSW 555 GEDCOM Project

This is a project for the SSW555 Agile Methods for Software Development at Stevens Institute of Technology taught by Prof. Jim Rowland.

---

- **Team Members**:

  - Vineet Singh
  - David Ovsiew
  - Weihan Rua
  - Mrunal Salvi

- **User stories for sprint 1**:

|Story ID|Story Name|Owner|
|:---:|:---:|:---:|
|US16|Male last names|Vineet|
|US22|Unique IDs|Vineet|
|US14|Multiple Births <= 5|David|
|US15|Fewer than 15 siblings|David|
|US30|List living married|Weihan|
|US31|List living single|Weihan|
|US33|List Orphans|Mrunal|
|US38|List upcoming birthdays|Mrunal|

---
- **User stories for sprint 2**:

|Story ID|Story Name|Owner|
|:---:|:---:|:---:|
|US27|Include individual ages|Vineet|
|US06|Divorce before death|Vineet|
|US35|List recent births|David|
|US36|List recent deaths|David|
|US10|Correct gender for role|Weihan|
|US17|No marriage to children|Weihan|
|US08|Birth before marriage of parents|Mrunal|
|US09|Birth before death of parents|Mrunal|

---
- **User stories for sprint 3**:

|Story ID|Story Name|Owner|
|:---:|:---:|:---:|
|US02|Birth before marriage|Vineet|
|US03|Birth before death|Vineet|
|US24|Unique families by spouse|David|
|US15|List upcoming anniversaries|David|
|US30|List deceased|Weihan|
|US31|Marriage after 14|Weihan|
|US33|Unique first names in families|Mrunal|
|US38|Siblings should not marry|Mrunal|

---
- **User stories for sprint 4**:

|Story ID|Story Name|Owner|
|:---:|:---:|:---:|
|US04|Marriage before divorce|Vineet|
|US05|Marriage before death|Vineet|
|US19|First cousins should not marry|David|
|US42|Reject illegitimate dates|David|
|US23|Unique name and birth date|Weihan|
|US04|Less than 150 years old|Weihan|
|US11|No bigamy|Mrunal|
|US40|Include input line numbers|Mrunal|

---

## Workflow of Version control

1. On the GitHub repository webpage, create your own branch with the name pattern `sprint4_initial` (e.g. `sprint4_mrunal`) based on branch `sprint4`

2. Go to the command line and pull down the current sprint branch with following steps, and create your own branch with the example of branch `sprint4_mrunal`:
    1. `git clone --single-branch --branch sprint4 <SSH/HTTPS Link>`
    2. `git checkout -b sprint4_mrunal sprint4`
    3. `git pull --all`

3. Develop your user stories, test cases on your branch and push it on your own branch. I will do the merging carefully after you push the branch. Once your branch is pushed to origin but you still need to develop your user stories and test cases:
    1. `git clone --single-branch --branch sprint4 <SSH/HTTPS Link>`
    2. `git checkout sprint4_mrunal`
    3. `git pull --all`

4. Everytime you work on your user stories and test cases make sure you pull the latest updates from the sprint branch to your own development branch: `git pull --all` should do that for you.

5. Make sure you push your developed user stories and test cases 2 days before the sprint deadline so that I have enough time to merge carefully.
