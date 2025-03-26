document.addEventListener("DOMContentLoaded", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length === 0) return;

        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"]
        });
    });
});

chrome.runtime.onMessage.addListener((message) => {
    if (message.jobTitle) {
        document.getElementById("jobTitle").innerText = message.jobTitle;
        document.getElementById("company").innerText = message.company;
        document.getElementById("location").innerText = message.location;
        document.getElementById("jobURL").href = message.url;
        document.getElementById("jobURL").innerText = message.url;

        const jobDetails = `Job Title: ${message.jobTitle}\nCompany: ${message.company}\nLocation: ${message.location}\nJob URL: ${message.url}`;

        // **Automatically copy job details to clipboard**
        navigator.clipboard.writeText(jobDetails).then(() => {
            console.log("Job details copied to clipboard automatically!");

            const notification = document.createElement("p");
            notification.innerText = "Copied to clipboard! Closing...";
            notification.style.color = "green";
            notification.style.fontWeight = "bold";
            notification.style.textAlign = "center";
            document.body.appendChild(notification);

            // Close the popup after 2 seconds
            setTimeout(() => {
                window.close();
            }, 2000);
        }).catch(err => {
            console.error("Failed to copy text: ", err);
        });
    }
});
