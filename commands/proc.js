const { SlashCommandBuilder } = require('@discordjs/builders');

const data = new SlashCommandBuilder()
	.setName('proc')
	.setDescription('returns OS information')

module.exports={
	'data':data
}