## Getting started with node js project


**Step 0. Install mongoDB in your machine**

You can find installation instructions on the official docs [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/).

**Step 1. Clone the project into a fresh folder**
```
# clone the github repo

$ git clone 'https://github.com/Smart-Logger/tarsier-backend'

# navigate to the project directory
$ cd 'tarsier-backend'

# create the virtual environment for MFlix
python3 -m venv mflix_venv

# activate the virtual environment
source mflix_venv/bin/activate
```

**Step 2. Install dependencies**
```
$ python3 -m pip install -r requirements.txt

```

**Step 3. Install external libraries**

This project rely on two external library to works properly `Ghostscript` version `9.25` and `graphicsmagick` version `1.3.35-Q16`

#### Ghostscript 9.52






**Step 4. Prepare Node.js environment**

Create new file named `.env` in the project root.

Copy the content from the file `.sample-env` to the new created `.env` file.

**Step 5. Run the server**
```
$ flask run index.js
```
