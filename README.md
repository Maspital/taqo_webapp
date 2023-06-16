### Development moved to https://gitlab.fkie.fraunhofer.de/lumberjacks/taqo

### Setup
Clone this repo and install TAQO in a virtual environment:
```bash
git clone git@github.com:Maspital/taqo_webapp.git
cd taqo_webapp
python -m venv "taqo_venv" && source taqo_venv/bin/activate
pip install -e .
```
And then run the app by simply executing `taqo`.
Note that you will need to update the paths in `datasets/datasets.json` manually
before being able to analyze anything.
