import React, {Component} from "react";
import './VKauth.css'
import * as VKID from '@vkid/sdk';

class VKauth extends Component{
    componentDidMount(){
        VKID.Config.set({
            app: 51813528, // Идентификатор приложения.
            redirectUrl: 'http://localhost:80', // Адрес для перехода после авторизации.
        });
    }

    login = () =>{
        VKID.Auth.login(res=>console.log(res))
    }

    render(){
        return(
            <div className="VKauth">
                <button onClick={()=>this.login()}> Войти через VK ID </button>
            </div>
        )
    }
}

export default VKauth;