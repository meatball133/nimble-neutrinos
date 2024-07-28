const all = document.getElementById("all");
const mine = document.getElementById("mine");
const favs = document.getElementById("favs");
let current = all;
let currentImage;
let currentImageIndex;
let currentPage = 0;
const extraFilters = [all, mine, favs];
for (const extraFilter of extraFilters) {
    extraFilter.addEventListener("click", (e) => {
        if (current !== extraFilter) {
            current.classList.toggle("current-extra-filter");
            extraFilter.classList.toggle("current-extra-filter");
            current = extraFilter;
        }
    });
}


const gallery = document.getElementById("gallery");

const popup = document.getElementById("popup");
const modal = document.getElementById("modal");
const modalImage = document.getElementById("modal-image");
const modalProfile = document.getElementById("modal-profile");
const modalUsername = document.getElementById("modal-username");
const modalImageUploadDate = document.getElementById("modal-image-upload-date");
const modalTags = document.getElementById("modal-tags");

const modalHeart = document.getElementById("modal-heart");
modalHeart.addEventListener("click", (e) => {
    currentImage.dataset.liked = !(currentImage.dataset.liked === "true");
    if (currentImage.dataset.liked === "true") {
        currentImage.heart.classList.add("heart-liked");
        modalHeart.classList.add("heart-liked");
    } else {
        currentImage.heart.classList.remove("heart-liked");
        modalHeart.classList.remove("heart-liked");
    }
});

const modalTitle = document.querySelector("h2");
const modalActions = document.getElementById("modal-actions");
const modalModify = document.getElementById("modal-modify");
const modalDelete = document.getElementById("modal-delete");
const modalExit = document.getElementById("modal-exit");
const deleteConfirmation = document.getElementById("confirmation");
const confirmationPrompt = document.getElementById("confirmation-prompt");
const confirmationPositive = document.getElementById("confirmation-positive");
const confirmationNegative = document.getElementById("confirmation-negative");
let mode = "Preview";

const saveTags = document.createElement("span");
saveTags.id = "save-tags";
saveTags.textContent = "Save";

saveTags.addEventListener("click", e => {
    if (getComputedStyle(deleteConfirmation)["opacity"] === "0") {
        deleteConfirmation.style.opacity = "1";
        deleteConfirmation.style.zIndex = "5";
    } else if (getComputedStyle(deleteConfirmation)["opacity"] === "1") {
        deleteConfirmation.style.opacity = "0";
        deleteConfirmation.style.zIndex = "-1";
    }
});

const cancelEditTags = document.createElement("span");
cancelEditTags.id = "cancel-edit-tags";
cancelEditTags.textContent = "Cancel";

cancelEditTags.addEventListener("click", e => {
    resetModal();
});

const modalSearchTag = document.createElement("input");
modalSearchTag.id = "modal-search-tag";
modalSearchTag.type = "text";
modalSearchTag.placeholder = "Search ..."
modalSearchTag.autocomplete = "off";

let tagsNotSaved = [];

modalSearchTag.addEventListener('keydown', function (e) {
    const key = e.key;
    if (key === " ") {
        let text = e.target.value;
        if (text === "" || text === " ") {
            e.target.value = "";
            e.preventDefault();
            return
        }
        let tag = document.createElement("div");
        tag.textContent = text;
        tag.classList.add("tag");
        tag.classList.add("modal-tag");

        let removeTag = document.createElement("div");
        removeTag.classList.add("remove-tag");

        removeTag.addEventListener("click", e => {
            modalTags.removeChild(tag)
        });
        tag.appendChild(removeTag);

        tag.removeTag = removeTag;

        modalTags.insertBefore(tag, modalSearchTag);

        tagsNotSaved.push(tag);
        e.target.value = "";
        e.preventDefault();
    }
    if (key === "Backspace" && e.target.value === "") {
        if (modalTags.children.length === 1) {
            return
        }
        e.target.value = e.target.previousElementSibling.textContent;
        modalTags.removeChild(e.target.previousElementSibling);
    }
});

