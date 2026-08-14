# *Vinyl Vault* - Testing Documentation

## Table of Contents

1. [Testing Approach](#testing-approach)
2. [Testing Timeline](#testing-timeline)
3. [Manual Testing](#manual-testing)
4. [Acceptance Criteria Testing](#acceptance-criteria-testing)
5. [HTML Validator](#html-validator)
6. [CSS Validator](#css-validator)
7. [JavaScript Validator](#javascript-validator)
8. [Python Linter](#python-linter)
9. [Automated Testing via Django](#automated-testing-via-django)
10. [Google Chrome Lighthouse](#google-chrome-lighthouse)
11. [Bug Fixes](#bug-fixes)

### Testing Approach
Test‑driven development principles were applied throughout the project, with core behaviours and expected outcomes defined before implementation. Writing tests early helped shape clearer, more reliable features, reduced regressions across iterations, and ensured that each new slice of functionality aligned with user needs and the project’s themes and stories.

This document summarises all testing completed throughout development. Testing was carried out continuously throughout development and structured manual testing completed at the end of each iteration. Regular automated testing was completed at appropriate intervals. Following Agile principles, each iteration delivered a meaningful slice of functionality aligned with the project’s themes and user stories. The project was organised into four major themes / iterations.

Iteration Breakdown:
- **Iteration 1 – Core Platform Foundations**
    - Verified account creation, login/logout, and email confirmation.
    - Checked guest browsing and consistent navigation.
    - Confirmed home page displays featured albums, new releases, and sale items.

- **Iteration 2 – Product Browsing & Shopping Bag**
    - Tested album browsing, filtering, and search functionality.
    - Validated sorting by price, release date, and name.
    - Checked album detail pages for accurate tracklists and formats.
    - Verified adding, updating, and removing items from the shopping bag.
    - Confirmed live total updates in the navbar.

- **Iteration 3 – Checkout & Payments**
    - Tested checkout flow: delivery details, order summary, and confirmation emails.
    - Verified secure card payments and graceful handling of failed transactions.
    - Checked contact form submissions and email notifications.

- **Iteration 4 – Profile, Admin & Polish**
    - Validated profile pages showing order history and saved delivery details.
    - Tested store management: add, edit, and delete albums via front end.
    - Checked toast notifications and mobile responsiveness.
    - Refined layout, feedback, and accessibility across all devices.


### Testing Timeline
A consistent testing routine was maintained throughout development to ensure each iteration met its acceptance criteria and remained stable as new features were introduced. The timeline below outlines the key testing milestones completed during the project.

| Phase  | Date |
|------------------------------------------------------------------|---------------|
| Project initiated | 25th July 2026 |
| Iteration 1 testing (manual testing + acceptance criteria checks) | 9th & 14th August 2026 |
| Iteration 2 testing (manual testing + acceptance criteria checks) | XX XX 2026 |
| Automated testing via Django | XX XX 2026|
| Iteration 3 testing (manual testing + acceptance criteria checks) | XX XX 2026 |
| Automated testing via Django | XX XX 2026|
| Iteration 4 testing (manual testing + acceptance criteria checks) | XX XX 2026 |
| Google lighthouse audit testing | XX XX 2026 |
| Validator and linter checks (HTML, CSS, JS, Python) | XX XX 2026 |
| Automated testing via Django | XX XX 2026|


### Manual Testing
Manual testing was carried out at the end of each iteration to confirm that newly implemented features were functioning correctly before progressing. Following Agile principles, each iteration delivered a complete slice of functionality, which was then tested for correctness, usability, and stability. This ensured issues were identified early and user flows remained coherent as the platform evolved.

#### Iteration One

| Area | Feature | Expected Outcome | Testing Performed | Result | Pass/Fail |
| --- | --- | --- | --- | --- | --- |
| Navigation | Header links | Each link loads the correct page | Clicked all header links | All pages load correctly | ✅ **PASS** |
| Navigation | Logo link | Returns user to home page | Clicked logo | Home page loads | ✅ **PASS** |
| Navigation | Navigation bar consistency | Nav appears on all pages | Browsed site | Nav consistent across pages | ✅ **PASS** |
| Navigation | Home page content | Featured albums and latest releases display | Loaded home page | Content loads correctly | ✅ **PASS** |
| Navigation | Guest browsing | Store accessible without login | Browsed as guest | All public pages accessible | ✅ **PASS** |
| Navigation | Footer links | Footer links open correct pages | Clicked each link | All links open correct pages | ✅ **PASS** |
| Layout | Desktop layout | Layout stable on large screens | Tested on desktop | No layout issues | ✅ **PASS** |
| Layout | Tablet layout | Layout adapts correctly | Tested at 768–991px | Minor spacing fix applied | ✅ **PASS** |
| Layout | Mobile layout | Layout adapts to small screens | Tested <768px | Layout clean and readable | ✅ **PASS** |
| Authentication | Signup form | Creates new user account | Submitted valid signup | Account created successfully | ✅ **PASS** |
| Authentication | Signup validation | Shows errors for invalid input | Submitted empty/invalid fields | Clear validation errors shown | ✅ **PASS** |
| Authentication | Email confirmation | Confirmation email sent | Registered new user | Email received | ✅ **PASS** |
| Authentication | Login form | Logs user in | Entered valid credentials | User logged in | ✅ **PASS** |
| Authentication | Incorrect login | Shows error message | Entered wrong password | Error message shown | ✅ **PASS** |
| Authentication | Logout | Logs user out | Clicked logout | User logged out | ✅ **PASS** |
| Authentication | Session privacy | Account remains private | Attempted accessing protected pages | Redirected correctly | ✅ **PASS** |
| Browsing | Album list loads | Displays all albums | Loaded albums page | All albums appear | ✅ **PASS** |
| Browsing | Deezer API integration | Album data loads dynamically | Refreshed page | All album data fetched correctly | ✅ **PASS** |
| Browsing | Card layout | Cards display correctly | Checked cards | Layout clean and readable | ✅ **PASS** |
| Browsing | Responsive layout | Cards adapt to screen size | Tested on multiple devices | No issues | ✅ **PASS** |
| Error Handling | Permission errors | Users cannot access others’ profiles | Attempted accessing another user’s profile | Redirected correctly | ✅ **PASS** |
| Error Handling | Form errors | Validation messages appear | Submitted invalid forms | Clear errors shown | ✅ **PASS** |
| Performance | Page load speed | Pages load quickly | Tested across pages | All pages load fast | ✅ **PASS** |
| Performance | Mobile responsiveness | Layout adapts to small screens | Tested on mobile | No overlap or scroll | ✅ **PASS** |
| Performance | Tablet responsiveness | Layout adapts to medium screens | Tested on tablet | Minor spacing issues | ✅ **PASS** |


#### Iteration Two – xx
x
Include 404 page.



#### Iteration Three – xxx
xxx




#### Iteration Four – xxx
xxx





### Acceptance Criteria Testing
This table outlines the key user stories and acceptance criteria completed during development. This demonstrates how the website meets the expectations of its target audience and ensures a satisfying user experience. All testing was carried out at the end of each iteration, with each iteration aligned to one of the three development themes to ensure focused, structured progress.

#### Iteration One

| User Story | Acceptance Criteria | Status | Evidence/Notes |
|------------|---------------------|--------|----------------|
| **US 1.1.1 – Account Creation (Must Have)** | Users can register with a valid email and password and receive confirmation of successful account creation. | ✅ **PASS** | Registration form tested with multiple valid emails; confirmation message displayed; redirect successful. |
| **US 1.1.1 – Account Creation (Must Have)** | Validation prevents duplicate accounts and ensures all required fields are completed before submission. | ✅ **PASS** | Duplicate email attempt blocked; empty fields trigger clear validation errors. |
| **US 1.1.2 – Secure Login & Logout (Must Have)** | Users can log in and log out successfully with clear feedback messages. | ✅ **PASS** | Login and logout tested across pages; success and error messages display correctly. |
| **US 1.1.2 – Secure Login & Logout (Must Have)** | Authentication ensures only registered users can access profile and order data. | ✅ **PASS** | Unauthenticated access redirects to login; protected routes verified. |
| **US 1.1.3 – Registration Confirmation Email (Must Have)** | A confirmation email is automatically sent after successful registration. | ✅ **PASS** | Email triggered on registration; received in test inbox; sender verified. |
| **US 1.1.3 – Registration Confirmation Email (Must Have)** | The email includes clear branding and confirmation of account activation. | ✅ **PASS** | Email template shows store logo and activation confirmation text. |
| **US 1.2.1 – Home Page Display (Must Have)** | The home page displays featured, new and sale products dynamically from the database. | ✅ **PASS** | Dynamic product data loads correctly; verified against database entries. |
| **US 1.2.1 – Home Page Display (Must Have)** | Layout remains responsive and accessible across all devices. | ✅ **PASS** | Tested on mobile, tablet, and desktop; layout adjusts smoothly. |
| **US 1.2.2 – Consistent Navigation Bar (Must Have)** | Navigation links are visible and consistent across all pages. | ✅ **PASS** | Navbar verified on all templates; links functional and consistent. |
| **US 1.2.2 – Consistent Navigation Bar (Must Have)** | Active page highlighting helps users understand their current location. | ✅ **PASS** | Active link styling confirmed; highlights update correctly on navigation. |
| **US 1.2.3 – Guest Browsing (Must Have)** | Guests can view all store pages and product details without authentication. | ✅ **PASS** | Guest access tested; browsing unrestricted; checkout prompts login. |
| **US 1.2.3 – Guest Browsing (Must Have)** | Restricted actions (checkout, profile) prompt login or registration. | ✅ **PASS** | Attempting checkout/profile redirects to login page with message. |


#### Iteration Two
xxx

#### Iteration Three
xxx

#### Iteration Four
xxx


### HTML Validator
xxx

### CSS Validator
xx

### JavaScript Validator
xx

### Python Linter
xxx

### Automated Testing via Django
xxx

### Google Chrome Lighthouse
xxx

### Bug Fixes
xxxx

<sub>[*Back to contents*](#table-of-contents)</sup>