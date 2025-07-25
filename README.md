# Earthquakes dataset


## Install

1. Check the version of python you need in `runtime.txt`
2. Create a virtual env with that python version.
3. In that virtual env, install the packages you need with `pip`

It is going to look something like:
```
/opt/python-3.10.6/bin/python3 -m venv myenv
. ./myenv/bin/activate
pip3 install -r requirements.txt
```

## Run

### mongodb

To run it, you'll need a mongodb available. The easiest way to configure is to set environment variable
`MONGODB_URI` to be a fully qualified mongo style uri `mongodb:// ...`
You need to set MLAB_DB


But you can set it also by components. Check the top of the code file for the name of the environment variables.

### running the actual server

standard call to flask run from the src app:

```
#export MONDODB_URI=<here goes the URI>
#export MLAB_DB=<here goes the DB>
cd src/
flask run --port=4765
```

### Running Mmultiple servers

I don't know why you would want multiple servers of this running at
the same time.  But if you are running multiple, you can theoretically
get into a race condition where a single earthquake get added
twice. This is unlikely because the server check IDs. But mongo is not
set up to check uniqueness of ids. So theoretically they could both be
adding it at the same time in the data base. Not sure it is worth
worrying about it too much.

