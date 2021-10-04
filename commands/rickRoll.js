const { SlashCommandBuilder } = require('@discordjs/builders');
const { joinVoiceChannel, createAudioResource, createAudioPlayer, NoSubscriberBehavior } = require('@discordjs/voice');

const player = createAudioPlayer({
	behaviors: {
		noSubscriber: NoSubscriberBehavior.Pause,
	},
});

const audioResource = createAudioResource('/home/walksanator/bots/nationStates/out.mp3');

const data = new SlashCommandBuilder()
	.setName('example')
	.setDescription('logs something to the console')

async function func(interaction,client){
	if (interaction.member.voice.channel.id == null){await interaction.reply('join a vc'); return} 
	const connection = joinVoiceChannel({
		channelId: interaction.member.voice.channel.id,
		guildId: interaction.channel.guild.id,
		adapterCreator: interaction.channel.guild.voiceAdapterCreator,
	});
	player.play(audioResource)
	connection.subscribe(player)
	setTimeout(() => player.unpause(), 5_000)
	await interaction.reply({ content:'rickrolling'})
}

module.exports={
	'data':data, //slash command
	'helpStr':"list off some device status information", //sting to be used when the help command is called
	'canDeploy':false, //can this command be deployed globally to all guilds
	'guildIds':['783738781097263140'], //guildIDs to deploy to (for specific commands) (strings)
	'function': func //async function to be executed when the command is run
}