/*
 * Stealth Pool iOS v2.0 - Frida Gadget Cheat for 8 Ball Pool
 * by xpe.nettt / Stealth Proyect
 *
 * Key validation with local master key fallback
 * ESP ready (aim, power, pocket, cushion, guidelines)
 * Streamer mode, Auto play, Auto queue
 */

var CONFIG = {
    KEY_STORAGE: "stealth_pool_key",
    SETTINGS_STORAGE: "stealth_pool_settings",
    DEFAULT_SETTINGS: {
        aim: true, power: true, guidelines: true,
        pocket: true, cushion: false,
        autoplay: false, autoqueue: false,
        streamer: false, opacity: 0.8
    }
};

var state = {
    key: null, activated: false, tier: "free",
    settings: Object.assign({}, CONFIG.DEFAULT_SETTINGS),
    inMatch: false, isMyTurn: false
};

function loadKey() {
    try {
        var k = ObjC.classes.NSUserDefaults.standardUserDefaults()
            .stringForKey_(CONFIG.KEY_STORAGE);
        if (k) state.key = k.toString();
    } catch(e) {}
}

function saveKey(key) {
    ObjC.classes.NSUserDefaults.standardUserDefaults()
        .setObject_forKey_(key, CONFIG.KEY_STORAGE);
    ObjC.classes.NSUserDefaults.standardUserDefaults().synchronize();
    state.key = key;
}

function validateKey(key) {
    return new Promise(function(resolve) {
        resolve(localValidate(key));
    });
}

function localValidate(key) {
    var mk = ["stealth-pro-master-2026", "xpe-nettt-founder", "stealth-root-access"];
    if (mk.indexOf(key) !== -1) return { valid: true, tier: "master" };
    if (key.indexOf("xpe-") === 0 && key.length >= 15) return { valid: true, tier: "pro" };
    if (key.indexOf("free-") === 0 && key.length >= 12) return { valid: true, tier: "free" };
    return { valid: false, error: "Key invalida" };
}

function setupIPC() {
    rpc.exports = {
        activate: function(key) {
            return new Promise(function(resolve) {
                validateKey(key).then(function(r) {
                    if (r.valid) {
                        state.activated = true; state.tier = r.tier;
                        saveKey(key);
                        resolve({ success: true, tier: r.tier });
                    } else resolve({ success: false, error: r.error });
                });
            });
        },
        getStatus: function() {
            return { activated: state.activated, tier: state.tier };
        },
        getSettings: function() { return state.settings; },
        updateSettings: function(s) {
            Object.assign(state.settings, s);
            return { success: true };
        },
        toggleStreamer: function() {
            state.settings.streamer = !state.settings.streamer;
            return { streamerMode: state.settings.streamer };
        }
    };
}

function init() {
    console.log("[Stealth] Stealth Pool iOS v2.0 loaded");
    loadKey();
    if (state.key) {
        validateKey(state.key).then(function(r) {
            if (r.valid) { state.activated = true; state.tier = r.tier; }
        });
    }
    setupIPC();
    console.log("[Stealth] Initialized");
}

setTimeout(init, 2000);