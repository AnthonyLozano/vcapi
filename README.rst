vcapi
=====

vcapi is a python cli wrapper to veracode's upload api.

Usage
-----

Save your credentials in a two line file named .veracoderc in your home directory, or specify a credential file
with the --cred-file option. The file should have your username on the first line and your password on the second line.

::

    Usage: vcapi [OPTIONS] COMMAND [ARGS]...

      Veracode command line interface

    Options:
      --cred-file TEXT  Two line file containing username and password.
      -v, --verbose     Enables logging
      --help            Show this message and exit.

    Commands:
      begin-prescan        Begins the prescan.
      begin-scan           Begins a scan
      create-app           Creates a new app.
      create-build         Creates a build.
      delete-build         Deletes a build.
      get-app-info         Gets information for a particular app.
      get-app-list         Gets a list of apps and their ids.
      get-build-info       Gets info for an app build.
      get-build-list       Gets a list of builds for an app.
      get-file-list        Gets a list of files uploaded to a build.
      get-policy-list      Gets a list of policies you have defined.
      get-prescan-results  Gets the results of a prescan.
      get-vendor-list      Gets a list of vendors you have defined.
      remove-file          Removes a file from an app.
      update-app           Updates an app.
      update-build         Updates build infomation for a build.
      upload-file          Uploads a file

Examples
--------

List all the apps you have access to::

    vcapi get-app-list

Get help on a particular command::

    vcapi update-app --help

Perform a command with verbosity::

    vcapi -v get-app-list

