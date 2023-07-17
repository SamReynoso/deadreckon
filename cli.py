"""Quick cli that was thrown together."""

import os
import numpy as np
from colorama import Fore, Style

import config
from deadreckon.vector import Vector


class ReadOuts:
    def unreachable(self):
        msg = f"{ Fore.RED }{ Style.BRIGHT}Off Course!:{Style.RESET_ALL} {Fore.YELLOW}Destination Unreachable - Increase engine power.{ Style.RESET_ALL }"
        print(msg)

    def run(self):
        msg = \
f"""
    { Fore.GREEN }{ Style.BRIGHT }Welcome to Deadreckon.
Navigate{Style.RESET_ALL}
    from: {Fore.YELLOW}{ config.BEGINNING }{Style.RESET_ALL} { Style.DIM }-  Not Titanic Wreckage{Style.RESET_ALL}
    to: {Fore.YELLOW}{ config.END}{Style.RESET_ALL} { Style.DIM }-  Titanic Wreckage{Style.RESET_ALL}
        { config.CRAFT_SPEED } meters/second craft speed
        { round((config.LIMIT * config.ELAPSE) / 3_600) } hour limit
{ Fore.GREEN }{ Style.BRIGHT }press any key continue:{Style.RESET_ALL}

"""
        print(msg)

    def status(self, loopcount):
        if config.DEBUG:
            debug_msg = f"{ Fore.YELLOW }Debug mode ON{Style.RESET_ALL}\n"
            print(debug_msg)
        msg = f"Running... { loopcount }\n"
        msg += f"{loopcount * config.ELAPSE / 60} minutes into journey"
        print(msg)

    def menu(self):
        msg = f"{ Fore.GREEN }{ Style.BRIGHT }Menu{ Style.RESET_ALL }\n\
    { Fore.YELLOW }(x) - To exit\n\
    (r) - Run with current settings\n\
    (about) - about Deadreckon\n\
    \n\
    (s) - Change craft speed\n\
    (l) - Change limit\n{ Style.RESET_ALL }\
Enter selection:\n"
        print(msg)

    def set_craft_speed(self, craft_speed, err=False):
        if err:
            err_msg = f"{ Fore.RED }Speed must be a number\n{Style.RESET_ALL}"
            print(err_msg)
        msg = f"{ Fore.GREEN }Set craft speed{ Style.RESET_ALL }\n\
    { Fore.YELLOW }Current speed is { craft_speed } m/s{ Style.RESET_ALL }\n\
enter speed in meters per second or (c) to cancel:"
        print(msg)

    def set_limit(self, limit, err=False):
        if err:
            err_msg = f"{ Fore.RED }Limit must be a number\n{Style.RESET_ALL}"
            print(err_msg)
        msg = f"{ Fore.GREEN }Set limit{ Style.RESET_ALL }\n\
    { Fore.YELLOW }Current limit is { limit }{ Style.RESET_ALL }\n\
enter limit or (c) to cancel:"
        print(msg)

    def about(self):
        msg = f"Deadreckon is a navigation program."
        print(msg)

    def craft_info(self, target: Vector, trav: Vector, err: Vector, err_delta: float, craft: Vector):
        a = lambda x: round(x * (180 /np.pi) + 360) % 360

        msg = f"Target angel { Fore.GREEN }{ a(target.theta) }°{ Style.RESET_ALL }\n"
        msg += f"Travel angel { Fore.GREEN }{ a(trav.theta) }°{ Style.RESET_ALL }\n"
        msg += f"err angel { Fore.GREEN }{ a(err.theta) }°{ Style.RESET_ALL }\n"
        msg += f"err delta { Fore.GREEN }{ a(err_delta) }°{ Style.RESET_ALL }\n"
        msg += f"Craft angel { Fore.GREEN }{ a(craft.theta) }°{ Style.RESET_ALL }\n"

        print(msg)

    def success(self):
        msg = f"{ Fore.GREEN }congratulations!{ Style.RESET_ALL }\n"
        msg += f"You made it to The Titanic wreckage site.\n"
        msg += f"That is all."
        print(msg)

class Cli:
    readout = ReadOuts()

    def run(self):
        if config.DEBUG:
            return config.ORIGIN, config.DESTINATION , config.CRAFT_SPEED, config.LIMIT, "r"
        self.readout.run()
        input()
        craft_speed, limit, selection = self.menu(config.CRAFT_SPEED, config.LIMIT)
        return config.ORIGIN, config.DESTINATION , craft_speed, limit, selection
    
    def set_craft_speed(self, craft_speed, err=False):
        self.clear()
        self.readout.set_craft_speed(craft_speed, err=err)
        speed_input = input()
        if speed_input == "c":
            return craft_speed
        try:
            craft_speed = int(speed_input)
        except:
            craft_speed = self.set_craft_speed(craft_speed, err=True)
        return craft_speed

    def set_limit(self, limit, err=False):
        self.clear()
        self.readout.set_limit(limit, err=err)
        limit_input = input()
        if limit_input == "c":
            return limit
        try:
            limit = int(limit_input)
        except:
            limit = self.set_limit(limit, err=True)
        return limit

    def about(self):
        self.clear()
        self.readout.about()
        input()

    def menu(self, craft_speed, limit):
        self.clear()
        self.readout.menu()
        selection = input()
        if selection == "s":
            craft_speed = self.set_craft_speed(craft_speed)
        if selection == "l":
            limit = self.set_limit(limit)
        if selection == "about":
            self.about()
        while selection not in ["r", "x"]:
            craft_speed, limit, selection = self.menu(craft_speed, limit)
        print(craft_speed, limit, selection)
        return craft_speed, limit, selection

    def success(self):
        self.clear()
        self.readout.success()
        input()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


cli = Cli()



