# Reimbursement Calculator
A simple tool to allow easy calculation of reimbursement each month without having to rely on manual entry of values from screenshots/bills. Works with Swiggy/Zomato/Blinkit/Zepto screenshots/bills out of the gate.

## Purpose
A lot of corporate offices have a reimbursement policy where you can reimburse expenditure throughout the month during office hours. This entails a lot of time of manually sifting through screenshots, filling forms and converting to PDF. This tool reads through your screeshots/photos, calculates the total amount, converts the images into the PDF (even names them according to the previous month's name using your computer's date and time), and saves the total amount to a text file too.

<br>

## Installation
You can download the latest ```.exe``` through [Releases](https://github.com/sudotman/zwigato-reimbursement-calculator/releases/) and double-click to run it.

or

You can clone the repo and build it manually.

```reimbursement.py``` contains the CLI code. When run, there will be no prompts for any sort of file selection but rather the current present jpegs/jpgs will be automatically read and then processed.

```reimbursementGUI.py``` contains the GUI code with a proper user interface. This is the one used to build the Releases ```Reimbursement.exe``` too.

## Contribute to the project
[Click here to see general collaboration information](#contribution)


# Contribution
Generate a pull request for whatever change you feel is necessary and I will be happy to review and add them.

## Current to-do:
- ~~Improve OCR for hindi locale.~~
- ~~Ability to convert images into PDF at the same place without relying on paid software~~
- Add a simple requirements.txt and more information on custom compilation.