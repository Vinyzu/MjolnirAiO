import traceback, multiprocessing, PySimpleGUI, hostsman, screeninfo, twocaptcha, cv2, pywinauto, urllib, os, ctypes, subprocess, random, string, requests, json, time, threading, websocket, shutil, proxy, psutil, socket, tempfile, webbrowser, warnings, logging, flask_sock
import matplotlib.pyplot as plt, matplotlib.gridspec as gridspec, selenium.webdriver as wd, numpy as np
from webdriver_manager.chrome import ChromeDriverManager; from selenium.webdriver.chrome.options import Options; from selenium.webdriver.common.by import By; from selenium.common.exceptions import ElementClickInterceptedException
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask import Flask, request, render_template, redirect; from PIL import Image

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
warnings.simplefilter("ignore", UserWarning)

app = Flask(__name__, template_folder="./frontend")
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
sock = flask_sock.Sock(app)

ctypes.windll.kernel32.SetConsoleTitleW("Mjolnir AiO Tool")
global server, paths
server, paths = "http://mjolnir.only-fans.club", {}
clear = lambda: os.system('cls')

@sock.route("/websockets")
def websockets(ws):
    while True:
        if request.args.get("ws") in paths:
            ws.receive()
            rn = 0
            while True:
                if rn != len(paths[request.args.get("ws")]):
                    for i in paths[request.args.get("ws")][rn:]:
                        ws.send(i)
                        rn = len(paths[request.args.get("ws")])

def log(path, msg):
    paths[path].append(msg)

def log1(path, msg):
    print(msg)

