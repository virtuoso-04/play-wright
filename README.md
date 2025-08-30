# IDEN Product Dashboard Scraper

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Playwright](https://img.shields.io/badge/Playwright-1.30+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

</div>

A sophisticated web scraper built with Playwright that automates the extraction of product data from the IDEN challenge dashboard. This tool elegantly handles authentication, session management, and efficiently extracts product information from lazy-loaded cards through infinite scrolling.

## � Features

- **Robust Authentication** - Secure login with credential management through environment variables
- **Persistent Sessions** - Smart cookie and storage state management to avoid repeated logins
- **Infinite Scroll Handling** - Dynamic content loading with intelligent scroll detection
- **Resilient Element Selection** - Multi-strategy element targeting with graceful fallbacks
- **Structured Data Extraction** - Clean parsing of product cards into well-organized JSON
- **Professional Logging** - Real-time progress tracking with clear, timestamped output
- **Error Recovery** - Graceful handling of network issues and unexpected page structures

## �️ Requirements

- Python 3.7+
- Playwright
- python-dotenv

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/iden-product-scraper.git
   cd iden-product-scraper
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install playwright python-dotenv
   ```

4. **Install Playwright browsers**:
   ```bash
   python -m playwright install chromium
   ```

## ⚙️ Configuration

1. **Create a `.env` file** in the project root:
   ```env
   EMAIL=your-email@example.com
   PASSWORD=your-password
   ```

2. **Adjust scraping parameters** (optional):
   
   Open `main.py` and modify the configuration constants:
   ```python
   MAX_PRODUCTS = 3751  # Maximum products to extract
   ```

## � Usage

Run the scraper with:

```bash
python main.py
```

The script will:
1. Attempt to use a saved session if available
2. Otherwise, perform authentication with provided credentials
3. Navigate through the challenge steps
4. Extract all product data with intelligent infinite scrolling
5. Save results to `products.json`

## � Data Format

The extracted data is saved as a structured JSON array:

```json
[
  {
    "name": "Essential Beauty Plus",
    "id": "0",
    "description": "A affordable, efficient...",
    "weight": "14.75", 
    "category": "Beauty"
  },
  ...
]
```

## 🧰 Implementation Details

### Authentication Flow

The script implements a robust authentication workflow:

1. **Cookie Management** - Checks for existing sessions before attempting login
2. **Form Submission** - Securely submits login credentials
3. **Navigation Handling** - Intelligently navigates through multi-step process

### Product Extraction

Product data is extracted using a sophisticated approach:

1. **Grid Detection** - Uses multiple selector strategies to identify the product grid
2. **Card Parsing** - Extracts structured data from each product card
3. **Infinite Scrolling** - Monitors page height changes to detect when all content is loaded
4. **Duplicate Prevention** - Uses set-based deduplication for product IDs

### Error Handling

The script implements comprehensive error handling:

1. **Selector Fallbacks** - Multiple selector strategies for each element
2. **Navigation Recovery** - Graceful handling of unexpected navigation paths
3. **Timeout Management** - Smart waiting for network stability and element visibility
4. **Diagnostic Logging** - Detailed error reporting with optional screenshots

##  Troubleshooting

### Common Issues

1. **Login Failures**:
   - Verify credentials in `.env` file
   - Check internet connection
   - Delete `session.json` to force re-authentication

2. **Missing Products**:
   - Increase `MAX_PRODUCTS` limit
   - Check if website structure has changed
   - Verify CSS selectors are still valid

3. **Browser Issues**:
   - Run `python -m playwright install chromium` again
   - Delete `userdata` folder to reset browser state

### Debug Mode

To run headlessly (for production):
```python
context = p.chromium.launch_persistent_context(
    user_data_dir,
    headless=True  # Change to True for production
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📮 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">
  <sub>Built with ❤️ by Anant Sharma</sub>
</div>
