# robo

kinematics code for a differential drive robot and an ui to test it.

## How to use

These instructions are for linux. For other OS's, good luck.

You have to have python3 and pip installed.

Clone the repository. Go to the repository and run
```
python3 -m venv venv
```
Activate venv with the command
```
source venv/bin/activate
```
Then install the dependencies by running
```
pip install -r requirements.txt
```
Now you can run the programs by running
```
python3 programname.py
```

## How to develop

When you have done everything described above, you are ready to start coding. Create a new branch by running
```
git checkout -b feature/new-branch-name
```
Make changes while the venv is active. If you have installed new packages, run
```
pip freeze > requirements.txt
```
Then commit the changes you made and the previous command made in the requirements.txt.
```
git add .
git commit -m "description of the changes"
```
Push them into github by running
```
git push origin feature/new-branch-name
```
