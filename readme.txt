In order to run tests successfully, the correct testfile locations and test information must be entered
into the YAML file in the format specified therein. The program searches the containing directory of this
text file for anything with the extension '.yaml', but will only accept one yaml file at a time. In order
to save backups or old files, they must be renamed to something like 'a_file.yaml.backup'.

Once the yaml file has been configured, the program should automatically load the file and configure
itself. Please report bugs to https://github.com/higewosoru/testbed_cli.

Note - the cli should work out of the box with a few dummy test files that do nothing but print text.
