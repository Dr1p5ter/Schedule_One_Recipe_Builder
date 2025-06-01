# Schedule_One_Recipe_Builder

## Instalation

For the time being, my latest release contains usable module code that can benefit anyone wanting to make their own code. Feel free to use my json files in the assets subdirectory. If you in fact want to change the values because of mods, feel free to. All I ask is to be credited please.

This application can run on any version of python 3.6+ but will need some other packages for runtime. Please consult my requirements.txt document I made. This is the minimal requirements. Run the following code using your own production enviornment to install the necessary modules:

```bash
> python -m pip install -r requirements.txt
```
### **Please be within the parent directory and not in any of the subdirectories. This will cause issues since the location of the requirements file is in the parent directory.** ###

## Testing

I attempted to make all tests universal and not strictly dependent on any constants aside from file pointers. In order to run, ensure you are within the production enviornment within either the root or branch of the parent directory. Then simply type the following into the terminal:

```bash
> pytest
```

The testing is entirely automated and will seek for the test files. ALL tests are located in the test subdirectory along with the assets used for the testing process. Please read all comments regarding each test.

## Mode to Come

Stay tuned for mixing classes and my revamped reverse BFS algorithm. I intend on making a GUI for this or some sort of light weight interface. We will see where I go :D

# Special Thanks

I wanted to extend a special thanks before continuing with this project to the people behind the website schedule1-calculator.com and their tireless work. Me making this project is in no way bashing their work. Please go check them out on their website.

@Shibka (Shane R) — Creator, Mix Specialist
@dangdoopdewc — Spreadsheet Master, Mix Specialist
@TMafono — In-Game Mixing, Mix Specialist
@King ToasterBath - In-Game Mixing
@froggy — Modder, Pricing Equations/Formulas

If you contributed to the development of the website send me an email :D
Email: mmclaren2021@outlook.com
