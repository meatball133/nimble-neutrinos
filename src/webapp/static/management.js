const installedOnList = document.getElementById("installed-on-list");
const installableOnList = document.getElementById("installable-on-list");
const channelsList = document.getElementById("channels-list");
const installButton = document.getElementById("install-button");

installButton.addEventListener("click", e => {
    // Send request to update server to have bot installed
});

let data = {};
let currentServer;
let currentInstallableServer;

function loadData(serversAndChannels) {
    data = serversAndChannels;
    for (const [serverName, serverData] of Object.entries(serversAndChannels)) {
        let serverElement = document.createElement("div");
        serverElement.classList.add("server");
        let serverImage = document.createElement("img");
        serverImage.classList.add("server-image");
        serverImage.src = serverData.serverImage;
        let serverNameElement = document.createElement("span");
        serverNameElement.classList.add("server-name");
        serverNameElement.textContent = serverName;

        let serverArrow = document.createElement("div");
        serverArrow.classList.add("server-arrow");

        serverElement.appendChild(serverImage);
        serverElement.appendChild(serverNameElement);
        serverElement.appendChild(serverArrow);

        serverElement.addEventListener("click", e => {
            if (!serverData.installed) {
                if (currentInstallableServer && currentInstallableServer !== e.target) {
                    currentInstallableServer.classList.remove("current-installable-server");
                }
                currentInstallableServer = serverElement;
                currentInstallableServer.classList.add("current-installable-server");
                return;
            }

            channelsList.innerText = "";
            if (currentServer && currentServer !== e.target) {
                currentServer.classList.remove("current-server");
            }
            
            currentServer = serverElement;
            currentServer.classList.add("current-server");
            for (const [channel, enabled] of Object.entries(data[serverName])) {
                let channelElement = document.createElement("div");
                let channelText = document.createElement("span");
                let channelCheckbox = document.createElement("input");
                channelText.textContent = channel;
                channelCheckbox.type = "checkbox";
                channelCheckbox.checked = enabled;
                channelCheckbox.addEventListener("change", e => {
                    data[serverName][channel] = channelCheckbox.checked;
                });

                channelElement.appendChild(channelCheckbox);
                channelElement.appendChild(channelText);
                channelsList.appendChild(channelElement);
            }
            
        });

        data[serverName] = serverData.channels;
        if (serverData.installed) {
            installedOnList.appendChild(serverElement);
        } else {
            installableOnList.appendChild(serverElement);
        }
    }
}

window.addEventListener("load", e => {
    loadData(testChannels);
});


let testChannels = {
    "Server 1": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# CH": true,
            "# CH2": true,
            "# CH3": false,
        },
    },
    "Server 2": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# Images": true,
            "# Videos": true,
        },
    },
    "Server 3": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 4": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 5": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# CH": true,
            "# CH2": true,
            "# CH3": false,
        },
    },
    "Server 6": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# Images": true,
            "# Videos": true,
        },
    },
    "Server 7": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 8": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 9": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# CH": true,
            "# CH2": true,
            "# CH3": false,
        },
    },
    "Server 10": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# Images": true,
            "# Videos": true,
        },
    },
    "Server 11": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 12": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 13": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# CH": true,
            "# CH2": true,
            "# CH3": false,
        },
    },
    "Server 14": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# Images": true,
            "# Videos": true,
        },
    },
    "Server 15": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 16": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 17": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# CH": true,
            "# CH2": true,
            "# CH3": false,
        },
    },
    "Server 18": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# Images": true,
            "# Videos": true,
        },
    },
    "Server 19": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: true,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
    "Server 20": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        installed: false,
        channels: {
            "# General": false,
            "# Cats": true,
            "# Dogs": true,
        },
    },
}