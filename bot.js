const discord = require('discord.js')
require('dotenv').config()
const client = new discord.Client();
console.log(typeof(process.env.DISCORD_TOKEN))
console.log(process.env.DISCORD_TOKEN)
client.once('ready', () => {
	console.log('Ready!');
});

client.on('message', message => {
	console.log(message.content);
});

client.login(process.env.DISCORD_TOKEN);