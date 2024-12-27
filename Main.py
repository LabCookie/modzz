# CHANGELOG for 0.3
# - Bug fixes
# - Full on mod opening functionality

# Import neccessary
import os
import runpy
import json
from random import choice as c

mods = {}
modname_list = []

apps = {}
appname_list = []
version = 0.3

def error(event,mod):
    splash = [
        f"modzz has failed to trigger event {event} at {mod}.",
        f"They always say blame the game, not the player. Failed to trigger event {event} at {mod}.",
        f"Ratio. (5 likes) Failed to trigger event {event} at {mod}."
    ]
    print(c(splash))

def call(event,arg=None):
    for name,mod in mods.items():
        if not os.path.isdir(mod["path"]):
            mod["runpy"]["whenstart"].get(event,error)(event,mod["name"],arg)
        else:
            try:
                mod["runpy"][event]["whenstart"](event,mod["name"],arg)
            except:
                error(event,mod["name"])

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

appnmod_globals = {
    "mod_list": modname_list,
    "mods": mods,
    "app_list": appname_list,
    "apps": apps,
    "cls": clear,
    "runpy": runpy,
    "call": call
}

def prepare_mods(directories):
    for directory in directories:
        for file in os.listdir(directory):
            if not file.endswith(".py"):
                with open(os.path.join(directory,file,"meta.json"), "r") as f:
                        meta = json.load(f)
                        runpy_funcs = {"whenstart": runpy.run_path(os.path.join(directory,file,meta["whenstart"]), init_globals=appnmod_globals)}
                        if meta.get("CUSTOM_EVENTS"):
                            for name in meta["CUSTOM_EVENTS"]:
                                if meta.get(name):
                                    runpy_funcs[name] = runpy.run_path(os.path.join(directory,file,meta[name]), init_globals=appnmod_globals)
                        mods[file] = {
                            "name": meta["name"],
                            "runpy": runpy_funcs,
                            "path": directory
                        }
                        modname_list.append(file)
                        
                        f.close()
            else:
                mods[file] = {
                    "name": file,
                    "runpy": {"whenstart": runpy.run_path(os.path.join(directory,file),init_globals=appnmod_globals)},
                    "path": directory
                }
                modname_list.append(file)
            print(f"loaded {file}")
        print(f"loaded all of {directory}")
def prepare_apps(directories):
    for directory in directories:
        for app in directory:
            with open(os.path.join(directory,app,"meta.json")) as f:
                meta = json.load(f)
                runpy_funcs = {"whenstart": runpy.run_path(os.path.join(os.getcwd(),directory,app,meta["whenstart"]), init_globals=appnmod_globals)}

def run_mod(mod,file):
    mods[mod]["runpy"].get(file).get("whenstart",error)(None,mod,None)
            
def main():
    print("Welcome to modzz, An upgradable esoteric operating \"system\"")
    print(f"Version {version} by LabCookie@modzz")
    prepare_mods(["./Default", "./Scripts"])
    input()
    clear()
    run_mod("Desktop","whenstart")
print(__name__)
if __name__ == "__main__":
    clear()
    main()
else:
    print("Currently, modzz does not want to be imported by a different python file.\nYou have to run the file on your own.")
    input()