const all = document.getElementById("all");
const mine = document.getElementById("mine");
const favs = document.getElementById("favs");
let current = all;
let currentImage;
let currentImageIndex;
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

modalSearchTag.addEventListener('keydown', function(e) {
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
        let tagElement = document.createElement("span");
        tagElement.textContent = tag;
        tagElement.classList.add('tag');
        tagElement.classList.add('modal-tag');
        modalTags.appendChild(tagElement)
    }
}

let columnCount = parseInt(getComputedStyle(gallery)["columnCount"]);
let listOfImages = [];
function addData(dataList) {
    for (const data of dataList) {
        let container = document.createElement("div");
        container.classList.add("gallery-item");

        let image = document.createElement("img");
        image.src = data.image;
        image.classList.add("gallery-image");
        image.dataset.user = data.user;
        image.dataset.profile = data.profile;
        image.dataset.postDate = data.postDate;
        image.dataset.liked = data.liked;
        image.dataset.postId = data.postId;
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

            modalImage.src = data.image;
            modalProfile.src = data.profile;
            modalUsername.textContent = data.user;
            modalImageUploadDate.textContent = data.postDate;
            
            if (image.dataset.liked === "true") {
                modalHeart.classList.add("heart-liked");
            } else {
                modalHeart.classList.remove("heart-liked");
            }

            for (const tag of data.tags.split(",")) {
                let tagElement = document.createElement("span");
                tagElement.textContent = tag;
                tagElement.classList.add('tag');
                tagElement.classList.add('modal-tag');
                modalTags.appendChild(tagElement)
            }

            
        });


        imageActions.appendChild(heart);

        container.appendChild(image);
        container.append(imageDarknessMask);
        container.appendChild(imageActions);

        listOfImages.push(container);
    }
    for (let i = 0; i < columnCount; i+=1) {
        for (let j = i; j < listOfImages.length; j += columnCount) {
            gallery.appendChild(listOfImages[j]);
        }
    }
}

window.addEventListener("resize", e => {
    if (parseInt(getComputedStyle(gallery)["columnCount"]) !== columnCount) {
        columnCount = parseInt(getComputedStyle(gallery)["columnCount"])
        for (let i = 0; i < columnCount; i+=1) {
            for (let j = i; j < listOfImages.length; j += columnCount) {
                gallery.appendChild(listOfImages[j]);
            }
        }
    }
})

const searchFilter = document.getElementById("search-filter");
const searchBar = document.getElementById("search-bar");

searchFilter.addEventListener('keydown', function(e) {
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


function addChannels(channels) {
    for (const [server, serverData] of Object.entries(channels)) {
        let serverOption = document.createElement("div");
        let serverName = document.createElement("span");
        let serverImage = document.createElement("img");
        serverImage.src = serverData.serverImage;
        serverImage.classList.add("server-image");
        serverName.textContent = server;
        serverOption.classList.add("server-option");
        serverOption.classList.add("channel-list-option");
        serverOption.appendChild(serverImage);
        serverOption.appendChild(serverName);
        serverOption.addEventListener("click", e => {
            e.target.classList.add("current-channel");
            if (currentChannel !== e.target && currentChannel) {
                currentChannel.classList.remove("current-channel");
            }
            currentChannel = e.target;

            channelSelectText.textContent = e.target.textContent;
            selectedChannel.classList.add("server-option");
            channelSelectImage.src = serverData.serverImage;
        });

        channelSelectItems.appendChild(serverOption);
        let serverChannels = serverData.channels;
        for (const channel of serverChannels) {
            let channelOption = document.createElement("div");
            let channelName = document.createElement("span");
            channelName.textContent = channel;
            channelOption.classList.add("channel-option");
            channelOption.classList.add("channel-list-option");
            channelOption.appendChild(channelName);
            channelOption.addEventListener("click", e => {
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

            channelSelectItems.appendChild(channelOption);
        }
    }
}

window.addEventListener("load", (e) => {
    // Todo: Implement get data and channels
    addData(testData);
    addChannels(testChannels)
});

// Test data below

const testData = [
    {
        image:
        "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187.jpg",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: true,
        postId: 1,
    },
    {
        image:
        "https://www.humanesociety.org/sites/default/files/styles/400x400/public/2018/06/cat-217679.jpg",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: false,
        postId: 2,
    },
    {
        image:
        "https://www.usatoday.com/gcdn/authoring/authoring-images/2023/11/02/USAT/71425480007-getty-images-1498838344.jpg?crop=1060,1413,x530,y0",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4,tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: false,
        postId: 3,
    },
    {
        image:
        "https://www.alleycat.org/wp-content/uploads/2015/12/RS34996_BuenaVistaColony_1518.jpg",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: false,
        postId: 4,
    },
    {
        image:
        "https://cats.com/wp-content/uploads/2024/02/96E4B546-9BE7-4977-9A29-05F2D9BB47BC_1_102_a-e1711411797978.jpeg",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: true,
        postId: 5,
    },
    {
        image:
        "https://static.scientificamerican.com/sciam/cache/file/2AE14CDD-1265-470C-9B15F49024186C10_source.jpg",
        user: "Username",
        profile:
        "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        tags: "tag1,tag2,tag3,tag4",
        postDate: "21/07/2024",
        liked: false,
        postId: 6,
    },
];

let testChannels = {
    "Server 1": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        channels: [
            "# CH",
            "# CH2",
        ],
    },
    "Server 2": {
        serverImage: "https://pyxis.nymag.com/v1/imgs/a59/8f2/af4ffa51c4bbd612e05e8a0f26cba27f5c-shrek.rsquare.w400.jpg",
        channels: [
            "# Images",
            "# Videos",
        ],
    }
}