function resetModal() {
    modalTitle.textContent = "Preview"

    modalActions.removeChild(saveTags);
    modalActions.removeChild(cancelEditTags);

    modalActions.insertBefore(modalHeart, deleteConfirmation);
    modalActions.insertBefore(modalModify, deleteConfirmation);
    modalActions.insertBefore(modalDelete, deleteConfirmation);

    confirmationPrompt.textContent = "Are you sure you want to delete this post?";
    mode = "Preview";

    for (const tag of tagsNotSaved) {
        modalTags.removeChild(tag);
    }
    tagsNotSaved = [];

    for (const tag of modalTags.childNodes) {
        if (tag === modalSearchTag) {
            continue;
        }
        tag.removeChild(tag.removeTag);
    }

    modalSearchTag.value = "";

    modalTags.removeChild(modalSearchTag);
}

modalModify.addEventListener("click", e => {
    modalTitle.textContent = "Edit Tags"

    modalActions.removeChild(modalHeart);
    modalActions.removeChild(modalModify);
    modalActions.removeChild(modalDelete);

    modalActions.appendChild(saveTags);
    modalActions.appendChild(cancelEditTags);

    confirmationPrompt.textContent = "Are you sure you want to save these changes?";

    for (const tag of modalTags.childNodes) {
        let removeTag = document.createElement("div");
        removeTag.classList.add("remove-tag");
        removeTag.addEventListener("click", e => {
            modalTags.removeChild(tag);
        });


        tag.appendChild(removeTag);
        tag.removeTag = removeTag;
    }

    modalTags.appendChild(modalSearchTag);

    mode = "Edit Tags";
});

modalDelete.addEventListener("click", e => {
    if (getComputedStyle(deleteConfirmation)["opacity"] === "0") {
        deleteConfirmation.style.opacity = "1";
        deleteConfirmation.style.zIndex = "5";
    } else if (getComputedStyle(deleteConfirmation)["opacity"] === "1") {
        deleteConfirmation.style.opacity = "0";
        deleteConfirmation.style.zIndex = "-1";
    }
});

confirmationPositive.addEventListener("click", e => {
    // Todo: Add delete post
    if (mode === "Preview") {

    } else if (mode === "Edit Tags") {
        tagsNotSaved = [];
    }
    deleteConfirmation.style.opacity = "0";
    setTimeout(() => {
        deleteConfirmation.style.zIndex = "-1";
    }, 200);
});

confirmationNegative.addEventListener("click", e => {
    deleteConfirmation.style.opacity = "0";
    setTimeout(() => {
        deleteConfirmation.style.zIndex = "-1";
    }, 200);
});

modalExit.addEventListener("click", () => {
    popup.style.opacity = "0";
    setTimeout(() => {
        popup.style.zIndex = "-1";

        modalImage.src = "";
        modalProfile.src = "";
        modalUsername.textContent = "";
        modalImageUploadDate.textContent = "";
        modalTags.textContent = "";
    }, 1000)
})

window.addEventListener("click", e => {
    if (e.target !== deleteConfirmation && e.target !== modalDelete && e.target !== confirmationPositive && e.target !== confirmationNegative && e.target !== saveTags) {
        deleteConfirmation.style.opacity = "0";
        setTimeout(() => {
            deleteConfirmation.style.zIndex = "-1";
        }, 200);
    }
});

popup.addEventListener("click", e => {
    if (e.target !== popup) return
    popup.style.opacity = "0";
    setTimeout(() => {
        popup.style.zIndex = "-1";

        modalImage.src = "";
        modalProfile.src = "";
        modalUsername.textContent = "";
        modalImageUploadDate.textContent = "";
        modalTags.textContent = "";
        if (popup.style.opacity !== "0") {
            popup.style.opacity = "0";
        }
        if (mode !== "Preview") {
            resetModal()
        }
    }, 1000);

});

const backButton = document.getElementById("back-button");
const forwardButton = document.getElementById("forward-button");

backButton.addEventListener("click", e => {
    if (currentImageIndex === 0) {
        return;
    }
    currentImageIndex -= 1;
    setModal(currentImageIndex);
});

forwardButton.addEventListener("click", e => {
    if (currentImageIndex === gallery.childNodes.length - 1) {
        return;
    }
    currentImageIndex += 1;
    setModal(currentImageIndex);
});

