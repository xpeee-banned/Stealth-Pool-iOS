const fs = require("fs");
const p = "site/version.json";
const v = JSON.parse(fs.readFileSync(p, "utf8"));
const parts = (v.version || "0.0.0").split(".");
parts[2] = String(parseInt(parts[2] || "0", 10) + 1);
v.version = parts.join(".");
v.build = (v.build || 0) + 1;
fs.writeFileSync(p, JSON.stringify(v, null, 2) + String.fromCharCode(10));
console.log("Bumped to " + v.version + " build " + v.build);
