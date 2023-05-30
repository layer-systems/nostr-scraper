# nostr-scraper
Scrape Relays to your own relay.

# Docker
```bash
docker build -t nostr-scraper:local . && docker run --rm -e INPUT_RELAY="wss://relay.nostr.band" -e OUTPUT_RELAY="wss://relay.example.com" nostr-scraper:local
```