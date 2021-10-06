const { SlashCommandBuilder } = require('@discordjs/builders');
const { joinVoiceChannel, createAudioResource, createAudioPlayer, NoSubscriberBehavior, AudioPlayerStatus } = require('@discordjs/voice');

const player = createAudioPlayer({
	behaviors: {
		noSubscriber: NoSubscriberBehavior.Pause,
	},
});

const data = new SlashCommandBuilder()
	.setName('rickroll')
	.setDescription('kills your sanity')

async function func(interaction,client){
	if (interaction.member.voice.channel.id == null){await interaction.reply({content:'join a vc',ephemeral: true}); return} 
	var connection = joinVoiceChannel({
		channelId: interaction.member.voice.channel.id,
		guildId: interaction.channel.guild.id,
		adapterCreator: interaction.channel.guild.voiceAdapterCreator,
	});
	player.stop(true)
	var audioResource = createAudioResource('/home/pi/gitrepo/discord-bot/out.mp3')
	player.play(audioResource)
	connection.subscribe(player)
	await interaction.reply({content:'rickrolling',ephemeral: true})
	player.on(AudioPlayerStatus.Idle, () => {
		connection.destroy()
	});
	
}

module.exports={
	'data':data, //slash command
	'helpStr':"slowly drains sanity", //sting to be used when the help command is called
	'canDeploy':false, //can this command be deployed globally to all guilds
	'guildIds':['783738781097263140'], //guildIDs to deploy to (for specific commands) (strings)
	'function': func //async function to be executed when the command is run
}