function setModal(index) {
    let imageContainer = listOfImages[index];
    let image = imageContainer.childNodes[0];
    modalImage.src = image.src;
    modalProfile.src = image.dataset.profile;
    modalUsername.textContent = image.dataset.user;
    modalImageUploadDate.textContent = image.dataset.postDate;

    if (image.dataset.liked === "true") {
        modalHeart.classList.add("heart-liked");
    } else {
        modalHeart.classList.remove("heart-liked");
    }

    for (const tag of modalTags.childNodes) {
        modalTags.removeChild(tag);
    }

    for (const tag of image.dataset.tags.split(",")) {
        if (tag != "") {
            let tagElement = document.createElement("span");
            tagElement.textContent = tag;
            tagElement.classList.add('tag');
            tagElement.classList.add('modal-tag');
            modalTags.appendChild(tagElement)
        }
    }
}

let columnCount = parseInt(getComputedStyle(gallery)["columnCount"]);
let listOfImages = [];

function addData(dataList) {
    for (const data of dataList) {
        let container = document.createElement("div");
        container.classList.add("gallery-item");

        let image = document.createElement("img");
        image.src = data.attachments[0];
        image.classList.add("gallery-image");
        image.dataset.user = data.author_name;
        image.dataset.profile = `https://cdn.discordapp.com/avatars/${data.author_discord_id}/${data.author_avatar}.png`;
        image.dataset.postDate = data.timestamp;
        image.dataset.liked = data.liked;
        image.dataset.postId = data.id;
        image.dataset.tags = data.tags;

        let imageActions = document.createElement("div");
        imageActions.classList.add("image-actions");

        let heart = document.createElement("div");
        heart.classList.add("heart");
        if (data.liked === "true") {
            heart.classList.add("heart-liked");
        }
        heart.addEventListener("click", (e) => {
            image.dataset.liked = !(image.dataset.liked === "true");
            if (image.dataset.liked === "true") {
                heart.classList.add("heart-liked");
                modalHeart.classList.add("heart-liked");
            } else {
                heart.classList.remove("heart-liked");
                modalHeart.classList.remove("heart-liked");
            }
        });

        image.heart = heart;

        let imageDarknessMask = document.createElement("div");
        imageDarknessMask.classList.add("image-darkness-mask");
        imageDarknessMask.addEventListener("click", e => {
            currentImage = image;
            currentImageIndex = listOfImages.indexOf(container);
            popup.style.opacity = "1";
            popup.style.zIndex = "20";

            modalImage.src = data.attachments[0];
            modalProfile.src = `https://cdn.discordapp.com/avatars/${data.author_discord_id}/${data.author_avatar}.png`;
            modalUsername.textContent = data.author_name;
            modalImageUploadDate.textContent = data.timestamp;

            if (image.dataset.liked === "true") {
                modalHeart.classList.add("heart-liked");
            } else {
                modalHeart.classList.remove("heart-liked");
            }

            for (const tag of data.tags.split(",")) {
                if (tag != "") {
                    let tagElement = document.createElement("span");
                    tagElement.textContent = tag;
                    tagElement.classList.add('tag');
                    tagElement.classList.add('modal-tag');
                    modalTags.appendChild(tagElement)
                }
            }


        });


        imageActions.appendChild(heart);

        container.appendChild(image);
        container.append(imageDarknessMask);
        container.appendChild(imageActions);

        listOfImages.push(container);
    }
    for (let i = 0; i < columnCount; i += 1) {
        for (let j = i; j < listOfImages.length; j += columnCount) {
            gallery.appendChild(listOfImages[j]);
        }
    }
}

window.addEventListener("resize", e => {
    if (parseInt(getComputedStyle(gallery)["columnCount"]) !== columnCount) {
        columnCount = parseInt(getComputedStyle(gallery)["columnCount"])
        for (let i = 0; i < columnCount; i += 1) {
            for (let j = i; j < listOfImages.length; j += columnCount) {
                gallery.appendChild(listOfImages[j]);
            }
        }
    }
})

const searchFilter = document.getElementById("search-filter");
const searchBar = document.getElementById("search-bar");

