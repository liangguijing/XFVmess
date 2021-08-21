
import base64
import dns.resolver
import re
import requests
import urllib.parse as urlparse


def bs64_decode(string, encoding="utf-8"):
    """
    -/ 避免网页编码+引起的问题
    """
    string += "=" * (4 - len(string) % 4)
    return base64.b64decode(string, altchars=b"-/").decode(encoding)


def bs64_encode(string, encoding="utf-8"):
    b = bytes(string, encoding)
    return base64.b64encode(b).decode(encoding)


def get_unicode(string):
    return string.encode("unicode_escape").decode("ascii")


def url_decode(string):
    return urlparse.unquote(string, "utf-8")


def url_encode(string):
    return urlparse.quote(string, "utf-8")


def get_ip_address(domain):
    try:
        r = dns.resolver.resolve(domain, 'A')
        return "".join([str(i) for a in r.response.answer for i in a.items if i.rdtype == 1][0])
    except Exception as e:
        print(f"获取IP地址出错{domain}", e)
        return "127.0.0.1"


def get_server_location(server):
    ip_rex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    rex = re.compile(r"[0-9a-zA-Z_.]+")
    if ip_rex.search(server):
        ip = server
    elif rex.match(server):
        ip = get_ip_address(server)
    else:
        return server
    url = "https://api.ip.sb/geoip/" + ip
    response = requests.get(url)
    if response.status_code == 200:
        if response.json()["isp"] == "Cloudflare":
            return response.json()["isp"] + "-" + response.json()["country_code"]
        return response.json()["country"] + "-" + server


def get_github_file_sha(token, url):
    url = url
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token,
    }
    response = requests.get(url, headers=headers).json()
    if response.get("sha"):
        return response["sha"]
    return ""


def update_github_file(token, url, string):
    url = url
    headers = {
        "accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token,
    }
    data = {
        "content": bs64_encode(string),
        "message": "update by actions",
        "sha": get_github_file_sha(token, url)
    }
    resp = requests.put(url=url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"{ url } updated.")
    else:
        print(f"update { url }  failed!")


