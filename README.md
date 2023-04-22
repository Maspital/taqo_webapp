## TAQO WebApp
A web interface to for easy and convenient visualization of security alerts as well as the application of
various processing steps to these security alerts.

Currently in a state you could probably call "pre-alpha".


### (Planned) Features
- Visualization of pipeline results on datasets containing security alerts
- Modification of pipeline parameters on the fly, enabling easy experimentation
- Possibility of adding new custom pipelines in a few simple steps
- (more to come)

### Setup
Clone this repo and install TAQO in a virtual environment:
```bash
git clone git@github.com:Maspital/taqo_webapp.git
cd taqo_webapp
python -m venv "taqo_venv" && source taqo_venv/bin/activate
pip install -e
```
And then run the app by simply executing `taqo`.