searchFilter.addEventListener('keydown', function (e) {
    const key = e.key;
    if (key === " ") {
        let text = e.target.value;
        if (text === "" || text === " ") {
            e.target.value = "";
            e.preventDefault();
            return
        }
        let tag = document.createElement("span");
        tag.textContent = text;
        tag.classList.add("tag");
        tag.classList.add("search-bar-tag");

        let removeTag = document.createElement("div");
        removeTag.classList.add("remove-tag");

        removeTag.addEventListener("click", e => {
            searchFilter.removeChild(e.target.parentNode)
        });

        tag.appendChild(removeTag);

        searchFilter.insertBefore(tag, searchBar);
        e.target.value = "";
        e.preventDefault();
    }
    if (key === "Backspace" && e.target.value === "") {
        if (searchFilter.children.length === 1) {
            return
        }
        e.target.value = e.target.previousElementSibling.textContent;
        searchFilter.removeChild(e.target.previousElementSibling);
    }
});

const channelSelect = document.getElementById("channel-select");
const channelSelectText = document.getElementById("channel-select-text");
const channelSelectItems = document.getElementById("channel-select-items");
const channelSelectImage = document.getElementById("channel-select-image");
const selectedChannel = document.getElementById("selected-channel");
channelSelect.addEventListener("click", e => {
    channelSelectItems.classList.toggle("channel-select-items-invisible");
});

let currentChannel = document.querySelector(".current-channel");
currentChannel.addEventListener("click", e => {
    e.target.classList.add("current-channel");
    if (currentChannel !== e.target && currentChannel) {
        currentChannel.classList.remove("current-channel");
    }
    currentChannel = e.target;

    channelSelectText.textContent = e.target.textContent;

    if (selectedChannel.classList.contains("server-option")) {
        selectedChannel.classList.remove("server-option");
        channelSelectImage.src = "";
    }
});

const sentinel = document.getElementById("sentinel");

window.addEventListener("load", (e) => {
    // addData(testData);

    let intersectionObserver = new IntersectionObserver(entries => {


        if (entries[0].intersectionRatio <= 0) {
            return;
        }

        // Load data
        currentPage++;
        fetchData();

    });

    intersectionObserver.observe(sentinel);

    document.querySelectorAll(".channel-list-option").forEach(element => {
        element.addEventListener("click", e => {
            currentChannel.classList.remove("current-channel");
            let selected = document.querySelector("#selected-channel");
            selected.innerHTML = "";
            selected.appendChild(e.currentTarget.cloneNode(true));
            currentChannel = e.currentTarget;
            currentChannel.classList.add("current-channel");
            const newUrlParams = new URLSearchParams();
            let server_id = element.querySelector(".server-id");
            if (server_id != null) {
                newUrlParams.set("server_id", server_id.innerText);
            }
            let channel_id = element.querySelector(".channel-id");
            if (channel_id != null) {
                newUrlParams.set("channel_id", channel_id.innerText);
            }
            window.history.pushState(newUrlParams.toString(), "", window.location.pathname + "?" + newUrlParams.toString());
            currentPage = 0;
            clearGallery();
            fetchData();
        })
    })
    getChannelSelectionFromParams();
    fetchData();
});

function getChannelSelectionFromParams() {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const serverId = urlParams.get('server_id');
    const channelId = urlParams.get('channel_id');
    let channelList = document.querySelector("#channel-select-items").children;
    if (channelId != null) {
        for (const channel of channelList) {
            let idElement = channel.querySelector(".channel-id")
            if (idElement == null) continue;
            let id = idElement.innerText;
            if (id == channelId) {
                document.getElementById("channel-select").click();
                channel.click();
                return;
            }
        }
    }
    if (serverId != null) {
        for (const channel of channelList) {
            let idElement = channel.querySelector(".server-id")
            if (idElement == null) continue;
            let id = idElement.innerText;
            if (id == serverId) {
                document.getElementById("channel-select").click();
                channel.click();
                return;
            }
        }
    }
}

function clearGallery() {
    document.getElementById("gallery").innerHTML = ""
    listOfImages = [];
}

function fetchData() {
    let tags = ""
    document.querySelectorAll(".search-bar-tag").forEach(element => {
        tags += `${element.innerText},`
    })
    let channel_id = currentChannel.querySelector(".channel-id");
    let server_id = currentChannel.querySelector(".server-id");
    fetch("/media?" + new URLSearchParams({
        "channel_id": channel_id == null ? "" : channel_id.innerText,
        "server_id": server_id == null ? "" : server_id.innerText,
        "page": currentPage,
        "mine_mode": current === mine ? 1 : 0,
        "tags": tags,
    }))
        .then(response => response.json()).then(data => {
        if (currentPage === 0) {
        }
        addData(data);
    })
}

