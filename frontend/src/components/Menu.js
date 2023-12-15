import React, {Component} from "react";
import './Menu.css'
import ActionCard from './ActionCard.js';

class Menu extends Component{

    login = () =>{
        // window.open(this.props.main_host+'/api/login_index', "hello", "top=200, left=200, menubar=no, width=220, scrollbars=no, height=200", '_blank', 'noreferrer');
        window.open(
            "https://oauth.vk.com/authorize?client_id=51813528&display=popup&redirect_uri=https://89.232.176.33:443/api/login_index&scope=groups&response_type=code&v=5.131&state="+this.props.login, 
            "hello", 
            "top=200, left=200, menubar=no, width=220, scrollbars=no, height=200", 
            '_blank', 
            'noreferrer'
        )
    }

    render(){
        return(
            <div className="Menu">
                <ActionCard onClick_func={()=>this.props.set_process('form')} name={"Пройти тестирование"} description={"Предлагаем пройти психологический тест, который поможет вам определиться с профессиональной ориентацией"} />
                <ActionCard onClick_func={()=>this.login()} name={"Анализ страницы в ВК"} description={"Вам будет предложено авторизоваться в ВК для анализа вашей страницы в целях помощи с профессиональной ориентацией"} />
            </div>
        )
    }
}

export default Menu;