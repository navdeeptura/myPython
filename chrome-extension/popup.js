document.addEventListener("DOMContentLoaded", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length === 0) return;

        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"]
        });
    });
});

document.getElementById("extract").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length === 0) return;

        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"]
        });
    });
});

document.getElementById("copy").addEventListener("click", () => {
    const jobTitle = document.getElementById("jobTitle").innerText;
    const company = document.getElementById("company").innerText;
    const location = document.getElementById("location").innerText;
    let jobURL = document.getElementById("jobURL").href;

    // Trim job URL to remove tracking parameters
    jobURL = cleanJobURL(jobURL);

    const jobDetails = `Job Title: ${jobTitle}\nCompany: ${company}\nLocation: ${location}\nJob URL: ${jobURL}`;

    navigator.clipboard.writeText(jobDetails).then(() => {
        // Show a temporary notification inside the popup
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
});

chrome.runtime.onMessage.addListener((message) => {
    if (message.jobTitle) {
        document.getElementById("jobTitle").innerText = message.jobTitle;
        document.getElementById("company").innerText = message.company;
        document.getElementById("location").innerText = message.location;
        
        // Trim the received job URL
        const cleanedJobURL = cleanJobURL(message.url);
        document.getElementById("jobURL").href = cleanedJobURL;
        document.getElementById("jobURL").innerText = cleanedJobURL;

        // Format job details for copying
        const jobDetails = `Job Title: ${message.jobTitle}\nCompany: ${message.company}\nLocation: ${message.location}\nJob URL: ${cleanedJobURL}`;

        // Automatically copy to clipboard
        navigator.clipboard.writeText(jobDetails).then(() => {
            console.log("Job details copied to clipboard automatically!");
        }).catch(err => {
            console.error("Failed to copy text: ", err);
        });
    }
});

// Function to clean job URL and remove tracking parameters
function cleanJobURL(url) {
    try {
        let jobID = null;

        // Case 1: Extract job ID from a direct job view page
        let match = url.match(/https:\/\/www\.linkedin\.com\/jobs\/view\/(\d+)/);
        if (match) {
            jobID = match[1];
        }

        // Case 2: Extract job ID from search page (e.g., currentJobId=4173118763)
        match = url.match(/[?&]currentJobId=(\d+)/);
        if (!jobID && match) {
            jobID = match[1];
        }

        return jobID ? `https://www.linkedin.com/jobs/view/${jobID}` : url;
    } catch (error) {
        console.error("Error trimming job URL:", error);
        return url;
    }
}