class DesktopGenerator:
    def __init__(self, websocket_url, proxies, minAge, maxAge, gender, order, alternative):
        #Global ClassValues
        self.start_time, self.generating = time.time(), True
        self.websocket_url, self.proxies, self.minAge, self.maxAge, self.gender, self.order = websocket_url, proxies.split("\r\n"), minAge if minAge else "1970", maxAge if maxAge else "1980", gender if gender else "male", order if order else "day"
        self.generated, self.failed, self.current_failed, self.accounts_mins = 0, 0, 0, []
        self.spotify_path = str(str(os.getenv('APPDATA')) + "\\Spotify\\")
        with tempfile.NamedTemporaryFile(suffix='.txt', prefix=os.path.basename(__file__)) as tf:
            temp_txt = tf.name
        self.temp_txt, self.alternative, self.waiting = temp_txt, alternative, 0
        #Checking and Modifying Installations
        if not self.check_installations(): return
        self.set_spotify()

    def check_installations(self):
        if not os.path.isdir(self.spotify_path):
            log(self.websocket_url, "[INSTALLATION] You have to install Spotify!")
            webbrowser.open("https://www.spotify.com/download/windows/")
            return False
        if not os.path.isdir("C:\Sandbox"):
            log(self.websocket_url, "[INSTALLATION] You have to install Sandboxie!")
            webbrowser.open("https://sandboxie-plus.com/downloads/")
            return False
        return True

    def set_spotify(self):
        #Setting Language to English
        log(self.websocket_url, "[SETUP] Setting Spotifys Preferences!")
        with open(f"{self.spotify_path}prefs", "r") as f:
            words = ['language="en"' if "language" in word else word for word in f.read().splitlines()]
            words = ["" if "autologin" in word else word for word in words]
            words = ["" if "network" in word else word for word in words]#
            open(f"{self.spotify_path}prefs", "w").close()
            with open(f"{self.spotify_path}prefs", 'w') as f:
                for item in words: f.write("%s\n" % item)
        #Deleting all users
        log(self.websocket_url, "[SETUP] Deleting Spotify Users!")
        try:
            roaming_path = str(self.spotify_path.replace("Roaming", "Local"))
            shutil.rmtree(str(roaming_path + "\\Users"))
            newpath = str(roaming_path + "\\Users")
            if not os.path.exists(newpath): os.makedirs(newpath)
        except: log(self.websocket_url, "[WARNING] Couldnt delete Spotify Users!")
        # #Deleting all sandboxes
        # log(self.websocket_url, "[SETUP] Deleting Mjolnir-Sandboxes!")
        # try:
        #     subfolders = [f.path for f in os.scandir("C:\Sandbox") if f.is_dir()]
        #     for folder in [f.path for f in os.scandir(subfolders[0]) if f.is_dir()]:
        #         if "Mjolnir" in str(folder): os.remove(folder)
        # except Exception as e: print(e); log(self.websocket_url, "[WARNING] Couldnt delete Sandboxes! (You have to run the .exe with Admin Permissions)")

    def kill_spotify(self):
        try: subprocess.check_call(["TASKKILL", "/F", "/IM", "spotify.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except: pass

    def generator(self, amount, names, passwords, threads, output_path, webhook_url):
        #Logging to server
        requests.post(f"{server}/generator/desktop", json={"amount": amount}, proxies=urllib.request.getproxies())
        #Setting Variable if not set (Maybe Temp)
        names = requests.get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt").text.splitlines() if not names else names.split("\r\n")
        passwords = requests.get("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/WPA-Length/Top4800-WPA-probable-v2.txt").text.splitlines() if not passwords else passwords.split("\r\n")
        output_path = "output.txt" if not output_path else output_path
        #Local Values
        threads, amount, count = int(threads), int(amount), 0
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        else: log(self.websocket_url, "[PROXY] No proxy server will be used")
        if webhook_url: threading.Thread(target=self.threaded_webhook, args=(webhook_url, threads, self.temp_txt,)).start()
        while count < amount:
            self.current_failed, self.waiting = 0, 0
            log(self.websocket_url, "[SPOTIFY] Killing all instances")
            self.kill_spotify()
            time.sleep(2)
            ports = []
            self.threadz = range(int(amount - count) if int(amount - count) <= threads else threads)
            for i in self.threadz:
                while True:
                    r_port = random.randint(19000, 19900)
                    if r_port not in ports: ports.append(r_port); break
                # Starting Spotify in Sandbox
                boks, SbieIni, Start  = f"Mjolnir{random.randint(0,9999999999)}", "C:\Program Files\Sandboxie\SbieIni.exe", "C:\Program Files\Sandboxie\Start.exe"
                better_lines = []
                for line in open("C:\Windows\Sandboxie.ini", "r").read().splitlines(): better_lines.append(''.join(ch for ch in line if ch.isalnum()))
                if any(boks in better_line for better_line in better_lines):
                    print(1)
                    try: subprocess.call(f'{Start} /box:{boks} delete_sandbox', False); subprocess.call(f"{SbieIni} set {boks} Enabled n", False); subprocess.call(f"{SbieIni} set {boks} Enabled y", False)
                    except: log(self.websocket_url, "[ERROR] You have to run the .exe with Admin Permissions"); return False
                else:
                    print(2)
                    try: subprocess.call(f"{SbieIni} set {boks} Enabled y", False)
                    except: log(self.websocket_url, "[ERROR] You have to run the .exe with Admin Permissions"); return False
                subprocess.call('"C:\Program Files\Sandboxie\Start.exe"  /reload', False)
                if any(self.proxies): subprocess.call(f'"C:\Program Files\Sandboxie\Start.exe" /box:{boks} "{self.spotify_path}Spotify.exe" --mute-audio --remote-debugging-port={r_port} --proxy-server="localhost:8899"', False)
                else: subprocess.call(f'"C:\Program Files\Sandboxie\Start.exe" /box:{boks} "{self.spotify_path}Spotify.exe" --mute-audio --remote-debugging-port={r_port}', False)
            log(self.websocket_url, "[SPOTIFY] Spawned all instances")
            for i in range(len(ports)):
                if i == range(len(ports))[-1]: self.threaded_gen(random.choice(names), str(random.choice(passwords) + random.choice(passwords) + "&/$!"), ports[i], output_path)
                else: threading.Thread(target=self.thread, args=([random.choice(names), str(random.choice(passwords) + random.choice(passwords) + "&/$!"), ports[i], output_path],)).start()
                count += 1
            amount += self.current_failed
        self.kill_spotify()
        self.generating = False
        log(self.websocket_url, "[DONE] Done generating all accounts")
        if webhook_url: self.webhook(webhook_url, threads, int(int(time.time() - self.start_time)/60), self.temp_txt, 'Mjolnir is done Generating!')

    def type_month(self, ws):
        if self.alternative:
            if self.waiting == self.threadz[-1]:
                for app in pywinauto.Desktop().windows():
                    if "Spotify" in str(app) and "#" in str(app) and "Chrome_WidgetWin_0" in str(app):
                        app.set_focus()
                        time.sleep(0.4)
                        app.type_keys("{ENTER}")
                        time.sleep(0.4)
                        app.type_keys("{DOWN}")
                        time.sleep(0.4)
                        app.type_keys("{ENTER}")

            self.waiting += 1
        else:
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"keyDown","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False}}
            ws.send(json.dumps(payload))
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"char","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False, "text": "\r", "unmodifiedText": "\r"}}
            ws.send(json.dumps(payload))
            payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 0, "code": "ArrowDown", "key":"ArrowDown", "windowsVirtualKeyCode": 40, "nativeVirtualKeyCode": 40, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
            ws.send(json.dumps(payload))
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"keyDown","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False}}
            ws.send(json.dumps(payload))
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"char","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False, "text": "\r", "unmodifiedText": "\r"}}
            ws.send(json.dumps(payload))

    def threaded_gen(self, name, password, port, output_path):
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        email = f"{rand}@gmail.com"
        time.sleep(5)
        # Connect with Websocket to DebugUrl to Inject Javascript
        wsUrl = requests.get(f"http://localhost:{port}/json").json()[0]["webSocketDebuggerUrl"]
        ws = websocket.create_connection(wsUrl)
        # Clicking Register Button
        self.inject_js(ws, "signup-link", 0)
        time.sleep(4)
        # Typing Email, Password and Username
        self.inject_js(ws, email, 1)
        time.sleep(2)
        payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 0, "code": "Tab", "key":"Tab", "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
        ws.send(json.dumps(payload))
        self.inject_js(ws, password, 1)
        time.sleep(2)
        payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 0, "code": "Tab", "key":"Tab", "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
        ws.send(json.dumps(payload))
        self.inject_js(ws, name, 1)
        time.sleep(2)
        #Clicking Submit Button
        self.inject_js(ws, "signup-button", 0)
        time.sleep(4)
        if self.order == "day":
            # Typing Birthday
            self.inject_js(ws, "day-field", 2)
            self.inject_js(ws, str(random.randint(1, 28)), 1)
            #Selecting Random Month
            time.sleep(1)
            payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 0, "code": "Tab", "key":"Tab", "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
            ws.send(json.dumps(payload))
            self.type_month(ws)
        else:
            #Selecting Random Month
            self.type_month(ws)
            # Typing Birthday
            time.sleep(1)
            self.inject_js(ws, "day-field", 2)
            self.inject_js(ws, str(random.randint(1, 28)), 1)
        #Typing Birthyear
        time.sleep(1)
        self.inject_js(ws, "year-field", 2)
        time.sleep(0.5)
        self.inject_js(ws, str(random.randint(int(self.minAge), int(self.maxAge))), 1)
        # Selecting a Gender
        time.sleep(1)
        ea = {"female": 0, "male": 1, "none": 2}
        try: payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": f"document.getElementsByClassName('FormRadioSelect__label')[{ea[self.gender.lower()]}].click()"}}
        except: payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": "document.getElementsByClassName('FormRadioSelect__label')[1].click()"}}
        ws.send(json.dumps(payload))
        # Clicking Tos, Privacy and Submit Buttons
        self.inject_js(ws, "agree-tos-2-field", 0)
        self.inject_js(ws, "agree-privacy-2-field", 0)
        self.inject_js(ws, "signup-button", 0)
        time.sleep(6)
        #"title": "Spotify - Login"
        title = requests.get(f"http://localhost:{port}/json").json()[0]["title"]
        if title == "Spotify - Login":
            log(self.websocket_url, "[ERROR] Bad Proxy (Use ISP/Residential)")
            self.failed += 1
            self.current_failed += 1
            return
        # Clicking Profile Button
        ## TODO: $ doesnt work use document.querySelectorAll
        # payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": '$("button[data-testid=user-widget-link]").click()'}}
        # ws.send(json.dumps(payload))
        # time.sleep(1)
        # # Clicking Logout Button
        # payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": '$("button[data-testid=user-widget-dropdown-logout]").click()'}}
        # ws.send(json.dumps(payload))
        log(self.websocket_url, f"[SUCCESS] Successfully created: {email}:{password}")
        with open(output_path,'a') as output_file:
            write_string = ''
            for i in [email, password, name]: write_string += str(i + ':')
            output_file.write(str(write_string[:-1] + '\n'))
        with open(self.temp_txt, 'a') as output_file:
            write_string = ''
            for i in [email, password, name,]: write_string += str(i + ':')
            output_file.write(str(write_string[:-1] + '\n'))
        self.generated += 1

    def inject_js(self, ws, text, i):
        if i == 0:
            payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": f"document.getElementById('{text}').click()"}}
            ws.send(json.dumps(payload))
        elif i == 1:
            payload = {"id": 1337, "method": "Input.insertText", "params": {"text": text}}
            ws.send(json.dumps(payload))
        else:
            payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": f"document.getElementById('{text}').focus()"}}
            ws.send(json.dumps(payload))

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        except Exception as e: pass#log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})"); import traceback; print(traceback.format_exc())

    def webhook(self, url, threads, runtime, accounts_path, title):
        webhook = DiscordWebhook(username='Mjolnir AiO Tool', url=url, avatar_url="https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-icon-marilyn-scott-0.png")
        # create embed object for webhook
        embed = DiscordEmbed(title=title, description=f'Total Generated Accounts: {self.generated}', color='1DB954')
        # set image
        runtime = 1 if runtime == 0  else runtime
        Minutes = list(range(int(runtime)+1))
        Accounts = self.accounts_mins
        Accounts[-1] = self.generated
        if len(Minutes) != len(Accounts):
            Minutes = list(range(len(Accounts)))

        fig = plt.figure()
        fig.patch.set_facecolor('#2F3136')
        ax = plt.axes()
        ax.set_facecolor('#23272A')
        plt.plot(Minutes, Accounts, color="#99AAB5")
        plt.title('Your Mjolnir Desktop-Generator Stats', color="#99AAB5")
        plt.xlabel('Minutes', color="#99AAB5")
        plt.ylabel('Accounts', color="#99AAB5")
        with tempfile.NamedTemporaryFile(suffix='.png', prefix=os.path.basename(__file__), delete=False) as tf:
            plt.savefig(tf.name)
            files = {'image': ('graph.png', open(tf.name, 'rb'))}
            r = requests.post("https://api.imgbb.com/1/upload?key=5b4141e2323a62c75b4fe2c5e5d58cec", files=files).json()
            url = r["data"]["display_url"].replace("\/", "/")
        embed.set_image(url=url)
        # add fields to embed
        embed.add_embed_field(name=':computer: Computer Name :computer:', value=socket.gethostname(), inline=False)
        embed.add_embed_field(name=':gear: CPU Usage :gear:', value=f"{str(100 - int(psutil.cpu_times_percent(interval=0.4, percpu=False).idle))} %", inline=False)
        embed.add_embed_field(name=':bar_chart: RAM Usage :bar_chart:', value=f"{psutil.virtual_memory().percent} %", inline=False)
        embed.add_embed_field(name=":file_cabinet: Threads :file_cabinet:", value=str(threads), inline=False)
        embed.add_embed_field(name=":stopwatch: Runtime :stopwatch:", value=f"{int(runtime)} Minutes", inline=False)
        embed.add_embed_field(name=":chart_with_upwards_trend: Accounts Generated :chart_with_upwards_trend:", value=str(self.generated), inline=False)
        embed.add_embed_field(name=":x: Failed Generations :x:", value=str(self.failed), inline=False)
        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
        with open(accounts_path, "rb") as f:
            webhook.add_file(file=f.read(), filename='accounts.txt')
        webhook.remove_embeds()
        webhook.execute(remove_embeds=True)

    def update_minutes(self):
        while self.generating:
            self.accounts_mins.append(self.generated)
            time.sleep(60)

    def threaded_webhook(self, url, threads, accounts_path):
        threading.Thread(target=self.update_minutes).start()
        runtimed = 1
        while self.generating:
            time.sleep(600)
            if self.generating:
                self.webhook(url, threads, int(runtimed * 10), accounts_path, 'Your Mjolnir Desktop-Generator Stats')
                runtimed += 1

    def thread(self, args):
        threading.Thread(target=self.threaded_gen, args=(tuple(args))).start()

class WebGenerator:
    def __init__(self, amount, threads, captcha_key, names, passwords, output_path, websocket_url, proxies, minAge, maxAge, gender):
        #Global ClassValues
        self.websocket_url, self.proxies, self.minAge, self.maxAge, self.gender = websocket_url, proxies.split("\r\n") if proxies else "", minAge if minAge else "1970", maxAge if maxAge else "1980", gender if gender else "male"
        self.output_path, self.threads, self.amount, self.count, self.captcha_key, self.pngs = "output.txt" if not output_path else output_path, int(threads) if threads else 10, int(amount) if amount else 1, 0, captcha_key, []
        self.names = requests.get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt").text.splitlines() if not names else names.split("\r\n")
        self.passwords = requests.get("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/WPA-Length/Top4800-WPA-probable-v2.txt").text.splitlines() if not passwords else passwords.split("\r\n")
        #Checking and Modifying Installations
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        else: log(self.websocket_url, "[PROXY] No proxy server will be used")

    def generator(self):
        #Logging to server
        requests.post(f"{server}/generator/web", json={"amount": self.amount}, proxies=urllib.request.getproxies())
        #Local Values
        while self.count < self.amount:
            self.current_failed, self.waiting = 0, 0
            # log(self.websocket_url, "[SPOTIFY] Killing all instances")
            # # self.kill_spotify
            # time.sleep(2)
            self.threadz = range(int(self.amount - self.count) if int(self.amount - self.count) <= self.threads else self.threads)
            try:
                solver = twocaptcha.TwoCaptcha(self.captcha_key)
                balance = solver.balance()
                if balance < 0.01:log(self.websocket_url, "[ERROR] Your 2Captcha Balance is to low"); return
                else: log(self.websocket_url, f"[INFO] Your 2Captcha Balance is: {balance}")
            except Exception as e: log(self.websocket_url, f"[ERROR] The key {self.captcha_key} is not a 2Captcha Key (ErrorMsg: {str(e)})"); return
            for i in self.threadz:
                if i == range(len(self.threadz))[-1]: self.threaded_gen()
                else: threading.Thread(target=self.threaded_gen).start()
                self.count += 1
            self.delete_captcha_images()
            self.amount += self.current_failed
        # self.kill_spotify()
        log(self.websocket_url, "[DONE] Done generating all accounts")
        try:
            for path in self.pngs: os.remove(f'{path}.png'); os.remove(f'{path}.jpg')
        except: log(self.websocket_url, "[WARNIN] Couldnt delete all Captcha Images")

    def delete_captcha_images(self):
        onlyfiles = [str(os.path.dirname(__file__) + "\\" + f) for f in os.listdir(os.path.dirname(__file__)) if os.path.isfile(os.path.join(os.path.dirname(__file__), f))]
        for file in onlyfiles:
            if "temp" in file and (".png" in file or ".jpg" in file):
                os.remove(file)

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        #log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})"); import traceback; print(traceback.format_exc())
        except Exception as e: pass

    def captcha(self, path):
        solver = twocaptcha.TwoCaptcha(self.captcha_key, defaultTimeout=60, pollingInterval=5)
        result = solver.coordinates(f'{path}.jpg')
        return result
        # return {'captchaId': '70226257460', 'code': 'coordinates:x=34,y=158;x=204,y=198;x=89,y=452;x=331,y=541'}

    def screenalize(self, page):
        while True:
            path = "temp" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
            page.screenshot(path=f"{path}.png")
            im = cv2.imread(f'{path}.png')
            try:
                Y, X = np.where(np.all(im==[232, 115, 26], axis=2))
                im = Image.open(open(f"{path}.png", 'rb'))
                im = im.crop((X[0], Y[0], X[-1], Y[-1]))
            except: return False
            else:
                rgb_im = im.convert('RGB')
                rgb_im.save(f'{path}.jpg')
                try:
                    captcha = self.captcha(path)
                except: return False
                code = captcha["code"].replace("coordinates:", "")
                for i in code.split(";"):
                    x, y = i.split(",")[0].replace("x=", ""), i.split(",")[1].replace("y=", "")
                    page.mouse.click(int(int(x)+X[0]), int(int(y)+Y[0]), delay=10)
                    time.sleep(1)

    def threaded_gen(self):
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        email, password, name = f"{rand}@gmail.com", str(random.choice(self.passwords) + random.choice(self.passwords) + "&/$!"), random.choice(self.names)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, proxy={"server": "http://localhost:8899"} if any(self.proxies) else None)
            page = browser.new_page()
            try: page.goto("https://www.spotify.com/signup")
            except: log(self.websocket_url, "[ERROR] Proxy Server timed out"); return
            time.sleep(2)
            try: page.click("id=onetrust-accept-btn-handler", timeout=10)
            except:
                try: page.evaluate('document.getElementById("onetrust-close-btn-container").firstElementChild.click()')
                except: log(self.websocket_url, "[WARNING] Coulnt click cookie-banner")
            try:
                page.evaluate('document.getElementById("onetrust-consent-sdk").style.visibility = "visible"')
                page.evaluate('document.getElementById("onetrust-consent-sdk").style.display = "none"')
            except: log(self.websocket_url, "[WARNING] Coulnt hide cookie-banner")
            page.set_viewport_size({"width": int(screeninfo.get_monitors()[0].width) - 100, "height": int(screeninfo.get_monitors()[0].height) - 200})
            page.evaluate('document.getElementsByTagName("iframe")[0].setAttribute("src", document.getElementsByTagName("iframe")[0].getAttribute("src").split("hl=")[0] + "hl=en&" + document.getElementsByTagName("iframe")[0].getAttribute("src").split("hl=")[1].split("&")[1])')
            typings = {"id=email": email, "id=confirm": email, "id=password": password, "id=displayname": name, "id=day": str(random.randint(1, 27)), "id=year": str(random.randint(int(self.minAge), int(self.maxAge)))}
            for types in typings.items():
                page.type(types[0], types[1], delay=10)
                time.sleep(0.4)
            # page.select_option('role=select[name="month"]', str(random.randint(1, 12)))
            page.locator('[name="month"]').select_option(f"0{str(random.randint(2, 9))}")
            # page.evaluate(f'document.getElementById("month").value = "0{str(random.randint(1, 9))}"')
            time.sleep(1)
            genders = {"male": "male", "female": "female", "none": "nonbinary"}
            page.evaluate(f'document.getElementById("gender_option_{genders[self.gender]}").click()')
            time.sleep(1)
            try: page.click("id=terms-conditions-checkbox", timeout=10)
            except:
                try: page.evaluate('document.getElementById("terms-conditions-checkbox").click()')
                except: log(self.websocket_url, "[WARNING] Coulnt click Terms Checkbox")
            # page.evaluate('document.getElementById("terms-conditions-checkbox").click()')
            time.sleep(1)
            page.frame_locator("iframe[role='presentation']").first.locator('#recaptcha-anchor').click()
            # page.evaluate('document.querySelector("[role=presentation]").click()')
            time.sleep(2)
            ye, prev_coords = 0, []
            for i in range(3): page.mouse.wheel(delta_y=screeninfo.get_monitors()[0].height, delta_x=0)
            while True:
                if ye % 2:
                    x, y = prev_coords[-1]
                    page.mouse.click(int(x)-10, int(y)-10, delay=10)
                else:
                    path = "temp" + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
                    page.screenshot(path=f"{path}.png")
                    im = cv2.imread(f'{path}.png')
                    try:
                        Y, X = np.where(np.all(im==[232, 115, 26], axis=2))
                        prev_coords.append([X[-1], Y[-1]])
                        im = Image.open(open(f"{path}.png", 'rb'))
                        im = im.crop((X[0], Y[0], X[-1], Y[-1]))
                    except: break
                    else:
                        rgb_im = im.convert('RGB')
                        rgb_im.save(f'{path}.jpg')
                        im.close()
                        try: rgb_im.close()
                        except: pass
                        try: captcha = self.captcha(path)
                        except: log(self.websocket_url, "[ERROR] Couldnt solve captcha"); self.current_failed += 1; browser.close(); return
                        code = captcha["code"].replace("coordinates:", "")
                        for i in code.split(";"):
                            try: x, y = i.split(",")[0].replace("x=", ""), i.split(",")[1].replace("y=", "")
                            except: log(self.websocket_url, f"[WARNING] Couldnt retreive Coordinates from 2Captcha-Answer: {i}"); continue
                            page.mouse.click(int(int(x)+X[0]), int(int(y)+Y[0]), delay=10)
                            time.sleep(1)
                ye += 1
            page.evaluate('document.querySelector("[type=submit]").click()')
            for i in range(10):
                if not "Sign up" in page.title():
                    log(self.websocket_url, f"[SUCCESS] Successfully created: {email}:{password}")
                    with open(self.output_path, 'a') as output_file:
                        write_string = ''
                        for i in [email, password, name]: write_string += str(i + ':')
                        output_file.write(str(write_string[:-1] + '\n'))
                    break
                time.sleep(2)
            else:
                self.current_failed += 1
                log(self.websocket_url, f"[ERROR] There was an uncaught Error, retrying!")
            browser.close()
            self.pngs.append(path)

class RequestGenerator:
    def __init__(self, path, proxies):
        self.websocket_url, self.proxies = path, proxies.split("\r\n")

    def generator(self, amount, threads, names, passwords, output_path):
        #Logging to server
        requests.post(f"{server}/generator/request", json={"amount": amount}, proxies=urllib.request.getproxies())
        names = requests.get("https://raw.githubusercontent.com/jeanphorn/wordlist/master/usernames.txt").text.splitlines() if not names else names.split("\r\n")
        passwords = requests.get("https://raw.githubusercontent.com/berzerk0/Probable-Wordlists/master/Real-Passwords/WPA-Length/Top4800-WPA-probable-v2.txt").text.splitlines() if not passwords else passwords.split("\r\n")
        threads = 10 if not threads else int(threads)
        self.count, amount = 0, int(amount)
        output_path = "output.txt" if not output_path else output_path.replace('"', "")
        while self.count < amount:
            for i in range(int(amount - self.count) if int(amount - self.count) <= threads else threads):
                name, password, proxy = random.choice(names), random.choice(passwords), random.choice(self.proxies)
                threading.Thread(target=self.threaded_gen, args=(name, password, proxy, output_path)).start()
            time.sleep(2)
        log(self.websocket_url, "[DONE] Done generating all accounts")

    def threaded_gen(self, name, password, proxy, output_path):
        email = "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(8)) + "@" + "".join(random.choice(string.ascii_lowercase) for i in range(5)) + ".com"
        try:
            headers={"Accept-Encoding": "gzip",
                     "Accept-Language": "en-US",
                     "App-Platform": "Android",
                     "Connection": "Keep-Alive",
                     "Content-Type": "application/x-www-form-urlencoded",
                     "Host": "spclient.wg.spotify.com",
                     "User-Agent": "Spotify/8.6.72 Android/29 (SM-N976N)",
                     "Spotify-App-Version": "8.6.72",
                     "X-Client-Id": "".join(random.choice(string.ascii_lowercase+string.digits) for i in range(32))}

            payload = {"creation_point": "client_mobile",
                    "gender": "male" if random.randint(0, 1) else "female",
                    "birth_year": random.randint(1990, 2000),
                    "displayname": name,
                    "iagree": "true",
                    "birth_month": random.randint(1, 11),
                    "password_repeat": password,
                    "password": password,
                    "key": "142b583129b2df829de3656f9eb484e6",
                    "platform": "Android-ARM",
                    "email": email,
                    "birth_day": random.randint(1, 20)}
            r = requests.post('https://spclient.wg.spotify.com/signup/public/v1/account/', headers=headers, data=payload, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None, timeout=15) #, proxies={'http': str('http://' + proxy)}
            if r.status_code==200:
                if r.json()['status']==1:
                    with open(output_path,'a') as output_file:
                        write_string = ''
                        for i in [email, password, name]: write_string += str(i + ':')
                        output_file.write(str(write_string[:-1] + '\n'))
                    self.count += 1
                    log(self.websocket_url, f"[SUCCESS] Successfully created: {email}:{password}")
                else:
                    log(self.websocket_url, f"[ERROR] An error occurred: {str(r.json())}")
                    # acc_queue.put([f'Error{random.randint(1, 99999)}', "Could not create the account, some errors occurred", "If you dont know what the following means, feel free to create a ticket!", str(r.json())])
            else: log(self.websocket_url, f"[ERROR] Couldnt load the URL. Status Code: {str(r.status_code)}")
                # acc_queue.put([f'Error{random.randint(1, 99999)}', "If you dont know what the error means, feel free to create a ticket!", "Could not load the page. Response code: ", str(r.status_code)])
        except Exception as e: log(self.websocket_url, f"[ERROR] An error occurred: {str(e)}")
            # acc_queue.put([f'Error{random.randint(1, 99999)}', "There was an error while generating the code", "If you dont know what the error means, feel free to create a ticket!", str(e)])

class Liker:
    def __init__(self, link, threads, timeout, proxies, proxy_type, path, url):
        self.link, self.threads, self.timeout, self.combo_path, self.websocket_url, self.count = link, int(threads) if threads else 10, int(timeout) if timeout else 5, path, url, 0
        self.proxy_type, self.proxies, self.driver_exe = proxy_type, proxies.split("\r\n"), ChromeDriverManager(print_first_line=False, log_level=0).install()
        os.environ['WDM_LOG'] = '0'

    def liker(self):
        combos = open(self.combo_path, "r").read().splitlines()
        #Logging to server
        requests.post(f"{server}/liker", json={"amount": len(combos)}, proxies=urllib.request.getproxies())
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        while self.count < len(combos):
            for i in range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads):
                combo = combos[i]
                if i == range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads)[-1]:
                    self.threaded_liker(combo)
                else: threading.Thread(target=self.threaded_liker, args=(combo,))
        log(self.websocket_url, "[DONE] Done liking with all accounts")

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        except Exception as e: log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})"); print(traceback.format_exc())

    def threaded_liker(self, combo):
        user, password = combo.split(":")
        options = Options()
        for item in ["--headless", "--no-sandbox", "--disable-dev-shm-usage", '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', '--no-sandbox', '--log-level=3', '--lang=en', "--window-size=1920,1080", "--mute-audio"]:
            options.add_argument(item)
        if any(self.proxies): options.add_argument('--proxy-server="localhost:8899"')
        options.ignore_protected_mode_settings = True
        driver = wd.Chrome(self.driver_exe, options=options)
        driver.get("https://accounts.spotify.com/login")
        for _ in range(5):
            try: driver.find_element(By.ID, "login-username").send_keys(user); break
            except: log(self.websocket_url, f"[REDO] Site didnt load: {combo} ({_ + 1})"); time.sleep(5)
        else: log(self.websocket_url, f"[ERROR] Site didnt load: {combo}"); driver.close(); return
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        if not "status" in driver.current_url:
            for _ in range(5):
                log(self.websocket_url, f"[REDO] Retrying to login: {combo} ({_ + 1})")
                try: driver.find_element(By.ID, "login-button").click()
                except: pass
                time.sleep(6)
                if "status" in driver.current_url: break
            else: log(self.websocket_url, f"[ERROR] Couldnt login: {combo}"); driver.close(); return
        driver.get(self.link)
        time.sleep(5)
        try: driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except: pass
        for _, button in enumerate(driver.find_elements(By.XPATH, "//button[@data-testid='add-button']")):
            if _ == 0:
                try: button.click()
                except ElementClickInterceptedException: pass
        log(self.websocket_url, f"[SUCCESS] Successfully liked: {combo}")
        self.count += 1
        driver.quit()

