# GodOfRATs
This is one of the **best RATs** I have ever coded...

## Getting Started
- This is a simple and quick guide on how to setup and install this RAT, but first I want to talk about the **functionality** of this RAT.
- This RAT can:
  - Open an improved **FTP** (FTP+) **session** with the client
  - **steal** all web browser **passwords** of the client
  - **screenshare** at almost 0.5fps!!!
  - **view the clients screen** with a screen shot tool
> It can do all of this while hiding your IP address!
> 
> `HoW?!?/` Well, the session is not directly created with the client, but all packets are forwarded thru the server...
> 
> `Is THaT a GOoD ThinG?!?$^?&` YES! That's a great thing! As it will be a LOT harded to track the attacker...
> 
> `cAN I HaCK SomEONe WitH THis??@?!` NO! But actually yes, you technically could hack someone, but keep in mind that **I will NOT be responsible for the damage you do using MY tool!** As this was created for penetration testing purposes only!

## Setup
- Firstly you have to setup/configure the RAT for yourself. So go ahead and change the **second last line** on each user used file (`virus.py`, `god.py`, `server.py`), set your public **IP** and the forwarded **port** to your *server*. And that's it, you're good to go on the Building/Installation part, yes it's **easy as that** lmao.

## Building/Installation
- I highly recommend using `pyinstaller` as a converter from python script to an actual executable (`pip install pyinstaller`). Now run `pyinstaller virus.py -w --onefile` to build our RAT. Now you just need to start the `server.py` on a static server as I mentioned before... And now you're done!
- All there is left to do is run the `virus.exe` on a machine you want to pen test...
- When the `.exe` file is running, you can go on your PC and run `god.py`, now you will connect to your server where you can start pen testing your pen testing machine, use `help` when you get lost in the commands.

## End
So that's it! That's my RAT...
It took me like 30+ hours to code this thing, so I hope you like it!!!



PS: If you have any ideas for future projects in python/js, that you want to share or need help with, hit me up on DC (LukiS#1430), I am always open for new challenges!
