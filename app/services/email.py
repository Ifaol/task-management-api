import resend

from app.core.config import settings


resend.api_key = settings.resend_api_key


async def send_email(
    to: str,
    subject: str,
    html: str,
) -> None:
    params: resend.Emails.SendParams = {
        "from": settings.email_from,
        "to": [to],
        "subject": subject,
        "html": html,
    }

    await resend.Emails.send_async(params)


async def send_welcome_email(to: str) -> None:
    await send_email(
        to=to,
        subject="Welcome to Task Management System",
        html="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Task Management System</title>
</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #f4f7fb;
    font-family: Arial, Helvetica, sans-serif;
    color: #1f2937;
">

    <table
        width="100%"
        cellpadding="0"
        cellspacing="0"
        border="0"
        style="background-color: #f4f7fb; padding: 40px 20px;"
    >
        <tr>
            <td align="center">

                <!-- Main Container -->
                <table
                    width="100%"
                    cellpadding="0"
                    cellspacing="0"
                    border="0"
                    style="
                        max-width: 600px;
                        background-color: #ffffff;
                        border-radius: 16px;
                        overflow: hidden;
                    "
                >

                    <!-- Header -->
                    <tr>
                        <td
                            style="
                                padding: 36px 40px;
                                background-color: #111827;
                                text-align: center;
                            "
                        >
                            <div style="
                                font-size: 28px;
                                font-weight: bold;
                                color: #ffffff;
                                letter-spacing: -0.5px;
                            ">
                                Task Management System
                            </div>

                            <div style="
                                margin-top: 8px;
                                font-size: 14px;
                                color: #9ca3af;
                            ">
                                Simple. Powerful. Organized.
                            </div>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td style="padding: 44px 40px 36px 40px;">

                            <div style="
                                font-size: 30px;
                                font-weight: bold;
                                line-height: 1.25;
                                color: #111827;
                                margin-bottom: 18px;
                            ">
                                Welcome! 👋
                            </div>

                            <p style="
                                margin: 0 0 18px 0;
                                font-size: 16px;
                                line-height: 1.7;
                                color: #4b5563;
                            ">
                                Your account has been created successfully.
                                We're excited to have you with us.
                            </p>

                            <p style="
                                margin: 0 0 30px 0;
                                font-size: 16px;
                                line-height: 1.7;
                                color: #4b5563;
                            ">
                                Task Management System gives you a simple way
                                to organize, manage, and keep track of your tasks.
                            </p>

                            <!-- Feature Box -->
                            <table
                                width="100%"
                                cellpadding="0"
                                cellspacing="0"
                                border="0"
                                style="
                                    background-color: #f9fafb;
                                    border-radius: 12px;
                                    margin-bottom: 30px;
                                "
                            >
                                <tr>
                                    <td style="padding: 24px;">

                                        <div style="
                                            font-size: 16px;
                                            font-weight: bold;
                                            color: #111827;
                                            margin-bottom: 14px;
                                        ">
                                            What you can do
                                        </div>

                                        <div style="
                                            font-size: 14px;
                                            line-height: 1.8;
                                            color: #6b7280;
                                        ">
                                            ✓ Create and manage tasks<br>
                                            ✓ Track task progress<br>
                                            ✓ Organize workspaces<br>
                                            ✓ Collaborate with your team
                                        </div>

                                    </td>
                                </tr>
                            </table>

                            <p style="
                                margin: 0;
                                font-size: 16px;
                                line-height: 1.7;
                                color: #4b5563;
                            ">
                                Thanks for joining us. We hope Task Management
                                System helps you stay organized and get more done.
                            </p>

                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding: 0 40px;">
                            <div style="
                                height: 1px;
                                background-color: #e5e7eb;
                            "></div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td
                            style="
                                padding: 28px 40px 32px 40px;
                                text-align: center;
                            "
                        >
                            <div style="
                                font-size: 13px;
                                line-height: 1.6;
                                color: #9ca3af;
                            ">
                                You received this email because an account
                                was created using this email address.
                            </div>

                            <div style="
                                margin-top: 12px;
                                font-size: 13px;
                                color: #9ca3af;
                            ">
                                © 2026 Task Management System
                            </div>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
        """,
    )