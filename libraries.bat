@echo off

echo This will install all of the packages required for the bot.

Packages:
    pip install discord
    @REM For creating Discord bots.

    pip install google-generativeai
    @REM Palm API.

    pip install textblob
    @REM Library for correcting sentences.

    pip install sympy
    @REM Mathematics

    pip install latex2sympy
    @REM turns sympy to maths.