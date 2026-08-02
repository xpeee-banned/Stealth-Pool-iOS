const fs = require("fs");
const v = JSON.parse(fs.readFileSync("site/version.json", "utf8"));
process.stdout.write(String(v.build || 0));
