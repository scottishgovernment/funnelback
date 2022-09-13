# Funnelback CLI

This is a CLI for managing Funnelback roles.

The CLI expects source (design) files for roles in common/roles.
Where roles differ between Funnelback environments, they will
be found in dev/roles, uat/roles or prd/roles.

It writes state files for roles to .state/<env>/roles, where
<env> is the name of the environment (dev, uat or prd).


## Usage

Credentials for Funnelback can be configured in the ~/.netrc
file. For example:

~~~
machine dev-govscot-admin.clients.uk.funnelback.com
login first.last@gov.scot
password secret123!
~~~

Initial setup:

~~~
# Install dependencies
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
~~~

To run:

~~~
# Add current directory to path
export PATH="$PWD:$PATH"
# Change to directory with configuration files
cd ../funnelback-config

# See help
fbctl --help
fbctl roles --help

# Sync roles in source files to uat
fbctl roles sync uat

# Fetch roles from dev to state directory
fbctl roles fetch dev

# Detect drift between source files and state directory for dev
# (This is an offline operation)
fbctl roles drift dev
~~~

