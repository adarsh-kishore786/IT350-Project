# IT350 Project

## First Timer

Clone the repository

```git
git clone git@github.com:adarsh-kishore786/IT350-Project.git
```

Switch to new branch

```git
git checkout -b <your-branch>
```

Create a new virtual environment.

For Windows CMD,

```cmd
python -m venv venv
venv/Scripts/activate.bat
```

For Linux,

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies

```python
pip3 install -r requirements.txt
```

---

## Otherwise

Switch to *existing* branch

```git
git checkout <your-branch>
```

Pull latest repo from `main`

```git
git pull origin main
```

Start virtual environment

Windows

```cmd
venv/Scripts/activate.bat
```

Linux

```bash
source venv/bin/activate
```

If required, install dependencies

```python
pip3 install -r requirements.txt
```

---

## Running the application

In [Display](Display) folder, type

```python
flask run
```

If you install new dependencies, run in root folder

```python
python3 -m pipreqs.pipreqs . --force
```

This will update `requirements.txt`.
