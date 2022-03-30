# DepT - A platform created by artists, for artists.

![DepT - AmIResponsive?](documentation/readme_images/dept-amiresponsive.png)

Dept is a full-stack, community-led, subscription-based platform allowing musicians and artists to advertise their skills and services
to band leaders, producers, other artists, or any client that requires a last-minute musician to provide a service.

If a musician booked for a gig has an unforeseen circumstance that means they have to cancel their arrangement, DepT
serves to alleviate the stress of scouring through their contacts to find a last-minute replacement, by providing the opportunity
to quickly and easily 'dep out' gigs to the musicians using the DepT network.

Through DepT, artists can discover one another, increase revenue through their art, and build communities. 

By building communities, artists will acquire a diverse workspace and connect with a wider network.

# Table of Contents

* [Overview](#overview)
* [UX](#ux)
    * [Strategy](#strategy)
        * [Stakeholder Interviews](#stakeholder-interviews)
        * [Ideal Users](#ideal-users)
        * [Project Goal](#project-goal)
        * [User Stories](#user-stories)
            * [First Time Visitors](#first-time-visitors)
            * [Potential Members](#potential-members)
            * [Deps For Hire](#deps-for-hire)
                * [Tier One Membership (Free)](#tier-one-membership-free)
                * [Tier Two Membership (Paid)](#tier-two-membership-paid)
            * [Members in need of a dep](#members-in-need-of-a-dep)
        * [Strategy Summary](#strategy-summary)
            * [User Needs](#user-needs)
            * [Project Objectives](#project-objectives)
    * [Scope](#scope)
        * [User Interface](#user-interface)
        * [Authorization/User Management](#authorizationuser-management)
        * [Dep Profiles](#dep-profiles)
        * [Dashboard](#dashboard)
        * [Tier One/Tier Two Content](#tier-onetier-two-content)
        * [Tier Two Content](#tier-two-content)
        * [Booking](#booking)
        * [Messaging](#messaging)
        * [Notifications](#notifications)
    * [Structure](#structure)
        * [Informational Architecture](#informational-architecture)
            * [General Considerations](#general-considerations)
            * [Navbar](#navbar)
            * [Home Page](#home-page)
            * [Account Management](#account-management)
            * [Sign Up/Subscription](#sign-upsubscription)
            * [Profile](#profile)
            * [Dashboard](#dashboard)
            * [Find a Dep](#find-a-dep)
            * [Invite Form](#invite-form)
            * [Invite Page](#invite-page)
            * [Booking Form](#booking-form)
            * [Booking Confirmation](#booking-confirmation)
            * [Post a Job](#post-a-job)
            * [Job List Page](#job-list-page)
        * [Database Structure](#database-structure)
            * [Schema](#schema)
                * [Iteration One](#iteration-1)
                * [Iteration Two](#iteration-2)
                * [Iteration Three](#iteration-3)
                * [Iteration Four](#iteration-4)
    * [Skeleton](#skeleton)
        * [Wireframes](#wireframes)
    * [Surface](#surface)
        * [Background Colours](#background-colours)
        * [Foreground Colours](#foreground-colours)
        * [Logo](#logo)
        * [Typography](#typography)
            * [Primary Font](#primary-font)
            * [Secondary Font](#secondary-font)
            * [Tertiary Font](#tertiary-font)
        * [Header Design](#header-design)
        * [Visual Effects](#visual-effects)
            * [Box Shadow](#box-shadow)
            * [Text Shadow](#text-shadow)
            * [Colour Gradient](#colour-gradient)
            * [Hover Effects](#hover-effects)
            * [Animations](#animiations)
* [Features](#features)
    * [Existing Features](#existing-features)
        * [Subscriptions](#subscriptions)
        * [Find a Dep](#find-a-dep-1)
        * [Profiles](#profiles)
            * [Profile Page](#profile-page)
                * [Header](#header)
                * [Body](#body)
                * [Modals](#modals)
                    * [Invitation Modal](#invitation-modal)
                    * [Review Modal](#review-modal)
            * [Edit Profile Page](#edit-profile-page)
                * [Edit Profile Pages](#edit-profile-pages)
                * [Breadcrumbs](#breadcrumbs)
                * [Skip Step/Go Back Buttons](#skip-stepgo-back-buttons)
            * [Dashboard](#dashboard-2)
                * [Page One](#page-one)
                * [Jobs Page](#jobs-page)
                    * [Tier One](#tier-one)
                    * [Tier Two (Premium)](#tier-two-premium)
        * [Find a Job](#find-a-job)
        * [Booking Form](#booking-form)
        * [Booking Details](#booking-details)
        * [Notifications](#notifications-1)
            * [Tier One](#tier-one)
            * [Tier Two](#tier-two)
    * [Responsive Design](#responsive-design)
* [Features for future implementation](#features-for-future-implementation)
    * [Asynchronous Messaging and Notifications](#aynschronous-messaging-and-notifications)
    * [Google Calendar API Integrations](#google-calendar-api-integration)
    * [Customised Emails with Attachments](#customised-emails-with-attachments)
    * [Sheet Music Resources](#sheet-music-resources)
* [Technologies Used](#technologies-used)
    * [Development](#development)
    * [Design](#design)
    * [Languages](#languages)
        * [HTML](#html)
        * [CSS](#css)
        * [JavaScript](#javascript)
        * [Python](#python)
            * [Python Libraries](#python-libraries)
    * [Other Libraries/Frameworks](#other-librariesframeworks)
    * [Database](#database)
    * [Technologies for Testing](#technologies-for-testing)
    * [Hosting](#hosting)
* [Testing](#testing)
* [Deployment](#deployment)
    * [Prerequisite](#prerequisite)
    * [Deployment to Heroku](#deployment-to-heroku)
        * [Creating an App](#creating-an-app)
        * [Initial Deployment](#initial-deployment)
    * [Environment Variables](#environment-variables)
        * [Production Environment](#production-environment)
        * [Your Django SECRET_KEY](#your-django-secret-key)
            * [Amazon S3 Bucket ACCESS_KEY_ID and SECRET_ACCESS_KEY](#amazon-s3-bucket-access-key-id-and-secret-access-key)
            * [Stripe Credentials](#stripe-credentials)
            * [Gmail Credentials](#gmail-credentials)
        * [Get your Postgres Database URL](#get-your-postgres-database-url)
        * [Create your Postgres Database URL in settings.py ](#connect-your-postgres-database-url-in-settingspy)
        * [Create a superuser](#create-a-superuser)
        * [Create your Production and Development Config](#create-your-production-and-development-config)
        * [Connect your Amazon S3 Bucket to Django](#connect-your-amazon-s3-bucket-to-django)
        * [Visit Heroku and Launch The App](#visit-heroku-and-launch-the-app)
    * [Running the Project in your Local Environment](#running-the-project-in-your-local-environment)
        * [Forking the local repository](#forking-the-local-repository)
        * [Cloning the repository](#cloning-the-repository)
        * [Downloading the files as a ZIP](#downloading-the-files-as-a-zip)
        * [Install project dependencies](#install-project-dependencies)
        * [Local Environment variables](#local-environment-variables)
* [Credits](#credits)
    * [Code](#code)
     * [Dropzone JS](#dropzone-js)
     * [FullCalendar](#fullcalendar)
     * [ToastifyJS](#toastifyjs)
     * [Formset Factory](#formset-factory)
     * [to_dict() function](#todict-function)
     * [Notifications](#notifications-2)
     * [handle_GET_params()/UserProfile custom queryset](#handlegetparamsuserprofile-custom-filter-queryset)
     * [Stripe Subscription/Customer Portal](#stripe-subscriptionscustomer-portal)
    * [Design](#design)
    * [Text Content](#text-content)
    * [Logo](#logo-1)
    * [Images](#images)
* [Acknowledgements](#acknowledgements)

# Overview

DepT comes from the word “to dep”, which is a term that is commonly used within the music industry to describe a musician who takes the place of a
regular band member temporarily - usually when a band member has fallen ill, has a personal issue, or more commonly has been offered a better-paid gig (such as a tour). 

The idea for the platform is born out of the personal struggle of finding last-minute “deps” outside of my immediate network.
Also, due to Covid-19, connecting with other artists and finding work has been difficult.

# UX

## Strategy

### Stakeholder Interviews

What problems/pain points do you experience when searching for a dep?

* *"My immediate network is limited by the number of musicians in my contact list"*

* *"My immediate network is limited to the locality of the area in which I live and work."*

* *"It takes a lot of time and effort to source a suitable dep, especially when the situation is time-sensitive"*

* *"A dep's availability (or lack thereof) can only be determined through a phone call or text, which is not time-effective."*

* *"A limited network of deps in the local area can result in travelling a long distance to a gig, which increases environmental impact."*

* *"There's a lack of opportunity to make myself more discoverable among a wider network of musicians."*

### Ideal Users

* Musicians/artists operating in the music industry who need to 'dep' out a gig.
* Musicians/artists operating in the music industry who are looking for job opportunities.
* Bookers/band-leaders/producers who are in need of a last-minute musician/artist to provide their services.

### Project Goal

To provide a sleek, efficient and trustworthy booking service, enabling musicians to dep out their gigs and for clients to find dep musicians, all with minimum stress.

### User Stories

#### First-Time Visitors

As a visitor using the website for the first time, I want...

1. The purpose of the website to be evident upon the first visit, so I can quickly determine that the website will suit my needs.
2. To be able to navigate the website intuitively and with ease on all devices, so that my time isn't wasted.
3. To easily find information about how to use the platform, so I can understand the model of the service provided.

#### Potential Members

As a potential member, I want...

1. To easily find out what benefits I get from being a paying member, so I can determine whether the service is worth my money.
2. To browse the website without having to register.
3. To be able to register to the website, so I can manage and display a profile.

#### Deps For Hire

##### Tier One Membership (Free)

As a Tier One member of the website, I want...

1. To be able to upload samples of my music to my profile, so I can showcase my skills and expertise.
2. A link to my profile to be listed on a page, so potential clients/musicians will be able to find me easily.
3. To be able to find other members using the service, so I am able to find a dep easily in the case that I can't make a gig.
4. To be notified when I get a job offer from a another member, so I can respond quickly and professionally.
5. To be able to message a member with a response or any questions without leaving the website, to make the process run as smoothly as possible.
6. To be able to message other members of the website, so I can grow my network.
7. To display reviews/ratings from members for who I have provided services, so I can improve my reputation in the community.
8. To access a dashboard displaying a record of ratings and reviews, so I can take account of how much I am benefitting from the service.
9. To be able to manage my subscription, so I can update my subscription tier when I like.
10. To be able to browse the Tier Two 'Find a Job' page without subscribing, so I can determine whether subscribing to a Tier Two service is worth the money.

##### Tier Two Membership (Paid)

As a Tier Two member of the website, I want...

1. All privileges provided by Tier One Membership.
2. To have access to a job listing, so I can find jobs that are in my area.
3. To be able to filter jobs by location or fee range, so I can more granularly search for a suitable job.
4. To be able to post a job that's in need of a dep, so I can be sure that my job gets the attention of Tier Two deps.
5. To be able to edit or delete a job that I've posted, in case I have made a mistake, or that I've found someone to do the job from outside the website.
6. To be notified when I received an offer for a job I've posted, so I can determine which member might be the right fit, with efficiency.
7. The members who have expressed interest in my job to be clearly visible, so I can inspect who might be a good fit, with ease.
8. To be listed at the top of searches when a potential client/musician is searching for a dep, so I can have a better chance of getting the work.

#### Members in need of a Dep

As a member who is looking for a dep musician, I want...

1. A page where I can search for dep musicians, so I can easily begin to find a dep.
2. To be able to filter musicians by their expertise, instrument or style of music they play, and location, so I can find a dep which suits my needs.
3. To be able to visit a dep's profile page, so I can find out more information about their experience and expertise.
4. To view a calendar of available/unavailable dates, so I can find out if a dep is available before pursuing further.
5. To hear samples of a dep's music, so I can be confident that they will provide a good service.
6. To be able to message a potential dep with an invitation from within the website, so that no unnecessary time is wasted.
7. To be able to or edit or delete my invitation, in the case that I make an error in the form, or I find another dep from another source.
8. To be notified when I have received a response from a dep I have messaged, so I can confirm the arrangement quickly and smoothly.
9. To be able to send a confirmed dep a document with job details (with location, timings, number of sets etc), to allow for effective communication.


### Strategy Summary

Taking the project goal and the user stories into account, below is bulletted summary of the user needs and project objectives, required to achieve an MVP.

#### User Needs

* To be able to navigate the site intuitively and with ease.
* To be able to register, log in, and log out.
* To be able to subscribe to a Tier 1 or Tier 2 subscription.
* To be able to upgrade from a Tier 1 to a Tier 2 subscription.
* To be able to find other musicians to dep a gig to.
* To be able to display a calendar of days where I am available/unavailable.
* To be able to find listed jobs.
* To hear samples of a potential dep's music.
* To be able to message a potential dep with a job offer.
* To be able to receive a message from a contacted dep, to receive confirmation or refusal of a request.
* To be able to send details of a job to a confirmed dep.
* To be notified whenever I receive a message from another user of the website.

#### Project Objectives

* To allow all users of the website to navigate the website with minimum cognitive overload.
* To allow musicians to dep out their gigs with ease.
* To offer clients a stress-free way to find a dep musician to provide their services.
* To provide an end-to-end searching, messaging and booking service for all users.
* To paywall features between Tier 1/Tier 2 users.
* To provide incentives for Tier 1 users to upgrade to Tier 2.

## Scope

### Features

#### User Interface

* Users must be able to navigate and use the website with minimum cognitive overload.
* Users must be provided a clear path through the searching, messaging and booking process, with sufficient indicators and feedback.
* Users should be provided notifications to users when they have been contacted.
* Ensure the design of the website is responsive on all device sizes.

#### Authorization/User Management

* Users must be allowed to register, confirm their email address, login and logout to the website.
* Users must be able to reset their password, should they need to.

#### Dep Profiles

* Allow users to create, visit and edit a profile.
* Allow users to upload samples of their music to their profile.
* Implement a music player to allow for playback of their music.
* Provide a calendar for users to input and show their availability. 
* Display star rating and reviews.
* Allow users to delete profile.

#### Dashboard

* Users can visit their own dashboard page.
* Users should be able to view metric data including completed jobs, repeat business, and number of different clients.
* Users should be able to see how many invites and active engagements they have received from clients.

#### Tier One/Tier Two Content

* Messaging between users of the website.
* Notifications to users who have been contacted.
* A page listing the musicians using the service.
* Search/filter functionality to filter for a musician specializing in a specific genre/style.

#### Tier Two Content

* Create a paywall between Tier One and Tier Two content.
* Place links to Tier Two profiles at the top of the list of musicians on the relevant page.
* Create a page displaying a list of jobs offered by clients, offered only to Tier Two users.
* Allow users to upgrade from a Tier One to a Tier Two account.

#### Booking

* Provide a page with a form to allow for users to message a potential dep with a job offer.
* Provide a page with a form to allow for users to message a confirmed dep with job details.

#### Messaging

* Messaging functionality between deps and clients.
* Ability to message clients/deps from profiles, artist-list page and notifications.

#### Notifications

* Display a clickable icon in the navbar, along with account of a user's unread notifications.
* A dropdown list of all notifications a user has received.
* When a notification has been read, update the database accordingly.

## Structure

### Informational Architecture

#### General Considerations

To achieve an effective, intuitive architecture that is simple to navigate, there are two primary users that need to be taken into consideration:

* Members looking for work
* Members looking for a dep

Taking this into account, it is important to provide two clear paths through the website. One which suits the dep who is signing up to the service, 
and another which suits the member who is searching for a dep.

The common denominator between these two types of user is the need to view notifications and messages easily. Since the model of the website is centered around
communication (clients contacting deps and vice versa), it is of primary importance that both users are always able to keep track of when they have been contacted.
In an attempt to provide intuitive navigation in this regard, both users must have the ability to view notifications and messages from a Navigation Bar, 
which persists across all pages of the website. Furthermore, the website must provide sufficient navigational aids in the NavBar, and an abundance of 'call-to-action' buttons
which provide a clear path through the website, relative to the type of user.

#### Navbar

The navigation bar will persist across all pages of the website, allowing the user to navigate to any page with ease. 

#### Home Page

The home page is the landing page of the website. At the top level, a lead paragraph will brief the user of the clear purpose of the website.
Three call-to-action buttons will be featured:

* Sign In - Takes the user to through the website's authentication process.
* Find a Dep - Takes the user to the dep list page.
* Post a Job - Takes the user to a page to post a specific job.

The section below will display a list of links directed towards a user who is looking for a dep. These links will be categorized based
on the instrument/service that's required (Pianist, Violinist, Cellist, Drummer etc).

Another section will be present, featuring a more detailed overview of the website and testimonials.

#### Account Management

Users will be allowed to register, create an account, login, logout and reset their password.

#### Sign Up/Subscription

Following the user registering, the website's sign up process will proceed with presenting the user with two membership options:

* Tier One (Free)
* Tier Two (Paid)

Each option will detail the price, the services that the subscription offers, along with an incentive for the user to select a Tier Two membership.

Selecting Tier One will take the user directly to a page to add more details to their profile.

Selecting Tier Two will take the user through a Stripe payment procedure. 

#### Profile

At the top level, an image of the member will be presented, along with the instruments that they play, their location,
 and a call-to-action to book this member.

If the profile belongs to the user visiting, a call-to-action to edit their profile will be presented clearly.

Below, a music player will be displayed, along with a calendar of their available and unavailable dates.

Additionally, a detailed overview/pitch will be displayed (if provided by the user), along with work experience, and links to videos/recordings that they have
contributed to in the past.

On laptop/desktop devices, a sidebar will also be present with a list of reviews and star ratings (if any). This will collapse to full-width column on mobile.

#### Dashboard

The member's dashboard will present an overview of a history of any interactions/bookings through DepT.

At the top level, the user's membership status will be displayed. If they are on Tier One, an invite will be offered to the user to upgrade to Tier Two.

A list of all engagements will be present, filterable by 'past', 'invited' and 'active' engagements.
Each item in the list of engagements will be clickable, taking the user to the booking confirmation with details about the booking.

Additionally, details on profile 'completeness' will be displayed through a graphical progress bar, along with metric data of the user's number of jobs, repeat business and past clients they have worked with.

#### Find a Dep

The list of deps will be categorized by instrument/expertise, each represented by a link. For instance, a user can click a button for 'Keyboard Players', and be taken to a page listing keyboard players.
The top level will feature most common categories of instruments, such as Guitar, Drums, Bass, Keyboards or Vocals. A list of all remaining instruments will be listed below.

The dep list itself will be filterable by location, rating and availability. Each dep will be displayed on a card, along with rating, and a link to their profile.

Premium users will be given preferential treatment in the listing, being listed at the top of searches.

#### Invite Form

If a member is interested in hiring a particular dep, they can send an invite through a form. The form includes the type of engagement (such as function, festival, or studio work), the fee, the location, and setlist (if required).

#### Invite Page

If a member has been invited to a booking, they are presented with the details of the engagement, along with two buttons to either accept or deny the invite.

Additionally, the invitee and inviter will be able to message each other through this page, should there be further information required from the invited dep before booking.

#### Booking Form

If a dep has accepted an invite, the member offering the gig can use a form to provide all details pertaining to the engagement, including a file input which will handle PDFs for sheet music.

#### Booking Confirmation

Once a dep has received a confirmed booking, they will be sent an email with the full details of the engagement. This will be downloadable to a PDF format.
An email will also be sent to both parties involved in the booking.

#### Post a Job

Users wanting to post a job to the Job Page can do so through a form.

The form will prompt the user to enter the type of engagement (such as function, festival, or studio work), 
the fee, location, instrument required, and setlist (if applicable).

#### Job List Page

Premium deps will be able to view a bulletin board of jobs posted by other members. Jobs will be presented on individual cards, which open modal windows displaying information about the job.
Deps can register their interest in a particular job by messaging the member who posted the job, from the modal window. 

The member who posted the job will then receive notification of a dep's interest. The notification will prompt to either accept or decline the request, or visit the dep's profile.

### Database Structure

The project makes use of the SQlite Relational Database to handle data served throughout the website during development, and will be migrated to postgresql upon deployment.

#### Schema 

##### Iteration 1

![Database Schema for DepT Website](documentation/er_diagram/dept_er_diagram_1.png)

##### Iteration 2

![Database Schema (Iteration 2) for Dept Website](documentation/er_diagram/dept_er_diagram_2.png)

##### Iteration 3

![Database Schema (Iteration 3) for Dept Website](documentation/er_diagram/dept_er_diagram_3.png)

##### Iteration 4

![Database Schema (Iteration 4) for Dept Website](documentation/er_diagram/dept_er_diagram_4.png)

## Skeleton

### Wireframes

* [Home Page](documentation/wireframes/dept_homepage.pdf)
* [Register](documentation/wireframes/dept_register.pdf)
* [Subscribe](documentation/wireframes/dept_subscribe.pdf)
* [Sign In](documentation/wireframes/dept_sign_in.pdf)
* [Edit Profile (Page 1)](documentation/wireframes/dept_edit_profile_1.pdf)
* [Edit Profile (Page 2)](documentation/wireframes/dept_edit_profile_2.pdf)
* [Profile](documentation/wireframes/dept_profile.pdf)
* [Find a Dep (Instrument List)](documentation/wireframes/dept_find_a_dep.pdf)
* [Find a Dep (Dep List)](documentation/wireframes/dept_dep_list.pdf)
* [Job List Page](documentation/wireframes/dept_find_a_job.pdf)
* [Dashboard](documentation/wireframes/dept_dashboard.pdf)
* [Enquiries](documentation/wireframes/dept_enquiries.pdf)
* [Booking Form](documentation/wireframes/dept_booking_form.pdf)
* [Booking Confirmation](documentation/wireframes/dept_booking_confirmation.pdf)

## Surface

### Background Colours

![Colour Scheme for Background Colours of DepT Website](documentation/readme_images/colour_palette/dept_background_colours.png)

* Space Cadet (#1a2342)
    - This colour is consistently used as the background for all top-level headers throughout the website, to provide a sufficient contrast against the white text that it sits behind, while also maintaining a satisfying, reputable aesthetic.

* Independence (#45425a)
    - Used for the navigation bar, footer and header background in modal alerts, and also as the background in one mid-level section of the home page, and in modal forms (Invitation Form, Job Post Form and Review Form). This colour was chosen primarily due to it's contrast between the primary background colour (Space Cadet). Furthermore, it also provided a pleasing contrast to the foreground colours that it sits behind (white font colour, and golden colour used for rating stars). 
* White (#FFF)
    - Used for mid-level elements throughout the website, where most of the interaction takes place, and features are presented. The developer experimented with less "basic" background colours for mid-level elements to achieve a more "artistic" look, but after consideration it was determined that it was more necessary to contrast the darker, more-bold top-level elements with a more-standard colour which presented it's foreground elements sufficiently.

* Cultured (#EEE)
    - Used to provide a small contrast against the white background of some mid-level elements, such as the filter accordion (featured in the Dep List and Job List pages). This background colour is used also for the wrappers for all form elements throughout the website.

* Violet Web (#FF91EF) & Lemon (#FFF900)
    - These two colours are used in combination with a linear-gradient with an light opaque overlay. Used as the background colour for the Sign Out page, and also for the authorization flow when a user resets their password. Furthermore, this colour is used on large screens to show secondary-lead text in top-level elements of certain pages (Checkout Success, Dashboard, Edit Profile), and as the background for default card-images and user profile images in the case where a user hasn't added a profile image.

* Smoky Black (#111)
    - Used as the background colour for filter-accordions in the Dep List and Job List pages. Since the top-level header background is already rather dark, and the mid-level contrasts heavily with a sheer white, it was decided that a darker, almost black colour was required to draw the user's attention to this filter-accordion feature.

### Foreground Colours

![Colour Scheme for Foreground Colours of DepT Website](documentation/readme_images/colour_palette/dept_foreground_colours.png)

* Space Cadet (#1a2342)
    - In addition to using this colour for backgrounds, it is used as the background for some buttons throughout the website. Featured in the Edit Profile pages ('Add More Gear'/'Add More Audio' buttons), as well as buttons in metrics cards in the first section of the Dashboard page. This colour was chosen so as not to provide too much suggestivity to the role of the button, suggesting that the call-to-action is of a neutral nature.

* Sea Green (#0E8347)
    - Heavy use of this colour is made as the backgrounf for buttons throughout the website, including those to visit profiles, invite members to gigs, post jobs, leave reviews and close modal alert windows. This colour is chosen as it suggests that the call-to-action that the button represents is of a positive nature.

* Ruby Red (#9C1E1E)
    - Also used as background for buttons throughout the website, this colour is used for call-to-actions which are of an alertive nature, such as when a user decides to delete a job, invitation, profile or review. Additionally, this colour is used as the font colour for form errors.

* Bronze (#CF8036)
    - This colour is used to highlight active sections in the Dashboard 'Jobs' Page, to inform the user whether they are on a tier-one or tier-two section, and whether they are on their 'Received Invitations' or 'Sent Invitations' section. This active colour contrasts against the alternative button's black background, and will hopefully serve to clearly indicate which section of the Dashboard's Job Page the user is browsing.

* Amber (#FFC107)
    - Used for button styling on cards to display invitations sent by a user, specifically for the button inviting the user to 'Send Complete Details' for a particular invitation. This colour was chosen to indicate to the user that there is action that might need to be taken.

* Spanish Grey (#9B9A9A)
    - Used to display user details on cards displayed in the Dep List page. Since the cards are fairly small, and a relatively large amount of textual information is presented on these cards, it was deemed that this colour would serve to provide enough contrast while not busying the screen real-estate, and retaining a pleasing aesthetic.

* White (#FAFAFA)
    - Used for font colours throughout the website, in sections that use a darker background colour. Chosen primarily to provide sufficient contrast.

* Eerie Black (#202020)
     - Used for font colours that sit on top of lighter background colours, again to provide sufficient contrast.

### Logo

![Image of DepT Logo](documentation/readme_images/logo/dept-logo.png)

A simple, white-on-black logo was designed to represent the website's brand, serving to clearly present the intention of the website without any artistic frills, while also looking sleek and reliable. Displayed in the website's navbar, home page header and in authorization flows, as well as a default logo in the Booking Details/Booking Success pages, should a user profile image not be available for use. Additionally, this logo is featured on any cards in Dep List and Job List pages where a user profile image hasn't been provided.

### Typography

#### Primary Font

![Primary Font for DepT Website](documentation/readme_images/fonts/dept_primary_font.png)

The font [Josefin Sans](https://fonts.google.com/specimen/Josefin+Sans) is used for top-level header elements throughout the website, as well as modal headers, and text content on job cards.
Intended to provide some personality and sleekness against the more utilitarian fonts used for the mid-level elements, and draw the user's attention while also remaining not-too overbearing.

![Secondary Font for DepT Website](documentation/readme_images/fonts/dept_secondary_font.png)

#### Secondary Font

The font [Oxygen](https://fonts.google.com/specimen/Oxygen) was chosen to present the text-content of mid-level body elements of the website. Intended to provide a more functional, utilitarian feel to contrast against the more-suggestive header font, and not be too overbearing or provide congitive overload, particularly for sections of the website that contain a relatively substantial amount of text content.

![Tertiary Font for DepT Website](documentation/readme_images/fonts/dept_tertiary_font.png)

#### Tertiary Font

The font [Open Sans](https://fonts.google.com/specimen/Open+Sans) was chosen to present bottom-level text content in the website's footer. Used to provide a little contrast against the secondary font, to reinforce the role of the footer while not being too contrasting.

### Header Design

![Header Design for DepT Website](documentation/readme_images/fonts/dept_tertiary_font.png)

When on large screens, many headers throughout the website are split into two halves. The left half of the header generally features header content along with any lead paragraphs, while the second half of the header, contrasting in colour, serves to act as a window, either displaying further text content (as is the case in the Dashboard and Edit Profile pages), or displaying a user's profile image (in the Profile, Booking Detail and Booking Success pages). A user's profile image is displayed as a background image on mobile/tablet devices, to retain responsivity while also maximising design flexibility.

Since the website is centered around social interaction and networking, it was deemed important that a user's profile image should be displayed in any pages which are centered around networking, such as the Profile, Booking Detail and Booking Success Page. Therefore the initial decision was made that these types of pages provide a header 'window' displaying a user's profile image. This split-header design decision was then extended throughout the headers on most other pages of the website, to provide stylistic consistency.

### Visual Effects

#### Box Shadow
The website makes heavy use of the box-shadow, primarily to present form elements and cards in Dep List and Job List pages. Since a white background is used for the body of many pages of the website, and the form elements are a lighter grey colour, a box-shadow helps to provide some depth to the light-coloured elements that sit against a white background, and make the website feel a little less two-dimensional.

#### Text Shadow
The foreground elements in pages that employ a linear gradient background colour have a slight shadow effect applied, to provide a little depth between the foreground and the background, and make the page feel more three-dimensional.

#### Colour Gradient

![Linear Gradient](documentation/readme_images/visual_effects/dept_linear_gradient.png)

A linear gradient with opaque-overlay was employed to between the colours Violet Web (#FF91EF) & Lemon (#FFF900) with, as a background colour for most pages used in the authorization flow. The decision to use this effect was purely of an aesthetic nature, in the hope that it serves to relax the user and reinforce the role of the pages, in addition to adding a little artistic flare and interest.

#### Hover Effects

Hover effects for top-level buttons are employed on large screens, which change a button's neutral off-white colour to a less neutral colour which indicates the nature of the call-to-action the button represents. Used so as not to busy the top-level with too much colour, and minimise cognitive overload.

#### Animations

Animation effects are employed in the website's 'Edit My Profile' page, used in the breadcrumb nav elements to indicate which section of the form a user is currently on. Once a user submits a section's form, the breadcrumb animates a colour fill, to indicate to the user that they have completed a section of the form page. The decision to use animated breadcrumbs should serve to make the form-filling process feel a little less mundane and boring, and provide the user with a feeling of progression.

# Features

## Existing Features

### Subscriptions

The [Stripe](https://stripe.com/gb) framework provides functionality for users to subscribe to the DepT service.

The subscriptions page provides the user a choice between either subscribing as a Tier One member, or as a Tier Two member.
The subscription choices are presented on relative cards, with a list of benefits tied to each subscription tier, along with a button inviting the user to subscribe.

Upon selection of a subscription tier, the user is redirected to a Stripe checkout, where the user can enter their card details and finalize their subscription. If a user decides to cancel their subscription, they may click Stripe's 'cancel' button, and be redirected back to DepT's Home Page.

If a user has already subscribed, the subscription card which is paired with their subscription status is indicated through the text content of the card's button, which will display 'Your Current Subscription'.

If a user wishes to update their subscription plan, they may click on the alternative card's button. Upon clicking, they will be redirected to Stripe's customer portal, which keeps a track of the subscribed user's status, and allow the user to make any changes to their subscription.


### Find a Dep

This page features a collection of all members who are registered and subscribed to the platform. Each dep is presented on a card, with high-level details and average review rating displayed (in the form of star icons, and number of reviews). Each card features a button to visit the member's profile page.

The collection is filterable by:

* Instrument
    - Presented as a dropdown
* Location
    - Presented as a search text input
* Genre
    - Presented as a dropdown
* Available Today
    - Presented as a checkbox

Additionally, a visitor can sort the collection of deps by rating, from low to high and high to low.

Tier Two members have priority and are featured at the top of the list, regardless of search and sort criteria.

### Profiles

[Django Allauth](https://django-allauth.readthedocs.io/en/latest/installation.html) is employed to handle user-management and provide authorization flow for registering, signing in, logging out, and resetting a user's password. Upon registration to the platform, a signal is sent to create a User Profile, which shares a One-To-One relationship with the auth-user model.

#### Profile Page

##### Header

![DepT Profile Header, Large Screens](documentation/readme_images/profile/dept_profile_header_lg.png)

A user's profile page serves as the base for a user to present themselves and the services they can provide, and is the first point of contact for a user who is searching for another user to play their gig.

The header of the profile page provides such details as a user's:

* Full Name
    - If no name has yet been provided, this defaults to the user's username

* Location 
    - Not displayed if no location has been provided.

* Instruments they play
    - Not displayed if no instruments have been provided.

* Review Rating (represented by stars)
    - "No Reviews" is displayed if a user has no reviews

* Profile Image
    - Defaults to the DepT Logo with a linear-gradient background if no profile image provided.

Below the header are two buttons, inviting the visiting user to either:

* Contact the user who owns the profile.
* Leave the user a review.

If user is unauthenticated, these buttons will take the user to the login page, and then will be re-directed back to the
profile page.

Furthermore, if a user doesn't have subscription status, a modal pop-up is shown, indicating that they need to subscribe in order to invite users to play gigs.

If the user visiting the profile is the profile owner, the two buttons change to invite the profile owner to either:

* Edit their Profile
* Delete their Profile

##### Body

![Dept Profile Body, Large Screens](documentation/readme_images/profile/dept_profile_body_lg.png)

The main body of the page is where the user can make their pitch, and provide an in-depth overview of their expertise and services they can provide. Reviews for a user are displayed below the user's pitch. The body also features the an interactive music player, which the visiting user can use to sample any music the profile owner has uploaded to their profile. 

Additionally, a calendar is featured displaying the user's unavailable dates (marked in a light red colour), so the visiting user can quickly determine whether the profile owner will be available to play a gig. 

Below the music player and calendar, a small list of the user's Genre expertise is displayed, along with any equipment information they would like to submit. 

The music player, calendar, genre list and equipment list are displayed as a sidebar on large screens, and collapse to full-width columns on tablet and mobile devices.

##### Modals

###### Invitation Modal
Should a user visiting the profile decide they want to invite the profile owner to play a gig. They may click a button to open a modal window to send an Invitation. Here they can provide gig details such as:

* Event Name
* Artist Name
* Event City
* Event Country
* Date and Time of the Event
* The Fee
* Additional Information

Form validation is provided using AJAX. 

The invitation modal is accessible only to members who have subscribed to the platform.

###### Review Modal
Should a user like to leave a review to the profile owner, they may click on a button to open a modal window to leave a review. The form features clickable star icons to leave a rating from 1-5, and submit text content using the text area provided in the form.

#### Edit Profile Page

##### Edit Profile Pages

A registered user can access a page where they can edit their personal and profile details. This page is split into three sections:

* Personal Details
    - Here the user can provide their name, location, instruments and genres of expertise, a list of their equipment, and a textarea where they may provided a detailed overview of their expertise, and make their pitch.

    Should the user decide they want to make a change, the initial data they provided will be presented as values in all
    the relevant fields when they next visit the page.

* Audio Files
    - Here the user may upload any audio files that they believe may be of interest to other users of the website.
    The Graphical User Interface is in the form of a drag-and-drop window (provided by [DropzoneJS](https://www.dropzone.dev/js/)), where users can choose to either click the window to open their file system and choose files manually, or drag and drop their files into the window. Upon loading of an audiofile, a widget is shown, displaying the name of the audio file they have added, and their filesize. 

    Files no larger than 5MB may be uploaded.

     Should the user decide they want to delete a file, the initial audio files they provided will be presented as widgets in the GUI, with an option to remove the file presented below the GUI.

* Unavailable Dates
    - The third and final form of the Edit Profile Page features a GUI calendar (provided by [FullCalendar](https://fullcalendar.io/)), where users can submit dates where they are unavailable. Users can interact with the calendar by cycling through each month (by clicking the caret buttons in the top right corner of the header), and clicking on dates where they are unavailable. Upon clicking a particular date, the background colour of the date they clicked will turn a light red, to indicate that this date has been selected, and provide feedback to the user.

    Should the user like to de-select a date, they may click the date again, which will remove the date from the collection to be submitted, and return the colour of the date to a white colour.

    If the user wants to make a change after submitting the form, all dates they have already selected will be presented as initial data on the calendar.

##### Breadcrumbs

Considering that the form is split into three pages, it was deemed necessary to provide breadcrumb navigation so that the user can feel some progression in what might feel like a long, drawn-out process, and provide a feeling that they are working towards a goal. 

Upon submission of each form, the breadcrumbs animate, and are filled with a green colour to indicate to the user that they have just completed a form section. On large screens, the breadcrumbs are presented as text. When collapsing to small screens, 
the text content is replaced with FontAwesome icons, to visually represent the purpose of each form page.

##### Skip Step/Go Back Buttons

Users have the option to skip a step, or return to a previous form page at their will. If the user chooses to skip a step instead of submitting a form, the breadcrumbs will not animate and fill with colour.

#### Dashboard

Each registered user has access to a dashboard. The top level header features a navigation bar with links to:

* **Dashboard**
* **Jobs**
* **Your Membership**

The 'Dashboard' and 'Jobs' links take the user to the respective child-pages of the parent 'Dashboard' page, while the 'Your Membership' link takes the user to the page to choose their subscription.

##### Page One

The first child page of the dashboard page features the user's profile metrics, such as:

* Their subscription status
* Invitations they have yet to respond to
* How complete their profile is (represented as a progress bar)
* Their average rating

Each item of metric data is presented as a card, with a call-to-action below each item. If a user has Tier One status, a list of Tier Two benefits and a button is presented, inviting them to upgrade their subscription. If a user has not yet subscribed, they are presented with a card inviting them to subscribe so that they can appear in searches and invite other members to jobs.

 If a user hasn't completed their profile, a call-to-action is presented to visit their Edit Profile page to complete their profile. 

 If a user has some invites they need to respond to, a call-to-action is presented, inviting the user to visit their Jobs page and respond to their pending invites.
 
Lastly, if a user has no reviews, a button is provided to take the user to the DepList page, to 'meet the community'. 

##### Jobs Page

The second child page of the Dashboard page is where the user can keep track of their active jobs. This page is split into two sections, "Tier One" and "Tier Two", which are accessible through navigation buttons.

###### Tier One

The Tier One section displays all invitations a user has sent or received. These two criteria are split into respective sections:

* Invitations Sent
* Invitations Received 

Each section is accessible through navigation buttons.

Both sent and received invitations are filterable by:

* All
* Pending
* Confirmed

The invitations themselves are presented as cards, featuring the high-level details of a particular engagement.

All cards for invitations that have been sent and pending a response, feature buttons for the user to edit or delete their invitation. 

All cards for invitations that have been received and pending a response, feature buttons for the invited user to either accept or decline an invitation.

If an invitation receiver has accepted an invitation, the card presenting that particular invitation then features a button to 'Send Complete Details', and take the invitation sender to a booking form, where they can finalize their booking.

Once an invitation receiver has accepted an invitation, a disabled button is presented informing that the accepted invitation is 'Waiting for Details'. Once the invitation sender has finalized the booking, the disabled button is replaced with a button to 'View Full Details', which takes the user to a Booking Detail page.

Both invitation senders and invitation receivers involved in an active engagement are able to message eachother about the engagement, by opening a modal chat window from clicking a button "Message <user>". Any messages that have been previously sent will persist, and be displayed in the modal window upon a later visit. 

###### Tier Two (Premium)

The Tier Two section displays all information about any jobs a Tier Two member has posted or made an offer for. Similarly to the Tier One section these two criteria are split into respective sections:

* Posted Jobs
* Offers Sent

Each section is accessible through navigation buttons.

Simlarly to Tier One, posted jobs and offers-sent are filterable by:

* All
* Pending
* Confirmed

Jobs are also presented on cards, featuring high-level details about the job the user has posted, or a job they have made an offer to play.

If the user has posted a job, the card displays information on how many other users are interested in taking the job. Clickable avatars of the interested members are displayed, which are linked to their respective profiles. A button is also displayed inviting the job poster to 'Choose a Member'. This opens a modal window displaying a list of all users who have expressed interest in taking a job. From here, the Job Poster can select one of the members to take the job.

If no offers have been made for the job, the 'Choose a Member' button is replaced with a disabled button displaying text content 'No Offers Received.

If a Job Poster has not yet chosen a member to take the job, they can either delete or edit their invitation, using buttons presented on the card.

Once a Job Poster has confirmed a member a line of communication is opened, and the Job Poster/Confirmed Member can exchange messages by use of a chat modal window, accessible through a button "Message <user>", displayed on a card. The list of avatars is replaced with an avatar of the confirmed member. Furthermore, similarly to the Tier One booking flow, the Job Poster is presented with a button to 'Send Complete Details', which takes them to a page to finalize their booking.

If a user has sent an offer to play a job that another user has posted, and has been confirmed, they are presented with a disabled button with text content 'Awaiting Full Details'. Once the Job Poster has finalized the booking through the booking form, this button is replaced with a button to 'View Full Details'.

Note, the Tier Two section is only accessible to users who have a Tier Two subscription.

### Find a Job

This page features a collection of all jobs that have been posted by members using the Tier Two service. 

A button is displayed in the page's header, inviting a user to 'Post a Job'. This triggers a modal window with a form for the user to provide details about the job, which will then be displayed on a card below. If a Tier One user clicks this button, an alert modal is displayed informing the user that they need to subscribe to Tier Two to post a job.

Similarly to the 'Find a Dep' page, all jobs are presented on individual cards, which high-level information about the job, and an image representing the artist or nature of the job that has been posted. Visual indicators are displayed to represent how lucrative the job is, by way of dollar signs (one dollar sign being not very lucrative, and five dollar signs being very lucrative).

The cards feature two buttons:

* View Details
    - Opens a modal window displaying further details about a job.

* Make An Offer
    - A user can click this button to register interest in taking this job.
    - If clicked, the user can 'Remove the Offer' by clicking the same button.
    - This feature is only accessible for Tier Two users.

 As with the 'Find a Dep' page, Jobs are filterable by:

 * Location
    - Presented as a search text input
* Fee Range
    - Presented as a select dropdown

### Booking Form

For Tier One or Tier Two users who have confirmed a member on their posted job, or had their invitation accepted, they can visit a booking form where they can finalize their booking. 

Here they are prompted to provide the venue address, any audio resources that would be useful for the acquired dep to peruse, and any travel or backline information.

Django's ``modelformset_factory`` is employed to dynamically add extra audio file fields to the form, should the user wish to provide more than one audio file. A maximum of five audio files can be added.

### Booking Details

The booking details page is shared between both Tier One and Tier Two engagements.

Once a booking has been finalized, both the invitation sender/invitation receiver (Tier One) or job_poster/confirmed_member (Tier Two) can visit this page to browse the finalized details of a given booking. 

If the invitation receiver/confirmed member is visiting this page, they are presented with two buttons to:

* Download the Booking Details as PDF
    - Useful if the venue the event is taking place might be in an area with no internet.

* Download any audio files that have been submitted, if any.

### Notifications

Notifications are in important aspect of a social networking website such as DepT. With this, there is a notification dropdown
which persists across all pages within the website's navigation bar. The dropdown button is represented with a bell icon, along with a Bootstrap 'badge', which displayed how many notifications a user has been sent.

Notifications to a user are sent in the following events:

#### Tier One

* A user has received an invitation from another user.
* A user has accepted another user's invitation.
* A user has received a message about an active engagement.
* A user has accepted another user's invitation.
* A user has received booking details for an accepted invitation.
* A user has decline another user's invitation.

#### Tier Two
* A user has registered interest in another user's posted job.
* A user who has registered interest in a posted job has been confirmed.
* A user has received booking details for a confirmed job.
* A user has received a message about a confirmed job.

Both Tier One and Tier Two users are sent notifications whenever they receive a review.

### Responsive Design

The Bootstrap framework was used to provide responsivity across all device screen sizes, using their pre-defined 
widths from 320px and up. Additionally, heavy use of CSS media queries have been made to re-arrange and re-style certain header and navigation elements featured in the website, and to ensure that the website is also responsive on extra large screens. 

All screen sizes have been taken into consideration when developing the website, to maximise responsivity and ensure a positive user-experience across all screen sizes.

## Features For Future Implementation

### Aynschronous Messaging and Notifications

In the initial planning stages of the website's development lifecycle, the developer embarked on tutorials in creating a chat service using the [Django Channels](https://channels.readthedocs.io/en/stable/) integration, which uses web sockets and asynchronous functions to provide real-time messaging. The developer sought to include this functionality in the MVP of the original website, and extend this functionality to offering users real-time notifications.

However, it was later discovered that this was all well and good on a development server, but deploying an Asynchronous Server Gateway Interface (ASGI) is rather a lot more involved than deploying on a standard Web Server Gateway Interface, which the developer was more familiar with. 

In the interests of time, and taking into consideration the priority of the other features that were central to the website, the developer determined that it was best to focus on the features to achieve a Minimal Viable Product. It is the developer's intention to undergo further research and practice to integrate asynchronous web sockets, and allow for real time message and notifications.

### Google Calendar API Integration

In the case of users adding their unavailable dates, the present deployment of the website requires that users update their unavailability calendar manually, which means they have to remember to log in, cycle through their calendar, and submit their unavailable dates each time they have receive a job either due to, or in spite of, the DepT service.

With this in mind, it would be useful to integrate the Google Calendar API, so the user's unavailability calendar is updated automatically whenever they add a job to their calendar in Google. This would most likely substantially improve the UX of DepT, as users would benefit from less manual labour when using the service.

It is the developer's intention to implement this functionality for future releases.

### Customised Emails with Attachments

At present, emails sent to a user (for accepted invitations/booking details that have been sent), have no customizing or branding, and are presented in their most-basic format. Furthermore, there are no options to add attachments for PDF or audio files. It would serve a better UX if emails were branded and more functional, and it would reinforce trust in the DepT brand.
With this, it is important to customize and enhance the emailing service in future releases.

### Sheet Music Resources

It was the developer's original intention to provide the option for users to submit sheet music (as PDF files) in the website's Booking Form when finalizing an accepted booking/confirmed job. However, the time it took to develop the other features of the website meant that this was neglected in favour of developing the core aspects of the website in order to reach a Minimal Viable Product. Once the project is submitted, the developer will create a new branch on the repository, and implement this functionality for the next release.

# Technologies Used

## Development

* The project was developed using the [Visual Studio Code 2](https://code.visualstudio.com/) IDE.
* The project was debugged using a combination of [Chrome Devtools](https://developer.chrome.com/docs/devtools/) and print statements in displayed in the Python terminal.
* [Sentry] was used along with Python Logger to log errors in the production version of the website, as print statements of course weren't an option in such circumstances

## Design

* The [FontAwesome](https://fontawesome.com/) icon library was used to provide icons to the website's user interface.
* [TinyPNG](https://tinypng.com/) was used to compress image files.
* [Convertio](https://convertio.co/png-webp/) was used to convert jpeg and png image files into a webp format.
* [remove.bg](https://www.remove.bg/) was used to remove the background from the website's logo.
* The projects wireframes were created using the [balsamiq](https://balsamiq.com/) wireframe suite.
* Entity Relationship Diagrams were created using [LucidChart](https://www.lucidchart.com/).

## Languages

### HTML
* Used alongside the Django Template Language to create templates throughout the website.

### CSS
* Used to style and position all elements across the website.

### JavaScript
* Used to provide interactivity to the many of the website's features.
* jQuery is used to perform AJAX, fetch and post requests to the website's backend.

### Python
* Python was used to build the website's backend, and to serve data to the client.

## Python Libraries

The website's backend infrastructure was developed using Python 3.9.9.

|Library|Usage|Environment|
|----|----|----|
|[Django](https://www.djangoproject.com/)|Framework|Both| 
|[Django Allauth](https://django-allauth.readthedocs.io/en/latest/installation.html)|User Management|Both|
|[Stripe](https://stripe.com/gb)|Subscriptions|Both|
|[Django Storages](https://django-storages.readthedocs.io/en/latest/)|Production Storage Backend|Production|
|[Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)|Amazon Media/Static File Management|Production|
|[Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/)|Bootstrap Form Rendering|Both|
|[Crispy Bootstrap 5](https://pypi.org/project/crispy-bootstrap5/)|Crispy Template Pack|Both|
|[Django Countries](https://pypi.org/project/django-countries/)|CountryField form widget|Both|
|[Django Bootstrap Datepicker Plus](https://pypi.org/project/django-bootstrap-datepicker-plus/)|DateTimes select form widget|Both|
|[xhtml2pdf](https://pypi.org/project/xhtml2pdf/)|Processing PDF Files|Both|
|[Raven](https://raven.readthedocs.io/en/stable/integrations/logging.html)|Logging|Production|
|[DJ Database URL](https://pypi.org/project/dj-database-url/)|Database Configuration|Production|
|[Psycobg2-binary](https://pypi.org/project/psycopg2-binary/)|PostgreSQL DB Config|Production|
|[Pillow](https://pypi.org/project/Pillow/2.2.1/)|Image Processing|Both|
|[Gunicorn](https://gunicorn.org/)|HTTP Server|Production|
|[Coverage](https://coverage.readthedocs.io/en/6.3.2/)|Unit Test Coverage|Development|

## Other Libraries/Frameworks

* [Bootstrap](https://getbootstrap.com/)
    - The Bootstrap Grid System was employed to ensure responsivity across all device sizes.
    - The website also makes fairly heavy use of Bootstrap's components, including buttons, badges, dropdowns and accordions.
* [SoundManager](http://www.schillmania.com/projects/soundmanager2/)
    - The SoundManager library was used to provide an interactive music player to play audio files on a user profile. 
* [FullCalendar](https://fullcalendar.io/)
    - The FullCalendar API was used to provide an interative calendar in the website's 'Edit My Profile Page'
    - Also used to display a user's unavailability calendar on their profile.
* [Dropzone JS](https://www.dropzone.dev/js/)
    - DropzoneJS was employed to provide drag-and-drop functionality when a user submits their audio files to display on their profile.
* [Toastify JS](https://apvarun.github.io/toastify-js/)
    - Used to display messages across all pages of the website.

For a full list of the website's dependencies, please visit the [requirements.txt](requirements.txt) file.

## Database

[PostgreSQL](https://www.postgresql.org/) is used to for data storage in the deployed version of the website. This service
is managed via [Heroku](https://www.heroku.com).

## Technologies for Testing

* The project's HTML files were tested for validation using the [W3C Markup Validation Service](https://validator.w3.org/)
* The project's CSS files were tested for validation using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/)
* Python PEP8 compliancy validation was tested using [PEP8 Online](http://pep8online.com/)
* Validation of the website's JavaScript files were performed using [JSHint](https://jshint.com/)
* The website's accessibility and performance was measured using Google Chrome's [Lighthouse](https://developers.google.com/web/tools/lighthouse) feature.
* Unit Testing for the backend was performed using [Django's Testing Tools](https://docs.djangoproject.com/en/3.2/topics/testing/tools/)

## Hosting

* The CDNs which provide the FontAwesome, Dropzone, Bootstrap and Toastify libraries are served through [jsdelivr](https://www.jsdelivr.com/) and [cloudflare](https://www.cloudflare.com/en-gb/).
* Static and Media Files are hosted using [Amazon AWS S3](https://aws.amazon.com/s3/)
* The website is hosted using [Heroku](https://www.heroku.com)

# Testing

Testing information can be found in a seperate [TESTING.md](TESTING.md) file.

# Deployment

## Prerequisite

In order to deploy this project, you need to have the following:

* An account with Amazon AWS.
* An account with Heroku
* An account with Stripe
* A Gmail account with 2-step verification enabled, and a password to tie to this application.

## Deployment to Heroku

To deploy the project to Heroku, take these steps:

* Navigate to the [Heroku](https://www.heroku.com) home page.
* Create an account, or log in if you have an account already.
    * If you are creating account, make sure to select `Python` as your primary language.

### Creating an App

![Screenshot of Heroku 'Create App'](documentation/readme_images/deployment/heroku_create_app.png)

* Once logged in, click on the dropdown 'New' and click 'Create App'.

![Screenshot of Heroku 'Select app name and region'](documentation/readme_images/deployment/heroku_appname_region.png)

* Create your own App name and select your nearest region, then click 'Create App'.

### Initial Deployment

![Screenshot of Heroku 'Deployment'](documentation/readme_images/deployment/heroku_deploy.png)

* Head over to your app's dashboard, and select the tab reading 'Deployment'.

![Screenshot of Heroku 'Connect to Github'](documentation/readme_images/deployment/heroku_connect_github.png)

* To connect to Github, click on the button reading 'Github'
* Enter your Github credentials.
* Search for the repository you would like to connect to, and click 'Connect'.

![Screenshot of Heroku 'Automatic Deployment'](documentation/readme_images/deployment/heroku_connect_github.png)

If you would like to deploy your project automatically once your Github repository is connected, click 'Enable Automatic Deploys"

## Environment Variables

The complete list of environment variables needed to run the project are as follows:

### Production Environment

|Key|Value|
|----|----|
|SECRET_KEY|<Generated Django Secret Key>|
|DATABASE_URL|<your_database_url>|
|AWS_ACCESS_KEY_ID|<your_aws_access_key_id>|
|AWS_SECRET_ACCESS_KEY|<your_aws_secret_access_key>|
|AWS_S3_SIGNATURE_VERSION|s3v4|
|ALLOWED_AUDIOFILE_EXTENSIONS|[.mp3, .mp4, .wav, .aac, .m4a, .flac]|
|STRIPE_PUBLIC_KEY|<your_stripe_public_key>|
|STRIPE_SECRET_KEY|<your_stripe_secret_key>|
|STRIPE_WH_SECRET|<your_stripe_wh_secret>|
|STRIPE_TIERONE_PRICE_ID|<your_stripe_tierone_price_id>|
|STRIPE_TIERTWO_PRICE_ID|<your_stripe_tiertwo_price_id>|
|EMAIL_HOST_PASSWORD|<your_email_host_password>|
|EMAIL_HOST_USER|<your_email_host_username>|
|USE_AWS|True|

#### Your Django SECRET KEY

In order to deploy your project successfully, you will need a secret key.
Visit [Django Secret Key Generator to Generate Your Key](https://miniwebtool.com/django-secret-key-generator/)

Add this to as the value to your environment variable `SECRET_KEY`

#### Amazon S3 Bucket Access Key ID and Secret Access Key

To configure your Amazon S3 Bucket and obtain your credentials to add to the environment variables, [visit this link](AWS_CONFIG.md).

Once you have configured your S3 Bucket, add your `AMAZON_ACCESS_KEY_ID` and `AMAZON_SECRET_ACCESS_KEY` values to the website's environment variables.


#### Stripe Credentials

In order to authenticate successful requests with Stripe, you will need five keys:

* STRIPE_PUBLIC_KEY - The client-side key, used to tokenize requests to create a 'checkout session'.
* STRIPE_SECRET_KEY - The server side key, used to call the Stripe API.
* STRIPE_WH_SECRET - Used to verify webhook authenticity when Stripe events are triggered.
* STRIPE_TIERONE_PRICE_ID - A unique identifier for the Tier One Subscription Price.
* STRIPE_TIERTWO_PRICE_ID - A unique identifier for the Tier Two Subscription Price.

**To create these credentials, you must:**
1. Create a [Stripe](https://www.stripe.com) account.
2. Once you have an account and signed in, enable "Test Mode" by clicking the switch in the top right corner.
3. Navigate to the developer settings. Under `API Keys`, you will find your Public and Secret Keys.
4. Add these keys to your environment variables:
    * STRIPE_PUBLIC_KEY
    * STRIPE_SECRET_KEY
5. In the Developer dashboard, click the "**Products**" tab.
6. In the "Products" page, click the button "Create Product" located in the top right corner of the dashboard.
7. Create a name.
8. Under "Price Information", enter your price and choose "Recurring" and select your billing frequency.
9. Click the button which reads "**Save Product**", located in the top right corner.
10. You will be directed to a page featuring an overview of your new product's details. 
11. Make a note of the `Price ID`, which can be found in the 'Pricing' section of the overview.
12. Repeat steps 4-9 to create your second price.
13. Once you have both prices, add them to your environment variables:
    * STRIPE_TIERONE_PRICE_ID
    * STRIPE_TIERTWO_PRICE_ID
14. Navigate to the your Stripe API dashboard. In the sidebar to the left, select "Webhooks".
15. On the webhooks page, click the button reading "**Add Endpoint**", located in the top right corner.
16. Add the endpoint URL:
    *<your_domain_name>/subscribe/wh/*
17. Then take your webook signing secret and at that as the value to your environment variable:
    * STRIPE_WH_SECRET

#### Gmail Credentials
To retrieve the values to your final two keys in your production environment variables, you need to:

1. Sign in or create a new Gmail account.
2. Upon signing in, navigate to your google account settings, by clicking the small circle in the top right of your Gmail dashboard.
3. In the sidebar to the left, click "**Security**".
4. Scroll down until you see the section "Signing in to Google".
5. Click "2 Step Verification" and enable.
6. Go back to your Security dashboard, and click "App passwords" which is located beneath the button to access 2-step verification.
7. In the dropdown which reads "Select App", choose "Other" and give your app a custom name.
8. Do the same in dropdown which reads "Select Device"
9. Click "**Generate password**".
10. Add your Gmail address and password as values to the follow environment variables:
    * `EMAIL_HOST_USER`
    * `EMAIL_HOST_PASSWORD`

### Get your Postgres Database URL

To add your Postgres URL to your production environment variables, follow these steps:

* In your heroku dashboard, navigate to your project's **Resources**

![Screenshot of Heroku 'Connect to PostgreSQL'](documentation/readme_images/deployment/heroku_postgres.png)

* In the 'Add-ons' search bar, type 'postgres', and select 'Heroku Postgres'.
* Select 'Hobby Dev - Free' to access the free version.
* Click "Submit Order Form" to connect to Heroku PostgreSQL.

* Navigate to your Settings tab
* Scroll down and click "Reveal Config Vars"
* Copy your Database URL
* Temporarily add `DISABLE_COLLECTSTATIC: True` to your config vars.
* Check to see if your key `DATABASE_URL` exists in your Heroku environment variables, alond with your new URL as it's value.

### Connect your PostGres Database URL in settings.py

* In your local environment, install the following packages:
    * `pip3 install dj_database_url`
    * `pip3 install psycopg2-binary`

* Then run the command `pip freeze > requirements.txt`

* Then, navigate to the project root, and locate `dept/settings.py`
* Import `dj_database_url` at the top of your file

* Connect your settings.py file to your Postgres Database URL
```
DATABASES = {
    'default': dj_database_url.parse(<your_database_url>)
    }
```

* Then, run `python3 manage.py migrate` to migrate your data to the production database.

### Create a superuser

* To create a superuser to act as admin, run `python3 manage.py createsuperuser` in your project environment's terminal.
* Give your superuser a name, email an password.
* Then, disconnect your production database URL from your settings.py file.

### Create your production and development config

In `dept/settings.py`, set the following configurations:

* Secret Key
    * `SECRET_KEY = os.environ.get(SECRET_KEY, '')`

* Debug:
    * `DEBUG = 'DEVELOPMENT' in os.environ`

* Allowed Hosts
    * `ALLOWED_HOSTS [https://dept-ci-ms4.herokuapp.com, <your_local_host_domain>]`

* Configure your Database to use the Postgres Database in production
 ```
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': django.db.backends.sqlite3,
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }
```

* Configure your email settings for production:
```
if "DEVELOPMENT" in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = "hello@dept.com"
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")
```

### Connect your Amazon S3 Bucket to Django

In order for Amazon S3 to serve your static and media files in production. Some configuration for Django is required.

In your IDE's terminal, install the following packages:

1. `pip3 install boto3`
2. `pip3 install django-storages`
    * Once installed, type `pip3 freeze > requirements.txt` to add these packages to your list of dependencies.

3. Create a file named `custom_storages.py` in the root of your project.
4. In `dept/settings.py` and `storages` to your list of `INSTALLED_APPS`.
5. Configure your Amazon S3 in `dept/settings.py like thus:`
    *   ```
        if "USE_AWS" in os.environ:
            # Cache control
            AWS_S3_OBJECT_PARAMETERS = {
                'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
                'CacheControl': 'max-age=94600000'
            }
            # Bucket Config
            AWS_STORAGE_BUCKET_NAME = "dept-bucket"
            AWS_S3_REGION_NAME = "eu-west-2"
            AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
            AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
            AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
            AWS_DOWNLOAD_EXPIRE = 5000

            # Set Signature Version to access files in Bucket
            AWS_S3_SIGNATURE_VERSION = os.environ.get("AWS_S3_SIGNATURE_VERSION")

            # Static and Media Files
            STATICFILES_STORAGE = "custom_storages.StaticStorage"
            STATICFILES_LOCATION = "static"

            MEDIAFILES_STORAGE = "custom_storages.MediaStorage"
            MEDIAFILES_LOCATION = "media"

            # Override Static and Media File URLS in production
            STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/"
            MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"
    ```



6. Configure boto3 file storage to handle user uploads in production:
    * ```
    # Use boto3 storage in production
    if "DEVELOPMENT" not in os.environ:
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    ```

7. Lastly, visit your Amazon S3 Bucket, and add a `/media` directory along side your `static/` directory.
    * Make sure you remove `DISABLE_COLLECTSTATIC` from your environment variables, so Amazon AWS can locate all of the static files.

### Visit Heroku and Launch The App

Do a last minute check to see if your Django, Stripe, Amazon AWS and Gmail credentials are present in Heroku's environment variables.

Click "**Launch App**", and the website should load with all static and media files displaying.

## Running the Project in your Local Environment

To browse or play with this project in your local IDE, you may either:

* Fork this repository
* Clone this respository
* Download the files in a ZIP folder

### Forking the local repository

You can fork this repository by taking the following steps:

1. Log in or sign up to Github.
2. Navigate to [the DepT repository](https://github.com/OliverCadman/dept_ci_ms4)

![Forking DepT Repository](documentation/readme_images/deployment/dept_fork_repository.png)

3. Click the button in the top right corner to fork the repository, and create a copy for you to play with.

### Cloning the repository

**Note:**
These steps assume that you already have the [Github CLI](https://github.com/cli/cli) installed.

To clone the repository and download onto your system, take the following steps:

1. Log in or sign up to Github.
2. Navigate to [the DepT repository](https://github.com/OliverCadman/dept_ci_ms4)

![Cloning DepT Repository](documentation/readme_images/deployment/dept_clone_repository.png)
3. Click the button saying "**Code**" to open a dropdown link.
4. Copy the github link.
5. Open your terminal and type `git clone <the repository link>`.
6. Open up the project in your favourite IDE and have fun!

### Downloading the files as a ZIP

Alternatively you can download the repositories files as a zip folder:

1. Navigate to the same dropdown accessible via the "**Code**" button.
2. Click "**Download all as ZIP**".
3. Unzip the files.
4. Open them in your favourite IDE.

### Install project dependencies

In order to run the project on your local machine, you will have to install it's dependencies.

To do this, just type `pip3 install -r requirements.txt`, and watch them all flood in.

### Local Environment variables

As with the production environment variables, you will need to provide values to the following local environment variables:

|Key|Value|
|----|----|
|SECRET_KEY|<Generated Django Secret Key>|
|AWS_ACCESS_KEY_ID|<your_aws_access_key_id>|
|AWS_SECRET_ACCESS_KEY|<your_aws_secret_access_key>|
|AWS_S3_SIGNATURE_VERSION|s3v4|
|ALLOWED_AUDIOFILE_EXTENSIONS|[.mp3, .mp4, .wav, .aac, .m4a, .flac]|
|STRIPE_PUBLIC_KEY|<your_stripe_public_key>|
|STRIPE_SECRET_KEY|<your_stripe_secret_key>|
|STRIPE_WH_SECRET|<your_stripe_wh_secret>|
|STRIPE_TIERONE_PRICE_ID|<your_stripe_tierone_price_id>|
|STRIPE_TIERTWO_PRICE_ID|<your_stripe_tiertwo_price_id>|
|EMAIL_HOST_PASSWORD|<your_email_host_password>|
|EMAIL_HOST_USER|<your_email_host_username>|

Once you have your environment variables added, you can start to have fun and play around with the project.

# Credits

## Code

### Dropzone JS
The developer used the [DropzoneJS](https://www.dropzone.dev/js/) API to create the drag-and-drop functionality in the website's 'Edit My Profile' page.

### FullCalendar
The developer used the [FullCalendar](https://fullcalendar.io/) library to render both the interactive calendar in the 'Edit My Profile' page, and as well as the 'Profile' page.

### ToastifyJS
The [ToastifyJS](https://apvarun.github.io/toastify-js/) library is used to display notifications.

### Formset Factory
The code to dynamically render form elements using Django's [modelformset_factory](https://docs.djangoproject.com/en/4.0/ref/forms/models/) was referenced from a YouTube tutorial:

Title: 61 - Manage QuerySets with Django Formsets + modelformset factory - Python & Django Tutorial Series
Uploader: Coding Entrepeneurs
Link: https://www.youtube.com/watch?v=6wHx-X1tEiY

### to_dict() function
The website's `to_dict()` function was referenced from a [post on StackOverflow](https://stackoverflow.com/questions/21925671/convert-django-model-object-to-dict-with-all-of-the-fields-intact)

### Notifications
The website's notifications were build with reference from a Youtube Tutorial:

Title: Building a Social Media App With Python 3 and Django: Part 12 User Notifications
Uploader: Legion Script
Link: https://www.youtube.com/watch?v=_JKWYkz597c

### handle_GET_params()/UserProfile Custom Filter Queryset

Custom queryset filter methods are used on the UserProfile and Job Models, to filter
through the UserProfile and Job objects in the 'Find a Dep' and 'Find a Job' pages, respectively.

The code to process the query parameters and the models was originally referenced from Benjamin Kavanagh's
project [CIRPG](https://github.com/BAK2K3/CIRPG/blob/main/codex/functions.py), and customised to the needs of
my own project.

### Stripe Subscriptions/Customer Portal

The code to integrate Stripe Subscriptions and the Customer Portal were referenced from [Stripe's Official Documentation](https://stripe.com/docs).

The query parameter code can be found here: https://github.com/BAK2K3/CIRPG/blob/main/codex/functions.py

The custom filter-queryset code can be found here: https://github.com/BAK2K3/CIRPG/blob/main/codex/models.py

## Design

The UI design of the project - in particular the headers and home page - was inspired by the website [SoundBetter](https://soundbetter.com/).

## Text Content

All text content was created by the developer.

## Logo

The logo was originally designed by the developer's good friend (and original conceiver of the project idea), [Sim Virdi](https://www.simvirdi.com/)

## Images

All static images are stock images, provided by [Pexels](https://www.pexels.com/) and [Shutterstock](https://www.shutterstock.com/).

# Acknowledgements

* Thanks to Adegbenga Adeye for giving me his vote of confidence when it all was getting a bit much.
* Thanks to my two really good friends Dwayne Kilvington and Sim Virdi, for coming up with the idea while
drunk on New Years Eve, 2020.
* Thanks to my girlfriend Dani, for supporting me throughout every step of the - sometimes painful but nevertheless invaluable - development process.

I have poured every ounce of my being into this final project for Code Institute. I hope you enjoy my work.



















