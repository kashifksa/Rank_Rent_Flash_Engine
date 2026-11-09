"""
gemini_browser_bridge.py — Rank & Rent Flash Engine
Automates sending data + prompts to your logged-in Google Gemini browser session
(using Gemini Advanced / Argon model) and extracting clean JSON back into the project.

Workflow:
1. Connects to Chrome via remote debugging (port 9222).
2. Navigates to or uses an existing tab at https://gemini.google.com/app.
3. Injects the complete prompt (P4 master brief, P5 topical, or P6 blueprint) + input data.
4. Submits to Gemini and waits for generation to finish.
5. Extracts and validates the resulting JSON.
6. Saves directly to master_brief.json (or specified output path).

Usage:
    # 1. Start Chrome with remote debugging (or use --launch):
    python scripts/gemini_browser_bridge.py --launch-browser

    # 2. Generate master_brief.json (Task P4):
    python scripts/gemini_browser_bridge.py --task brief

    # 3. Generate topical_authority.json (Task P5):
    python scripts/gemini_browser_bridge.py --task topical

    # 4. Generate master_site_blueprint.json (Task P6):
    python scripts/gemini_browser_bridge.py --task blueprint
"""

import os
import re
import sys
import json
import time
import socket
import argparse
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

CDP_DEFAULT_PORT = 9222
CDP_DEFAULT_URL = f"http://127.0.0.1:{CDP_DEFAULT_PORT}"
GEMINI_URL = "https://gemini.google.com/app"
DEFAULT_PROFILE_DIR = os.path.expanduser(r"~\.gemini_automation_profile")
REAL_PROFILE_DIR = r"C:\Users\Kashif\AppData\Local\Google\Chrome\User Data"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def is_port_open(host="127.0.0.1", port=CDP_DEFAULT_PORT):
    """Check if Chrome remote debugging port is already open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False


def launch_chrome_debugger(profile_dir=DEFAULT_PROFILE_DIR, port=CDP_DEFAULT_PORT, use_real_profile=False):
    """Launch Chrome with remote debugging port and persistent profile."""
    if use_real_profile:
        profile_dir = REAL_PROFILE_DIR
    if not os.path.exists(CHROME_PATH):
        raise FileNotFoundError(f"Chrome not found at {CHROME_PATH}")

    os.makedirs(profile_dir, exist_ok=True)
    cmd = [
        CHROME_PATH,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        GEMINI_URL
    ]
    print(f"Launching Chrome with remote debugging on port {port}...")
    proc = subprocess.Popen(cmd)
    
    # Wait for port to become active
    for _ in range(15):
        time.sleep(1)
        if is_port_open("127.0.0.1", port):
            print(f"Chrome is ready and listening on port {port}.")
            return proc
    raise TimeoutError(f"Chrome did not start listening on port {port} in time.")


def extract_json_from_text(raw_text):
    """Extract valid JSON from markdown code block or raw string."""
    raw_text = raw_text.strip()
    
    # 1. Try markdown code block ```json ... ```
    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text, re.IGNORECASE)
    if code_block_match:
        candidate = code_block_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # 2. Try outermost curly braces { ... }
    first_brace = raw_text.find("{")
    last_brace = raw_text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = raw_text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Fix common trailing comma errors
            cleaned = re.sub(r",\s*([\]}])", r"\1", candidate)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass

    raise ValueError("Could not extract valid JSON from Gemini response.")


def read_file_safe(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def build_task_payload(task_name, input_file=None):
    """Assemble the complete prompt and input data for the task."""
    _here = Path(__file__).resolve().parent
    base_dir = _here if (_here / 'AGENTS.md').exists() else _here.parent

    if task_name == "brief":
        prompt_file = base_dir / "prompts" / "P4_brief.md"
        # Prioritize FULL data.txt — Argon / Gemini Advanced handles the entire 18 sections directly!
        data_file = Path(input_file) if input_file else (base_dir / "data.txt")
        if not data_file.exists():
            data_file = base_dir / "data_brief.txt"
        
        if not data_file.exists():
            raise FileNotFoundError(f"Input file not found. Checked data_brief.txt and data.txt in {base_dir}")

        prompt_template = read_file_safe(prompt_file)
        data_content = read_file_safe(data_file)
        
        payload = f"""{prompt_template}

=== INPUT DATA TO PROCESS ===
{data_content}
=== END INPUT DATA ===

Generate the complete master_brief.json as requested in the prompt. Return ONLY valid JSON."""
        output_file = base_dir / "master_brief.json"
        return payload, str(output_file)

    elif task_name == "topical":
        prompt_file = base_dir / "prompts" / "P5_topical.md"
        brief_file = base_dir / "master_brief.json"
        if not brief_file.exists():
            raise FileNotFoundError("master_brief.json does not exist. Run task 'brief' first.")

        prompt_template = read_file_safe(prompt_file)
        brief_content = read_file_safe(brief_file)

        payload = f"""{prompt_template}

