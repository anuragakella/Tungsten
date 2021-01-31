settings = {
    "port": '80',
    "host": '',
    "serve_folder": "serve"
}

# tungsten uses a settings.tgs file to read settings
# the user can change some parameters, like the HOST IP, PORT, server folder, etc

# this method parses the settings.tgs file and stores them in a settings dictionary
# this dict is used by other files / classes to change how the server runs
def parse_settings():
    setting_string = ["", ""]

    # use a list and a selector to switch between inputs when it sees a '='
    # selector 0 is for the setting name (LHS), 1 is for the setting value (RHS) -- both are stored in a list (some_array[0] and some_array[1]) and then transferred to a dict
    selector = 0
    with open('./settings.tgs') as settings_file:
        settings_f_str = settings_file.read()
    if(settings_f_str[-1] != '\n'):
        settings_f_str += str('\n')
    for c in settings_f_str:
        if(c == '='):
            selector = 1
            continue
        if(c == '\n'):
            settings[setting_string[0]] = (setting_string[1])
            setting_string = ["", ""]
            selector = 0
            continue
        setting_string[selector] += c
    settings["serve_folder"] = "./" + settings["serve_folder"]
    if("log_file" in settings):
        settings["log_file"] = "./" + settings["log_file"]