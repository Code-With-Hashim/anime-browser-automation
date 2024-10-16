const puppeteer = require('puppeteer');
const axios = require('axios');

// Constants
const SCRAPOPS_API_KEY = "fd2d0dcd-c9d7-47ff-ba7c-1be8a63f5df4";
const user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36";

// Verify success by checking for the presence of a specific element
async function verifySuccess(page) {
    try {
        await page.waitForSelector('img[alt="Logo Assembly"]', { timeout: 4000 });
        await page.waitForTimeout(3000); // Sleep for 3 seconds
    } catch (error) {
        console.error("Verification failed: ", error);
    }
}

// Main function using Puppeteer
async function main(link, search, eps) {
    // Launch the Puppeteer browser
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    // Navigate to the specified link
    await page.goto(link);

    // Retrieve all anime cards
    const animeCards = await page.$$('.herald-post-thumbnail');

    // Iterate over each anime card
    for (const animeCard of animeCards) {
        // Get the title element and its text
        const titleElement = await animeCard.$('a[title]');
        const title = await page.evaluate(el => el.textContent, titleElement);
        const animeLink = await page.evaluate(el => el.href, titleElement);
        
        console.log(title); // Log the title of the anime

        // Check if the title includes the search term
        if (title.includes(search)) {
            await animeCard.click(); // Click on the anime card
            await page.waitForSelector('#pryc-wp-acctp-original-content', { timeout: 10000 });

            // Get the HTML content for the selected anime
            const linkHtml = await page.$('#pryc-wp-acctp-original-content');
            const pLists = await linkHtml.$$('p'); // Get all <p> elements

            // Iterate over the <p> elements
            for (let pIndex = 0; pIndex < pLists.length; pIndex++) {
                const strongElement = await pLists[pIndex].$('strong');
                if (strongElement) {
                    const titleText = await page.evaluate(el => el.textContent, strongElement);
                    const linkElement = await pLists[pIndex + 2]?.$('a'); // Use optional chaining to prevent errors
                    
                    if (linkElement) {
                        const linkPart = await page.evaluate(el => el.textContent, linkElement);
                        
                        console.log(titleText, eps, linkPart); // Log relevant information
                        
                        // Split the title into words and check for the episode
                        const titleWords = titleText.split(" ");
                        if (titleWords.some(word => !isNaN(word) && parseInt(word) === eps) && linkPart === 'Mir') {
                            console.log("GOES IN");
                            await linkElement.click(); // Click the link if conditions are met
                            // Add any additional logic for this link here...
                        }
                    }
                }
            }
        }
    }

    await browser.close(); // Close the browser when done
}

async function publicEarnFormByPass(page, id) {
    try {
        await page.evaluate(id => {
            const ads = document.getElementById('SoumyaHelp-Ads');
            if (ads) ads.remove();
            const footerAds = document.getElementById('BR-Footer-Ads');
            if (footerAds) footerAds.remove();
            document.getElementById(id).style.display = 'block';
        }, id);

        const continueClick = await page.$(`#${id}`);
        console.log('findit', await continueClick.evaluate(el => el.outerHTML));

        try {
            await continueClick.click();
        } catch (error) {
            console.error('error', error);
        }

        await page.waitForSelector('body', { timeout: 10000 });
        console.log(await page.url());
    } catch (error) {
        console.error('form is not found', id);
    }
}

async function testProxy() {
    const response = await axios.get('https://proxy.scrapeops.io/v1/', {
        params: {
            api_key: SCRAPOPS_API_KEY,
        },
    });

    if (response.status === 200) {
        const proxyData = response.data;
        console.log(proxyData); // This will print the list of proxies you can use
    } else {
        console.error(`Failed to retrieve proxies: ${response.status}, ${response.data}`);
    }
}

// Example usage
(async () => {
    await main('https://tpxsub.com/', 'Demon Lord 2099', 1);
})();
