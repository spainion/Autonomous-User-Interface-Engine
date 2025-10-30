"""
Simple HTTP Server for UI Showcase
Serves the generated UIs and provides easy browsing
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time
from pathlib import Path


class ShowcaseHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="showcase_output", **kwargs)
    
    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


def start_server(port=8000):
    """Start the HTTP server"""
    
    # Change to the repository directory
    os.chdir('/home/runner/work/Autonomous-User-Interface-Engine/Autonomous-User-Interface-Engine')
    
    handler = ShowcaseHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print("=" * 80)
        print(f"  UI SHOWCASE SERVER")
        print("=" * 80)
        print(f"\n  Server running at: http://localhost:{port}")
        print(f"  Main showcase: http://localhost:{port}/index.html")
        print("\n  Available UIs:")
        
        # List all generated UIs
        showcase_dir = Path("showcase_output")
        if showcase_dir.exists():
            for item in sorted(showcase_dir.iterdir()):
                if item.is_dir():
                    print(f"    - http://localhost:{port}/{item.name}/index.html")
        
        print("\n  Press Ctrl+C to stop the server")
        print("=" * 80)
        print()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")


def open_browser(url, delay=2):
    """Open browser after a delay"""
    time.sleep(delay)
    webbrowser.open(url)


if __name__ == "__main__":
    import sys
    
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    # Start browser in a separate thread
    url = f"http://localhost:{port}/index.html"
    browser_thread = threading.Thread(target=open_browser, args=(url,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    start_server(port)