class Checker:
    def __init__(self, threads, proxies, proxy_type, max, combo_path, path):
        self.threads, self.max, self.combo_path, self.websocket_url = int(threads) if threads else 10, int(max) if max else 5, combo_path, path
        self.proxy_type, self.proxies = proxy_type, proxies.split("\r\n")
        self.count, self.valid = 0, 0
        os.environ['WDM_LOG'] = '0'
        self.driver_exe = ChromeDriverManager(print_first_line=False, log_level=0).install()

    def checker(self):
        combos = open(self.combo_path, "r").read().splitlines()
        #Logging to server
        requests.post(f"{server}/checker", json={"amount": len(combos)}, proxies=urllib.request.getproxies())
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        while self.count < len(combos):
            threadz = range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads)
            for i in threadz:
                combo = combos[i]
                if i == threadz[-1]:
                    self.threaded_checker(combo)
                else: threading.Thread(target=self.threaded_checker, args=(combo,)).start()
        log(self.websocket_url, f"[VALID] {self.valid} / [INVALID] {self.count - self.valid}")
        log(self.websocket_url, "[DONE] Done checking with all accounts")

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        except Exception as e: log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})"); print(traceback.format_exc())

    def threaded_checker(self, combo):
        try:
            user, pw, rest =  combo.split(":", 2)
        except:
            user, pw = combo.split(":")
        options = Options()
        l = ['--log-level=3', '--lang=en', "--window-size=1920,1080", "--mute-audio", "--log-level=3", "disable-logging"]
        if any(self.proxies): l.append('--proxy-server="localhost:8899"')
        for item in l:
            options.add_argument(item)
        options.ignore_protected_mode_settings = True
        driver = wd.Chrome(self.driver_exe, options=options)
        driver.get("https://accounts.spotify.com/en/login")
        driver.find_element(By.ID, "login-username").send_keys(user)
        driver.find_element(By.ID, "login-password").send_keys(pw)
        driver.find_element(By.ID, "login-button").click()
        for _ in range(self.max):
            time.sleep(1)
            if driver.current_url == "https://accounts.spotify.com/en/status":
                log(self.websocket_url, f"[VALID] {combo}")
                self.valid += 1
                break
        else: log(self.websocket_url, f"[INVALID] {combo}")
        self.count += 1
        driver.quit()

