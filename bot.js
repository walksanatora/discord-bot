require('dotenv').config()
const discord = require('discord.js')
const client = new discord.Client({intents: [discord.Intents.FLAGS.GUILD_MESSAGES,discord.Intents.FLAGS.GUILDS]});
const fs = require('fs');
/*
variables in .env
DISCORD_TOKEN: your discord token
BOT_PREFIX the prefix for the bot
*/

var PREFIX=process.env.BOT_PREFIX


client.once('ready', () => {
	console.log('Ready!');
	client.user.setPresence({ activities: [{ name: 'Ready to help!' }], status: 'online' });
});

//TODO: https://support-dev.discord.com/hc/en-us/articles/4404772028055 (deprecation of reading message content)
/*
client.on('messageCreate', message => {
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
*/

const commands = {}
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	commands[command.data.name] = command.function
}

client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;
	try {
		await commands[interaction.commandName](interaction,client)	
	} catch (error) {
		const exampleEmbed = new discord.MessageEmbed()
		.setColor('#ff0000')
		.setTitle('Error occured')
		.addField('Excpetion',error.toString())
		.addField('Detail',error.stack.toString())
		await interaction.reply({embeds: [exampleEmbed]})
	}
});

client.login(process.env.DISCORD_TOKEN);