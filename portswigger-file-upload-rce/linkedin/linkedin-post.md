# LinkedIn Post Draft

I completed another practical Web Application Security lab using PortSwigger Web Security Academy and Burp Suite Community Edition.

This lab focused on exploiting an unrestricted file upload vulnerability that led to server-side PHP execution.

What I practiced:

- Using Burp's built-in browser for authenticated testing
- Capturing upload traffic in Burp Proxy HTTP history
- Analyzing multipart file upload requests
- Uploading a controlled PHP payload in an authorized lab
- Accessing the uploaded file from a web-accessible directory
- Demonstrating sensitive file disclosure through server-side code execution
- Writing the finding with impact, evidence, and remediation

Finding:

Remote Code Execution via Unrestricted PHP File Upload

Key takeaway:

File upload features must not rely only on client-side controls or filenames. Uploaded files should be validated server-side, stored safely, renamed, and prevented from executing as server-side code.

GitHub: https://github.com/davinzidan/Ahammed-Zidan-M/tree/main/portswigger-file-upload-rce

Portfolio: https://davinzidan.github.io/cybersecurity-portfolio/

#CyberSecurity #VAPT #AppSec #BurpSuite #PortSwigger #WebSecurity #PenetrationTesting #OWASP
