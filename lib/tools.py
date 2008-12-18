#!/usr/bin/env python

"""tools.py - miscellaneous tools"""

import time, locale, os, sys, urllib
locale.setlocale(locale.LC_ALL, "")


def number(num):
    """returns formatted number"""

    return locale.format("%s", num, True)

def file(path, mode="r"):
    """returns file object using relative path of script regardless of execution path"""

    f = os.path.join(os.path.dirname(sys._getframe(1).f_code.co_filename), path)
    if mode != "p":
    	f = __builtins__["file"](f, mode)
    return f

def authenticate(*args):
    """simplified way of adding authentication details to urllib"""

    if not (urllib._urlopener and hasattr(urllib._urlopener, "toolsLogins")):
        class _Login(urllib.FancyURLopener):
            def prompt_user_passwd(self, host, realm):
                credentials = ("", "")
                for login in self.toolsLogins:
                    if host == login["host"] and (realm == login["realm"]
                    or not login["realm"]):
                        credentials = (login["user"], login["pass"])
                        break
                return credentials
        urllib._urlopener = _Login()
        urllib._urlopener.toolsLogins = []

    args = dict(zip(("host", "realm", "user", "pass"), args))
    if args["realm"]:
        urllib._urlopener.toolsLogins.insert(0, args)
    else:
        urllib._urlopener.toolsLogins.append(args)

def firefoxinate(urlmod):
    """fakes mozilla browser for urllib"""

    if not urlmod._urlopener:
        class Opener(urlmod.FancyURLopener):
            version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.5) Gecko/20060719 Firefox/1.5.0.5"
        urlmod._urlopener = Opener()

def like(a, b):
    """returns true if args are equal when stripped of non-alphanumeric chars"""

    _strip = lambda s: "".join([char.lower() for char in s if char.isalpha() or char.isdigit()])
    return _strip(a) == _strip(b)

def elapsed(seconds=time.time()):
    """returns seconds elapsed in human readable format"""

    now = time.time()
    if seconds > now:
        now, seconds = seconds, now
    units = [["second", float(now) - seconds], ["minute", 60], ["hour", 60], ["day", 24], ["week", 7]]
    if not units[0][1]:
        units = ["%s %ss" % (int(units[0][1]), units[0][0])]
    else:
        for i in range(1, len(units)):
            units[i][1], units[i - 1][1] = divmod(units[i - 1][1], units[i][1])
        units = [unit for unit in units if int(unit[1])]
        for i in range(len(units)):
            units[i][0] += plural(units[i][1])
            if i == 1:
                units[i][0] += " and "
            elif i > 1:
                units[i][0] += ", "
            units[i] = "%s %s" % (locale.format("%s", int(units[i][1]), True), units[i][0])
        units.reverse()
    return "".join(units)

def choose(lst, name, selected=""):
    """console list selector"""

    if lst and not selected:
        selected = lst[0]
    if len(lst) > 1:
        entered = raw_input("enter %s or number, r for random or hit enter to default to %s - available %ss are:\n%s\n" % (
            name, selected, name,
            "\n".join(["[%s] %s" % (item[0] + 1, item[1]) for item in list(enumerate(lst))])
        ))
        if entered.isdigit() and int(entered) - 1 in range(len(lst)):
            selected = lst[int(entered) - 1]
        elif entered == "r" and lst:
            selected = random.choice(lst)
        elif entered in lst:
            selected = entered
    print "using %s: %s\n" % (name, selected)
    return selected

def plural(items):
    """returns "s" for pluralising strings"""

    s = ""
    if int(items) != 1:
        s = "s"
    return s

