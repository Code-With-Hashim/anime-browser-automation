// const puppeteer = require('puppeteer');
const { executablePath } = require('puppeteer');
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

async function waitFor(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

async function simulateMouseMovements(page) {
    const width = 1920;
    const height = 1080;

    // Simulate some random mouse movements
    for (let i = 0; i < 10; i++) {
        const randomX = Math.floor(Math.random() * width);
        const randomY = Math.floor(Math.random() * height);
        await page.mouse.move(randomX, randomY);
        await waitFor(100)
        // await page.waitForTimeout(100); // Random delay between movements
    }

    // Perform a click on a specific element
    const button = await page.$('selector-for-click'); // Replace with your button selector
    if (button) {
        await button.click();
    }
}

async function publicEarnFormByPass(page, id) {
    try {
        // Set the display of the element to 'block'
        await page.evaluate((elementId) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.style.display = 'block';
            }
        }, id);

        // Wait for the element to be present in the DOM
        await page.waitForSelector(`#${id}`, { timeout: 10000 });
        
        // Find the button element and click it
        await page.click(`#${id}`);

        // Wait until the body is present on the new page
        await page.waitForSelector('body', { timeout: 10000 });

        simulateMouseMovements(page)
    } catch (e) {
        console.log('Form is not found:', e);
    }
}

async function main(link, search, eps) {
    const PROXY = 'http://36.94.232.177:3113';
    
    // Launch browser with proxy settings
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: executablePath(),
        args: [

            '--no-sandbox',


            '--disable-notifications',

            '--disable-dev-shm-usage',

        ],
    });
    
    const page = await browser.newPage();
    
    try {
        // Open the provided link
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')
        await page.goto(link, { timeout: 60000 });

        // Get anime cards
        const animeCards = await page.$$('.herald-post-thumbnail');

        for (const animeCard of animeCards) {
            try {
                const anchorTg = await animeCard.$('a');
            const title = await anchorTg.evaluate(el => el.getAttribute('title'));
            const href = await anchorTg.evaluate(el => el.getAttribute('href'));
            console.log(title);

            if (title.includes(search)) {
                await anchorTg.click();
                console.log('open-link');

                await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 60000 });

                const linkHtml = await page.$('#pryc-wp-acctp-original-content');
                if (!linkHtml) {
                    console.log('Content not found!');
                    continue;
                }

                const pLists = await linkHtml.$$('p');

                // print(pLists)
                for (let pIndex = 0; pIndex < pLists.length; pIndex++) {
                    try {
                        const strongTag = await pLists[pIndex].$('strong');
                        const titleText = await strongTag.evaluate(el => el.innerText);
                        const link = await pLists[pIndex + 2].$('a');
                        if (!link) continue; // Skip if link is not found

                        const linkPart = await link.evaluate(el => el.innerHTML);
                        console.log(titleText, eps, linkPart);

                        const titleWords = titleText.split(" ");
                        if (titleWords.some(word => eps.includes(word)) && linkPart === 'Mir') {
                            console.log("GOES IN");
                            await link.click();
                            
                            console.log('LINK CLICK')
                            await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 60000 });
                            console.log('wait completed')

                            const linkBtn = await page.$('.btn-success');
                            if (!linkBtn) {
                                console.log('Button not found');
                                continue;
                            }
                            
                            const clickLink = await linkBtn.evaluate(el => el.getAttribute('href'));
                            console.log(clickLink)
                            if (clickLink.includes("https://publicearn.com")) {
                                console.log('isExists')
                                await linkBtn.click();
                                await waitFor(10000)
                                console.log('wait is done')
                                // await page.waitForTimeout(1000); // Wait for new tab to open

                                const pages = await browser.pages();
                                const newPage = pages[pages.length - 1]; // Get the newly opened tab

                                await newPage.waitForSelector('body');

                                const urlPattern = /window\.location\.href\s*=\s*"(https?:\/\/.*?)"/;
                                const pageContent = await newPage.content();

                                console.log(pageContent);
                                const match = pageContent.match(urlPattern);
                                
                                    // Call the bypass function
                                    await publicEarnFormByPass(newPage, 'tp98');
                                    await publicEarnFormByPass(newPage, 'btn6');
                                    await publicEarnFormByPass(newPage, 'tp98');

                                    
                                    await waitFor(160000)

                                    // await newPage.waitForTimeout(10000); // Wait for some time
                                    await newPage.screenshot({ path: 'test.png' });
                                    console.log(await newPage.content());
                               
                            } else {
                                console.log("NOT PUBLIC", clickLink);
                            }
                        }
                    } catch (e) {
                        console.log("Error processing p tag:");
                    }
                }
            }
            } catch (error) {
                console.log('error')
            }
        }
    } catch (e) {
        console.error('Error in main function:', e);
    } finally {
        // Close the browser when done
        await browser.close();
    }
}

// Usage example
const link = 'https://tpxsub.com/'; // Provide the link
const search = 'Tower of God'; // Provide the search term
const eps = '15'; // Provide the eps term
main(link, search, eps);
