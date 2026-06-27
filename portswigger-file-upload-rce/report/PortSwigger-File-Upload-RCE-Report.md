# PortSwigger File Upload RCE Report

## Executive Summary

A file upload vulnerability was tested in an authorized PortSwigger Web Security Academy lab. The application allowed a PHP file to be uploaded through the avatar upload feature and stored the file in a web-accessible directory. When the uploaded file was requested, the server executed the PHP code and disclosed the contents of `/home/carlos/secret`.

This demonstrates a high-impact unrestricted file upload weakness that can lead to remote code execution and sensitive file disclosure.

## Scope

- Target: Temporary PortSwigger Web Security Academy lab instance
- Lab: Remote code execution via web shell upload
- Account used: `wiener`
- Tools: Burp Suite Community Edition and Burp built-in browser
- Activity: Authorized lab testing only

## Methodology

1. Accessed the PortSwigger lab using Burp's built-in browser.
2. Logged in as the provided normal user.
3. Located the avatar upload feature under the account page.
4. Uploaded a PHP payload as the avatar file.
5. Reviewed the upload transaction in Burp Proxy HTTP history.
6. Requested the uploaded PHP file from the `/files/avatars/` path.
7. Verified that server-side PHP execution disclosed `/home/carlos/secret`.
8. Submitted the disclosed secret to solve the lab.

## Finding 1: Remote Code Execution via Unrestricted PHP File Upload

**Severity:** Critical  
**Category:** File Upload Vulnerability / Remote Code Execution  
**Affected Feature:** Avatar upload  
**Affected Endpoint:** `/my-account/avatar`

### Description

The avatar upload feature accepted a PHP file and stored it in a web-accessible directory. The uploaded file could then be accessed from `/files/avatars/portswigger-file-upload-shell.php`. Instead of serving the file as static content, the server executed the PHP code.

The uploaded payload read the contents of `/home/carlos/secret`, proving that attacker-controlled server-side code execution was possible in the lab environment.

### Payload

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

### Evidence

- The account page exposed an avatar upload form.
- Burp Proxy HTTP history captured a successful `POST /my-account/avatar` request.
- The server response confirmed that `avatars/portswigger-file-upload-shell.php` was uploaded.
- Accessing `/files/avatars/portswigger-file-upload-shell.php` returned the contents of `/home/carlos/secret`.
- The lab was solved after submitting the disclosed secret.

### Impact

If this vulnerability existed in a real application, an attacker could:

- Execute arbitrary server-side code.
- Read sensitive files available to the web server user.
- Steal credentials, configuration files, or application secrets.
- Modify application content.
- Use the server as an initial foothold for deeper compromise.

### Remediation

- Validate uploaded files using an allowlist of safe file extensions and MIME types.
- Verify file content server-side instead of trusting client-supplied headers.
- Rename uploaded files and remove user-controlled extensions.
- Store uploads outside the web root when possible.
- Disable script execution in upload directories.
- Serve uploaded content through a safe file handler.
- Apply strict size limits and antivirus/content scanning where appropriate.
- Enforce least privilege on the web server user.

## Screenshots

1. `screenshots/01-lab-homepage.png` - Lab environment.
2. `screenshots/02-account-avatar-upload-form.png` - Avatar upload surface.
3. `screenshots/03-burp-upload-request-response.png` - Burp HTTP history showing upload request and successful response.
4. `screenshots/04-secret-disclosed-via-uploaded-php.png` - Uploaded PHP file disclosing the lab secret.
5. `screenshots/05-lab-solved.png` - Lab solved confirmation.

## Conclusion

This lab demonstrated how an insecure file upload feature can become a remote code execution vulnerability when executable files are accepted and served from a web-accessible directory. Burp Suite was used to inspect the upload request and response, verify the server behavior, and document the exploit path.
