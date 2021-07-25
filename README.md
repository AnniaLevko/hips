<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
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
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
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
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

There are many great README templates available on GitHub, however, I didn't find one that really suit my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

Here's why:
* Your time should be focused on creating something amazing. A project that solves a problem and helps others
* You shouldn't be doing the same tasks over and over like creating a README from scratch
* You should element DRY principles to the rest of your life :smile:

Of course, no one template will serve all projects since your needs may be different. So I'll be adding more in the near future. You may also suggest changes by forking this repo and creating a pull request or opening an issue. Thanks to all the people have have contributed to expanding this template!

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Laravel](https://laravel.com)



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

# Pre requisitos

  Para la instalacion del sistema necesitamos instalar varias herramientas
  ## python3
  ```sh
  sudo yum install python3
  ```

  Si python3 no les trae incluido pip3
  ## pip3
  ```sh
  sudo yum install python3-pip
  ```
  
  ## PostgreSQL
  Para la base de datos de nuestro sistema, necesitamos instalar y configurar postgresql
  ```sh
  sudo yum install postgresql
  ```
  ```sh
  sudo yum install postgresql-server
  ```

  Creamos un nuevo cluster de la base de datos PostgreSQL
  ```sh
  sudo postgresql-setup --initdb
  ```

  Inciamos el servicio de postgres y habilitamos:
  ```sh
  sudo systemctl start postgresql
  ```
  ```sh
  sudo systemctl enable postgresql
  ```

# Instalacion
  Necesitamos instalar algunos modulos y hacer algunas configuraciones en nuestro sistema.

  ## Instalar Modulos de python3:
  * flask
    ```sh
    pip3 install --user flask
    ```
  * dotenv
    ```sh
    pip3 install --user python-dotenv
    ```
  * flask-bootstrap
    ```sh
    pip3 install --user flask_bootstrap
    ```
  * flask-wtf
    ```sh
    pip3 install --user flask_wtf
    ```
  * flask_sqlalchemy
    ```sh
    pip3 install --user flask_sqlalchemy
    ```
  * flask-login
    ```sh
    pip3 install --user flask_login
    ```
  * psycopg2
    ```sh
    pip3 install --user psycopg2
    ```

  ## Base de datos PostgreSQL
  *
    Cambiamos a la cuenta de postgres, para hacer algunas configuraciones
    ```sh
    sudo -i -u postgres
    ```

    <!-- Accedemos a Postgres
    ```sh
    psql
    ``` -->
  *
    Creamos un nuevo rol para root
    ```sh
    create user root with password '<BD_ROOT_PASSWORD>';
    ```
  *  
    Le asignamos los permisos necesario a root
    ```sh
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO root;
    ```

    <!-- Salimos de la cuenta de postgres
    ```sh
    exit
    ``` -->
  *
    Creamos una nueva base de datos llamada hips2021 
    ```sh
    createdb hips2021
    ```
  *
    Cambiamos el duenho de hips2021 a root
    ```sh
    alter database hips2021 owner to root
    ```


## Variable de entorno
*
  Necesitamos crear un archivo .env en el directorio de nuestro proyecto hips, para esconder nuestras contrasenhas de la base de datos, nuestro email de hips, el email del administrador, etc

  ```sh
  [root@localhost hips] vi .env
  ```
  Y Adjuntamos estos Valores
  ```sh
  BD_PASSWORD=<La_contrasenha_de_root>
  BD_USER=root
  SECRET_KEY=<Cualquier_palabra_podes_escribir_aca_es_solo_para_alg_de_flask>
  MY_HIPS_EMAIL=<gmail_del_hips>
  MY_HIPS_EMAIL_PASSWORD=<contrasenha_del_gmail_del_hips>
  MAIL_HIPS_ADMIN=<email_del_administrador_de_hips>
  ```
  guardamos el archivo.
  
  Cambiamos los permisos del archivo, para que solo root pueda usar
  ```sh
  [root@localhost hips] chmod 700 .env
  ```

## Generar contrasenha hash para el administrador del hips
*
  Ejecutamos una vez el servidor de hips (solo para que se cree automaticamente las tablas en la base de datos hips)
  ```sh
  [root@localhost hips] python3 server.py
  ```
  y apagamos el server
  ```sh
  control + c
  ```

  Corremos con python3 el archivo borrar.py que se encuentra en el directorio del proyecto para generar una contrasenha encriptada para un usuario del hips
  ```sh
  [root@localhost hips] python3 borrar.py
  ```
  Ingresas la contrasenha del administrador que va a usar el hips, dale a enter y copiamos la contrasenha encriptada  que imprime en consola

  Pasamos a cargar el administrador de hips en la base de datos:
  * Entramos de nuevo al usuario de postgres y abrimos postgres
    ```sh
    psql
    ```
  * Seleccionamos la base de datos hips2021
    ```sh
    postgres=$ \c hips2021
    ```
  * Insertamos el usuario/administrador en la tabla de users el administrador que va a ingresar al sistema hips2021
    ```sh
    hips2021=$ INSERT INTO users (username, password) values ('<username_admin>', '<contrasenha_encriptada_que_copiamos>');
    ```  


## Crear Carpetas necesarias
*
  En el directorio del projecto hips, necesitamos crear varias carpetas que se usan para almacenar resultados, estos resultados se leen y se borran una vez mostrado en la pagina web.
  ```sh
    [root@localhost hips] mkdir ./resultados
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/base_de_datos
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/cola_correo
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/sniffers
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/usuarios
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/verificar_logs
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/verificar_procesos
  ```
  ```sh
    [root@localhost hips] mkdir ./resultados/verificar_tmp
  ```


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_




<!-- CONTACT -->
## Contact

Annia Levko - annialevko@hotmail.com

Erik Wasmosy - erikwasmosy98@gmail.com

Project Link: [https://github.com/AnniaLevko/hips](https://github.com/AnniaLevko/hips)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
