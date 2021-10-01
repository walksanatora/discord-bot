require('dotenv').config()
const discord = require('discord.js')
const client = new discord.Client({intents: [discord.Intents.FLAGS.GUILD_MESSAGES,discord.Intents.FLAGS.GUILDS]});
const os = require('os')

/*
variables in .env
DISCORD_TOKEN: your discord token
BOT_PREFIX the prefix for the bot
*/
//utility function for fotmatting bytes
function formatBytes(a,b=2,k=1024){with(Math){let d=floor(log(a)/log(k));return 0==a?"0 Bytes":parseFloat((a/pow(k,d)).toFixed(max(0,b)))+" "+["Bytes","KB","MB","GB","TB","PB","EB","ZB","YB"][d]}}


var PREFIX=process.env.BOT_PREFIX

console.log(typeof(process.env.DISCORD_TOKEN))
console.log(process.env.DISCORD_TOKEN)
client.once('ready', () => {
	console.log('Ready!');
});

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



client.on('interactionCreate', async interaction => {
	if (!interaction.isCommand()) return;

	if (interaction.commandName === 'echo') {
		await interaction.reply(interaction.options.getString('input'));
	}else if (interaction.commandName == 'proc'){
		const exampleEmbed = new discord.MessageEmbed()
			.setColor('#00ffaa')
			.setTitle('Device Specs')
			.setDescription('Lets see what we got')
			.addField({ name: 'Arch', value: os.arch() })
			.addField({ name: 'Remaining Ram', value: formatBytes(os.freemem()) + '/' + formatBytes(os.totalmem()) })
			.addField({ name: 'Uptime', value: new Date(os.uptime * 1000).toISOString().substr(11, 8) })
			.addField({ name: 'OS', value: os.type() +' '+ os.release() })
			.setTimestamp()
		await interaction.reply({ embeds:[exampleEmbed], ephemeral: true })
	} 
});

client.login(process.env.DISCORD_TOKEN);