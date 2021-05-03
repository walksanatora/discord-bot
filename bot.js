const discord = require('discord.js')
require('dotenv').config()
const client = new discord.Client();

var PREFIX="?"

console.log(typeof(process.env.DISCORD_TOKEN))
console.log(process.env.DISCORD_TOKEN)
client.once('ready', () => {
	console.log('Ready!');
});

client.on('message', message => {
	console.log(message.content);
	cmds=message.content.split(' ')
	switch(cmds[0]){
		case `${PREFIX}test`:
			message.channel.send("message recieved")
		break;
		case `${PREFIX}owo`:
			message.channel.send("dont make me kill you weeb")
		break;
		default:
			console.log("none of my buisness")
	}
});

client.login(process.env.DISCORD_TOKEN);