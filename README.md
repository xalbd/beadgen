# Bead Generation

### Install

First, install Python 3.10+ and the requesite Python packages for the back-end file generation listed in `backend/requirements.txt`.The latest versions of each should work.

Then, install the Node environment/dependencies needed for the front-end user interface.

```
$ cd frontend
$ npm install
```

### Running

First, activate the Python backend. It runs on localhost:8000. If you're using a virtual environment (venv, conda, etc), enter it.

```
$ cd backend
$ uvicorn main:app --reload
```

Open a new terminal window in the base directory and run the SvelteKit front-end using Vite. It runs on localhost:5173.

```
$ cd frontend
$ npm run dev
```

Navigate to http://localhost:5173/ on a browser to view the web app.
