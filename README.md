# 🎾 Favorite Tennis Player (FTP) Match Notifier

#### Video Demo:  <LINK_KA_TVOM_YOUTUBE_SNIMKU>

#### Description:
The **Favorite Tennis Player (FTP) Notifier** is a desktop application designed for tennis enthusiasts who want to be alerted the moment their favorite players start a match. Built with Python, this tool combines a modern GUI, web scraping, and real-time notifications to ensure you never miss a serve.

### 🌟 Key Features
* **Real-time Scraping:** Uses Selenium to monitor live scores and match schedules.
* **Multithreaded Architecture:** The bot runs in a background thread, keeping the GUI responsive.
* **Dynamic Player Management:** Add or remove players from your "Following List" without restarting the application.
* **System Tray Integration:** Minimize the app to the system tray (beside the clock) to keep it running discreetly in the background.
* **Graceful Shutdown:** Implements protocols to safely stop background processes when the application is closed.

### 🛠 Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** `customtkinter` (Modern UI)
- **Automation/Scraping:** `selenium` & `webdriver-manager`
- **Background Tasks:** `threading`
- **System Tray:** `pystray` & `Pillow`
- **Environment:** `python-dotenv` for sensitive information.

### 📁 File Structure
- **`interface.py`**: The main entry point of the application. It contains the `TennisApp` class, defines the modern GUI using `customtkinter`, and manages the system tray integration.
- **`ftp.py`**: Acts as the central state manager. It holds the shared list of target players and coordinates the communication between the UI and the background bot.
- **`scraper.py`**: The engine of the project. It contains the Selenium-based logic for web scraping, match detection, and real-time data extraction from tennis websites.
- **`test_ftp.py`**: The testing suite designed for `pytest`. It ensures that data validation, player list management, and core logic functions work as expected.
- **`emailpass.env`**: A secure configuration file used to store sensitive credentials (like email app passwords) without hardcoding them into the scripts.
- **`requirements.txt`**: A comprehensive list of all third-party Python libraries needed to run the project.
- **`icon.ico`**: The visual asset used for the application's window icon and the system tray notification area.
- **`.gitignore`**: Ensures that temporary files (`__pycache__`) and sensitive data (`emailpass.env`) are not tracked by version control.

### 🚀 Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone <'private for now'>

----------------------------------
## 🚀 Future Roadmap (V2 Ideas)

Since this is a private project, I am planning to implement the following features in the next major update:

### 💾 1. Data Persistence (JSON Storage)
- **Current State:** User has to re-enter the email and player list every time the app starts.
- **V2 Goal:** Implement a `config.json` file to automatically save and load the user's email and the "Following List". This will provide a much smoother user experience.

### ⚙️ 2. Run on Startup
- **V2 Goal:** Add an option in the settings to allow the application to launch automatically when Windows starts. 
- **Implementation:** The app will minimize directly to the System Tray upon startup, ensuring the bot starts monitoring matches without any user intervention.

### 🔔 3. Native Desktop Notifications
- **V2 Goal:** Supplement email alerts with native Windows desktop notifications (toasts) for immediate feedback while the user is active on the computer.

### 🌑 4. Theme Switcher
- **V2 Goal:** Add a toggle between Light and Dark mode within the UI, saved via the JSON configuration.