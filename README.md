# cloudflare-ddns

Python dynamic DNS client for the CloudFlare v4 API

## Installation

```
git clone https://github.com/ianunruh/cloudflare-ddns.git
cd cloudflare-ddns

pip install -r requirements.txt
```

## Usage

```
export CF_EMAIL=YOUR_CLOUDFLARE_EMAIL
export CF_API_KEY=YOUR_CLOUDFLARE_API_KEY

./cloudflare.py YOUR_ZONE YOUR_RECORD
```
