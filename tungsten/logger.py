from tungsten.settings import settings

# logger, prints stuff to the console
# file log support coming soon
class Logger:
    def log(self, s):
        print(s)
        if("log_file" in settings):
            with open(settings["log_file"], "w+") as logfile:
                logfile.write(s+"\n")