=== MASTER_BRIEF.JSON ===
{brief_content}
=== END MASTER_BRIEF.JSON ===

Generate the complete topical_authority.json. Return ONLY valid JSON."""
        output_file = base_dir / "topical_authority.json"
        return payload, str(output_file)

    elif task_name == "blueprint":
        prompt_file = base_dir / "prompts" / "P6_blueprint.md"
        brief_file = base_dir / "master_brief.json"
        topical_file = base_dir / "topical_authority.json"

        if not brief_file.exists():
            raise FileNotFoundError("master_brief.json does not exist.")
        if not topical_file.exists():
            raise FileNotFoundError("topical_authority.json does not exist.")

        prompt_template = read_file_safe(prompt_file)
        brief_content = read_file_safe(brief_file)
        topical_content = read_file_safe(topical_file)

        payload = f"""{prompt_template}

=== MASTER_BRIEF.JSON ===
{brief_content}

=== TOPICAL_AUTHORITY.JSON ===
{topical_content}
=== END INPUTS ===

Generate the complete master_site_blueprint.json. Return ONLY valid JSON."""
        output_file = base_dir / "master_site_blueprint.json"
        return payload, str(output_file)

    else:
        raise ValueError(f"Unknown task: {task_name}")


def send_to_gemini(payload, cdp_url=CDP_DEFAULT_URL):
    """Automate Gemini web interaction via Playwright connected to CDP."""
    print(f"Connecting to Chrome via CDP: {cdp_url} ...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(cdp_url)
        except Exception as e:
            print(f"ERROR: Could not connect to Chrome on {cdp_url}.")
            print("Make sure Chrome was started with --remote-debugging-port=9222.")
            print("Run: python scripts/gemini_browser_bridge.py --launch-browser")
            raise e

        # Find existing Gemini tab or open new one
        gemini_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "gemini.google.com" in page.url:
                    gemini_page = page
                    print("Found active Gemini tab.")
                    break
            if gemini_page:
                break

        if not gemini_page:
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            gemini_page = context.new_page()
            print(f"Navigating to {GEMINI_URL} ...")
            gemini_page.goto(GEMINI_URL, wait_until="networkidle")

        gemini_page.bring_to_front()
        time.sleep(2)

        # Verify user is logged in
        if "accounts.google.com" in gemini_page.url:
            print("\n" + "!" * 60)
            print("ACTION REQUIRED: You are not signed into Google on this Chrome profile.")
            print("Please sign into your Google account (with Gemini Argon/Advanced) in the opened Chrome window.")
            print("Once signed in, rerun this script.")
            print("!" * 60 + "\n")
            return None

        # Locate input editor (contenteditable div)
        print("Locating Gemini prompt input box...")
        selectors = [
            'div[contenteditable="true"]',
            'rich-textarea div[role="textbox"]',
            'div.ql-editor',
            'textarea[aria-label*="Prompt"]',
            'p[data-placeholder]'
        ]

        editor = None
        for sel in selectors:
            try:
                locator = gemini_page.locator(sel).first
                if locator.is_visible(timeout=2000):
                    editor = locator
                    print(f"Found input editor using selector: {sel}")
                    break
            except Exception:
                continue

        if not editor:
            raise RuntimeError("Could not find Gemini prompt input area. Ensure you are on https://gemini.google.com/app")

        # Focus and inject text cleanly
        print(f"Injecting payload ({len(payload.split())} words) into Gemini...")
        editor.click()
        time.sleep(0.5)

        # Use JavaScript clipboard / execCommand for fast insertion of large payloads
        gemini_page.evaluate("""(text) => {
            const el = document.querySelector('div[contenteditable="true"]') || document.querySelector('div[role="textbox"]');
            if (el) {
                el.focus();
                // Set innerText and dispatch input events
                el.innerText = text;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""", payload)
        time.sleep(1)

        # Check if text was set, if not fallback to typing or keyboard paste
        current_text = editor.inner_text().strip()
        if len(current_text) < 20:
            print("Fallback: Sending text via keyboard paste...")
            gemini_page.evaluate("text => navigator.clipboard.writeText(text)", payload)
            editor.focus()
            gemini_page.keyboard.press("Control+V")
            time.sleep(1)

        # Click send button
        print("Submitting prompt to Gemini...")
        send_selectors = [
            'button[aria-label*="Send message"]',
            'button[aria-label*="Send"]',
            'button.send-button',
            'button.mat-mdc-button-base[aria-label*="Send"]'
        ]
        
        sent = False
        for s_sel in send_selectors:
            btn = gemini_page.locator(s_sel).first
            try:
                if btn.is_visible(timeout=1500) and btn.is_enabled():
                    btn.click()
                    sent = True
                    print(f"Clicked Send button ({s_sel}).")
                    break
            except Exception:
                continue

        if not sent:
            print("Send button not clicked directly, pressing Enter...")
            gemini_page.keyboard.press("Enter")

        # Monitor generation progress
        print("Waiting for Gemini response to start and complete...")
        time.sleep(3)

        # Wait while response is streaming (Stop response button is active)
        stop_selectors = [
            'button[aria-label*="Stop response"]',
            'button[aria-label*="Stop"]',
            'div.stop-button',
            'mat-progress-spinner'
        ]

        # Max timeout 4 minutes for large blueprint tasks
        max_wait = 240
        start_time = time.time()
        was_generating = False

        while time.time() - start_time < max_wait:
            is_busy = False
            for st_sel in stop_selectors:
                try:
                    if gemini_page.locator(st_sel).first.is_visible(timeout=500):
                        is_busy = True
                        was_generating = True
                        break
                except Exception:
                    pass

            if is_busy:
                time.sleep(2)
                sys.stdout.write(".")
                sys.stdout.flush()
            else:
                if was_generating or (time.time() - start_time > 8):
                    # Stabilized! Wait 3 extra seconds
                    print("\nGeneration finished! Extracting response...")
                    time.sleep(3)
                    break
                time.sleep(1)

        # Extract latest model response
        response_selectors = [
            'message-content',
            'div.model-response-text',
            'div.response-content',
            '.model-response',
            'div.markdown'
        ]

        response_elements = None
        for r_sel in response_selectors:
            loc = gemini_page.locator(r_sel)
            if loc.count() > 0:
                response_elements = loc
                break

        if not response_elements:
            raise RuntimeError("Could not find generated response in Gemini UI.")

        # Get the very last response block
        count = response_elements.count()
        last_response = response_elements.nth(count - 1)
        raw_text = last_response.inner_text()

        print(f"Extracted response: {len(raw_text)} characters.")
        return raw_text


def main():
    parser = argparse.ArgumentParser(description="Automate Gemini Argon/Advanced web interface for Rank & Rent pipeline")
    parser.add_argument("--task", choices=["brief", "topical", "blueprint"], default="brief",
                        help="Pipeline task to execute (brief=P4, topical=P5, blueprint=P6)")
    parser.add_argument("--input", default=None, help="Optional custom input file path")
    parser.add_argument("--output", default=None, help="Optional custom output file path")
    parser.add_argument("--cdp-url", default=CDP_DEFAULT_URL, help="Chrome Remote Debugging URL")
    parser.add_argument("--use-real-profile", action="store_true",
                        help="Use your real Chrome profile so Argon is already logged in")
    parser.add_argument("--launch-browser", action="store_true",
                        help="Launch Chrome with debugging enabled and exit")
    args = parser.parse_args()

    if args.launch_browser:
        use_real = getattr(args, 'use_real_profile', False)
        launch_chrome_debugger(use_real_profile=use_real)
        print("\nChrome has been launched with remote debugging enabled.")
        print("Log into your Google account if not already logged in, then run:")
        print("  python scripts/gemini_browser_bridge.py --task brief")
        return

    # Check if port 9222 is open; if not, offer to launch or launch automatically
    if not is_port_open():
        print(f"Chrome remote debugging is not running on {args.cdp_url}.")
        print("Starting Chrome debugging instance automatically...")
        try:
            launch_chrome_debugger(use_real_profile=getattr(args, 'use_real_profile', False))
        except Exception as e:
            print(f"Could not auto-launch Chrome: {e}")
            print("\nPlease start Chrome manually with:")
            print('  chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\Users\\Kashif\\AppData\\Local\\Google\\Chrome\\User Data"')
            sys.exit(1)

    payload, default_output = build_task_payload(args.task, args.input)
    target_output = args.output or default_output

    print("=" * 60)
    print(f"TASK: {args.task.upper()}")
    print(f"OUTPUT TARGET: {target_output}")
    print("=" * 60)

    try:
        raw_response = send_to_gemini(payload, args.cdp_url)
        if not raw_response:
            return

        print("Parsing and validating JSON...")
        data = extract_json_from_text(raw_response)

        with open(target_output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 60)
        print(f"SUCCESS: Valid JSON successfully saved to:")
        print(f"  --> {target_output}")
        print("=" * 60)

    except Exception as e:
        print(f"\nERROR: Failed to complete task: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