class MailChecker:
    def __init__(self, threads, proxies, max, combo_path, path):
        self.threads, self.max, self.combo_path, self.websocket_url = int(threads) if threads else 10, int(max) if max else 5, combo_path, path
        self.proxies = proxies.split("\r\n")
        self.count, self.valid = 0, 0

    def checker(self):
        combos = open(self.combo_path, "r").read().splitlines()
        #Logging to server
        requests.post(f"{server}/mailchecker", json={"amount": len(combos)}, proxies=urllib.request.getproxies())
        while self.count < len(combos):
            threadz = range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads)
            for i in threadz:
                combo = combos[i]
                if i == threadz[-1]:
                    print(0)
                    self.threaded_checker(combo)
                else: print(1); threading.Thread(target=self.threaded_checker, args=(combo,)).start()
        log(self.websocket_url, f"[VALID] {self.valid} / [INVALID] {self.count - self.valid}")
        log(self.websocket_url, "[DONE] Done checking with all accounts")

    def threaded_checker(self, combo):
        try:
            user, pw, rest =  combo.split(":", 2)
        except:
            try:
                user, pw = combo.split(":")
            except: user = combo

        prox = random.choice(self.proxies)
        proxy = {"https": f"http://{prox}", "http": f"http://{prox}"} if any(self.proxies) else {}
        if requests.post("https://spclient.wg.spotify.com/signup/public/v1/account", params={'validate': '1', 'email': user}, proxies=proxy).json()["status"] == 20:
            log(self.websocket_url, f"[VALID] {combo}")
            self.valid += 1
        else: log(self.websocket_url, f"[INVALID] {combo}")
        self.count += 1

