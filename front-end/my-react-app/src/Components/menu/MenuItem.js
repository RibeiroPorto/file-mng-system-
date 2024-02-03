import React from 'react';
import './menu.css'

const MenuItem = ({ icon, text, link }) => (
  <li className="side-menu">
    <a className="side-menu" href={link}>
      <span className="icon side-menu"><i className={`fas ${icon}`}></i></span>
      <span className="text hide">{text}</span>
    </a>
  </li>
);

export default MenuItem;