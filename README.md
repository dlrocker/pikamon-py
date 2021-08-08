# pikamon-py
Python native Pokemon bot for Discord

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
