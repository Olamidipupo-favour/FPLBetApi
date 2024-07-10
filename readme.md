# FantasyPremierLeague Match Week Betting implementation

This is an implementation of an api that manages api based fpl betting based on match weeks. I.e, one user challenges the other and at the end of the match week, the fellow with the highest point takes the money home.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Implmentation Details](#Implementation)

## Installation

Instructions for how to install the project. For example:

```bash
git clone https://github.com/Olamidipupo-favour/FPLBetApi
cd FPLBetApi
pip install -r requirements.txt
```

Run the software

```bash
fastapi run main.py
```
## Usage
Api endpoints can be accessed at {{base_url}}/docs

## Implementation
This entire APi service was designed from scratch using fastAPI to handle requests, pydantic to handle models, github actions to handle daily cron jobs and render for deployment.