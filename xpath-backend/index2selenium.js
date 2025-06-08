// const express = require('express');
// const puppeteer = require('puppeteer');
// const cors = require('cors');

// const app = express();
// app.use(cors());
// app.use(express.json());

// // In-memory storage for XPaths keyed by URL
// const urlToXpaths = {};

// app.post('/extract-xpaths', async (req, res) => {
//   const { url } = req.body;

//   if (!url) return res.status(400).json({ error: 'URL is required' });

//   try {
//     const browser = await puppeteer.launch({ headless: 'new' });
//     const page = await browser.newPage();
//     await page.goto(url, { waitUntil: 'networkidle2' });

//     const xpaths = await page.evaluate(() => {
//       const elements = document.querySelectorAll('input, textarea, button');
//       const getXPath = (element) => {
//         if (element.id) return `//*[@id="${element.id}"]`;
// 		console.log(element.id);
//         const path = [];
//         while (element && element.nodeType === Node.ELEMENT_NODE) {
//           let index = 1;
//           let sibling = element.previousSibling;
//           while (sibling) {
//             if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) index++;
//             sibling = sibling.previousSibling;
//           }
//           path.unshift(`${element.nodeName.toLowerCase()}[${index}]`);
//           element = element.parentNode;
//         }
//         return '/' + path.join('/');
//       };

//       return Array.from(elements).map(el => ({
//         tag: el.tagName,
//         xpath: getXPath(el),
//         name: el.name || '',
//         placeholder: el.placeholder || '',
//       }));
//     });

//     await browser.close();

//     // Store the xpaths by url
//     urlToXpaths[url] = xpaths;

//     // Respond with success only
//     res.json({ message: 'XPaths extracted and stored successfully' });
//   } catch (err) {
//     console.error(err);
//     res.status(500).json({ error: 'XPath extraction failed' });
//   }
// });

// // Optional: Endpoint to get stored xpaths for a URL
// app.get('/xpaths', (req, res) => {
//   const { url } = req.query;
//   if (!url || !urlToXpaths[url]) {
//     return res.status(404).json({ error: 'XPaths not found for this URL' });
//   }
//   res.json({ xpaths: urlToXpaths[url] });
// });

// app.listen(5000, () => console.log('Server running on http://localhost:5000'));
