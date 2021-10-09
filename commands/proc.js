const { SlashCommandBuilder,codeBlock } = require('@discordjs/builders');
const discord = require('discord.js')
const os = require('os')
const {execSync} = require('child_process')

//utility function for converting bytes to a human-readable format
function formatBytes(a,b=2,k=1024){with(Math){let d=floor(log(a)/log(k));return 0==a?"0 Bytes":parseFloat((a/pow(k,d)).toFixed(max(0,b)))+" "+["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][d]}}

const data = new SlashCommandBuilder()
	.setName('proc')
	.setDescription('returns OS information')

async function func(interaction,client) {
	ramUsage = require('../tmp.js')
	stats = ''
	versions = ''
	stats = stats + `Arch:       ${execSync('arch').toString()}`
	stats = stats + `Ram Usage:  ${formatBytes(ramUsage.used) + '/' + formatBytes(ramUsage.total)}\n`
	stats = stats + `Bot Uptime: ${ new Date(client.uptime).toISOString().substr(11, 8)}\n`
	stats = stats + `OS:         ${os.type() +' '+ os.release()}`
	versions = versions + `NodeJS version:       ${process.version}\n`
	versions = versions + `Discord.js version:   ${discord.version}`
	const exampleEmbed = new discord.MessageEmbed()
		.setColor([0,255,128])
		.setTitle('Device Specs')
		.setDescription('Lets see what we got')
		.addField('Stats',codeBlock(stats))
		.addField('Versions',codeBlock(versions))
		.setTimestamp()
	await interaction.reply({ embeds:[exampleEmbed], ephemeral: true })
}

module.exports={
	'data':data, //slash command
	'helpStr':"list off some device status information", //sting to be used when the help command is called
	'canDeploy':true, //can this command be deployed globally to all guilds
	'guildIds':['783738781097263140'], //guildIDs to roll out to when running for test,
	'function': func
}