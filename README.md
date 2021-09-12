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
2. Give your bot a name, and optionally a description and image. Example: `PikamonBot`.
3. Save your changes
4. Go to the `Bot` menu on the left-hand side
5. Click `Add Bot` and then `Yes, do it!`
6. Under the `TOKEN` section click either `Click to Reveal Token` or `Copy` to copy the token. This is the OAuth token your bot will use when connecting to your server. **Save this permanently and do not lose this.**

Add the bot to the discord server
1. On the developer portal, go to the OAuth menu on the left-hand side
2. Under the `SCOPES` section check the box for `bot`
3. Once you do this, a URL will appear. **Save this for later - do not lose this URL.** You will need this URL again if you wish to connect your bot to another server.
4. Under the `BOT PERMISSIONS` section check the boxes for `Read Message History` and `Send Messages`
5. Navigate to the bot URL you copied in the previous step in a browser
6. A page will come up which will prompt you to select a server. Select the server you wish to add the bot to, then select `Authorize`.

### Adding the bot to a new server
At this point, your bot has already been registered. You already have a OAuth token for your bot that you have saved. If you still have the URL you saved in step 3 under `Add the bot to the discord server`, then adding the bot to a new server is as easy as doing the following:
- Navigate to the bot URL
- Select the new server you wish to add the bot to, then select `Authorize`

And that's it! A single instance of your bot will now work across multiple servers, and it will maintain data between each. What this means is that if the same user is on multiple servers which contain the bot, then that user can catch Pokemon on any server and have it saved to their account. They can then list their caught Pokemon on any server, and it will show Pokemon caught from any server.

# Running the Bot
To run the bot, simply run `bot.py`. Note that before you do this, you must set the following environment variables:
- `TOKEN`: Your OAuth token from when you created the bot
- `DATABASE_CONFIG_PATH`: Path to the SQL definition files of the SQLite tables for the Pikamon bot. By default,
    it is under this projects [database configuration](https://github.com/dlrocker/pikamon-py/tree/main/configuration/database) directory.

Different IDEs and editors have different ways to do this. Here are a few ways to do this:
- Use a `.env` file
- Add the environment variable to your execution configuration (if using something such as PyCharm, there is a section where you can define environment variables)
- Manually export the variable if using a UNIX environment
