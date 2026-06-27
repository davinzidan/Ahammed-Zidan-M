# OWASP Juice Shop VAPT Report

**Prepared by:** Ahammed Zidan M  
**Test Date:** 27 June 2026  
**Target:** OWASP Juice Shop running locally at `http://localhost:3001`  
**Assessment Type:** Web Application Vulnerability Assessment and Penetration Testing  

## 1. Executive Summary

This assessment was performed against OWASP Juice Shop, an intentionally vulnerable web application deployed locally in a Docker container. The goal was to practice a realistic VAPT workflow: reconnaissance, automated scanning, manual verification, exploitation of selected vulnerabilities, evidence collection, and professional reporting.

The assessment identified multiple vulnerabilities across authentication, information disclosure, directory exposure, error handling, and security headers. The most severe finding was a SQL injection authentication bypass that allowed administrative login without valid credentials.

## 2. Scope

### In Scope

- Local OWASP Juice Shop instance
- Host URL: `http://localhost:3001`
- Web application functionality exposed through the local browser
- Publicly accessible application paths and files

### Out of Scope

- Any third-party production system
- Denial-of-service testing
- Social engineering
- Attacks against Docker, the host OS, or external networks

## 3. Tools Used

- Docker
- Nmap
- Nikto
- Browser-based manual testing
- OWASP Juice Shop

## 4. Methodology

The assessment followed a lightweight VAPT methodology:

1. Deployed OWASP Juice Shop locally using Docker.
2. Confirmed target availability in the browser.
3. Performed service discovery with Nmap.
4. Ran Nikto for automated web server checks.
5. Manually verified scanner findings.
6. Exploited authentication bypass using a SQL injection payload.
7. Captured evidence screenshots.
8. Documented business impact and remediation guidance.

## 5. Reconnaissance Summary

Nmap service detection was performed against localhost on port `3001`.

```bash
nmap -sV -p 3001 localhost
```

The scan confirmed that TCP port `3001` was open and serving an HTTP web application. Although Nmap did not identify the service accurately, the HTTP response contained the application title `OWASP Juice Shop`, confirming the target.

Evidence:

- `screenshots/03-nmap-scan-result.png`

## 6. Automated Scan Summary

Nikto was used to perform an automated web scan.

```bash
nikto -h http://localhost:3001
```

Nikto identified several issues and interesting paths, including:

- Wildcard CORS header: `Access-Control-Allow-Origin: *`
- Missing security headers
- `/robots.txt`
- `/ftp/`
- Uncommon `X-Recruiting` header

Automated scanner output was manually reviewed before converting issues into report findings.

Evidence:

- `screenshots/04-nikto-scan-result.png`

## 7. Findings Summary

| ID | Finding | Severity |
| --- | --- | --- |
| F-01 | SQL Injection Authentication Bypass | Critical |
| F-02 | Confidential Document Exposure | High |
| F-03 | Exposed FTP Directory Listing | Medium |
| F-04 | Verbose Error / Stack Trace Disclosure | Medium |
| F-05 | Missing Security Headers | Medium |
| F-06 | Overly Permissive CORS Header | Medium |
| F-07 | Robots.txt Sensitive Path Disclosure | Low |

## 8. Detailed Findings

## F-01: SQL Injection Authentication Bypass

**Severity:** Critical  
**Affected Function:** Login page  
**Payload Used:** `' OR 1=1--`

### Description

The login function was vulnerable to SQL injection. By entering a crafted SQL payload into the email field and any value in the password field, authentication was bypassed and administrative access was obtained.

### Evidence

After submitting the payload, the application displayed a success message stating that the `Login Admin` challenge was solved, indicating successful login as the admin user.

Evidence screenshots:

- `screenshots/09-sqli-admin-login-bypass.png`
- `screenshots/10-admin-session-evidence.png`

### Impact

An attacker could bypass authentication and gain unauthorized administrative access without valid credentials. This could lead to account takeover, data exposure, privilege abuse, and full compromise of application functionality.

### Recommendation

Use parameterized queries or prepared statements, validate and sanitize user input, avoid string concatenation in database queries, implement secure authentication controls, and monitor suspicious login attempts.

## F-02: Confidential Document Exposure

**Severity:** High  
**Affected URL:** `http://localhost:3001/ftp/acquisitions.md`

### Description

A confidential internal document was publicly accessible through the exposed `/ftp/` directory. The document contained a clear confidentiality warning and business-sensitive information related to planned company acquisitions.

### Evidence

The file `acquisitions.md` contained the statement `This document is confidential! Do not distribute!` and described planned acquisitions.

Evidence screenshot:

- `screenshots/08-confidential-document-exposure.png`

### Impact

Unauthorized access to confidential business documents could lead to information disclosure, reputational damage, insider trading risks, and competitive intelligence exposure.

### Recommendation

