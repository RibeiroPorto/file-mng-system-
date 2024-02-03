import React,{ useState} from 'react';
import MenuItem from './MenuItem';
import './menu.css'


const Menu = () => {
  const [usestate, setstate] = useState('');

  const toggleMenu = () => {
    const menu = document.getElementById('menu');
    const textMenu = document.querySelectorAll('.side-menu .text');
    const button = document.querySelector('button.side-menu')
    setstate('minha-classe-adicionada');
  };

return(

  
  <><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"></link>
  <script>
    {function toggleMenu() {
  const menu = document.getElementById('menu');
  const textMenu = document.querySelectorAll('.side-menu .text');
  const button = document.querySelector('button.side-menu')
  //menu.style.width = menu.style.width === '250px' ? '50px' : '250px';
  menu.classList.toggle('hide')
  button.classList.toggle('hide')
  textMenu.forEach( item => {
      item.classList.toggle('hide')
  })
  
}}
  </script>

  <section class="side-menu">
  <nav id="menu" className="side-menu hide">
    
    <button class="side-menu hide" id="menu-toggle" onclick="toggleMenu()">
      <i class="fas fa-bars"></i>
    </button>
    <ul class='side-menu'>
    <MenuItem
      icon="fa-home"
      text="Pagina inicial"
      link="/"
      />
    
    <MenuItem
      icon="fa-industry"
      text="Produção"
      link="/"
    />
    <MenuItem
      icon="fa-folder"
      text="Documentações"
      link="/"
    />
    <MenuItem
      icon="fa-wrench"
      text="Configurações"
      link="/"
    />
     <MenuItem
      icon=" fa-cubes"
      text="Desenvolvimento"
      link="/"
    />
    <MenuItem
      icon="fa-plus"
      text="Adicionar Área"
      link="/"
    />
    <MenuItem
      icon="fa-cogs"
      text="Registrar Produção"
      link="/"
    />
    <MenuItem
      icon="fa-chart-line"
      text="Monitoramento de Linha"
      link="/"
    />
    <MenuItem
      icon="fa-chart-line"
      text="Monitoramento de Linha"
      link="/"
    />
    <MenuItem
      icon="fa-users"
      text="Ver Usuários"
      link="/"
    />
    <MenuItem
      icon="fa-user-plus"
      text="Criar Usuários"
      link="/"
    />
    <MenuItem
      icon="fa-sign-out-alt"
      text="Sair"
      link="/"
    />
    
    
    </ul>
  </nav>
  </section>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/js/all.min.js"></script>
  </>
)};

export default Menu;