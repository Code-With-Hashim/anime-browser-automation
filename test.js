const puppeteer = require('puppeteer');

async function verifyTabOpen(page) {
    try {
        const currentUrl = await page.url();
        console.log('Current URL:', currentUrl);
        return true;
    } catch (error) {
        console.log(`Error: ${error}`);
        return false;
    }
}

async function main() {
    const args = [
        '--disable-extensions',  // Disable Chrome extensions
        '--no-sandbox',  // Needed for running in EC2
        '--disable-infobars',  // Disable infobars
        '--disable-gpu',  // Disable GPU acceleration
        // '--headless',  // Uncomment if running in headless mode
    ];

    const browser = await puppeteer.launch({
        headless: false,  // Set to true if you want to run in headless mode
        args: args,
        defaultViewport: null,
    });

    const page = await browser.newPage();
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36");

    // Open the URL and wait for the page to load
    await page.goto("https://modijiurl.com/fBUFTv", { waitUntil: 'networkidle2' });

    // Handle potential tab opening
    const pages = await browser.pages();  // Get all open tabs
    for (let tab of pages) {
        const url = await tab.url();
        if (url.includes("modijiurl.com")) {
            await tab.bringToFront();  // Switch to the correct tab
            break;
        }
    }

    // If the verify button exists, click it
    const verifyButton = await page.$('input[value*="Verify"]');
    if (verifyButton) {
        await verifyButton.click();
        console.log('clickable');
    }

    // Verify the current URL and tab status
    if (await verifyTabOpen(page)) {

        await delayFnc(10000)
        // await page.waitFor(10000);  // Wait to make sure the page is loaded
        console.log('Final URL:', await page.url());
    } else {
        console.log('The browser window was closed or not accessible.');
    }

    await browser.close();
}

async function delayFnc(ms) {
    return new Promise((resolve , reject) => {
        setTimeout(()=> {
            resolve()
        }, ms)
    })
}
main().catch(console.error);
