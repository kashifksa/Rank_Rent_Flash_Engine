@echo off
echo ======================================================================
echo   Launching Chrome with Remote Debugging for Gemini Argon Bridge
echo ======================================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\.gemini_automation_profile" --no-first-run --no-default-browser-check "https://gemini.google.com/app"
echo Chrome launched. Log into your Google account if not already logged in.
echo You can now run:
echo   python scripts/gemini_browser_bridge.py --task brief