class DesktopStreamer:
    def __init__(self, combo_path, threads, proxies, link, max, like, follow, mute, pos, webhook, path):
        self.threads, self.start_time = int(threads) if threads else 10, time.time()
        self.combo_path, self.max, self.like, self.follow, self.mute, self.pos = combo_path.replace('"', ""), int(max) if max else 5, int(like) if like else 0, int(follow) if follow else 0, mute if mute else True, int(int(pos) if pos else 0) + 1
        self.proxies, self.webhook_url, self.websocket_url = proxies.split("\r\n"), webhook, path
        self.spotify_path = str(str(os.getenv('APPDATA')) + "\\Spotify\\")
        link = link.replace('"', "").replace(" ", "")
        if os.path.exists(link): self.links = open(link).read().splitlines()
        else: self.links = link.split(",")
        self.streamed, self.stream_failed, self.stream_current_failed, self.streaming, self.likes, self.current_streaming = 0, 0, 0, 0, 0, False
        self.streams_mins, self.streaming_mins, self.like_mins = [], [], []
        #Checking and Modifying Installations
        if not self.check_installations(): return
        self.set_spotify()

    def check_installations(self):
        if not os.path.isdir(self.spotify_path):
            log(self.websocket_url, "[INSTALLATION] You have to install Spotify!")
            webbrowser.open("https://www.spotify.com/download/windows/")
            return False
        if not os.path.isdir("C:\Sandbox"):
            log(self.websocket_url, "[INSTALLATION] You have to install Sandboxie!")
            webbrowser.open("https://sandboxie-plus.com/downloads/")
            return False
        return True

    def set_spotify(self):
        #Setting Language to English
        log(self.websocket_url, "[SETUP] Setting Spotifys Preferences!")
        with open(f"{self.spotify_path}prefs", "r") as f:
            words = ['language="en"' if "language" in word else word for word in f.read().splitlines()]
            words = ["" if word in ("autologin", "network") else word for word in words]
            open(f"{self.spotify_path}prefs", "w").close()
            with open(f"{self.spotify_path}prefs", 'w') as f:
                for item in words: f.write("%s\n" % item)
        #Deleting all users
        log(self.websocket_url, "[SETUP] Deleting Spotify Users!")
        try:
            roaming_path = str(self.spotify_path.replace("Roaming", "Local"))
            shutil.rmtree(str(roaming_path + "\\Users"))
            newpath = str(roaming_path + "\\Users")
            if not os.path.exists(newpath): os.makedirs(newpath)
        except: log(self.websocket_url, "[WARNING] Couldnt delete Spotify Users!")
        #Deleting all sandboxes
        log(self.websocket_url, "[SETUP] Deleting Mjolnir-Sandboxes!")
        try:
            subfolders = [f.path for f in os.scandir("C:\Sandbox") if f.is_dir()]
            for folder in [f.path for f in os.scandir(subfolders[0]) if f.is_dir()]:
                if "Mjolnir" in str(folder): os.remove(folder)
        except: log(self.websocket_url, "[WARNING] Couldnt delete Sandboxes! (You have to run the .exe with Admin Permissions)")

    def kill_spotify(self):
        try: subprocess.check_call(["TASKKILL", "/F", "/IM", "spotify.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except: pass

    def streamer(self):
        #Local Values
        combo, count, self.current_streaming = open(self.combo_path, "r").read().splitlines(), 0, True
        #Logging to server
        requests.post(f"{server}/streamer/desktop", json={"amount": len(combo)}, proxies=urllib.request.getproxies())
        combo = [x for x in combo if x]
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        else: log(self.websocket_url, "[PROXY] No proxy server will be used")
        if self.webhook_url: threading.Thread(target=self.threaded_webhook).start()
        while count < len(combo):
            self.current_failed, self.waiting = 0, 0
            log(self.websocket_url, "[SPOTIFY] Killing all instances")
            self.kill_spotify()
            time.sleep(2)
            ports = []
            self.threadz = range(int(len(combo) - count) if int(len(combo) - count) <= self.threads else self.threads)
            for i in self.threadz:
                while True:
                    r_port = random.randint(19000, 19900)
                    if r_port not in ports: ports.append(r_port); break
                # Starting Spotify in Sandbox
                boks, SbieIni, Start  = f"Mjolnir{i}", "C:\Program Files\Sandboxie\SbieIni.exe", "C:\Program Files\Sandboxie\Start.exe"
                better_lines = []
                for line in open("C:\Windows\Sandboxie.ini", "r").read().splitlines(): better_lines.append(''.join(ch for ch in line if ch.isalnum()))
                if any(boks in better_line for better_line in better_lines):
                    try: subprocess.call(f'{Start} /box:{boks} delete_sandbox', False); subprocess.call(f"{SbieIni} set {boks} Enabled n", False); subprocess.call(f"{SbieIni} set {boks} Enabled y", False)
                    except: log(self.websocket_url, "[ERROR] You have to run the .exe with Admin Permissions"); return False
                else:
                    try: subprocess.call(f"{SbieIni} set {boks} Enabled y", False)
                    except: log(self.websocket_url, "[ERROR] You have to run the .exe with Admin Permissions"); return False
                subprocess.call('"C:\Program Files\Sandboxie\Start.exe"  /reload', False)
                if any(self.proxies): subprocess.call(f'"C:\Program Files\Sandboxie\Start.exe" /box:{boks} "{self.spotify_path}Spotify.exe" --mute-audio --remote-debugging-port={r_port} --proxy-server="localhost:8899"', False)
                else: subprocess.call(f'"C:\Program Files\Sandboxie\Start.exe" /box:{boks} "{self.spotify_path}Spotify.exe" --mute-audio --remote-debugging-port={r_port}', False)
            log(self.websocket_url, "[SPOTIFY] Spawned all instances")
            current_combo = []
            for i in range(len(ports)):
                if i == range(len(ports))[-1]:
                    self.threaded_streamer(combo[i], ports[i], self.like, self.max)
                else: threading.Thread(target=self.thread, args=([combo[i], ports[i], self.like, self.max],)).start()
                count += 1
            for comb in current_combo: combo.remove(comb)
        self.kill_spotify()
        self.current_streaming = False
        log(self.websocket_url, "[DONE] Done streaming with all accounts")
        if self.webhook_url: self.webhook(int(int(time.time() - self.start_time)/60), 'Mjolnir is done Streaming!')

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        except Exception as e: log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})")#; import traceback; print(traceback.format_exc())

    def inject_js(self, ws, text, i):
        if i == 0:
            payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": f"document.getElementById('{text}').click()"}}
            ws.send(json.dumps(payload))
        elif i == 1:
            payload = {"id": 1337, "method": "Input.insertText", "params": {"text": text}}
            ws.send(json.dumps(payload))
        else:
            payload = {"id": 1337, "method": "Runtime.evaluate", "params": {"expression": f"document.getElementById('{text}').focus()"}}
            ws.send(json.dumps(payload))

    def threaded_streamer(self, combo, port, like, wait):
        # global streamed, stream_failed, stream_current_failed, likes, streaming
        wsUrl = requests.get(f"http://localhost:{port}/json").json()[0]["webSocketDebuggerUrl"]
        ws = websocket.create_connection(wsUrl)
        self.inject_js(ws, "GlueTextInput-1", 0)
        for i in range(10):
            payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 2, "code": "Back", "key":"Back", "windowsVirtualKeyCode": 8, "nativeVirtualKeyCode": 8, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
            ws.send(json.dumps(payload))
        self.inject_js(ws, combo.split(":")[0], 1)
        payload = {"id": 162, "method": "Input.dispatchKeyEvent", "params": {"type": "keyDown", "modifiers": 0, "code": "Tab", "key":"Tab", "windowsVirtualKeyCode": 9, "nativeVirtualKeyCode": 9, "autoRepeat": False, "isKeypad": False, "isSystemKey": False}}
        ws.send(json.dumps(payload))
        self.inject_js(ws, combo.split(":")[1], 1)
        self.inject_js(ws, "login-button", 0)
        time.sleep(4)
        title = requests.get(f"http://localhost:{port}/json").json()[0]["title"]
        if title == "Spotify - Login":
            log(self.websocket_url, f"[ERROR] Couldnt login: {combo}")
            self.stream_failed += 1
            self.stream_current_failed += 1
            return
        if self.mute:
            time.sleep(2)
            payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": 'document.querySelectorAll("[aria-describedby=volume-icon]")[0].click()'}}
            ws.send(json.dumps(payload))
            payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": 'document.querySelectorAll("[data-testid=volume-bar]")[0].children[0].click()'}}
            ws.send(json.dumps(payload))
            time.sleep(2)
        for url in random.sample(self.links, k=len(self.links)):
            ea = '"/search"'
            payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f"document.querySelectorAll('[href={ea}]')[0].click()"}}
            ws.send(json.dumps(payload))
            time.sleep(2)
            self.inject_js(ws, url, 1)
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"keyDown","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False}}
            ws.send(json.dumps(payload))
            payload = {"id":1,"method":"Input.dispatchKeyEvent","params": {"type":"char","modifiers":0,"code":"Enter","key":"Enter","windowsVirtualKeyCode":13,"nativeVirtualKeyCode":13,"autoRepeat":False,"isKeypad":False,"isSystem":False, "text": "\r", "unmodifiedText": "\r"}}
            ws.send(json.dumps(payload))
            time.sleep(2)
            # ea = '"action-bar-row"'
            # payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f"document.querySelectorAll('[data-testid={ea}]')[0].children[0].click()"}}
            # ws.send(json.dumps(payload))
            for i in range(-(-self.pos//2)+1):
                payload = {"id":1337, "method":"Input.emulateTouchFromMouseEvent", "params":{"button": "none", "clickCount": 0, "deltaX": 0, "deltaY": -153.24323918368367, "modifiers": 0, "type": "mouseWheel", "x": 493, "y": 190}}
                ws.send(json.dumps(payload))
            if "show" in url:
                log(f"[ERROR] Cant stream Shows: {url}")
                continue
            if requests.get(url).text.split(" songs")[0].split()[-1] < self.pos - 1 or "episode" in url or "track" in url:
                ea = '"action-bar-row"'
                payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f"document.querySelectorAll('[data-testid={ea}]')[0].children[0].click()"}}
                ws.send(json.dumps(payload))
            else:
                ea = f"'{self.pos}'"
                payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f'document.querySelector("[aria-rowindex={ea}]").children[0].children[0].children[0].children[1].click()'}}
                ws.send(json.dumps(payload))
            log(self.websocket_url, f"[SUCCESS] Account successfully streaming: {combo}")
            self.streaming += 1
            if random.choices([1,0], [self.like/100, int(100-self.like)/100]):
                time.sleep(2)
                ea = '"action-bar-row"'
                payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f"document.querySelectorAll('[data-testid={ea}]')[0].children[1].click()"}}
                ws.send(json.dumps(payload))
                self.likes += 1
                log(self.websocket_url, f"[SUCCESS] Account successfully liked: {combo}")
            # if random.choices([1,0], [self.follow/100, int(100-self.follow)/100]):
            #     time.sleep(2)
            #     payload = {"id":1337, "method":"Runtime.evaluate", "params":{"expression": f"document.querySelectorAll('[data-testid={ea}]')[0].children[1].click()"}}
            #     ws.send(json.dumps(payload))
            #     self.follows += 1
            #     log(self.websocket_url, f"[SUCCESS] Account successfully followed: {combo}")
            time.sleep(wait*60)
        log(self.websocket_url, f"[DONE] Account done streaming: {combo}")
        self.streamed += 1
        self.streaming -= 1
        payload = {"id":1,"method":"Browser.crash"}
        ws.send(json.dumps(payload))

    def webhook(self, runtime, title):
        webhook = DiscordWebhook(username='Mjolnir AiO Tool', url=self.webhook_url, avatar_url="https://www.freepnglogos.com/uploads/spotify-logo-png/spotify-icon-marilyn-scott-0.png")
        # create embed object for webhook
        embed = DiscordEmbed(title=title, description=f'Total Streaming Accounts: {self.streaming}', color='1DB954')
        # set image
        runtime = 1 if runtime == 0  else runtime
        Minutes = list(range(int(runtime)+1))
        print(self.streams_mins, self.streaming_mins, self.like_mins)
        self.streams_mins[-1] = self.streamed
        self.streaming_mins[-1] = self.streaming
        self.like_mins[-1] = self.likes
        if len(Minutes) != len(self.streams_mins): Minutes = list(range(len(self.streams_mins)))
        Seconds = [round(x* 0.20,2) for x in range(len(self.streaming_mins))]

        gs = gridspec.GridSpec(2, 2)
        fig= plt.figure()
        fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
        fig.patch.set_facecolor('#2F3136')
        fig.suptitle('Your Mjolnir Desktop-Streamer Stats', color="#99AAB5")

        ax = plt.subplot(gs[1, 0]) # row 0, col 0
        ax.set_facecolor('#23272A')
        ax.set_title('Streamed')
        plt.plot(Minutes, self.streams_mins, color="#99AAB5")
        ax = plt.subplot(gs[1, 1]) # row 0, col 0
        ax.set_facecolor('#23272A')
        ax.set_title('Likes')
        plt.plot(Minutes, self.like_mins, color="#99AAB5")

        ax = plt.subplot(gs[0, :]) # row 0, col 0
        ax.set_facecolor('#23272A')
        ax.set_title('Streaming')
        plt.plot(Seconds, self.streaming_mins, color="#99AAB5")
        with tempfile.NamedTemporaryFile(suffix='.png', prefix=os.path.basename(__file__), delete=False) as tf:
            plt.savefig(tf.name)
            files = {'image': ('graph.png', open(tf.name, 'rb'))}
            r = requests.post("https://api.imgbb.com/1/upload?key=5b4141e2323a62c75b4fe2c5e5d58cec", files=files).json()
            url = r["data"]["display_url"].replace("\/", "/")
        embed.set_image(url=url)
        # add fields to embed
        embed.add_embed_field(name=':computer: Computer Name :computer:', value=socket.gethostname(), inline=False)
        embed.add_embed_field(name=':gear: CPU Usage :gear:', value=f"{str(100 - int(psutil.cpu_times_percent(interval=0.4, percpu=False).idle))} %", inline=False)
        embed.add_embed_field(name=':bar_chart: RAM Usage :bar_chart:', value=f"{psutil.virtual_memory().percent} %", inline=False)
        embed.add_embed_field(name=":file_cabinet: Threads :file_cabinet:", value=str(self.threads), inline=False)
        embed.add_embed_field(name=":stopwatch: Runtime :stopwatch:", value=f"{int(runtime)} Minutes", inline=False)
        embed.add_embed_field(name=":stopwatch: Maximal Runtime :stopwatch:", value=f"{int(self.max)} Minutes", inline=False)
        embed.add_embed_field(name=":stopwatch: Likes :stopwatch:", value=str(self.likes), inline=False)
        embed.add_embed_field(name=":white_check_mark: Accounts Streamed :white_check_mark:", value=str(self.streamed), inline=False)
        embed.add_embed_field(name=":chart_with_upwards_trend: Accounts Currently Streaming :chart_with_upwards_trend:", value=str(self.streaming), inline=False)
        embed.add_embed_field(name=":x: Failed Streams :x:", value=str(self.stream_failed), inline=False)
        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()

    def update_minutes(self):
        while self.current_streaming:
            print("0", self.streams_mins, self.streaming_mins, self.like_mins)
            self.streams_mins.append(self.streamed)
            self.like_mins.append(self.likes)
            print("1", self.streams_mins, self.streaming_mins, self.like_mins)
            time.sleep(60)
            print("2", self.streams_mins, self.streaming_mins, self.like_mins)

    def update_seconds(self):
        while self.current_streaming:
            self.streaming_mins.append(self.streaming)
            time.sleep(20)

    def threaded_webhook(self):
        print(1)
        threading.Thread(target=self.update_minutes).start()
        threading.Thread(target=self.update_seconds).start()
        runtimed = 1
        while self.current_streaming:
            time.sleep(600)
            if self.current_streaming:
                self.webhook(int(runtimed * 10), 'Your Mjolnir Desktop-Streamer Stats')
                runtimed += 1

    def thread(self, args):
        threading.Thread(target=self.threaded_streamer, args=(tuple(args))).start()