country_mapping = {
    "Ascension Island": "🇦🇨",
    "Andorra": "🇦🇩",
    "United Arab Emirates": "🇦🇪",
    "Afghanistan": "🇦🇫",
    "Antigua & Barbuda": "🇦🇬",
    "Anguilla": "🇦🇮",
    "Albania": "🇦🇱",
    "Armenia": "🇦🇲",
    "Angola": "🇦🇴",
    "Antarctica": "🇦🇶",
    "Argentina": "🇦🇷",
    "American Samoa": "🇦🇸",
    "Austria": "🇦🇹",
    "Australia": "🇦🇺",
    "Aruba": "🇦🇼",
    "Åland Islands": "🇦🇽",
    "Azerbaijan": "🇦🇿",
    "Bosnia & Herzegovina": "🇧🇦",
    "Barbados": "🇧🇧",
    "Bangladesh": "🇧🇩",
    "Belgium": "🇧🇪",
    "Burkina Faso": "🇧🇫",
    "Bulgaria": "🇧🇬",
    "Bahrain": "🇧🇭",
    "Burundi": "🇧🇮",
    "Benin": "🇧🇯",
    "St. Barthélemy": "🇧🇱",
    "Bermuda": "🇧🇲",
    "Brunei": "🇧🇳",
    "Bolivia": "🇧🇴",
    "Caribbean Netherlands": "🇧🇶",
    "Brazil": "🇧🇷",
    "Bahamas": "🇧🇸",
    "Bhutan": "🇧🇹",
    "Bouvet Island": "🇧🇻",
    "Botswana": "🇧🇼",
    "Belarus": "🇧🇾",
    "Belize": "🇧🇿",
    "Canada": "🇨🇦",
    "Cocos (Keeling) Islands": "🇨🇨",
    "Congo - Kinshasa": "🇨🇩",
    "Central African Republic": "🇨🇫",
    "Congo - Brazzaville": "🇨🇬",
    "Switzerland": "🇨🇭",
    "Côte d’Ivoire": "🇨🇮",
    "Cook Islands": "🇨🇰",
    "Chile": "🇨🇱",
    "Cameroon": "🇨🇲",
    "China": "🇨🇳",
    "Colombia": "🇨🇴",
    "Clipperton Island": "🇨🇵",
    "Costa Rica": "🇨🇷",
    "Cuba": "🇨🇺",
    "Cape Verde": "🇨🇻",
    "Curaçao": "🇨🇼",
    "Christmas Island": "🇨🇽",
    "Cyprus": "🇨🇾",
    "Czechia": "🇨🇿",
    "Germany": "🇩🇪",
    "Diego Garcia": "🇩🇬",
    "Djibouti": "🇩🇯",
    "Denmark": "🇩🇰",
    "Dominica": "🇩🇲",
    "Dominican Republic": "🇩🇴",
    "Algeria": "🇩🇿",
    "Ceuta & Melilla": "🇪🇦",
    "Ecuador": "🇪🇨",
    "Estonia": "🇪🇪",
    "Egypt": "🇪🇬",
    "Western Sahara": "🇪🇭",
    "Eritrea": "🇪🇷",
    "Spain": "🇪🇸",
    "Ethiopia": "🇪🇹",
    "European Union": "🇪🇺",
    "Finland": "🇫🇮",
    "Fiji": "🇫🇯",
    "Falkland Islands": "🇫🇰",
    "Micronesia": "🇫🇲",
    "Faroe Islands": "🇫🇴",
    "France": "🇫🇷",
    "Gabon": "🇬🇦",
    "United Kingdom": "🇬🇧",
    "Grenada": "🇬🇩",
    "Georgia": "🇬🇪",
    "French Guiana": "🇬🇫",
    "Guernsey": "🇬🇬",
    "Ghana": "🇬🇭",
    "Gibraltar": "🇬🇮",
    "Greenland": "🇬🇱",
    "Gambia": "🇬🇲",
    "Guinea": "🇬🇳",
    "Guadeloupe": "🇬🇵",
    "Equatorial Guinea": "🇬🇶",
    "Greece": "🇬🇷",
    "South Georgia & South Sandwich Islands": "🇬🇸",
    "Guatemala": "🇬🇹",
    "Guam": "🇬🇺",
    "Guinea-Bissau": "🇬🇼",
    "Guyana": "🇬🇾",
    "Hong Kong SAR China": "🇭🇰",
    "Heard & McDonald Islands": "🇭🇲",
    "Honduras": "🇭🇳",
    "Croatia": "🇭🇷",
    "Haiti": "🇭🇹",
    "Hungary": "🇭🇺",
    "Canary Islands": "🇮🇨",
    "Indonesia": "🇮🇩",
    "Ireland": "🇮🇪",
    "Israel": "🇮🇱",
    "Isle of Man": "🇮🇲",
    "India": "🇮🇳",
    "British Indian Ocean Territory": "🇮🇴",
    "Iraq": "🇮🇶",
    "Iran": "🇮🇷",
    "Iceland": "🇮🇸",
    "Italy": "🇮🇹",
    "Jersey": "🇯🇪",
    "Jamaica": "🇯🇲",
    "Jordan": "🇯🇴",
    "Japan": "🇯🇵",
    "Kenya": "🇰🇪",
    "Kyrgyzstan": "🇰🇬",
    "Cambodia": "🇰🇭",
    "Kiribati": "🇰🇮",
    "Comoros": "🇰🇲",
    "St. Kitts & Nevis": "🇰🇳",
    "North Korea": "🇰🇵",
    "South Korea": "🇰🇷",
    "Kuwait": "🇰🇼",
    "Cayman Islands": "🇰🇾",
    "Kazakhstan": "🇰🇿",
    "Laos": "🇱🇦",
    "Lebanon": "🇱🇧",
    "St. Lucia": "🇱🇨",
    "Liechtenstein": "🇱🇮",
    "Sri Lanka": "🇱🇰",
    "Liberia": "🇱🇷",
    "Lesotho": "🇱🇸",
    "Lithuania": "🇱🇹",
    "Luxembourg": "🇱🇺",
    "Latvia": "🇱🇻",
    "Libya": "🇱🇾",
    "Morocco": "🇲🇦",
    "Monaco": "🇲🇨",
    "Moldova": "🇲🇩",
    "Montenegro": "🇲🇪",
    "St. Martin": "🇲🇫",
    "Madagascar": "🇲🇬",
    "Marshall Islands": "🇲🇭",
    "North Macedonia": "🇲🇰",
    "Mali": "🇲🇱",
    "Myanmar (Burma)": "🇲🇲",
    "Mongolia": "🇲🇳",
    "Macao Sar China": "🇲🇴",
    "Northern Mariana Islands": "🇲🇵",
    "Martinique": "🇲🇶",
    "Mauritania": "🇲🇷",
    "Montserrat": "🇲🇸",
    "Malta": "🇲🇹",
    "Mauritius": "🇲🇺",
    "Maldives": "🇲🇻",
    "Malawi": "🇲🇼",
    "Mexico": "🇲🇽",
    "Malaysia": "🇲🇾",
    "Mozambique": "🇲🇿",
    "Namibia": "🇳🇦",
    "New Caledonia": "🇳🇨",
    "Niger": "🇳🇪",
    "Norfolk Island": "🇳🇫",
    "Nigeria": "🇳🇬",
    "Nicaragua": "🇳🇮",
    "Netherlands": "🇳🇱",
    "Norway": "🇳🇴",
    "Nepal": "🇳🇵",
    "Nauru": "🇳🇷",
    "Niue": "🇳🇺",
    "New Zealand": "🇳🇿",
    "Oman": "🇴🇲",
    "Panama": "🇵🇦",
    "Peru": "🇵🇪",
    "French Polynesia": "🇵🇫",
    "Papua New Guinea": "🇵🇬",
    "Philippines": "🇵🇭",
    "Pakistan": "🇵🇰",
    "Poland": "🇵🇱",
    "St. Pierre & Miquelon": "🇵🇲",
    "Pitcairn Islands": "🇵🇳",
    "Puerto Rico": "🇵🇷",
    "Palestinian Territories": "🇵🇸",
    "Portugal": "🇵🇹",
    "Palau": "🇵🇼",
    "Paraguay": "🇵🇾",
    "Qatar": "🇶🇦",
    "Réunion": "🇷🇪",
    "Romania": "🇷🇴",
    "Serbia": "🇷🇸",
    "Russia": "🇷🇺",
    "Rwanda": "🇷🇼",
    "Saudi Arabia": "🇸🇦",
    "Solomon Islands": "🇸🇧",
    "Seychelles": "🇸🇨",
    "Sudan": "🇸🇩",
    "Sweden": "🇸🇪",
    "Singapore": "🇸🇬",
    "St. Helena": "🇸🇭",
    "Slovenia": "🇸🇮",
    "Svalbard & Jan Mayen": "🇸🇯",
    "Slovakia": "🇸🇰",
    "Sierra Leone": "🇸🇱",
    "San Marino": "🇸🇲",
    "Senegal": "🇸🇳",
    "Somalia": "🇸🇴",
    "Suriname": "🇸🇷",
    "South Sudan": "🇸🇸",
    "São Tomé & Príncipe": "🇸🇹",
    "El Salvador": "🇸🇻",
    "Sint Maarten": "🇸🇽",
    "Syria": "🇸🇾",
    "Eswatini": "🇸🇿",
    "Tristan Da Cunha": "🇹🇦",
    "Turks & Caicos Islands": "🇹🇨",
    "Chad": "🇹🇩",
    "French Southern Territories": "🇹🇫",
    "Togo": "🇹🇬",
    "Thailand": "🇹🇭",
    "Tajikistan": "🇹🇯",
    "Tokelau": "🇹🇰",
    "Timor-Leste": "🇹🇱",
    "Turkmenistan": "🇹🇲",
    "Tunisia": "🇹🇳",
    "Tonga": "🇹🇴",
    "Turkey": "🇹🇷",
    "Trinidad & Tobago": "🇹🇹",
    "Tuvalu": "🇹🇻",
    "Taiwan": "🇹🇼",
    "Tanzania": "🇹🇿",
    "Ukraine": "🇺🇦",
    "Uganda": "🇺🇬",
    "U.S. Outlying Islands": "🇺🇲",
    "United Nations": "🇺🇳",
    "United States": "🇺🇸",
    "Uruguay": "🇺🇾",
    "Uzbekistan": "🇺🇿",
    "Vatican City": "🇻🇦",
    "St. Vincent & Grenadines": "🇻🇨",
    "Venezuela": "🇻🇪",
    "British Virgin Islands": "🇻🇬",
    "U.S. Virgin Islands": "🇻🇮",
    "Vietnam": "🇻🇳",
    "Vanuatu": "🇻🇺",
    "Wallis & Futuna": "🇼🇫",
    "Samoa": "🇼🇸",
    "Kosovo": "🇽🇰",
    "Yemen": "🇾🇪",
    "Mayotte": "🇾🇹",
    "South Africa": "🇿🇦",
    "Zambia": "🇿🇲",
    "Zimbabwe": "🇿🇼",
}
