# pikamon-py
Python native Pokemon bot for Discord

[![python-report Actions Status](https://github.com/dlrocker/pikamon-py/workflows/python-report/badge.svg?branch=main)](https://github.com/dlrocker/pikamon-py/actions)

Please see the [Wiki Page](https://github.com/dlrocker/pikamon-py/wiki) for more information about the bots design.

# Adding bot to server
Create a server if you do not have on already
1. Create a discord server
2. Go to the `Server Settings`
3. Navigate to the `Roles` menu and for an existing role (or a new role you create), enable the `Manage Server` option

Once you have a server, you need to get a OAuth token for your bot
1. Go to the developer portal: https://discord.com/developers/applications/
2. Give your bot a name, and optionally a description and image. I called mine `PikamonBot`.
3. Save your changes
4. Go to the `Bot` menu on the left-hand side
5. Click `Add Bot` and then `Yes, do it!`
6. Under the `TOKEN` section click either `Click to Reveal Token` or `Copy` to copy the token. This is the OAuth token your bot will use when connecting to your server.

Add the bot to the discord server
1. On the developer portal, go to the OAuth menu on the left-hand side
2. Under the `SCOPES` section check the box for `bot`
3. Once you do this, a URL will appear. Copy this for later.
4. Under the `BOT PERMISSIONS` section check the boxes for `Read Message History` and `Send Messages`
5. Navigate to the bot URL you copied in the previous step in a browser
6. A page will come up which will prompt you to select a server. Select the server you wish to add the bot to, then select `Authorize`.

# Running the Bot
To run the bot, simply run `bot.py`. Note that before you do this, you must set the following environment variables:
- `TOKEN`: Your OAuth token from when you created the bot
- `DATABASE_CONFIG_PATH`: Path to the SQL definition files of the SQLite tables for the Pikamon bot. By default,
    it is under this projects [database configuration](https://github.com/dlrocker/pikamon-py/tree/main/configuration/database) directory.

Different IDEs and editors have different ways to do this. Here are a few ways to do this:
- Use a `.env` file
- Add the environment variable to your execution configuration (if using something such as PyCharm, there is a section where you can define environment variables)
- Manually export the variable if using a UNIX environment
