# Candidate Data Sources & Connector Strategy Assessment

## Evaluated Data Sources (5 Candidates)

1. **Deterministic Demo / CSV Connector (Selected for Baseline MVP)**
   * **Authorization**: Fully Authorized (Internal/User Provided)
   * **Coverage**: Configurable / Infinite
   * **Cost**: Free ($0)
   * **Rate Limits**: None
   * **Verdict**: Primary source for testing end-to-end data pipelines without external credential blockers.

2. **OpenCorporates API**
   * **Authorization**: Official Public Registry API
   * **Coverage**: Global official company register records
   * **Cost**: Free tier / Paid API
   * **Rate Limits**: Restricted on free tier
   * **Verdict**: Candidate for official company name and registration verification.

3. **Clearbit / Hubspot Enrichment API**
   * **Authorization**: Official Commercial API
   * **Coverage**: High domain-level tech and firmographic coverage
   * **Cost**: Paid (Freemium trial)
   * **Rate Limits**: Standard API quota
   * **Verdict**: Good live connector candidate if API key is provided.

4. **Hunter.io API**
   * **Authorization**: Official API
   * **Coverage**: Professional domain email patterns and company verification
   * **Cost**: Free tier (25 searches/mo)
   * **Rate Limits**: 25 requests/month
   * **Verdict**: Candidate for contact domain metadata verification.

5. **Public Web Scraping / Google Search API (Custom Search JSON API)**
   * **Authorization**: Official API Key required
   * **Coverage**: Real-time web discovery
   * **Cost**: 100 free queries/day
   * **Rate Limits**: 100 queries/day
   * **Verdict**: Primary live connector for discovery jobs in Week 2.

## Selected Initial Strategy
* **Week 1-2 Focus**: CSV Upload + Deterministic Demo Mock + Public Web API wrapper with safe retries, backoff, and strict terms compliance.