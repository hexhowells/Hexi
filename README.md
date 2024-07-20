<p align="center">
  <img src="https://github.com/hexhowells/Hexi/blob/main/images/logo.png" width=70%>
</p>

## Hexi - A custom built social robot

Hexi is an open source, custom built, social robot and digital assistant. 

<p align="left">
  <img src="https://github.com/hexhowells/Hexi/blob/main/images/hexi-with-cube.png" width=60%>
</p>

## Hexi Folder Structure
```
.
└── Hexi/
    ├── assets/
    │   ├── face
    │   └── fonts
    ├── auth  // used to store auth tokens
    ├── boot  // scripts to run on boot
    ├── config
    ├── core/
    │   ├── intent  // natural language intent engine
    │   └── skills  // list of skills/features Hexi can perform
    ├── features  // image detection features
    ├── interfaces/  // hardware interfaces
    │   ├── battery
    │   ├── button
    │   ├── camera
    │   ├── display
    │   ├── motor
    │   └── speaker
    ├── speech  // wakeword detection and speech processing
    └── telegram  // used to listen and send messages via telegram
```

## Core

### Intent Engine

The intent engine (Harpie) is designed to determine what the user is asking Hexi to do given a textual command (generated via speech-to-text). Harpie uses TF-IDF against the list of commands for each supported skill to get the best match.

### Skills
```hexi/core/skills``` stores all of the skills Hexi can support. Each skill is stored in its own folder and genreated using the ```add_skill.py``` script. Each skill is identified by a unique name and has a list of associated commands which are used to activate the skill. **Note: Given the intent engine commands given to Hexi do not have to perfectly match the ones listed**.

All skills are stored in [skills.json](https://github.com/hexhowells/Hexi/blob/main/hexi/core/skills/skills.json).

Each skill contains a script called ```run.py``` which contains the ```start``` entry point function. This function takes in the original command as input if needed for the skill. The skill can also be run from the command line like any Python script for testing.

## Interfaces

The ```hexi/interfaces``` folder contains hardware interfaces for each sensor and actuator in Hexi. Interfaces can be imported into a skill script with the following:
```python
from hexi.interfaces.camera import camera
from hexi.interfaces.motor import Motor
from hexi.interfaces.button import Button
from hexi.interfaces.display import display, icons
from hexi.interfaces.battery import Battery
from hexi.interfaces.speaker import sound
```