class WebStreamer:
    def __init__(self, combo_path, threads, proxies, link, max, like, pos, webhook, path):
        self.threads, self.count = int(threads) if threads else 10, 0
        self.combo_path, self.max, self.like, self.pos = combo_path.replace('"', ""), int(max) if max else 5, int(like) if like else 0, int(pos) if pos else 0
        self.proxies, self.webhook_url, self.websocket_url = proxies.split("\r\n"), webhook, path
        link = link.replace('"', "").replace(" ", "")
        if os.path.exists(link): self.links = open(link).read().splitlines()
        else: self.links = link.split(",")
        os.environ['WDM_LOG'], self.driver_exe = '0', ChromeDriverManager(print_first_line=False, log_level=0).install()

    def streamer(self):
        combos = open(self.combo_path, "r").read().splitlines()
        #Logging to serverq
        requests.post(f"{server}/streamer/web", json={"amount": len(combos)}, proxies=urllib.request.getproxies())
        if any(self.proxies): threading.Thread(target=self.proxy_pool).start() #Spawning ProxyPool on Port 8899
        while self.count < len(combos):
            for i in range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads):
                combo = combos[i]
                if i == range(int(len(combos) - self.count) if int(len(combos) - self.count) <= self.threads else self.threads)[-1]:
                    self.threaded_streamer(combo)
                else: threading.Thread(target=self.threaded_streamer, args=(combo)).start()
        log(self.websocket_url, "[DONE] Done liking with all accounts")

    def proxy_pool(self):
        log(self.websocket_url, "[PROXY] Spawning ProxyPool")
        proxy_pool = []
        for proxie in self.proxies: proxy_pool.extend(["--proxy-pool", proxie])
        try:
            with proxy.Proxy(["--log-level", "e", "--plugins" , "proxy.plugin.ProxyPoolPlugin", *proxy_pool]) as p:
                proxy.sleep_loop()
        except Exception as e: log(self.websocket_url, f"[ERROR] Couldnt spawn ProxyPool (Error: {str(e)})"); import traceback; print(traceback.format_exc())

    def threaded_streamer(self, combo):
        try:
            user, pw, rest =  combo.split(":", 2)
        except:
            user, pw = combo.split(":")
        options = Options()
        l = ['--log-level=3', '--lang=en', "--window-size=1920,1080", "--mute-audio", "--log-level=3", "disable-logging"]
        if any(self.proxies): l.append('--proxy-server="localhost:8899"')
        for item in l:
            options.add_argument(item)
        options.ignore_protected_mode_settings = True

        driver = wd.Chrome(self.driver_exe, options=options)
        driver.get("https://accounts.spotify.com/login")
        time.sleep(3)
        driver.find_element(By.ID, "login-username").send_keys(user)
        time.sleep(1)
        driver.find_element(By.ID, "login-password").send_keys(pw)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        i=0
        while not "status" in driver.current_url and i < 15:
            try: driver.find_element(By.ID, "login-button").click()
            except: pass
            time.sleep(2)
            if "status" in driver.current_url:
                break
            i+=1
        else:
            if i == 15:
                log(self.websocket_url, f"[ERROR] Couldnt login: {combo}")
                driver.quit()
                return
        time.sleep(5)
        try: driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except: pass
        for url in random.sample(self.links, k=len(self.links)):
            driver.get(url)
            for _ in range(15):
                try:
                    driver.execute_script('document.querySelector("[data-testid=play-button]").click()')
                    break
                except:
                    time.sleep(2)
            else:
                log(self.websocket_url, f"[ERROR] Couldnt stream with account: {combo}")
                driver.quit()
                return

            if random.choices([1,0], [self.like/100, int(100-self.like)/100]):
                play_buttons = driver.find_elements(By.XPATH, "//button[@data-testid='add-button']")
                for _, button in enumerate(play_buttons):
                    if _ == 0:
                        try:
                            button.click()
                        except ElementClickInterceptedException:
                            pass
                log(self.websocket_url, f"[SUCCESS] Account successfully liked: {combo}")
            time.sleep(5)
            driver.minimize_window()
            log(self.websocket_url, f"[SUCCESS] Account successfully streaming: {combo}")
            if self.max > 1: time.sleep(random.randint(int(self.max - 1), self.max)*60)
            else: time.sleep(self.max*60)
        log(self.websocket_url, f"[DONE] Account done streaming: {combo}")

