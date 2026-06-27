from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "report" / "OWASP-Juice-Shop-VAPT-Report.pdf"


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(inch * 0.7, 0.45 * inch, "OWASP Juice Shop VAPT Report")
    canvas.drawRightString(A4[0] - inch * 0.7, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def finding(story, styles, fid, title, severity, affected, description, evidence, impact, recommendation):
    story.append(Paragraph(f"{fid}: {title}", styles["Heading2"]))
    data = [["Severity", severity], ["Affected", affected]]
    table = Table(data, colWidths=[1.2 * inch, 5.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F1F5F9")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8))
    for label, text in [
        ("Description", description),
        ("Evidence", evidence),
        ("Impact", impact),
        ("Recommendation", recommendation),
    ]:
        story.append(Paragraph(label, styles["FindingLabel"]))
        story.append(Paragraph(text, styles["BodyText"]))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 10))


def build():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            leading=28,
            spaceAfter=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FindingLabel",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=4,
            spaceAfter=2,
        )
    )
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 14
    styles["Heading1"].spaceBefore = 14
    styles["Heading1"].spaceAfter = 8
    styles["Heading2"].spaceBefore = 12
    styles["Heading2"].spaceAfter = 6

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    story = []
    story.append(Paragraph("OWASP Juice Shop VAPT Report", styles["TitleCenter"]))
    story.append(Paragraph("<b>Prepared by:</b> Ahammed Zidan M", styles["BodyText"]))
    story.append(Paragraph("<b>Test Date:</b> 27 June 2026", styles["BodyText"]))
    story.append(Paragraph("<b>Target:</b> OWASP Juice Shop running locally at http://localhost:3001", styles["BodyText"]))
    story.append(Paragraph("<b>Assessment Type:</b> Web Application Vulnerability Assessment and Penetration Testing", styles["BodyText"]))
    story.append(Spacer(1, 18))

    story.append(Paragraph("Executive Summary", styles["Heading1"]))
    story.append(
        Paragraph(
            "This assessment was performed against OWASP Juice Shop, an intentionally vulnerable web application deployed locally in a Docker container. The goal was to practice a realistic VAPT workflow: reconnaissance, automated scanning, manual verification, exploitation of selected vulnerabilities, evidence collection, and professional reporting.",
            styles["BodyText"],
        )
    )
    story.append(
        Paragraph(
            "The assessment identified multiple vulnerabilities across authentication, information disclosure, directory exposure, error handling, and security headers. The most severe finding was a SQL injection authentication bypass that allowed administrative login without valid credentials.",
            styles["BodyText"],
        )
    )

    story.append(Paragraph("Scope", styles["Heading1"]))
    story.append(Paragraph("In scope: local OWASP Juice Shop instance at http://localhost:3001, web application paths, and public application functionality.", styles["BodyText"]))
    story.append(Paragraph("Out of scope: third-party production systems, denial-of-service testing, social engineering, Docker host attacks, and external networks.", styles["BodyText"]))

    story.append(Paragraph("Tools Used", styles["Heading1"]))
    story.append(Paragraph("Docker, Nmap, Nikto, browser-based manual testing, and OWASP Juice Shop.", styles["BodyText"]))

    story.append(Paragraph("Findings Summary", styles["Heading1"]))
    summary = [
        ["ID", "Finding", "Severity"],
        ["F-01", "SQL Injection Authentication Bypass", "Critical"],
        ["F-02", "Confidential Document Exposure", "High"],
        ["F-03", "Exposed FTP Directory Listing", "Medium"],
        ["F-04", "Verbose Error / Stack Trace Disclosure", "Medium"],
        ["F-05", "Missing Security Headers", "Medium"],
        ["F-06", "Overly Permissive CORS Header", "Medium"],
        ["F-07", "Robots.txt Sensitive Path Disclosure", "Low"],
    ]
    table = Table(summary, colWidths=[0.7 * inch, 4.5 * inch, 1.2 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())

    story.append(Paragraph("Detailed Findings", styles["Heading1"]))
    finding(
        story,
        styles,
        "F-01",
        "SQL Injection Authentication Bypass",
        "Critical",
        "Login page",
        "The login function was vulnerable to SQL injection. By entering a crafted SQL payload into the email field and any value in the password field, authentication was bypassed and administrative access was obtained.",
        "Payload used: ' OR 1=1--. The application displayed a success message that the Login Admin challenge was solved. Evidence: screenshots/09-sqli-admin-login-bypass.png and screenshots/10-admin-session-evidence.png.",
        "An attacker could bypass authentication and gain unauthorized administrative access without valid credentials.",
        "Use parameterized queries or prepared statements, validate and sanitize input, avoid string concatenation in database queries, and monitor suspicious login attempts.",
    )
    finding(
        story,
        styles,
        "F-02",
        "Confidential Document Exposure",
        "High",
        "http://localhost:3001/ftp/acquisitions.md",
        "A confidential internal document was publicly accessible through the exposed /ftp/ directory.",
        "The file acquisitions.md contained the statement 'This document is confidential! Do not distribute!' and described planned acquisitions. Evidence: screenshots/08-confidential-document-exposure.png.",
        "Unauthorized access to confidential business documents could lead to information disclosure, reputational damage, insider trading risks, and competitive intelligence exposure.",
        "Remove confidential documents from public directories, enforce access controls, disable directory listing, and implement secure file storage.",
    )
    finding(
        story,
        styles,
        "F-03",
        "Exposed FTP Directory Listing",
        "Medium",
        "http://localhost:3001/ftp/",
        "The application exposed a publicly accessible directory listing at /ftp/ containing backup files, markdown documents, package files, and an encrypted database file.",
        "Visible files included acquisitions.md, coupons_2013.md.bak, incident-support.kdbx, package.json.bak, and suspicious_errors.yml. Evidence: screenshots/05-ftp-directory-listing.png.",
        "An attacker could gather application information, identify backup files, analyze package data, or retrieve sensitive documents.",
        "Disable directory listing, restrict sensitive file paths, remove backup/configuration files from the web root, and enforce proper access controls.",
    )
    finding(
        story,
        styles,
        "F-04",
        "Verbose Error / Stack Trace Disclosure",
        "Medium",
        "http://localhost:3001/ftp/package.json.bak",
        "A restricted backup file request returned a verbose 403 error containing internal framework details, Express version information, file paths, and stack trace data.",
        "The response disclosed OWASP Juice Shop (Express ^4.22.1), /juice-shop/build/routes/fileServer.js, and /juice-shop/node_modules/express/. Evidence: screenshots/07-verbose-error-disclosure.png.",
        "Verbose errors can help attackers fingerprint the technology stack and understand internal routing logic.",
        "Disable verbose errors in production, return generic error pages, avoid exposing framework versions and internal paths, and log detailed errors server-side only.",
    )
    finding(
        story,
        styles,
        "F-05",
        "Missing Security Headers",
        "Medium",
        "http://localhost:3001/",
        "Nikto identified missing recommended security headers including Content-Security-Policy, Referrer-Policy, Permissions-Policy, Strict-Transport-Security, and X-Content-Type-Options.",
        "Evidence: screenshots/04-nikto-scan-result.png.",
        "Missing security headers can increase exposure to client-side attacks such as XSS, data leakage through referrers, MIME sniffing, and unsafe browser feature access.",
        "Implement appropriate HTTP security headers, tuned to the application context.",
    )
    finding(
        story,
        styles,
        "F-06",
        "Overly Permissive CORS Header",
        "Medium",
        "http://localhost:3001/",
        "The application returned Access-Control-Allow-Origin: *, allowing any origin.",
        "Nikto detected the wildcard CORS header. Evidence: screenshots/04-nikto-scan-result.png.",
        "If combined with sensitive endpoints or weak authentication controls, permissive CORS can increase cross-origin data exposure risk.",
        "Restrict CORS to explicitly trusted origins and avoid wildcard origins for sensitive applications.",
    )
    finding(
        story,
        styles,
        "F-07",
        "Robots.txt Sensitive Path Disclosure",
        "Low",
        "http://localhost:3001/robots.txt",
        "The robots.txt file disclosed the /ftp directory.",
        "The file contained User-agent: * and Disallow: /ftp. Evidence: screenshots/06-robots-txt-discloses-ftp.png.",
        "Robots.txt is public and should not be used as access control. Disclosed paths can help attackers discover hidden directories.",
        "Do not rely on robots.txt to protect sensitive paths. Enforce access controls server-side.",
    )

    story.append(Paragraph("Conclusion", styles["Heading1"]))
    story.append(
        Paragraph(
            "This project demonstrated a practical web application security testing workflow from reconnaissance through exploitation and reporting. The assessment reinforced secure query handling, access control, safe file storage, generic error handling, secure HTTP headers, and manual validation of scanner findings.",
            styles["BodyText"],
        )
    )

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)


if __name__ == "__main__":
    build()
