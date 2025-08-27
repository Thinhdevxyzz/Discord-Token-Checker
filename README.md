# Discord Token Checker
Overview
This Python script is designed to check the validity of Discord tokens by interacting with the Discord API. It verifies whether tokens are valid, invalid, locked, or require verification, and organizes the results into separate files. The script supports proxy usage for anonymity and includes a colorful console interface with ASCII art for a better user experience.
Features

Token Validation: Checks Discord tokens by making API requests to determine their status (valid, invalid, locked, or requiring verification).
Proxy Support: Loads and validates proxies from a file to anonymize requests.
Multi-threading: Processes tokens in parallel using multiple threads for faster execution.
User Simulation: Mimics real user behavior by sending requests to various Discord endpoints to avoid detection.
Result Logging: Saves results to separate files (valid_tokens.txt, invalid_tokens.txt, locked_tokens.txt, verified_tokens.txt) in the data directory.
Customizable Delays: Includes configurable delays to handle rate limits and avoid bans.
Console UI: Displays a colorful menu and ASCII art, with centered text output based on terminal size.

Prerequisites
To run this script, you need Python 3.6+ and the following dependencies.
Required Libraries
Install the required Python libraries using pip:
pip install requests tls_client pystyle colorama


requests: For making HTTP requests to the Discord API.
tls_client: For advanced HTTP client functionality with TLS fingerprinting to mimic browser behavior.
pystyle: For colorful and styled console output.
colorama: For cross-platform colored terminal text.

Input Files

input/tokens.txt: A text file containing Discord tokens (one per line) to be checked.
input/proxies.txt: (Optional) A text file containing proxies in the format host:port or username:password@host:port (one per line).

Ensure these files are created in the input directory before running the script.
Usage

Prepare Input Files:

Create an input directory in the same directory as the script.
Add your Discord tokens to input/tokens.txt (one token per line).
(Optional) Add proxies to input/proxies.txt if you want to use proxies.


Install Dependencies:Run the pip command above to install required libraries.

Run the Script:Execute the script using Python:
python discord_token_checker.py


Interact with the Menu:

The script displays a colorful menu with the number of loaded tokens and proxies.
Select option 01 to start the token checker or 0 to exit.
Results are saved to the data directory in separate files based on token status.


Output:

Valid tokens are saved to data/valid_tokens.txt.
Invalid tokens are saved to data/invalid_tokens.txt.
Locked tokens are saved to data/locked_tokens.txt.
Tokens requiring verification are saved to data/verified_tokens.txt.



Notes

Rate Limiting: The script handles HTTP 429 (rate limit) responses by retry gabinete waiting and adjusting delays dynamically.
Proxy Management: Proxies are validated before use, and banned proxies are excluded from further requests.
Error Handling: The script includes robust error handling for network issues, invalid tokens, and file operations.
Platform Compatibility: Works on Windows, Linux, and macOS, with special handling for Windows console titles.

Example File Structure
discord_token_checker/
├── input/
│   ├── tokens.txt
│   ├── proxies.txt
├── data/
│   ├── valid_tokens.txt
│   ├── invalid_tokens.txt
│   ├── locked_tokens.txt
│   ├── verified_tokens.txt
├── discord_token_checker.py

Limitations

Requires a stable internet connection for API requests.
Proxies must be reliable and properly formatted to avoid errors.
The script may be affected by Discord API changes or rate limit policies.

Disclaimer
This script is for educational purposes only. Misusing Discord tokens or violating Discord's Terms of Service may result in account bans or legal consequences. Use responsibly and ensure you have permission to test the tokens.
Developer

Author: ThinhDev
Community: Discord.gg/anhemnova
