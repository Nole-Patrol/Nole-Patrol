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
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/michaelsousajr/Nole-Patrol">
    <img src="static/img/fsuicon.pnglogo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Nole Patrol: FSU Data Breach Search Engine</h3>

  <p align="center">
    A data breach search engine for Florida State University
    <br />
    <a href="https://github.com/michaelsousajr/Nole-Patrol"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/michaelsousajr/Nole-Patrol">View Demo</a>
    ·
    <a href="https://github.com/michaelsousajr/Nole-Patrol/issues">Report Bug</a>
    ·
    <a href="https://github.com/michaelsousajr/Nole-Patrol/issues">Request Feature</a>
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
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]]<!--(https://example.com)-->

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
   git clone https://github.com/michaelsousajr/Nole-Patrol.git
   ```
2. Install Django packages
   ```sh
   python -m pip install Django
   ```
3. Navigate to the Nole-Patrol directory.
4. Run the following command sequence inside the Nole-Patrol directory to set up the product.
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Run the following command to import the data from the text files into the database.
   ```sh
   python manage.py updatemodels
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
<!-- documentation in progress - cmg
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/michaelsousajr/Nole-Patrol/issues) for a full list of proposed features (and known issues).
-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing
<!-- documentation in progress - cmg

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License
<!-- documentation in progress - cmg

Distributed under the MIT License. See `LICENSE.txt` for more information.

-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Nole Patrol Team - <!--[@twitter_handle](https://twitter.com/twitter_handle) - --> email@email_client.com(mailto:email@email_client.com) ( <-- Replace with email Brian created)

Project Link: [https://github.com/michaelsousajr/Nole-Patrol](https://github.com/michaelsousajr/Nole-Patrol)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [PyProg](https://github.com/Bill13579/pyprog/releases)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[contributors-url]: https://github.com/michaelsousajr/Nole-Patrol/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[forks-url]: https://github.com/michaelsousajr/Nole-Patrol/network/members
[stars-shield]: https://img.shields.io/github/stars/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[stars-url]: https://github.com/michaelsousajr/Nole-Patrol/stargazers
[issues-shield]: https://img.shields.io/github/issues/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[issues-url]: https://github.com/michaelsousajr/Nole-Patrol/issues
[license-shield]: https://img.shields.io/github/license/michaelsousajr/Nole-Patrol.svg?style=for-the-badge
[license-url]: https://github.com/michaelsousajr/Nole-Patrol/blob/master/LICENSE.txt
<!--[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: static/img/screenshot.JPG
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