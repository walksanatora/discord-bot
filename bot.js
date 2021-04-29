const discord = require('discord.js')
require('dotenv').config()
const client = new discord.Client();

client.once('ready', () => {
	console.log('Ready!');
});

client.login(process.env.DISCORD_TOKEN);