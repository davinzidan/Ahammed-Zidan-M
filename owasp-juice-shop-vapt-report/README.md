# OWASP Juice Shop VAPT Report

This repository contains a practical Vulnerability Assessment and Penetration Testing (VAPT) project performed against OWASP Juice Shop, an intentionally vulnerable web application used for security training and AppSec practice.

> Scope note: All testing was performed locally against a deliberately vulnerable lab target running on `localhost`. No third-party production systems were tested.

## Project Overview

- Target application: OWASP Juice Shop
- Local URL: `http://localhost:3001`
- Testing type: Web application VAPT
- Focus areas: OWASP Top 10, authentication bypass, information disclosure, security misconfiguration, exposed files, and security headers
- Date: 27 June 2026

## Tools Used

- Docker
- Nmap
- Nikto
- Browser-based manual testing
- OWASP Juice Shop

## Methodology

1. Deployed OWASP Juice Shop locally using Docker.
2. Performed service discovery with Nmap.
3. Ran automated web checks with Nikto.
4. Manually verified exposed paths and files.
5. Tested authentication bypass using SQL injection.
6. Documented confirmed findings with evidence, impact, and remediation.

## Key Findings

| ID | Finding | Severity |
| --- | --- | --- |
| F-01 | SQL Injection Authentication Bypass | Critical |
| F-02 | Confidential Document Exposure | High |
| F-03 | Exposed FTP Directory Listing | Medium |
| F-04 | Verbose Error / Stack Trace Disclosure | Medium |
| F-05 | Missing Security Headers | Medium |
| F-06 | Overly Permissive CORS Header | Medium |
| F-07 | Robots.txt Sensitive Path Disclosure | Low |

## Evidence

Evidence screenshots are stored in [`screenshots/`](screenshots/).

Selected screenshots:

- Docker target running: [`01-docker-juice-shop-running.png`](screenshots/01-docker-juice-shop-running.png)
- Nmap scan result: [`03-nmap-scan-result.png`](screenshots/03-nmap-scan-result.png)
- Nikto scan result: [`04-nikto-scan-result.png`](screenshots/04-nikto-scan-result.png)
- Exposed FTP directory: [`05-ftp-directory-listing.png`](screenshots/05-ftp-directory-listing.png)
- SQL injection login bypass: [`09-sqli-admin-login-bypass.png`](screenshots/09-sqli-admin-login-bypass.png)

## Report

The full report is available here:

- [`report/OWASP-Juice-Shop-VAPT-Report.pdf`](report/OWASP-Juice-Shop-VAPT-Report.pdf)
- [`report/OWASP-Juice-Shop-VAPT-Report.md`](report/OWASP-Juice-Shop-VAPT-Report.md)

## What I Learned

This project strengthened my practical understanding of web application testing, authentication bypass, information disclosure, exposed file risks, scanner validation, and professional vulnerability reporting. It also helped me practice translating technical findings into business impact and remediation guidance.
