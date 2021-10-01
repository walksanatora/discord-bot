const { execSync } = require("child_process");

j = JSON.parse(execSync('sh -c ./getRam.sh').toString())
total = j[0].total
used = j[0].used
free = total - used
module.exports = {
	'free':free,
	'used': used,
	'total': total,
	'JSON': j
}
