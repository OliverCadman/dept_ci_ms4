# DepT - Testing Documentation

If you wish to return to the main README file, please visit [README.md](README.Md)

# Markup Validation

## HTML

The [W3C HTML Markup Validator](https://validator.w3.org/) was used to validate the website's HTML files.

All the following pages passed with no issues:

* Home Page
* Find a Dep
* Find a Job
* Dashboard
* Edit Invitation
* Edit Job
* Sign Out
* Login
* Register
* Reset Password (all pages of reset-password authorization flow)
* Booking Success
* Booking Detail
* Edit Profile

While these pages passed with no errors, issues were encountered on these pages:

* Subscription Page
* Profile Page

### HTML Validation Issues

Unfortunately, HTML validation errors were thrown when upon validating HTML generated automatically by third-party packages.

#### Subscription Page

The [Stripe](https://www.stripe.com) JS library is imported via a CDN in a script tag, to provide functionality to the website's subscription page.

Upon validating this page, errors were thrown due to Stripe's automatically-generated iframe.

![Stripe Validation Errors](documentation/readme_images/validation/stripe_validation_errors.png)

The developer went to great lengths to try and find a way to rectify this error, so that the page would pass validation with a clean sheet. However much to their frustration, they were unable to find a suitable method to successfully alter how Stripe's ``iframe`` attributes are rendered.

#### Profile Page

Similarly to the issues faced by a third-party package in the Subscription page, issues were faced when validating the automatically-generated HTML table, generating by the [FullCalendar](https://fullcalendar.io/) API.

Upon validating the HTML code for the Profile page, many errors were thrown due to the semantics used in FullCalendar's automatically-generated calendar.

![FullCalendar Validation Errors](documentation/readme_images/validation/fullcalendar_validation_errors.png)

Errors and warnings of this nature are present for every ``td`` element used in their calendar. Again, the developer made great efforts to research and find a way to solve this issue so the calendar passed validation with a clean sheet. 

Initially, the developer deducted that they could download the library and add it to their project without CDN, and edit the JavaScript file to remove the offending attributes of the table elements. However, the website offers no support for downloading the package. Users can only use FullCalendar via CDN or as an NPM package.

Much to the developer's frustration and dejection, no success was had in finding a way to alter the table element's attributes in order to pass validation with no errors. 

Short of researching and integrating a completely new calendar library, or removing the calendar feature from the website altogether, a useful solution could not be found in time before project submission.

#### Overview

The developer's HTML code was validated throughout the lifecycle of the project's development, and has passed all validator tests with no errors shown.

All errors and warnings that were thrown by the validator are a direct result of the third-party packages used by the website. The developer is aware that regardless of whether they wrote the code or not, using a third-party package that generates unsemantic code isn't a good practice. 

Careful consideration will be made in the developer's future, when choosing third-party packages to use in their websites.

## CSS

The [W3C Jigsaw CSS Validator](https://validator.w3.org/) was used to validate the website's CSS files.

All CSS files passed validation tests with no issues.

At the time of deployment, there are 36 warnings:

1. Imported style sheets are not checked in direct input and file upload modes.
    * Accounts for 1 of the 36 warnings

2. <extension> is an unknown vendor extension
    * Accounts for 35 of 36 warnings

Since these warnings are a result of W3C Jigsaws inability to interpret them by default,
the developer is satisfied that the warnings can be dismissed.

## PEP8 Compliancy

All custom Python code was validated for PEP8 Compliancy using the [pep8online validator](http://pep8online.com/)

The following files have been checked for validation:

* Root
    * custom_storages.py
    * test_helpers.py
    * 

* Bookings
    * admin.py
    * apps.py
    * classes.py
    * forms.py
    * functions.py
    * models.py
    * test_views.py 
    * tests.py
    * urls.py
    * utils.py
    * views.py

* Home
    * admin.py
    * apps.py
    * models.py
    * tests.py
    * urls.py
    * views.py

* Jobs
    * admin.py
    * apps.py
    * forms.py
    * functions.py
    * models.py
    * test_models.py
    * tests.py
    * urls.py
    * views.py

Profiles
    * custom_tags.py
    * admin.py
    * apps.py
    * forms.py
    * functions.py
    * models.py
    * signals.py
    * test_models.py
    * test_urls.py
    * test_views.py
    * urls.py
    * views.py
    * widgets.py

Social
    * admin.py
    * apps.py
    * forms.py
    * functions.py
    * models.py
    * signals.py
    * test_models.py
    * test_views.py
    * urls.py
    * views.py

Subscriptions
    * tests.py
    * urls.py
    * views.py
    * webhook_handler.py

At the time of deployment, there are no validation errors in any files listed.

## JS Validation

The project's JavaScript files are validated by [JSHint](https://jshint.com/)

The following files have been ran through the JSHint Validator:

* Root Static JS
    * ajax_error_message.js
    * delete_alert_modals.js
    * form_ajax.js
    * format_date.js
    * notification.js
    * toastify.js 
* Bookings
    * booking_form.js
    * rating.js
* Home
    * index.js
* Jobs
    * filter.js
    * job_detail_modal.js
    * job_fee_icons.js
* Profiles
    * audio_dropzone.js
    * bar-ui.js
    * calendar_profile.js
    * calendar.js
    * dashboard_modals.js
    * display_star_rating.js
    * edit_review_modals.js
    * formset.js
    * progress_bar.js
    * soundmanager.js
    * switch_form_pages.js
* Subscriptions
    * checkout.js

## Unused/Undefined Variables

JSHint threw warnings related to the use of unused/undefined variables.

### Unused Variables

The following custom functions are the "unused variables" flagged by JSHint:

* ``displayAJAXErrorMessage()``
    * Defined in it's own file and shared among JavaScript files which use AJAX to communicate with the backend.

* ``formatDate()``
    * Defined in it's own file and shared in `dashboard_modals.js`

* ``dateDiffInDays()``
    *  Defined in it's own file and shared in `dashboard_modals.js`

* ``displayToast()``
    * Defined in it's own file and shared among various JavaScript files which required toasts to be displayed (principally in AJAX success callbacks).

These functions are defined in a seperate file to keep the workspace clean, and are used across other files involved in the project. Though the functions aren't being used in the file they are defined in, it is indeed being used in other files of the project.

### Undefined Variables

The following custom functions and variables are the "undefined variables" flagged by JSHint:

* ``displayToast()``
    * Defined in a seperate file.

* ``displayAJAXErrorMessage()``
    * Defined in a seperate file.

* ``mediaUrl``
    * Define in script tags in 'base.html'

* ``formatDate()``
    * Defined in another file

* ``dateDiffInDays``
    * Define in another file

The following variables and functions are provided by third-party CDNs:

* `Stripe`

* `Toastify`

* `FullCalendar`

* `Dropzone`

Since the custom variables and functions are defined in a seperate file to keep a clean workspace, JSHint of course will assume that they are not being used if it cannot find a reference to the variable/function in the same file.

Similarly with variables and functions provided via CDN link, JSHint won't be aware of their definition since it doesn't have access to the files provided via CDN.

With this, the developer is satisfied that these warnings can be dismissed.

# Testing User Stories from UX Section of README.md

## First-Time Visitors

### As a visitor using the website for the first time, I want...

1. **The purpose of the website to be evident upon the first visit, so I can quickly determine that the website will suit my needs.**
    * Upon landing on the website, the user is presented immediately with the brand's logo, along with a lead paragraph "The best musicians and singers for hire."
    * A Call-to-Action is immediately visible to the user, inviting them to 'Find a Dep' 
    by visiting the 'Find a Dep' page to browse a list of musicians.
    * The home page features three itemised benefits that can be gained from using the website:
        * "Find a local musician to play your gig anywhere in the world, stress free."
        * "Perform and earn extra money"
        * "Make new connections and expand your network."

2. **To be able to navigate the website intuitively and with ease on all devices, so that my time isn't wasted.**
    * There is a persistent navbar across all pages of the website. 
    * The navbar is fixed, so is present when users scroll down a page.
    * The navbar collapses down to a burger icon on mobile devices.

3. **To easily find information about how to use the platform, so I can understand the model of the service provided.**
    * An ordered list providing an overview of the website's usage is present in the website's home page.
    * The ordered list is accompany by images of the website's pages, to further reinforce website usage, and to provide a visual stimulus for the user.

### As a potential member, I want...

1. To easily find out what benefits I get from being a paying member, so I can determine whether the service is worth my money.
    * The website's 'Subscribe' page features two cards, each with a bulleted list featuring what a certain subscription-tier can offer them.
    * The 'Tier Two' subscription card features FontAwesome check icons to accompany the extra features a Tier Two subscription offers, so as to clearly indicate that a paid service can benefit a paid user.

2. To browse the website without having to register.
    * Each main page of the website is accessible to the user without them having to register.
    * Features such as the profile's music player are also interactive for non-registered users.

3. To be able to register to the website, so I can manage and display a profile.
    * A link to the registration page is presented at the top-level of the website's home-page.
    * A link to the registration page is also featured clearly in the website's navigation bar.
    * Upon registration, a link to "My Account" is featured in the navigation bar, where the user can find links to edit their profile. 

### As a Tier One Member of the website, I want...

1. To be able to upload samples of my music to my profile, so I can showcase my skills and expertise.
    * The website's 'Edit My Profile' features a form for a user to add their audio files.
    * The form is presented as a Graphical User Interface, where users can drag and drop their audio files at their will.
    * Should a user wish to remove an audio file, they can do so easily and intuitively.

2. A link to my profile to be listed on a page, so potential clients/musicians will be able to find me easily.
    * The website features a link to 'Find a Dep' in the navigation bar, persistent across all pages.
    * All registered members of the website are displayed on a card in the 'Find a Dep' page.
    * The cards feature member details, average rating, and a link to the member's profile.

3. To be able to find other members using the service, so I am able to find a dep easily in the case that a can't make a gig.
     * The website features a link to 'Find a Dep' in the navigation bar, persistent across all pages.
    * All registered members of the website are displayed on a card in the 'Find a Dep' page.
    * The cards feature member details, average rating, and a link to the member's profile.
    * The page is filterable by instrument, genre, city and whether a member is available on the day of searching, to provide a more granular search for a suitable dep.
    * Search results can be sorted by rating.

4. To be notified when I get a job offer from another member, so I can respond quickly and professionally.
    * The website's navigation features a notification icon, with a badge indicated how many notifications a user has.
    * Upon clicking, the notification icon opens a dropdown menu, displaying the user's notifications.
    * Users receive notifications about all events related to an invitation/booking.
    * Users can click the notification to be taken to the relative card on their dashboard page, where they can make further actions about the given invitation/booking.

5. To be able to message a member with a response, or any questions, without leaving the website, to make the process run as smoothly as possible.
    * Each active invitation is presented on it's own card, in the user's dashboard page.
    * From these cards, the user can either choose to message the other member about the invitation, accept the invitation, or decline the invitation.
    * All messaging, accepting and declining events send a notification to the other user invovled in the active invitation.

6. To be able to message other members of the website, so I can grow my network.
    * Users are able to message other users in an active invitation/booking, available from the invitation cards displayed in the dashboard page.
    * The messaging service is in the form of a chat box, to provide familiarity and a pleasing user interface.
    * Notifications are sent to either user if they receive a message.

7. To display reviews/ratings from members for who I have provided services, so I can improve my reputation in the community.
    * All of a member's reviews/ratings are displayed clearly on their profile page, directly below a user's pitch.
    * The date of the review is present, along with an indication that a review has been edited (if applicable).
    * A user's average rating is displayed as star icons both in the top-level of their profile page, and on their card in the 'Find a Dep' page.

8. To access a dashboard displaying a record of ratings and reviews, so I can take account of how much I am benefitting from the service.
    * Upon landing on the dashboard page, the user is presented immediately with metric data and analytics related to their profile.
    * Their average rating is displayed on a card, with a short encouraging message if their rating is below 5 stars.

9. To be able to manage my subscription, so I can update my subscription tier when I like.
    * Upon visiting the website's 'Subscribe' page through the navigation bar, the user is presented with the cards. The card representing their current subscription-tier is highlighted.
    * The card displaying the tier that the user is not currently subscribed to features a button, which redirects the user to a Stripe customer portal, to manage their subscription.
    * The website's dashboard also features a navigation link which reads 'Manage My Subscription', so they can visit the Subscription page from multiple points of the website.

10. To be able to browse the Tier Two 'Find a Job' page without subscribing, so I can determine whether subscribing to a Tier Two service is worth the money.
    * Tier One members may browse the Tier Two page with no restrictions.
    * If a Tier One member likes the look of the page and would like to get involved by clicking on a button to 'Post a Job' or 'Send an Offer', they are presented with an alert that they need Tier Two access to use that service.
    * The alert modal window features a button inviting the user to subscribe to the Tier Two service, and reap the benefits of being a Tier Two member.

### As a Tier Two member of the website, I want...

1. All privileges provided by Tier One Membership.
    * This user story is satisfied by all solutions outlined in User Stories testing for Tier One Users.

2. To have access to a job listing, so I can find jobs that are in my local area.
    * The website features a 'Find a Job' page, where users can browse a list of available jobs.
    * The jobs are presented clearly on cards, with an image of the artist that requires a musician (if an image is provided), and a visual indicator of how lucrative the job is.

3. To be able to filter jobs by location or fee range, so I can more granularly search for a suitable job.
    * The 'Find a Job' page features a filter accordion bar.
    * The accordion bar displays a search text input, where a user can search for a job by city.
    * The accordion bar also features a select dropdown, where a user can search by fee range.
    * Fee amounts are presented graphically on the cards through dollar signs, indicating how lucrative a job is.

4. To be able to post a job that's in need of a dep, so I can be sure that my job gets the attention of Tier Two deps.
    * Tier Two members are able to post a job from the 'Find a Job' page.
    * This page clearly features a call-to-action in her page header.
    * The form to post a job advertisement opens in a modal window, so they are
    not redirected away from the 'Find a Job' page.
    * Members who post a job will see their job post immediately on the 'Find a Job' page.

5. To be able to edit or delete a job that I've posted, in case I have made a mistake, or that I've found someone to do the job from outside the website.
    * Members who have posted a job are able to edit their job from a seperate page.
    * The page is accessible via to points; either from the dashboard, or from the 'Find a Job' Page.
    * The job card on either of these pages features a link to either edit or delete a job.
    * If a member chooses to delete a job, a modal alert window is displayed, to confrim the deletion of the job.

6. To be notified when I received an offer for a job I've posted, so I can determine which member might be the right fit, with efficiency.
    * A notification object is created each time another Tier Two member registers interest in a job. 
    * All notifications are presented in a dropdown in the website's navigation bar, so they are available across all pages of the website.
    * Clicking a notification will direct the job poster to the dashboard card, displaying the job post in question.


7. The members who have expressed interest in my job to be clearly visible, so I can inspect who might be a good fit, with ease.
    * Upon landing on the job post card, a list of all the members who have registered interest is displayed with their profile avatars.
    * Each avatar is clickable, which will take the job poster to the profile of the member who has registered interest.
    * The card also features a button to 'Choose A Member'. If the job poster would like to do a quick inspection from the dashboard, they may see a list of all the interest members, along with their profile images, and instruments they play.

8. To be listed at the top of searches when a potential client/musician is searching for a dep, so I can have a better chance of getting the work.
    * The User Profile model's queryset methods are designed to prioritise Tier Two members, regardless of rating.

### As a member who is looking for a dep musician, I want...

1. A page where I can search for dep musicians, so I can easily begin to find a dep.
    * The website's 'Find a Dep' page features a comprehensive list of all members of the website.
    * Each card that belongs to a user features their name, profile image, instruments they play, rating, and an overview of their skills/personal details/pitch.

2. To be able to filter musicians by their expertise, instrument or style of music they play, and location, so I can find a dep which suits my needs.
    * The 'Find a Dep' page features a bootstrap accordion, displaying a form that can be used to filter deps.
    * Deps can be filtered by either location, genre, instrument or whether they are available on the day that the user is searching. 
    * Search results can be sorted by rating, from low to high or high to low.

3. To be able to visit a dep's profile page, so I can find out more information about their experience and expertise.
    * Each card featured in the 'Find a Dep' page holds a button, inviting the user searching for a dep to visit the member's profile page.
    * Upon landing on a member's profile page, the user is presented clearly with the member's location, instruments they play and average rating, along with their profile picture (if provided).
    * Immediately below the header is the member's pitch, which a user can browse and determine if the member is a good fit for the user's needs.
    * A list of the member's genres of expertise is clearly detailed in a sidebar.
    * The sidebar collapses to a full-width column on mobile devices, to ensure responsivity across all devices.

4.  To view a calendar of available/unavailable dates, so I can find out if a dep is available before pursuing further.
    * Each member's profile page features a calendar displaying their dates of unavailability.
    * The calendar is responsive across all device sizes.
    * Dates of unavailability are clearly marked in a light red colour, to give a clear visual indicator that the member is unavailable.
    * Unavailability calendars can be updated by a member from the 'Edit My Profile' page.

5. To hear samples of a dep's music, so I can be confident that they will provide a good service.
    * Each member's profile page features a music player, if the member has provided audio tracks.
    * The music player is interactive, and the user can scroll through tracks in the playlist, and turn volume up or down.
    * Music played via the music player persists while the user browses other aspects of the user's profile page.
    * The music player is responsive across all screen sizes.

6. To be able to message a potential dep from within the website, so that no unnecessary time is wasted.
    * Each member's profile page features a button to 'Contact <user>'.
    * Upon clicking this button, a line of communication can be opened by way of filling in an Invitation Form.
    * As well as event information, the Invitation Form provides a a textarea field for the user to give a detailed explanation as to what service they require.

7. To be notified when I have received a response from a dep I have messaged, so I can confirm the arrangement quickly and smoothly.
    * A notification icon is persistent across all pages of the website through the navigation bar.
    * The notifications icon is accompanied with a bootstrap badge, providing the user with a clear indication of how many notifications they have received.
    * A user is notified either when they have received a message about an invitation, or when an invitation has been accepted.
    * Clicking a received notification will take the user directly to the invitation in question.

8. To be able to send a confirmed dep a document with job details (with location, timings, number of sets etc), to allow for effective communication.
    * Upon acceptance of an invitation, the user is sent a notification, which upon clicking, will take them to a form to finalize their booking.
    * The booking for features fields for the user to provide the venue address, and textareas to inform the confirmed user about any travel or backline information.
    * Additionally, a dynamic form is presented, allowing the user to add up to 5 tracks, to provide any audio resources related to the booking.
    * Upon sending the booking form, an email and notification is sent to the confirmed member.
    * Upon clicking the notification, the confirmed member is taken directly to the page featuring the finalized booking details that the booker has sent.

















