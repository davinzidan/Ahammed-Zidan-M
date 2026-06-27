### PortSwigger File Upload RCE Lab

Performed a Burp Suite based assessment of a PortSwigger Web Security Academy file upload lab. Exploited an unrestricted avatar upload by uploading a PHP payload, verified the upload transaction in Burp HTTP history, executed the uploaded file from a web-accessible directory, and documented sensitive file disclosure from `/home/carlos/secret` with impact and remediation.

**Tools:** Burp Suite, Burp Browser, HTTP history, PHP  
**Focus:** File upload vulnerability, remote code execution, evidence-based reporting  
**GitHub:** https://github.com/davinzidan/Ahammed-Zidan-M/tree/main/portswigger-file-upload-rce
