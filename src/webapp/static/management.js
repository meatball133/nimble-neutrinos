const channelsList = document.getElementById("channels-list");


function updateChannel(channelID, newState) {
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
