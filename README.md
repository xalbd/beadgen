# Bead Generation

### Install

First, install the requesite Python packages for the back-end file generation. Assuming conda usage, run

```
$ conda env create -f environment.yml
```

In case of manual installs, the following are requesites:

```
python=3.10.12
```

Then, install the Node environment/dependencies needed for the front-end user interface.

```
$ cd frontend
$ npm install
```

### Running

First, activate the Python backend. It runs on localhost:8000.

```
$ cd backend
$ conda activate lemur
$ uvicorn main:app --reload
```

Open a new terminal window in the base directory and run the SvelteKit front-end using Vite. It runs on localhost:5173.

```
$ cd frontend
$ npm run dev
```

Navigate to http://localhost:5173/ on a browser to view the web app.
