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

    function getTextByXPath(xpath) {
        try {
            const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            return result ? result.textContent.trim() : "Not found";
        } catch (error) {
            console.error("Error finding element by XPath:", xpath, error);
            return "Not found";
        }
    }

    function cleanJobURL(url) {
        try {
            // Trim LinkedIn job URLs to remove tracking parameters
            const match = url.match(/(https:\/\/www\.linkedin\.com\/jobs\/view\/\d+)/);
            return match ? match[1] + "/" : url; // Keep only the base job URL
        } catch (error) {
            console.error("Error trimming job URL:", error);
            return url;
        }
    }

    function extractJobDetails() {
        try {
            const jobTitle = getText(["h1.t-24.t-bold.inline"]);

            const company = getText([
                "div.job-details-jobs-unified-top-card__company-name a", // Primary company selector
                "a[data-test-app-aware-link]" // Alternate selector
            ]) || getTextByXPath("//div[contains(@class, 'job-details-jobs-unified-top-card__company-name')]//a");

            const location = getText([
                "span.tvm__text.tvm__text--low-emphasis", // Primary location selector
                "span.job-details-jobs-unified-top-card__bullet", // Alternate location selector
                "div.t-black--light.mt2 span.tvm__text.tvm__text--low-emphasis" // New location selector based on your screenshot
            ]) || getTextByXPath("//div[contains(@class, 'job-details-jobs-unified-top-card__primary-description-container')]//span[contains(@class, 'tvm__text--low-emphasis')]");

            const rawURL = window.location.href;
            const url = cleanJobURL(rawURL); // Trim the job URL

            console.log("Extracted Data:", { jobTitle, company, location, url });

            if (jobTitle !== "Not found" || company !== "Not found" || location !== "Not found") {
                chrome.runtime.sendMessage({ jobTitle, company, location, url });
            } else {
                console.warn("Some job details were not found. Retrying...");
                setTimeout(extractJobDetails, 2000); // Retry after 2 seconds
            }
        } catch (error) {
            console.error("Error extracting job details:", error);
        }
    }

    // Run immediately when injected
    extractJobDetails();
})();
