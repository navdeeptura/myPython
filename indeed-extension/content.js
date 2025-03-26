(function() {
    function getText(selectors) {
        for (let selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.innerText.trim()) {
                return element.innerText.trim();
            }
        }
        return "Not found";
    }

    function cleanLocation(locationText) {
        if (locationText.includes("\n")) {
            return locationText.split("\n")[0].trim(); // Take only the first line (City, Province)
        }
        return locationText;
    }

    function cleanJobURL(url) {
        try {
            const match = url.match(/(https:\/\/ca\.indeed\.com\/viewjob\?jk=[a-zA-Z0-9]+)/);
            return match ? match[1] : url; // Keep only the base job URL
        } catch (error) {
            console.error("Error trimming job URL:", error);
            return url;
        }
    }

    function extractJobDetails() {
        try {
            const jobTitle = getText(["h2[data-testid='simpler-jobTitle']"]);
            
            // Check for primary company selector first, if not found, use alternate selector
            let company = getText(["a.jobsearch-JobInfoHeader-companyNameLink"]);
            if (company === "Not found") {
                company = getText(["span.jobsearch-JobInfoHeader-companyNameSimple"]);
            }

            let location = getText(["div.css-xb6x8x.e37uo190"]);
            location = cleanLocation(location); // Trim location text

            const rawURL = window.location.href;
            const url = cleanJobURL(rawURL); // Trim the job URL

            console.log("Extracted Data:", { jobTitle, company, location, url });

            if (jobTitle !== "Not found" || company !== "Not found" || location !== "Not found") {
                chrome.runtime.sendMessage({ jobTitle, company, location, url });
            } else {
                console.warn("Some job details were not found. Retrying...");
                setTimeout(extractJobDetails, 2000);
            }
        } catch (error) {
            console.error("Error extracting job details:", error);
        }
    }

    extractJobDetails();
})();
