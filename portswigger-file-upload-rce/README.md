# PortSwigger File Upload RCE Lab

This project documents an authorized PortSwigger Web Security Academy lab focused on exploiting an unrestricted file upload vulnerability with Burp Suite Community Edition.

## Lab

- Platform: PortSwigger Web Security Academy
- Lab: Remote code execution via web shell upload
- Category: File upload vulnerabilities
- Target type: Temporary PortSwigger lab instance
- Testing date: 27 June 2026

## Objective

Upload a PHP web shell through the avatar upload feature, execute it from the web-accessible upload directory, read `/home/carlos/secret`, and submit the secret to solve the lab.

## Tools Used

- Burp Suite Community Edition
- Burp built-in browser
- Proxy HTTP history
- PHP payload

## Vulnerability Summary

The application allowed a user to upload a PHP file through the avatar upload feature and stored it in a web-accessible directory. When the uploaded file was requested from `/files/avatars/`, the server executed the PHP code instead of treating it as inert content. This allowed disclosure of a sensitive local file.

## Evidence

| Step | Evidence |
| --- | --- |
| Lab home page | `screenshots/01-lab-homepage.png` |
| Avatar upload form | `screenshots/02-account-avatar-upload-form.png` |
| Burp upload request and response | `screenshots/03-burp-upload-request-response.png` |
| Secret disclosed through uploaded PHP | `screenshots/04-secret-disclosed-via-uploaded-php.png` |
| Lab solved confirmation | `screenshots/05-lab-solved.png` |

## Payload

The lab payload used for the avatar upload is included at:

```text
payload/portswigger-file-upload-shell.php
```

```php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

## Key Learning

- File extension validation must not trust only the client request.
- Uploaded user files should not be stored in executable web paths.
- Servers should prevent script execution in upload directories.
- Burp HTTP history helps verify upload endpoints, request headers, multipart body content, and server responses.

## Report

Full write-up:

```text
report/PortSwigger-File-Upload-RCE-Report.md
```
