const { SlashCommandBuilder } = require('@discordjs/builders');

const data = new SlashCommandBuilder() //creating a /command via the special builder
	.setName('example')
	.setDescription('logs something to the console')

async function func(interaction,client){ // first arg is the interaction object, second arg is the discord client
	console.log('this was ran')
}

module.exports={
	'data':data, //slash command
	'helpStr':"list off some device status information", //sting to be used when the help command is called
	'canDeploy':false, //can this command be deployed globally to all guilds
	'guildIds':[], //guildIDs to roll out to when running for test,
	'function': func
}