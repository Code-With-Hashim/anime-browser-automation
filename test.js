
const { connect } = require("puppeteer-real-browser")

async function test() {

    const { browser, page } = await connect({

        headless: false,

        args: [],

        customConfig: {},

        turnstile: true,

        connectOption: {},

        disableXvfb: false,
        ignoreAllFlags: false
        // proxy:{
        //     host:'<proxy-host>',
        //     port:'<proxy-port>',
        //     username:'<proxy-username>',
        //     password:'<proxy-password>'
        // }

    })
    await page.goto('https://modijiurl.com/fBUFTv')

    await dealy(20000)
    const currentUrl = page.url();
    console.log('Current URL:', currentUrl);
    console.log(await page.content())

    page.close()

}

async function dealy(ms) {
    return new Promise((resolve , reject) => {
        setTimeout(() => {
           resolve() 
        }, ms);
    })
}

test()