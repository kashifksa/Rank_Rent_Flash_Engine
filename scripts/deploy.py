import os
import sys
import subprocess

def run_cmd(cmd, cwd=None):
    print(f">> {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.returncode != 0:
        if res.stderr:
            print("ERROR:", res.stderr.strip())
        return False
    return True

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else "Update site content and templates"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print("=" * 65)
    print(" 🚀 Rank & Rent Flash Engine — 1-Click Deploy to Hostinger")
    print("=" * 65)
    
    # Step 1: Re-export production dist
    export_script = os.path.join(base_dir, "scripts", "export_live_site.py")
    if os.path.exists(export_script):
        print("\n[Step 1/3] Compiling production distribution...")
        success = run_cmd([sys.executable, export_script], cwd=base_dir)
        if not success:
            print("Export warning: continuing with current dist files...")
            
    # Step 2: Stage & commit changes
    print("\n[Step 2/3] Staging changes in Git...")
    run_cmd(["git", "add", "-A"], cwd=base_dir)
    
    status = subprocess.run(["git", "status", "--porcelain"], cwd=base_dir, text=True, capture_output=True).stdout.strip()
    if not status:
        print("Everything is already up to date! Nothing new to commit.")
    else:
        print(f"Committing: '{commit_msg}'")
        run_cmd(["git", "commit", "-m", commit_msg], cwd=base_dir)
        
    # Step 3: Push to GitHub origin main
    print("\n[Step 3/3] Pushing to GitHub (origin/main)...")
    pushed = run_cmd(["git", "push", "origin", "main"], cwd=base_dir)
    
    if pushed:
        print("\n" + "=" * 65)
        print(" ✅ SUCCESS: Pushed to GitHub!")
        print(" ⚡ GitHub Actions is now auto-syncing the 'deploy' branch.")
        print(" 🌐 Hostinger will pull the update automatically in ~15-30 seconds.")
        print("=" * 65)
    else:
        print("\n❌ Push failed. Please check your internet or git credentials.")

if __name__ == "__main__":
    main()
