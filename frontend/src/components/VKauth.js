import React, {Component} from "react";
import './VKauth.css'
import * as VKID from '@vkid/sdk';
import VKlogo from "../resources/imgs/new_logo_vk_28.svg"

class VKauth extends Component{
    componentDidMount(){
        VKID.Config.set({
            app: 51813528, // Идентификатор приложения.
            redirectUrl: 'http://localhost:80', // Адрес для перехода после авторизации.
        });
    }

    login = () =>{
        VKID.Auth.login((res)=>console.log(res));
    }

    render(){
        const oneTap = new VKID.OneTap();
        return(
            <div className="VKauth">
                {/* <button onClick={()=>VKID.Auth.login((res)=>console.log(res))}> <img src={VKlogo}></img> Войти через VK ID </button> */}
                {oneTap.render()}
            </div>
        )
    }
}

export default VKauth;