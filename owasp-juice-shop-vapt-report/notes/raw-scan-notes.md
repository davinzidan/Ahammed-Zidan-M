# Raw Scan Notes

## Target

- Application: OWASP Juice Shop
- Local URL: `http://localhost:3001`
- Runtime: Docker container mapped from container port `3000` to host port `3001`
- Testing date: 27 June 2026

## Nmap Result Summary

Command:

```bash
nmap -sV -p 3001 localhost
```

Result:

```text
PORT     STATE SERVICE VERSION
3001/tcp open  nessus?
```

Nmap did not accurately identify the service, but the HTTP response contained:

```text
<title>OWASP Juice Shop</title>
```

Interpretation:

Port `3001/tcp` was open and serving an HTTP web application identified as OWASP Juice Shop.

## Nikto Result Summary

Command:

```bash
nikto -h http://localhost:3001
```

Relevant observations:

```text
Retrieved access-control-allow-origin header: *.
Uncommon header(s) 'x-recruiting' found, with contents: /#/jobs.
/robots.txt: contains 1 entry which should be manually viewed.
Suggested security header missing: strict-transport-security.
Suggested security header missing: referrer-policy.
Suggested security header missing: permissions-policy.
Suggested security header missing: content-security-policy.
/ftp/: This might be interesting.
/public/: This might be interesting.
The X-Content-Type-Options header is not set.
```

Manual verification notes:

- `/ftp/` was confirmed as a browsable directory listing.
- `/robots.txt` disclosed `/ftp`.
- `/public/` did not expose useful content during manual verification.
- JSON endpoints reported by Nikto routed back to the frontend and were not treated as confirmed sensitive data exposure.
- `.htpasswd`, `.bash_history`, and `.sh_history` were not treated as confirmed findings because they require further verification and scanner output alone may include false positives.

## Confirmed Manual Findings

- `/ftp/` directory listing exposed files including `acquisitions.md`, `package.json.bak`, `incident-support.kdbx`, and `suspicious_errors.yml`.
- `/ftp/acquisitions.md` exposed a confidential document.
- `/ftp/package.json.bak` returned a verbose error with Express version and internal file paths.
- Login form was vulnerable to SQL injection authentication bypass using:

```text
' OR 1=1--
```
