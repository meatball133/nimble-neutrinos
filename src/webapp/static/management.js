const installedOnList = document.getElementById("installed-on-list");
const installableOnList = document.getElementById("installable-on-list");
const channelsList = document.getElementById("channels-list");
const installButton = document.getElementById("install-button");

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

function updateChannel(channelID, newState) {
    console.log(channelID, newState);
    fetch(`/updatechannel`, {
        method: "POST",
        body: JSON.stringify({
            "id": channelID,
            "new_state": newState,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    })
}

function loadChannelList(serverID) {
    channelsList.innerHTML = "";
    fetch(`/channels?server_id=${serverID}`).then(response => response.json()).then(data => {
        for (const channel of data) {
            let channelElement = document.createElement("div");
            let channelText = document.createElement("span");
            let channelCheckbox = document.createElement("input");
            channelText.innerText = channel.name;
            channelCheckbox.type = "checkbox";
            channelCheckbox.checked = channel.enabled;
            channelCheckbox.addEventListener("change", e => {
                updateChannel(channel.id, e.target.checked);
            });
            channelElement.appendChild(channelCheckbox);
            channelElement.appendChild(channelText);
            channelsList.appendChild(channelElement);
        }
    });
}

function setupServerListClickActions() {
    document.querySelectorAll("#installed-on-list .server").forEach(element => {
        let serverID = element.querySelector(".server-id").innerText;
        element.addEventListener("click", e => {
            loadChannelList(serverID);
        })
    })
}

window.addEventListener("DOMContentLoaded", setupServerListClickActions)

// window.addEventListener("load", e => {
//     // loadData(testChannels);
// });