Remove confidential documents from publicly accessible directories, enforce authentication and authorization checks for sensitive files, disable directory listing, and implement secure file storage with proper access control.

## F-03: Exposed FTP Directory Listing

**Severity:** Medium  
**Affected URL:** `http://localhost:3001/ftp/`

### Description

The application exposed a publicly accessible directory listing at `/ftp/`. The directory contained multiple files, including backup files, markdown documents, package files, and an encrypted database file.

### Evidence

The `/ftp/` endpoint displayed a browsable directory containing files such as:

- `acquisitions.md`
- `coupons_2013.md.bak`
- `incident-support.kdbx`
- `package.json.bak`
- `suspicious_errors.yml`

Evidence screenshot:

- `screenshots/05-ftp-directory-listing.png`

### Impact

An attacker could use exposed files to gather information about the application, identify backup files, analyze package or dependency information, or attempt to retrieve sensitive documents.

### Recommendation

Disable public directory listing, restrict access to sensitive file paths, remove backup and configuration files from the web root, and enforce proper access controls for file storage locations.

## F-04: Verbose Error / Stack Trace Disclosure

**Severity:** Medium  
**Affected URL:** `http://localhost:3001/ftp/package.json.bak`

### Description

When attempting to access a restricted backup file, the application returned a verbose `403` error page containing internal framework details, Express version information, file paths, and stack trace data.

### Evidence

The response disclosed:

- `OWASP Juice Shop (Express ^4.22.1)`
- `/juice-shop/build/routes/fileServer.js`
- `/juice-shop/node_modules/express/`

Evidence screenshot:

- `screenshots/07-verbose-error-disclosure.png`

### Impact

Verbose error messages can help attackers fingerprint the technology stack, identify framework versions, understand internal routing logic, and plan targeted attacks.

### Recommendation

Disable verbose error messages in production, return generic error pages to users, avoid exposing framework versions and internal file paths, and log detailed errors server-side only.

## F-05: Missing Security Headers

**Severity:** Medium  
**Affected URL:** `http://localhost:3001/`

### Description

Nikto identified multiple missing recommended security headers, including:

- `Content-Security-Policy`
- `Referrer-Policy`
- `Permissions-Policy`
- `Strict-Transport-Security`
- `X-Content-Type-Options`

### Evidence

Nikto reported the missing headers during the automated scan.

Evidence screenshot:

- `screenshots/04-nikto-scan-result.png`

### Impact

Missing security headers can increase exposure to client-side attacks such as cross-site scripting, clickjacking, data leakage through referrers, MIME sniffing, and unsafe browser feature access.

### Recommendation

Implement appropriate HTTP security headers, including Content Security Policy, Referrer-Policy, Permissions-Policy, Strict-Transport-Security where HTTPS is used, and X-Content-Type-Options.

## F-06: Overly Permissive CORS Header

**Severity:** Medium  
**Affected URL:** `http://localhost:3001/`

### Description

The application returned a wildcard CORS header:

```text
Access-Control-Allow-Origin: *
```

### Evidence

Nikto detected the permissive CORS header during the automated scan.

Evidence screenshot:

- `screenshots/04-nikto-scan-result.png`

### Impact

Overly permissive CORS policies may allow untrusted origins to interact with application resources. If combined with sensitive endpoints or weak authentication controls, this can increase the risk of cross-origin data exposure.

### Recommendation

Restrict CORS to explicitly trusted origins, avoid using wildcard origins for sensitive applications, and review whether credentials or sensitive data can be accessed cross-origin.

## F-07: Robots.txt Sensitive Path Disclosure

**Severity:** Low  
**Affected URL:** `http://localhost:3001/robots.txt`

### Description

The `robots.txt` file disclosed the `/ftp` directory:

```text
User-agent: *
Disallow: /ftp
```

### Evidence

The disclosed path led to the discovery of a publicly browsable `/ftp/` directory.

Evidence screenshot:

- `screenshots/06-robots-txt-discloses-ftp.png`

### Impact

Robots.txt is publicly accessible and should not be used as an access control mechanism. Disclosing sensitive paths can help attackers discover hidden directories and files.

### Recommendation

Do not rely on `robots.txt` to protect sensitive paths. Remove sensitive path references where possible and enforce authentication and authorization controls on the server side.

## 9. False Positives / Not Confirmed

Nikto reported several possible sensitive JSON endpoints and shell history files. During manual review, some paths routed back to the Juice Shop frontend or were not verified as exposing sensitive data. These were not included as confirmed findings.

## 10. Conclusion

This VAPT project demonstrated a practical web application security testing workflow from reconnaissance through exploitation and reporting. The most critical risk identified was SQL injection authentication bypass, followed by multiple information disclosure and security misconfiguration issues.

The assessment reinforced the importance of secure query handling, access control, safe file storage, generic error handling, secure HTTP headers, and manual validation of scanner findings.
