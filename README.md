Under Test..

===============================================================================
GYM MEMBER MODULE - Odoo 2.1
===============================================================================

Module:   gym_member
Version:  2.1
Author:   AMS Logic
License:  LGPL-3 (GNU Lesser General Public License v3)
Website:  https://www.amslogic.com

-------------------------------------------------------------------------------
DESCRIPTION
-------------------------------------------------------------------------------

The Gym Member module is a complete gym management solution for Odoo. It allows
gym owners and staff to manage memberships, track attendance, schedule fitness
classes, handle payments, and communicate with members through automated
notifications and bulk emails. The module provides a user-friendly dashboard
with key performance indicators and detailed reports for better business insights.

-------------------------------------------------------------------------------
FEATURES
-------------------------------------------------------------------------------

- **Membership Management**
  - Create and manage member profiles (name, phone, email)
  - Multiple membership types: Basic, Standard, Premium
  - Track membership start and end dates
  - Automatic expiration and deactivation of expired memberships
  - Manual activation/deactivation toggle

- **Payment Tracking**
  - Record payments linked to members
  - Payment statuses: Draft, Confirmed, Cancelled
  - Payment methods: Cash, Credit Card, Bank Transfer
  - Automatic sequence generation for payment references

- **Attendance Logging**
  - Check-in and check-out functionality
  - Compute duration automatically
  - Location tracking (Main Gym, Studio, Pool, Cardio Area)
  - Real-time active check-ins and daily attendance counts

- **Class Management**
  - Create fitness classes with instructor, capacity, schedule
  - Track enrolled members and available spots
  - Class types: Yoga, Pilates, Spinning, Zumba, HIIT, Boxing
  - Enroll/remove members directly from class form
  - Toggle class active status

- **Notifications & Communication**
  - Automated expiry notifications (sent 7 days before end date)
  - Notification templates for: expiring, expired, payment due, promotions, announcements, class reminders
  - Bulk email wizard: send emails to filtered member groups (active/inactive, membership type)
  - Email templates for welcome and expiry notifications

- **Reports & Analytics**
  - Member list report (PDF): includes name, type, dates, status
  - Payment summary report (PDF): total revenue, payment details
  - Dashboard with KPI cards: Total Members, Active Members, Monthly Revenue, Today's Attendance
  - Pivot and graph views for membership distribution, attendance trends, class popularity, revenue by payment method

- **Data Export**
  - Export member data to CSV or JSON format
  - Filter by membership type and include inactive members

- **Security & Access Rights**
  - Record rules: users see only their own records (if applicable)
  - Managers (system group) have full access

- **Demo Data**
  - Pre-loaded sample classes (Yoga, Spinning, Zumba) for quick testing

-------------------------------------------------------------------------------
INSTALLATION
-------------------------------------------------------------------------------

1. Copy the `gym_member` folder to your Odoo addons directory.
2. Restart your Odoo server.
3. Go to Apps and search for "Gym Member".
4. Click "Install".

No additional dependencies are required beyond the core Odoo modules:
- base
- mail
- web
- board

-------------------------------------------------------------------------------
CONFIGURATION
-------------------------------------------------------------------------------

1. **System Parameters** (optional)
   No specific configuration is mandatory. However, you may adjust the cron jobs:
   - "Send Membership Expiry Notifications" (daily, sends reminders 7 days before expiry)
   - "Deactivate Expired Memberships" (daily, deactivates memberships past end date)

   These can be accessed from Settings > Technical > Scheduled Actions.

2. **Email Templates**
   - Welcome Email (sent manually or triggered on membership creation)
   - Expiry Notification (sent automatically by cron)
   - Generic Notification (used for bulk emails)

   You can customize these templates under Settings > Technical > Email Templates.

3. **Security**
   Access rights are defined via CSV (`security/ir.model.access.csv`) and record rules.
   By default, all internal users can manage all data. To restrict access, modify the
   security file accordingly.

-------------------------------------------------------------------------------
USAGE
-------------------------------------------------------------------------------

1. **Members**
   - Go to Gym Management > Members > All Members.
   - Click "Create" to add a new member. Fill in name, contact details, membership type, and dates.
   - Use the "Active" toggle to manually activate or deactivate a member.
   - The "Is Active?" field automatically indicates if the membership is valid (active + end date not passed).

2. **Payments**
   - Go to Gym Management > Financial > Payments.
   - Click "Create" to record a payment. Select the member, amount, payment date and method.
   - Confirm or cancel payments using the buttons on the form.

3. **Attendance**
   - Go to Gym Management > Members > Attendance Logs.
   - Click "Create" to log a check-in. Select member, location, and check-in time (defaults to now).
   - Use the "Check Out" button to record departure and compute duration.

4. **Classes**
   - Go to Gym Management > Members > Gym Classes.
   - Click "Create" to define a new class. Set name, instructor, capacity, schedule, etc.
   - Use the "Enrolled Members" tab to add or remove members.
   - The available spots and enrolled count update automatically.

5. **Notifications**
   - The system automatically sends expiry notifications 7 days before a membership ends.
   - To send a custom bulk email, use the wizard (available from a menu or action). Go to Members > All Members, then select "Send Bulk Email" (if added via menu).
   - Alternatively, create notifications manually in the Notification model (if you have technical access) and send.

6. **Reports**
   - Go to Gym Management > Reports > Member Reports or Payment Reports.
   - Click "Print" to generate a PDF report of the current list view (filtered as needed).

7. **Dashboard**
   - Go to Gym Management > Dashboard to view KPI cards and graphs.

8. **Export Members**
   - From the Members list view, you can use the "Export" action (provided by a wizard).
   - Select CSV or JSON format, choose filters, and download.

-------------------------------------------------------------------------------
TECHNICAL NOTES
-------------------------------------------------------------------------------

- **Models**:
  - `gym.membership`: member records
  - `gym.payment`: payment transactions
  - `gym.attendance`: check-in/out logs
  - `gym.class`: fitness classes
  - `gym.notification`: email notifications
  - `member.export.wizard`: export wizard
  - `bulk.email.wizard`: bulk email wizard

- **Cron Jobs**:
  - `cron_send_expiry_notifications`: runs daily, checks for members expiring in 7 days, sends email and creates notification record.
  - `cron_deactivate_expired`: runs daily, deactivates memberships where end_date < today.

- **Dependencies**:
  - The module uses `mail` for email templates and sending.
  - `board` for dashboard support.

- **Internationalization**: Arabic (ar) and French (fr) translations are included in the `i18n` folder. Additional languages can be added.

-------------------------------------------------------------------------------
LICENSE
-------------------------------------------------------------------------------

This module is licensed under the GNU Lesser General Public License v3.0.
You can find a copy of the license in the `LICENSE` file included with the module.

-------------------------------------------------------------------------------
SUPPORT
-------------------------------------------------------------------------------

Contact me if needed agcinfo77@gmail.com

-------------------------------------------------------------------------------
CHANGELOG
-------------------------------------------------------------------------------

Version 2.1 (July 2026)
- Initial release

===============================================================================
