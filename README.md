## Requirements

`flake8` - python linter. We use it to enforce PEP8

`Flask` microframework, that allows us to receive HTTP requests, and run appropriate python code for them.

`marshmallow` - a library to easily serialize and deserialize python objects 

`attrs` - relieves you from the drudgery of implementing object protocols

`marshmallow-annotations` - library to automatically convert attrs classes to marshmallow schemas

`marshenum` - library to automatically convert python enums to marshmallow enums, so they appear nicely in the API.

`flask-smorest` is a set of flask extensions, that include
  - 'flask>=1.1.0'
  - 'marshmallow>=2.15.2',
  - 'webargs>=1.5.2' - Define Flask API arguments and response types using marshmallow schemas
  - 'apispec>=3.0.0' - Convert marshmallow schemas to OpenAPI specifications
  - 'werkzeug>=0.15' - Serve OpenAPI specifications using Swagger UI & ReDoc

`gunicorn` - used to deploy our application with systemd

`pyinstrument` - python profiler that also works with flask
  - Add `?profile` query parameter to the url, and instead of the output, you'll get an HTML with the profiler information.
