# IDEN Product Dashboard Scraper

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.30+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

An intelligent web scraper designed to help you extract product data from the IDEN challenge dashboard with ease. Built with Playwright, this tool takes care of all the heavy lifting - from logging in to scrolling through thousands of products - so you don't have to.

## What This Tool Does

- **Smart Login** - Remembers your login session so you don't have to enter credentials every time
- **Handles Lazy Loading** - Automatically scrolls and waits for all products to load
- **Intelligent Element Detection** - Uses multiple strategies to find page elements, even if the website changes
- **Clean Data Export** - Organizes all product information into a neat JSON file
- **Real-time Progress** - Shows you exactly what's happening as it works
- **Error Recovery** - Gracefully handles network hiccups and unexpected page changes

## What You'll Need

- Python 3.7 or newer
- A working internet connection
- Your IDEN challenge login credentials

## Getting Started

### 1. Download the Code

```bash
git clone https://github.com/virtuoso-04/play-wright.git
cd play-wright
```

### 2. Set Up Your Environment (Recommended)

This keeps everything clean and organized:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install What You Need

```bash
pip install playwright python-dotenv
python -m playwright install chromium
```

### 4. Add Your Login Details

Create a file called `.env` in the project folder and add:

```env
EMAIL=your-email@example.com
PASSWORD=your-actual-password
```

Don't worry - this file stays on your computer and won't be shared.

## Running the Scraper

It's as simple as:

```bash
python main.py
```

The scraper will:
1. Check if you have a saved login session (saves time!)
2. If not, log you in automatically
3. Navigate through the challenge interface
4. Scroll through all the products and extract their data
5. Save everything to a `products.json` file

## What You'll Get

Your data will be saved as a clean JSON file like this:

```json
[
  {
    "name": "Essential Beauty Plus",
    "id": "0",
    "description": "A affordable, efficient...",
    "weight": "14.75", 
    "category": "Beauty"
  }
]
```

## How It Works Under the Hood

### Smart Authentication
The tool remembers your login using browser cookies, so you won't need to log in every time you run it.

### Intelligent Product Extraction
It uses multiple strategies to find products on the page, making it resilient to website changes. The scraper automatically:
- Detects the product grid layout
- Scrolls to load all products (even with thousands of items)
- Extracts clean, structured data from each product card
- Prevents duplicate entries

### Built-in Error Handling
If something goes wrong, the scraper:
- Tries alternative methods to find page elements
- Takes screenshots for debugging
- Continues working even if some products can't be processed
- Provides clear error messages

## Troubleshooting

### If Login Isn't Working
- Double-check your credentials in the `.env` file
- Make sure you have internet access
- Delete the `session.json` file to force a fresh login

### If You're Missing Products
- Increase the `MAX_PRODUCTS` number in `main.py`
- The website might have changed - check if the scraper needs updates

### If the Browser Won't Start
- Run `python -m playwright install chromium` again
- Delete the `userdata` folder and try again

### Running in the Background
For production use, you can run it without the browser window:

```python
# Change this line in main.py
headless=True  # Instead of False
```

## Contributing

Found a bug or have an idea to make this better? I'd love your help! Feel free to:
- Open an issue to report problems
- Submit a pull request with improvements
- Share your feedback

## License

This project is open source under the MIT License - feel free to use it however you'd like.

## Questions?

If you run into any issues or have questions, just open an issue on GitHub and I'll help you out.

---

<div align="center">
  <sub>Created with care by Anant Sharma</sub>
</div>
