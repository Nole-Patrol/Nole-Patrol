# Nole-Patrol
<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!--[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Nole-Patrol/Nole-Patrol">
    <img src="static/images/fsuicon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Nole Patrol: FSU Data Breach Search Engine</h3>

  <p align="center">
    A data breach search engine for Florida State University
    <br />
    <a href="https://github.com/Nole-Patrol/Nole-Patrol"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Nole-Patrol/Nole-Patrol">View Demo</a>
    ·
    <a href="https://github.com/Nole-Patrol/Nole-Patrol/issues">Report Bug</a>
    ·
    <a href="https://github.com/Nole-Patrol/Nole-Patrol/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#disclaimers">Disclaimers</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Nole-Patrol Screen Shot][product-screenshot]<!--(https://example.com)-->

Students, faculty, staff, and administrators at Florida State University face the risk of data breaches that could leak
sensitive information including credentials associated with their fsu.edu email addresses and associated accounts. Nole
Patrol offers an intuitive data breach search engine that utilizes proprietary code along with third-party APIs to 
identify and catalog leaked fsu.edu credentials from a variety of publicly available sources. Users can utilize our
product to search for data breaches affecting them by entering their university email addresses and the site will return
relevant results. We are currently working implementing the option for users to opt-in to receiving automated email 
notifications when their data has been discovered in new breaches.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Django
<!--* [![JQuery][JQuery.com]][JQuery-url] saving this as template for badges - cmg -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy of our project up and running follow these simple steps.

### Prerequisites

To run this project, you will need to set up a Python virtual environment (venv). Please see the official Python documentation
at https://docs.python.org/3/library/venv.html to complete this process.

Once you've created and activated your venv, install the following dependencies inside it.
* django
  ```sh
  python -m pip install Django
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Nole-Patrol/Nole-Patrol.git
   ```
2. Navigate to the Nole-Patrol directory.
3. Install Django and relevant packages.
   ```sh
   pip install -r requirements.txt
   ```
4. Run the following command sequence inside the Nole-Patrol directory to set up the product.
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Run the following command to launch the site on localhost:8000.
   ```sh
   python manage.py runserver
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

<!-- documentation in progress - cmg

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

Our development roadmap includes the following milestones:

- **Milestone 1:** Implement efficient data imports and search functionality.
- **Milestone 2:** Enhance encryption for stored passwords.
- **Milestone 3:** Expand features for notifying users about potential breaches.
- **Milestone 4:** Improve user interface and user experience.
- **Milestone 5:** Ongoing maintenance and bug fixes.

Feel free to open issues or pull requests related to these milestones.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

We welcome contributions from the community. If you'd like to contribute to Nole Patrol, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request to the main repository, explaining your changes and why they should be merged.
6. We will review and, if approved, merge your changes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## License
<!-- documentation in progress - cmg

Distributed under the MIT License. See `LICENSE.txt` for more information.

-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- DISCLAIMERS -->
## Disclaimers
<!-- documentation in progress - cmg
-->
Nole Patrol is a student-developed product and is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Florida State University or any of its subsidiaries or its affiliates. All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them. All data referenced in this product has been acquired from publically available sources including but not limited to public records, public data leaks, and public APIs. For questions or concerns, please see the team contact information below.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Nole Patrol Team - <!--[@twitter_handle](https://twitter.com/twitter_handle) - --> NolePatrolProj@gmail.com

Project Link: [https://github.com/Nole-Patrol/Nole-Patrol](https://github.com/Nole-Patrol/Nole-Patrol)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [PyProg](https://github.com/Bill13579/pyprog/releases)
* [HaveIBeenPwned](https://haveibeenpwned.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Nole-Patrol/Nole-Patrol.svg?style=for-the-badge
[contributors-url]: https://github.com/Nole-Patrol/Nole-Patrol/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Nole-Patrol/Nole-Patrol.svg?style=for-the-badge
[forks-url]: https://github.com/Nole-Patrol/Nole-Patrol/network/members
[stars-shield]: https://img.shields.io/github/stars/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[stars-url]: https://github.com/Nole-Patrol/Nole-Patrol/stargazers
[issues-shield]: https://img.shields.io/github/issues/Nole-Patrol/Nole-Patrol.svg?style=for-the-badge
[issues-url]: https://github.com/Nole-Patrol/Nole-Patrol/issues
[license-shield]: https://img.shields.io/github/license/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[license-url]: https://github.com/Nole-Patrol/Nole-Patrol/blob/master/LICENSE.txt
[product-screenshot]: static/img/screenshot.JPG
<!--[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com -->
