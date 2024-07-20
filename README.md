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