@app.route("/dgen", methods=["POST"])
def dgen():
    amount, threads, names, passwords, proxies, webhook, gender, order, minAge, maxAge, alternative, output_path = request.json.get("amount"), request.json.get("threads"), request.json.get("names"), request.json.get("passwords"), request.json.get("proxies"), request.json.get("webhook"), request.json.get("gender"), request.json.get("order"), request.json.get("minAge"), request.json.get("maxAge"), request.json.get("alternative"), request.json.get("path")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    paths[path] = ["[INFO] Started Generator"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    generator = DesktopGenerator(path, proxies, minAge, maxAge, gender, order, alternative)
    threading.Thread(target=generator.generator, args=(amount, names, passwords, threads, output_path, webhook)).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/wgen", methods=["POST"])
def wgen():
    amount, threads, key, names, passwords, proxies, gender, minAge, maxAge, output_path = request.json.get("amount"), request.json.get("threads"), request.json.get("key"), request.json.get("names"), request.json.get("passwords"), request.json.get("proxies"), request.json.get("gender"), request.json.get("minAge"), request.json.get("maxAge"), request.json.get("path")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    paths[path] = ["[INFO] Started Generator"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    generator = WebGenerator(amount, threads, key, names, passwords, output_path, path, proxies, minAge, maxAge, gender)
    threading.Thread(target=generator.generator).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/rgen", methods=["POST"])
def rgen():
    amount, threads, names, passwords, proxies, output_path = request.json.get("amount"), request.json.get("threads"), request.json.get("names"), request.json.get("passwords"), request.json.get("proxies"), request.json.get("path")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not output_path: paths[path] = ["[INFO] Invalid Output Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Generator"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    generator = RequestGenerator(path, proxies)
    threading.Thread(target=generator.generator, args=(amount, threads, names, passwords, output_path)).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/dstream", methods=["POST"])
def dstream():
    link, threads, max, like, follow, mute, pos, proxies, webhook, combo_path = request.json.get("link"), request.json.get("threads"), request.json.get("max"), request.json.get("like"), request.json.get("follow"), request.json.get("mute"), request.json.get("pos"), request.json.get("proxies"), request.json.get("webhook"), request.json.get("path")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not link or "https://" not in link or "spotify" not in link: paths[path] = ["[INFO] Invalid Spotify URL"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    if not combo_path: paths[path] = ["[INFO] Invalid Combo Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Streamer"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    streamer = DesktopStreamer(combo_path, threads, proxies, link, max, like, follow, mute, pos, webhook, path)
    threading.Thread(target=streamer.streamer).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/wstream", methods=["POST"])
def wstream():
    link, threads, max, like, pos, proxies, webhook, combo_path = request.json.get("link"), request.json.get("threads"), request.json.get("max"), request.json.get("like"), request.json.get("pos"), request.json.get("proxies"), request.json.get("webhook"), request.json.get("path")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not link or "https://" not in link or "spotify" not in link: paths[path] = ["[INFO] Invalid Spotify URL"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    if not combo_path: paths[path] = ["[INFO] Invalid Combo Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Streamer"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    streamer = WebStreamer(combo_path, threads, proxies, link, max, like, pos, webhook, path)
    threading.Thread(target=streamer.streamer).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/liker", methods=["POST"])
def liker():
    link, threads, timeout, proxies, proxy_type, combo_path = request.json.get("link"), request.json.get("threads"), request.json.get("timeout"), request.json.get("proxies"), request.json.get("proxy_type"), request.json.get("path").replace('"', "")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not link or "https://" not in link or "spotify" not in link: paths[path] = ["[INFO] Invalid Spotify URL"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    if not combo_path: paths[path] = ["[INFO] Invalid Combo Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Liker"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    if not timeout: paths[path] += "[INFO] Invalid Timeout, using 10"
    liker = Liker(link, threads, timeout, proxies, proxy_type, combo_path, path)
    threading.Thread(target=liker.liker).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/checker", methods=["POST"])
def checker():
    threads, proxies, proxy_type, max, combo_path = request.json.get("threads"), request.json.get("proxies"), request.json.get("proxy_type"), request.json.get("max"), request.json.get("path").replace('"',  "")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not combo_path: paths[path] = ["[INFO] Invalid Combo Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Checker"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    if not max: paths[path] += "[INFO] Invalid Maximum, using 5"
    checker = Checker(threads, proxies, proxy_type, max, combo_path, path)
    threading.Thread(target=checker.checker).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/mchecker", methods=["POST"])
def mchecker():
    threads, proxies, max, combo_path = request.json.get("threads"), request.json.get("proxies"), request.json.get("max"), request.json.get("path").replace('"',  "")
    path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    if not combo_path: paths[path] = ["[INFO] Invalid Combo Path"]; return f"ws://mjolnir.tool/websockets?ws={path}"
    paths[path] = ["[INFO] Started Checker"]
    paths[path] += "[INFO] Coded by Vinyzu (https://github.com/Vinyzu/MjolnirAiO)"
    if not max: paths[path] += "[INFO] Invalid Maximum, using 5"
    checker = MailChecker(threads, proxies, max, combo_path, path)
    threading.Thread(target=checker.checker).start()
    return f"ws://mjolnir.tool/websockets?ws={path}"

@app.route("/")
def main():
    return redirect("http://mjolnir.tool/generator", code=302)

@app.route("/<ea>")
def run_general(ea):
    try: return render_template(f"{ea}.html")
    except: return redirect("http://mjolnir.tool/generator", code=302)

if __name__ == '__main__':
    #Check Version from Server and open Download Url if not newest
    multiprocessing.freeze_support()
    try: hostsman.Host().add("mjolnir.tool")
    except: PySimpleGUI.Popup('You have to run Mjolnir as Administrator!', background_color='#111', button_color="#818181",  no_titlebar=True, font=('Monaco Monospace', 11)); exit()
    webbrowser.open("http://mjolnir.tool")
    app.run("mjolnir.tool", 80, debug=True, use_reloader=False)
