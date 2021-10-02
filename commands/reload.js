const { SlashCommandBuilder } = require('@discordjs/builders');
const discord = require('discord.js')
const os = require('os');
const { exit } = require('process');

const data = new SlashCommandBuilder()
	.setName('reload')
	.setDescription('reloads the bots state')

const allowedUsers = ['596098777941540883']
async function func(interaction,client) {
	if (interaction.user.id in allowedUsers) {
		await interaction.reply('reloading Bot, git pulling, npm installing and restarting')
		exit()
	} else {
		await interaction.reply('not authorized to reload the bot')
	}
}

module.exports={
	'data':data, //slash command
	'helpStr':"list off some device status information", //sting to be used when the help command is called
	'canDeploy':true, //can this command be deployed globally to all guilds
	'guildIds':['783738781097263140'], //guildIDs to roll out to when running for test,
	'function': func
}