# Are-You-OK
<p align="center">
  <a href="https://github.com/qyxtim/Are-You-OK/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/qyxtim/Are-You-OK"></a>
  <a href="https://github.com/qyxtim/Are-You-OK"><img alt="GitHub issues" src="https://img.shields.io/github/last-commit/qyxtim/Are-You-OK"></a>
  <a href="https://github.com/qyxtim/Are-You-OK/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/qyxtim/Are-You-OK"></a>
  <a href="https://github.com/qyxtim/Are-You-OK/blob/main/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/qyxtim/Are-You-OK"></a>
Are-You-OK is a Flask-based Web App to monitor whether the Internet Service you care is still working.

# Demo-Preview

![Banner](https://github.com/qyxtim/Are-You-OK/blob/main/images/pc.jpeg)

![Banner](https://github.com/qyxtim/Are-You-OK/blob/main/images/phone.jpeg)

# Get Started
Before using this project, please make sure you have:

- Python
- Flask

To use it, you should first clone the repo on your device using the command below:

```
git clone https://github.com/qyxtim/Are-You-OK.git
```

Then, `cd` into the directory you want to access and use the command below to set up your database, and administrator username and password:

```makefile
python init_db.oy
```

Then, just type `flask run` and enjoy.

# Development

The implementation of this Web App is split into five files:

- `init_db.py` initializes the database
- `app.py` is in charge of using flask to create correct routing
- `login.py` provides the functionality to check whether the user is logged in
- `network.py` provides two functions. `is_valid_url` is used to check the validity of the user's input url. `ping` is used to check whether the online service is still working
- `db.py` enables the database to be opened by Context Manager

# New Features in the Future

- [ ] Delete websites added before

# License
[GNU General Public License version 3](https://opensource.org/licenses/GPL-3.0)
