import React, {Component} from "react";
import './Logo.css'
import logo from "./../resources/imgs/ProfilumLogo.png"

function Logo(){
    return(
        <div className="Logo">
            <img className="LogoImg" src={logo}></img>
        </div>
    )
}

export default Logo;